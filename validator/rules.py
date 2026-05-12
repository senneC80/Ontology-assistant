"""Symbolic validation rules. Registry-based; add a new rule by appending to ALL_RULES."""
from __future__ import annotations
from typing import Callable, Dict, List

import networkx as nx
from rdflib import Graph

from .models import (
    Finding, Severity,
    RULE_DISCONNECTED_ISLAND,
    RULE_GENERALIZATION_CYCLE,
    RULE_RELATOR_NO_MEDIATION,
    RULE_ROLE_NO_IDENTITY,
    RULE_SUBKIND_NO_KIND,
    RULE_NONSORTAL_SPECIALIZES_SORTAL,
    RULE_RIGID_SPECIALIZES_ANTIRIGID,
    RULE_PARTICIPATION_SOURCE_IS_EVENT,
    RULE_CREATION_SOURCE_IS_EVENT,
    RULE_CHARACTERIZATION_SOURCE_INVALID,
    RULE_MEDIATION_NO_RELATOR_ENDPOINT,
    RULE_CHARACTERIZATION_BEARER_MULT,
)


IDENTITY_PROVIDERS = {"kind", "collective", "quantity", "quality", "relator", "mode"}

NON_SORTALS = {"category", "mixin", "roleMixin", "phaseMixin"}
SORTALS     = {"kind", "subkind", "role", "phase", "relator", "collective", "quantity", "quality", "mode"}
RIGID       = {"kind", "subkind", "category"}
ANTI_RIGID  = {"role", "phase", "roleMixin", "phaseMixin"}

Rule = Callable[[nx.DiGraph, Graph], List[Finding]]


def rule_disconnected_island(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    full = gen_graph.graph["full_undirected"]
    out: List[Finding] = []
    for node in gen_graph.nodes():
        if node not in full or full.degree(node) == 0:
            name = gen_graph.nodes[node].get("name", node)
            out.append(Finding(
                severity=Severity.WARNING,
                code=RULE_DISCONNECTED_ISLAND,
                message=f"Class '{name}' is not connected to any relation or generalization",
                entity_id=node,
                entity_name=name,
                repair_hint="Connect this class to at least one relation or add a generalization.",
            ))
    return out


def rule_generalization_cycle(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    out: List[Finding] = []
    for cycle in nx.simple_cycles(gen_graph):
        names = [gen_graph.nodes[n].get("name", n) for n in cycle]
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_GENERALIZATION_CYCLE,
            message=f"Generalization cycle: {' → '.join(names)} → {names[0]}",
            repair_hint="Remove one generalization in this cycle.",
        ))
    return out


