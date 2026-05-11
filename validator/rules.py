"""Symbolic validation rules. Registry-based; add a new rule by appending to ALL_RULES."""
from __future__ import annotations
from typing import Callable, List

import networkx as nx
from rdflib import Graph

from .models import (
    Finding, Severity,
    RULE_DISCONNECTED_ISLAND,
    RULE_GENERALIZATION_CYCLE,
    RULE_RELATOR_NO_MEDIATION,
    RULE_ROLE_NO_IDENTITY,
    RULE_SUBKIND_NO_KIND,
)


IDENTITY_PROVIDERS = {"kind", "collective", "quantity", "quality", "relator", "mode"}

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


def rule_relator_no_mediation(gen_graph: nx.DiGraph, rdf_graph: Graph) -> List[Finding]:
    """A «relator» must mediate at least one class, directly or via ancestor."""
    mediated_query = """
    PREFIX ontouml: <https://w3id.org/ontouml#>
    SELECT DISTINCT ?cls WHERE {
        ?rel a ontouml:Relation ;
             ontouml:stereotype ontouml:mediation .
        { ?rel ontouml:sourceEnd ?prop } UNION { ?rel ontouml:targetEnd ?prop }
        ?prop ontouml:propertyType ?cls .
        ?cls a ontouml:Class .
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
    mediated_uris = {str(r[0]) for r in rdf_graph.query(mediated_query)}
    mediated_nodes = {uri_to_node[u] for u in mediated_uris if u in uri_to_node}

    out: List[Finding] = []
    for row in rdf_graph.query(relator_query):
        cls_uri = str(row[0])
        cls_name = str(row[1])
        node_id = uri_to_node.get(cls_uri)
        if cls_uri in mediated_uris:
            continue
        if node_id and _ancestor_in_set(node_id, gen_graph, mediated_nodes):
            continue
        out.append(Finding(
            severity=Severity.ERROR,
            code=RULE_RELATOR_NO_MEDIATION,
            message=f"«relator» class '{cls_name}' has no mediation relation",
            entity_name=cls_name,
            repair_hint="Add a «mediation» relation connecting this relator to its mediated entities.",
        ))
    return out


def rule_role_no_identity(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """role/phase classes must have an identity-provider ancestor (ERROR)."""
    return _identity_check(gen_graph, {"role", "phase"}, Severity.ERROR, RULE_ROLE_NO_IDENTITY)


def rule_subkind_no_kind(gen_graph: nx.DiGraph, _: Graph) -> List[Finding]:
    """subkind without identity-provider ancestor — WARNING (DPO often relies
    on UFO-C background assumptions; see DP6 design finding)."""
    return _identity_check(gen_graph, {"subkind"}, Severity.WARNING, RULE_SUBKIND_NO_KIND)


# Helpers

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


def _ancestor_in_set(node_id: str, gen_graph: nx.DiGraph, target: set) -> bool:
    visited: set = set()
    stack = [node_id]
    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        for parent in gen_graph.successors(cur):
            if parent in target:
                return True
            stack.append(parent)
    return False


# Registry — add new rules here.
ALL_RULES: List[Rule] = [
    rule_disconnected_island,
    rule_generalization_cycle,
    rule_relator_no_mediation,
    rule_role_no_identity,
    rule_subkind_no_kind,
]