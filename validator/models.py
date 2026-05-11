"""Validator data types: Severity, Finding, Report, rule code constants."""
from __future__ import annotations
import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


# Rule codes
RULE_STRUCTURAL_SANITY    = "STRUCT_001"  # ERROR; short-circuits downstream
RULE_MISSING_PROJECT      = "STRUCT_002"  # WARNING; bare Package normalized
RULE_DISCONNECTED_ISLAND  = "SYMV_001"    # WARNING
RULE_GENERALIZATION_CYCLE = "SYMV_002"    # ERROR
RULE_RELATOR_NO_MEDIATION = "SYMV_003"    # ERROR
RULE_ROLE_NO_IDENTITY     = "SYMV_004"    # ERROR (role/phase only)
RULE_SUBKIND_NO_KIND      = "SYMV_005"    # WARNING (DPO uses orphaned subkinds)


@dataclass
class Finding:
    severity: Severity
    code: str
    message: str
    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    repair_hint: Optional[str] = None

    def __str__(self) -> str:
        base = f"[{self.severity.value.upper()}] {self.code} — {self.message}"
        if self.entity_name:
            base += f" ({self.entity_name})"
        return base


class Report:
    def __init__(self, findings: Optional[List[Finding]] = None) -> None:
        self.findings: List[Finding] = list(findings) if findings else []

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def errors(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == Severity.ERROR]

    def warnings(self) -> List[Finding]:
        return [f for f in self.findings if f.severity == Severity.WARNING]

    def has_errors(self) -> bool:
        return any(f.severity == Severity.ERROR for f in self.findings)

    def has_findings(self) -> bool:
        return len(self.findings) > 0

    def to_dict(self) -> dict:
        return {
            "summary": {
                "total": len(self.findings),
                "errors": len(self.errors()),
                "warnings": len(self.warnings()),
            },
            "findings": [dataclasses.asdict(f) for f in self.findings],
        }