def rule_relator_insufficient_mediation(gen_graph: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """A «relator» must have mediation target ends whose minimum cardinality sum is ≥ 2.

    Counts only the non-relator ends of each mediation (i.e. the mediated entity ends).
    A relator that inherits sufficient mediation from an ancestor passes.
    """
    # Get the non-relator (mediated) end cardinality for each mediation involving a relator.
    mediation_card_query = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?relator ?cardStr WHERE {
        ?relator a ontouml:Class ;
                 ontouml:stereotype ontouml:relator .
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:mediation .
        {
            ?rel ontouml:sourceEnd ?relEnd ;
                 ontouml:targetEnd ?otherEnd .
            ?relEnd ontouml:propertyType ?relator .
        } UNION {
            ?rel ontouml:targetEnd ?relEnd ;
                 ontouml:sourceEnd ?otherEnd .
            ?relEnd ontouml:propertyType ?relator .
        }
        ?otherEnd ontouml:cardinality ?cardNode .
        ?cardNode ontouml:cardinalityValue ?cardStr .
    }
    """
    relator_query = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?cls ?name WHERE {
        ?cls a ontouml:Class ;
             ontouml:stereotype ontouml:relator ;
             ontouml:name ?name .
    }
    """
    base_uri = "https://example.org#"
    uri_to_node = {base_uri + nid: nid for nid in gen_graph.nodes()}

    # relator_uri → list of lower bounds from its own mediation target ends
    relator_cards: Dict[str, List[int]] = {}
    for row in rdf_graph.query(mediation_card_query):
        uri = str(row[0])
        card_sum = _lower_bound(str(row[1]))
        relator_cards.setdefault(uri, []).append(card_sum)

    out: List[Finding] = []
    for row in rdf_graph.query(relator_query):
        cls_uri = str(row[0])
        cls_name = str(row[1])
        node_id = uri_to_node.get(cls_uri)

        own_sum = sum(relator_cards.get(cls_uri, []))

        # Add cardinalities inherited from ancestor relators.
        ancestor_sum = 0
        if node_id:
            visited: set = set()
            stack = list(gen_graph.successors(node_id))
            while stack:
                anc = stack.pop()
                if anc in visited:
                    continue
                visited.add(anc)
                anc_uri = base_uri + anc
                ancestor_sum += sum(relator_cards.get(anc_uri, []))
                stack.extend(gen_graph.successors(anc))

        total = own_sum + ancestor_sum
        if total < 2:
            out.append(Finding(
                severity=Severity.ERROR,
                code=RULE_RELATOR_NO_MEDIATION,
                message=(
                    f"«relator» '{cls_name}' has insufficient mediation: "
                    f"minimum cardinality sum of mediated ends is {total} (need ≥ 2)"
                ),
                entity_name=cls_name,
                repair_hint=(
                    "Add «mediation» relations so the sum of minimum cardinalities "
                    "across all mediated (non-relator) endpoints is at least 2."
                ),
            ))
    return out


def rule_role_no_identity(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """role/phase classes must have an identity-provider ancestor (ERROR)."""
    return _identity_check(gen_graph, {"role", "phase"}, Severity.ERROR, RULE_ROLE_NO_IDENTITY)


def rule_subkind_no_kind(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """subkind without identity-provider ancestor — WARNING (DPO often relies
    on UFO-C background assumptions; see DP6 design finding)."""
    return _identity_check(gen_graph, {"subkind"}, Severity.WARNING, RULE_SUBKIND_NO_KIND)


def rule_nonsortal_specializes_sortal(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """Non-sortals (category, mixin, roleMixin, phaseMixin) must NOT specialize sortals."""
    out: List[Finding] = []
    for specific, general in gen_graph.edges():
        spec_st = gen_graph.nodes[specific].get("stereotype", "")
        gen_st  = gen_graph.nodes[general].get("stereotype", "")
        if spec_st in NON_SORTALS and gen_st in SORTALS:
            spec_name = gen_graph.nodes[specific].get("name", specific)
            gen_name  = gen_graph.nodes[general].get("name", general)
            out.append(Finding(
                severity=Severity.ERROR,
                code=RULE_NONSORTAL_SPECIALIZES_SORTAL,
                message=(
                    f"«{spec_st}» '{spec_name}' specializes sortal «{gen_st}» '{gen_name}' — "
                    f"non-sortals cannot specialize sortals"
                ),
                entity_name=spec_name,
                repair_hint=(
                    f"Remove the generalization from '{spec_name}' to '{gen_name}', "
                    f"or change '{spec_name}' to a sortal stereotype (e.g. role or subkind)."
                ),
            ))
    return out


def rule_rigid_specializes_antirigid(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """Rigid types (kind, subkind, category) must NOT specialize anti-rigid types."""
    out: List[Finding] = []
    for specific, general in gen_graph.edges():
        spec_st = gen_graph.nodes[specific].get("stereotype", "")
        gen_st  = gen_graph.nodes[general].get("stereotype", "")
        if spec_st in RIGID and gen_st in ANTI_RIGID:
            spec_name = gen_graph.nodes[specific].get("name", specific)
            gen_name  = gen_graph.nodes[general].get("name", general)
            out.append(Finding(
                severity=Severity.ERROR,
                code=RULE_RIGID_SPECIALIZES_ANTIRIGID,
                message=(
                    f"«{spec_st}» '{spec_name}' specializes anti-rigid «{gen_st}» '{gen_name}' — "
                    f"rigid types cannot specialize anti-rigid types"
                ),
                entity_name=spec_name,
                repair_hint=(
                    f"Remove the generalization from '{spec_name}' to '{gen_name}'. "
                    f"Rigid types must only specialize other rigid types or semi-rigid mixins."
                ),
            ))
    return out


def rule_participation_source_is_event(_: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """For every «participation» relation, at least one endpoint must have stereotype event."""
    q = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?rel ?relName ?srcName ?srcSt ?tgtName ?tgtSt WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:participation ;
             ontouml:sourceEnd ?se ;
             ontouml:targetEnd ?te .
        OPTIONAL { ?rel ontouml:name ?relName }
        ?se ontouml:propertyType ?srcCls .
        OPTIONAL { ?srcCls ontouml:name ?srcName }
        OPTIONAL { ?srcCls ontouml:stereotype ?srcSt }
        ?te ontouml:propertyType ?tgtCls .
        OPTIONAL { ?tgtCls ontouml:name ?tgtName }
        OPTIONAL { ?tgtCls ontouml:stereotype ?tgtSt }
    }
    """
    out: List[Finding] = []
    for row in rdf_graph.query(q):
        rel_name = str(row[1]) if row[1] else ""
        src_name = str(row[2]) if row[2] else "?"
        src_st   = str(row[3]).split("#")[-1] if row[3] else ""
        tgt_name = str(row[4]) if row[4] else "?"
        tgt_st   = str(row[5]).split("#")[-1] if row[5] else ""
        if src_st == "event" or tgt_st == "event":
            continue
        label = f"'{rel_name}'" if rel_name.strip() else f"between '{src_name}' and '{tgt_name}'"
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_PARTICIPATION_SOURCE_IS_EVENT,
            message=(
                f"«participation» relation {label}: "
                f"neither endpoint is an event (endpoints: «{src_st}», «{tgt_st}»)"
            ),
            repair_hint=(
                "A «participation» relation must connect an endurant to an «event». "
                "Ensure at least one endpoint class has stereotype «event»."
            ),
        ))
    return out


def rule_creation_source_is_event(_: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """For every «creation» relation, the source endpoint must have stereotype event."""
    q = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?rel ?relName ?srcName ?srcSt ?tgtName ?tgtSt WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:creation ;
             ontouml:sourceEnd ?se ;
             ontouml:targetEnd ?te .
        OPTIONAL { ?rel ontouml:name ?relName }
        ?se ontouml:propertyType ?srcCls .
        OPTIONAL { ?srcCls ontouml:name ?srcName }
        OPTIONAL { ?srcCls ontouml:stereotype ?srcSt }
        ?te ontouml:propertyType ?tgtCls .
        OPTIONAL { ?tgtCls ontouml:name ?tgtName }
        OPTIONAL { ?tgtCls ontouml:stereotype ?tgtSt }
    }
    """
    out: List[Finding] = []
    for row in rdf_graph.query(q):
        rel_name = str(row[1]) if row[1] else ""
        src_name = str(row[2]) if row[2] else "?"
        src_st   = str(row[3]).split("#")[-1] if row[3] else ""
        tgt_name = str(row[4]) if row[4] else "?"
        tgt_st   = str(row[5]).split("#")[-1] if row[5] else ""
        if src_st == "event":
            continue
        label = f"'{rel_name}'" if rel_name.strip() else f"between '{src_name}' and '{tgt_name}'"
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_CREATION_SOURCE_IS_EVENT,
            message=(
                f"«creation» relation {label}: "
                f"source is «{src_st}» not «event» (target: «{tgt_st}»)"
            ),
            repair_hint=(
                "The source of a «creation» relation must be an «event» (event → created endurant). "
                "Change the source class to stereotype «event», or reverse the relation direction."
            ),
        ))
    return out


CHARACTERIZATION_SOURCES = {"quality", "mode", "intrinsic-mode", "extrinsic-mode"}


def rule_characterization_source_is_quality_or_mode(_: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """For every «characterization» relation, the source endpoint must be a quality or mode."""
    q = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?rel ?relName ?srcName ?srcSt ?tgtName ?tgtSt WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:characterization ;
             ontouml:sourceEnd ?se ;
             ontouml:targetEnd ?te .
        OPTIONAL { ?rel ontouml:name ?relName }
        ?se ontouml:propertyType ?srcCls .
        OPTIONAL { ?srcCls ontouml:name ?srcName }
        OPTIONAL { ?srcCls ontouml:stereotype ?srcSt }
        ?te ontouml:propertyType ?tgtCls .
        OPTIONAL { ?tgtCls ontouml:name ?tgtName }
        OPTIONAL { ?tgtCls ontouml:stereotype ?tgtSt }
    }
    """
    out: List[Finding] = []
    for row in rdf_graph.query(q):
        rel_name = str(row[1]) if row[1] else ""
        src_name = str(row[2]) if row[2] else "?"
        src_st   = str(row[3]).split("#")[-1] if row[3] else ""
        tgt_name = str(row[4]) if row[4] else "?"
        tgt_st   = str(row[5]).split("#")[-1] if row[5] else ""
        if src_st in CHARACTERIZATION_SOURCES:
            continue
        label = f"'{rel_name}'" if rel_name.strip() else f"between '{src_name}' and '{tgt_name}'"
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_CHARACTERIZATION_SOURCE_INVALID,
            message=(
                f"«characterization» relation {label}: "
                f"source is «{src_st}» not a quality or mode (target: «{tgt_st}»)"
            ),
            repair_hint=(
                "Change the source class stereotype to «quality» or «mode», "
                "or change the relation stereotype to «material» or an informal association "
                "if the source is not a moment."
            ),
        ))
    return out


def rule_mediation_has_relator_endpoint(_: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """For every «mediation» relation, at least one endpoint must have stereotype relator."""
    q = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?rel ?srcName ?srcSt ?tgtName ?tgtSt WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:mediation ;
             ontouml:sourceEnd ?se ;
             ontouml:targetEnd ?te .
        ?se ontouml:propertyType ?srcCls .
        OPTIONAL { ?srcCls ontouml:name ?srcName }
        OPTIONAL { ?srcCls ontouml:stereotype ?srcSt }
        ?te ontouml:propertyType ?tgtCls .
        OPTIONAL { ?tgtCls ontouml:name ?tgtName }
        OPTIONAL { ?tgtCls ontouml:stereotype ?tgtSt }
    }
    """
    out: List[Finding] = []
    for row in rdf_graph.query(q):
        src_name = str(row[1]) if row[1] else "?"
        src_st   = str(row[2]).split("#")[-1] if row[2] else ""
        tgt_name = str(row[3]) if row[3] else "?"
        tgt_st   = str(row[4]).split("#")[-1] if row[4] else ""
        if src_st == "relator" or tgt_st == "relator":
            continue
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_MEDIATION_NO_RELATOR_ENDPOINT,
            message=(
                f"«mediation» relation between '{src_name}' and '{tgt_name}' "
                f"has no relator endpoint (endpoints: «{src_st}», «{tgt_st}»)"
            ),
            repair_hint=(
                "A «mediation» must connect a «relator» to the entity it mediates. "
                "Change one endpoint's class stereotype to «relator», or change the relation "
                "stereotype to «participation» / «material» / an informal association."
            ),
        ))
    return out


def rule_characterization_bearer_multiplicity(_: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """For every «characterization» relation, the bearer (target) end must have multiplicity 1."""
    q = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT ?rel ?relName ?srcName ?tgtName ?cardStr WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:characterization ;
             ontouml:sourceEnd ?se ;
             ontouml:targetEnd ?te .
        OPTIONAL { ?rel ontouml:name ?relName }
        ?se ontouml:propertyType ?srcCls .
        OPTIONAL { ?srcCls ontouml:name ?srcName }
        ?te ontouml:propertyType ?tgtCls .
        OPTIONAL { ?tgtCls ontouml:name ?tgtName }
        OPTIONAL {
            ?te ontouml:cardinality ?cardNode .
            ?cardNode ontouml:cardinalityValue ?cardStr .
        }
    }
    """
    out: List[Finding] = []
    for row in rdf_graph.query(q):
        rel_name = str(row[1]) if row[1] else ""
        src_name = str(row[2]) if row[2] else "?"
        tgt_name = str(row[3]) if row[3] else "?"
        card_str = str(row[4]) if row[4] is not None else None
        if card_str is None:
            continue
        if _is_exactly_one(card_str):
            continue
        label = f"'{rel_name}'" if rel_name.strip() else f"between '{src_name}' and '{tgt_name}'"
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_CHARACTERIZATION_BEARER_MULT,
            message=(
                f"«characterization» relation {label}: "
                f"bearer '{tgt_name}' has multiplicity '{card_str}', expected '1'"
            ),
            repair_hint=(
                "Set the bearer end of this characterization to multiplicity '1' "
                "(a quality or mode is borne by exactly one entity)."
            ),
        ))
    return out


# Helpers

def _lower_bound(card: str) -> int:
    """Extract the minimum cardinality integer from a string like '1', '1..1', '0..*', '1..*'."""
    s = card.strip()
    lower = s.split("..", 1)[0] if ".." in s else s
    return 0 if lower == "*" else int(lower)


def _is_exactly_one(card: str) -> bool:
    """Return True iff the cardinality string represents exactly 1 (lower=1 and upper=1)."""
    s = card.strip()
    if s == "1":
        return True
    parts = s.split("..", 1)
    return len(parts) == 2 and parts[0] == "1" and parts[1] == "1"


def _identity_check(gen_graph, stereotypes, severity, code) -> List[Finding]:
    out: List[Finding] = []
    for node in gen_graph.nodes():
        st = gen_graph.nodes[node].get("stereotype", "")
        if st not in stereotypes:
            continue
        if _has_identity_ancestor(node, gen_graph):
            continue
        name = gen_graph.nodes[node].get("name", node)
        out.append(Finding(
            severity=severity,
            code=code,
            message=(
                f"«{st}» class '{name}' has no identity-provider ancestor "
                f"(kind, collective, quantity, quality, relator, or mode)"
            ),
            entity_id=node,
            entity_name=name,
            repair_hint=(
                "Add a generalization from this class to a "
                "«kind», «collective», «quantity», «relator», or «mode»."
            ),
        ))
    return out


def _has_identity_ancestor(node_id: str, gen_graph: nx.DiGraph) -> bool:
    visited: set = set()
    stack = list(gen_graph.successors(node_id))
    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        if gen_graph.nodes[cur].get("stereotype", "") in IDENTITY_PROVIDERS:
            return True
        stack.extend(gen_graph.successors(cur))
    return False


# Registry — add new rules here.
ALL_RULES: List[Rule] = [
    rule_disconnected_island,
    rule_generalization_cycle,
    rule_relator_insufficient_mediation,
    rule_role_no_identity,
    rule_subkind_no_kind,
    rule_nonsortal_specializes_sortal,
    rule_rigid_specializes_antirigid,
    rule_participation_source_is_event,
    rule_creation_source_is_event,
    rule_characterization_source_is_quality_or_mode,
    rule_mediation_has_relator_endpoint,
    rule_characterization_bearer_multiplicity,
]
