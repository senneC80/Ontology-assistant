"""Validator tests.

CLI usage:
    python tests/test_validator.py <path_to_ontology.json>

Pytest usage:
    pytest tests/test_validator.py
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validator import validate
from validator.rules import _lower_bound


# ---------------------------------------------------------------------------
# CLI entry point (unchanged)
# ---------------------------------------------------------------------------

def run(json_path: Path) -> int:
    if not json_path.exists():
        print(f"File not found: {json_path}")
        return 1

    with json_path.open(encoding="utf-8") as f:
        project = json.load(f)

    report = validate(project)

    print(f"Validating: {json_path.name}")
    print(f"  {len(report.errors())} error(s), {len(report.warnings())} warning(s)")
    print()
    for f in report.findings:
        print(f"  {f}")

    return 1 if report.has_errors() else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tests/test_validator.py <path_to_ontology.json>")
        sys.exit(2)
    sys.exit(run(Path(sys.argv[1])))


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _cls(id_, name, stereotype, restricted_to=None):
    return {
        "id": id_,
        "name": name,
        "type": "Class",
        "stereotype": stereotype,
        "isAbstract": False,
        "isDerived": False,
        "properties": [],
        "restrictedTo": restricted_to or ["functional-complex"],
    }


def _rel(id_, name, stereotype, src_id, src_card, tgt_id, tgt_card):
    return {
        "id": id_,
        "name": name,
        "type": "Relation",
        "stereotype": stereotype,
        "isAbstract": False,
        "isDerived": False,
        "properties": [
            {
                "id": f"{id_}_src",
                "type": "Property",
                "isDerived": False,
                "isReadOnly": False,
                "isOrdered": False,
                "cardinality": src_card,
                "propertyType": {"id": src_id, "type": "Class"},
                "aggregationKind": "NONE",
            },
            {
                "id": f"{id_}_tgt",
                "type": "Property",
                "isDerived": False,
                "isReadOnly": False,
                "isOrdered": False,
                "cardinality": tgt_card,
                "propertyType": {"id": tgt_id, "type": "Class"},
                "aggregationKind": "NONE",
            },
        ],
    }


def _gen(id_, specific_id, general_id):
    return {
        "id": id_,
        "type": "Generalization",
        "specific": {"id": specific_id, "type": "Class"},
        "general": {"id": general_id, "type": "Class"},
    }


def _project(*contents):
    return {
        "type": "Project",
        "id": "test_proj",
        "model": {
            "id": "test_pkg",
            "name": "Test",
            "type": "Package",
            "contents": list(contents),
        },
    }


def _codes(report):
    return {f.code for f in report.findings}


# ---------------------------------------------------------------------------
# _lower_bound unit tests
# ---------------------------------------------------------------------------

def test_lower_bound_single_number():
    assert _lower_bound("1") == 1

def test_lower_bound_exact():
    assert _lower_bound("1..1") == 1

def test_lower_bound_zero_star():
    assert _lower_bound("0..*") == 0

def test_lower_bound_one_star():
    assert _lower_bound("1..*") == 1


# ---------------------------------------------------------------------------
# SYMV_003 — rule_relator_insufficient_mediation
# ---------------------------------------------------------------------------

def test_symv003_fires_when_cardinality_sum_below_two():
    # Relator mediates one class with target cardinality 0..* (lower=0). Sum=0 < 2.
    proj = _project(
        _cls("rel1", "Employment", "relator", ["relator"]),
        _cls("c1",   "Person",     "role"),
        _rel("m1", "", "mediation", "rel1", "1", "c1", "0..*"),
    )
    report = validate(proj)
    assert "SYMV_003" in _codes(report)


def test_symv003_passes_when_cardinality_sum_is_two():
    # Relator mediates two classes each with target cardinality 1. Sum=2 >= 2.
    proj = _project(
        _cls("rel1", "Contract",   "relator", ["relator"]),
        _cls("c1",   "Employer",   "role"),
        _cls("c2",   "Employee",   "role"),
        _rel("m1", "", "mediation", "rel1", "1", "c1", "1"),
        _rel("m2", "", "mediation", "rel1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_003" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_006 — rule_nonsortal_specializes_sortal
# ---------------------------------------------------------------------------

def test_symv006_fires_when_category_specializes_kind():
    proj = _project(
        _cls("k1", "Agent",   "kind"),
        _cls("c1", "Animate", "category"),
        _gen("g1", "c1", "k1"),
    )
    report = validate(proj)
    assert "SYMV_006" in _codes(report)


def test_symv006_passes_when_category_specializes_category():
    proj = _project(
        _cls("c1", "PhysicalObject", "category"),
        _cls("c2", "LivingThing",    "category"),
        _gen("g1", "c2", "c1"),
    )
    report = validate(proj)
    assert "SYMV_006" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_007 — rule_rigid_specializes_antirigid
# ---------------------------------------------------------------------------

def test_symv007_fires_when_kind_specializes_role():
    proj = _project(
        _cls("r1", "Employee", "role"),
        _cls("k1", "Worker",   "kind"),
        _gen("g1", "k1", "r1"),
    )
    report = validate(proj)
    assert "SYMV_007" in _codes(report)


def test_symv007_passes_when_subkind_specializes_kind():
    proj = _project(
        _cls("k1", "Person",  "kind"),
        _cls("s1", "Student", "subkind"),
        _gen("g1", "s1", "k1"),
    )
    report = validate(proj)
    assert "SYMV_007" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_008 — rule_participation_source_is_event
# ---------------------------------------------------------------------------

def test_symv008_fires_when_neither_endpoint_is_event():
    # Both endpoints are roles — no event involved.
    proj = _project(
        _cls("c1", "Person",   "role"),
        _cls("c2", "Activity", "role"),
        _rel("p1", "plays", "participation", "c1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_008" in _codes(report)


def test_symv008_passes_when_one_endpoint_is_event():
    proj = _project(
        _cls("c1", "Person",  "role"),
        _cls("ev", "Meeting", "event", ["event"]),
        _rel("p1", "participates in", "participation", "c1", "1", "ev", "1"),
    )
    report = validate(proj)
    assert "SYMV_008" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_009 — rule_creation_source_is_event
# ---------------------------------------------------------------------------

def test_symv009_fires_when_source_is_not_event():
    # Source is a role, not an event.
    proj = _project(
        _cls("c1", "Person",    "role"),
        _cls("c2", "Document",  "kind"),
        _rel("cr", "creates", "creation", "c1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_009" in _codes(report)


def test_symv009_passes_when_source_is_event():
    proj = _project(
        _cls("ev", "Signing",   "event", ["event"]),
        _cls("c2", "Contract",  "kind"),
        _rel("cr", "creates", "creation", "ev", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_009" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_010 — rule_characterization_source_is_quality_or_mode
# ---------------------------------------------------------------------------

def test_symv010_fires_when_source_is_not_quality_or_mode():
    # Source is a kind, not a quality/mode.
    proj = _project(
        _cls("c1", "Weight",  "kind"),
        _cls("c2", "Person",  "kind"),
        _rel("ch", "characterizes", "characterization", "c1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_010" in _codes(report)


def test_symv010_passes_when_source_is_quality():
    proj = _project(
        _cls("q1", "Weight",  "quality", ["quality"]),
        _cls("c2", "Person",  "kind"),
        _rel("ch", "characterizes", "characterization", "q1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_010" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_011 — rule_mediation_has_relator_endpoint
# ---------------------------------------------------------------------------

def test_symv011_fires_when_neither_endpoint_is_relator():
    # Both endpoints are non-relators.
    proj = _project(
        _cls("c1", "Employee", "role"),
        _cls("c2", "Employer", "kind"),
        _rel("m1", "", "mediation", "c1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_011" in _codes(report)


def test_symv011_passes_when_relator_is_source():
    proj = _project(
        _cls("r1", "Contract",  "relator", ["relator"]),
        _cls("c2", "Employer",  "kind"),
        _cls("c3", "Employee",  "kind"),
        _rel("m1", "", "mediation", "r1", "1", "c2", "1"),
        _rel("m2", "", "mediation", "r1", "1", "c3", "1"),
    )
    report = validate(proj)
    assert "SYMV_011" not in _codes(report)


def test_symv011_passes_when_relator_is_target():
    # Relator on the target end — direction-agnostic check must pass.
    proj = _project(
        _cls("c1", "Traveller", "role"),
        _cls("r1", "Booking",   "relator", ["relator"]),
        _cls("c3", "Provider",  "role"),
        _rel("m1", "", "mediation", "c1", "1", "r1", "1"),
        _rel("m2", "", "mediation", "c3", "1", "r1", "1"),
    )
    report = validate(proj)
    assert "SYMV_011" not in _codes(report)


# ---------------------------------------------------------------------------
# SYMV_012 — rule_characterization_bearer_multiplicity
# ---------------------------------------------------------------------------

def test_symv012_fires_when_bearer_multiplicity_is_not_one():
    # Bearer (target) has cardinality 0..* — not exactly 1.
    proj = _project(
        _cls("q1", "Weight",  "quality", ["quality"]),
        _cls("c2", "Person",  "kind"),
        _rel("ch", "characterizes", "characterization", "q1", "1", "c2", "0..*"),
    )
    report = validate(proj)
    assert "SYMV_012" in _codes(report)


def test_symv012_passes_when_bearer_multiplicity_is_one():
    proj = _project(
        _cls("q1", "Weight",  "quality", ["quality"]),
        _cls("c2", "Person",  "kind"),
        _rel("ch", "characterizes", "characterization", "q1", "1", "c2", "1"),
    )
    report = validate(proj)
    assert "SYMV_012" not in _codes(report)


def test_symv012_skips_when_bearer_has_no_cardinality():
    # Omit cardinality on the target end entirely — rule must not fire.
    proj = _project(
        _cls("q1", "Weight",  "quality", ["quality"]),
        _cls("c2", "Person",  "kind"),
        {
            "id": "ch",
            "name": "characterizes",
            "type": "Relation",
            "stereotype": "characterization",
            "isAbstract": False,
            "isDerived": False,
            "properties": [
                {
                    "id": "ch_src",
                    "type": "Property",
                    "isDerived": False,
                    "isReadOnly": False,
                    "isOrdered": False,
                    "cardinality": "1",
                    "propertyType": {"id": "q1", "type": "Class"},
                    "aggregationKind": "NONE",
                },
                {
                    "id": "ch_tgt",
                    "type": "Property",
                    "isDerived": False,
                    "isReadOnly": False,
                    "isOrdered": False,
                    # cardinality deliberately omitted
                    "propertyType": {"id": "c2", "type": "Class"},
                    "aggregationKind": "NONE",
                },
            ],
        },
    )
    report = validate(proj)
    assert "SYMV_012" not in _codes(report)
