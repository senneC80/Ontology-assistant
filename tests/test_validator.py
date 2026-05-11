"""Run the validator against an OntoUML JSON file.

Usage:
    python tests/test_validator.py <path_to_ontology.json>
    python tests/test_validator.py commutrip_FINAL.txt
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validator import validate



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