"""Build a repair prompt from a list of findings — for the 'Send repair' button."""
from __future__ import annotations
from typing import List

from .models import Finding, Severity


def build_repair_prompt(findings: List[Finding], additional_instructions: str = "") -> str:
    """Return a repair prompt for the given findings.

    Empty findings + empty instructions → "".
    Empty findings + non-empty instructions → just the instructions.
    Otherwise: optional instructions block, then the structured findings block.
    """
    if not findings and not additional_instructions:
        return ""

    if not findings:
        return additional_instructions

    lines: list[str] = []

    if additional_instructions:
        lines.append(additional_instructions)
        lines.append("")

    lines += ["The validator found issues with the previous proposal:", ""]

    errors = [f for f in findings if f.severity == Severity.ERROR]
    warnings = [f for f in findings if f.severity == Severity.WARNING]

    if errors:
        lines.append("**Errors (must fix):**")
        for f in errors:
            line = f"- [{f.code}] {f.message}"
            if f.repair_hint:
                line += f"  \n  Hint: {f.repair_hint}"
            lines.append(line)
        lines.append("")

    if warnings:
        lines.append("**Warnings (review):**")
        for f in warnings:
            line = f"- [{f.code}] {f.message}"
            if f.repair_hint:
                line += f"  \n  Hint: {f.repair_hint}"
            lines.append(line)
        lines.append("")

    lines.append(
        "Please regenerate the OntoUML JSON envelope addressing these findings."
    )
    return "\n".join(lines)
