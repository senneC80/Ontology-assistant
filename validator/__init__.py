"""Validator package. Public API: validate(project) -> Report."""
from __future__ import annotations
import json
from typing import Union

from .models import (
    Finding, Report, Severity,
    RULE_MISSING_PROJECT,
    RULE_STRUCTURAL_SANITY,
)
from .graph import build_graphs
from .rules import ALL_RULES
from .repair import build_repair_prompt

__all__ = ["validate", "Report", "Finding", "Severity", "build_repair_prompt"]


def validate(project: Union[dict, str]) -> Report:
    """Validate an OntoUML project dict or JSON string.

    Runs structural sanity first; if that fails, returns a single ERROR
    finding and skips downstream rules.
    """
    report = Report()

    if isinstance(project, str):
        try:
            project = json.loads(project)
        except json.JSONDecodeError as e:
            report.add(Finding(
                severity=Severity.ERROR,
                code=RULE_STRUCTURAL_SANITY,
                message=f"Could not parse JSON: {e}",
                repair_hint="Return valid JSON in a fenced ```json block.",
            ))
            return report

    bare_package = (
        isinstance(project, dict)
        and project.get("type") == "Package"
        and "contents" in project
        and "model" not in project
    )
    if bare_package:
        project = {
            "type": "Project",
            "id": "auto_project",
            "model": project,
        }

    if not isinstance(project, dict) or "model" not in project:
        report.add(Finding(
            severity=Severity.ERROR,
            code=RULE_STRUCTURAL_SANITY,
            message="JSON does not look like an OntoUML Project (missing 'model' key)",
            repair_hint="Return a complete OntoUML Project envelope per ontouml-schema.",
        ))
        return report

    if bare_package:
        report.add(Finding(
            severity=Severity.WARNING,
            code=RULE_MISSING_PROJECT,
            message=(
                "Missing Project wrapper, normalized for validation; required "
                "for Visual Paradigm import"
            ),
            repair_hint=(
                "Wrap the Package in a Project envelope with `type`, `id`, "
                "and `model` before returning the ontology JSON."
            ),
        ))

    try:
        gen_graph, rdf_graph = build_graphs(project)
    except Exception as e:
        report.add(Finding(
            severity=Severity.ERROR,
            code=RULE_STRUCTURAL_SANITY,
            message=f"Could not build graphs ({type(e).__name__}: {e})",
            repair_hint=(
                "This often means a field value doesn't match the OntoUML JSON schema "
                "(e.g. `restrictedTo` must use OntologicalNature values like "
                "'functional-complex', 'relator', 'event' — not stereotype names like "
                "'kind' or 'subkind')."
            ),
        ))
        return report

    for rule in ALL_RULES:
        for finding in rule(gen_graph, rdf_graph):
            report.add(finding)

    return report
