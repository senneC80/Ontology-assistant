"""Validator package. Public API: validate(project) -> Report."""
from __future__ import annotations
import json
from typing import Union

from .models import (
    Finding, Report, Severity,
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

    if not isinstance(project, dict) or "model" not in project:
        report.add(Finding(
            severity=Severity.ERROR,
            code=RULE_STRUCTURAL_SANITY,
            message="JSON does not look like an OntoUML Project (missing 'model' key)",
            repair_hint="Return a complete OntoUML Project envelope per ontouml-schema.",
        ))
        return report

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