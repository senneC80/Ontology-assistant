import json
import unittest
from unittest.mock import patch

from backend.envelope import extract_envelope
from validator import validate, Severity


class EnvelopeValidationTests(unittest.TestCase):
    def test_extract_envelope_accepts_bare_package_json_block(self):
        package = {
            "type": "Package",
            "id": "pkg",
            "contents": [],
        }
        reply = f"Here is the model:\n```json\n{json.dumps(package)}\n```"

        self.assertEqual(extract_envelope(reply), package)

    def test_validate_warns_and_normalizes_bare_package(self):
        captured = {}

        def fake_build_graphs(project):
            captured["project"] = project
            return object(), object()

        package = {
            "type": "Package",
            "id": "pkg",
            "contents": [],
        }
        with patch("validator.build_graphs", fake_build_graphs), patch(
            "validator.ALL_RULES", []
        ):
            report = validate(package)

        self.assertFalse(report.has_errors())
        self.assertEqual(len(report.warnings()), 1)
        self.assertEqual(report.warnings()[0].severity, Severity.WARNING)
        self.assertEqual(report.warnings()[0].code, "STRUCT_002")
        self.assertEqual(
            captured["project"],
            {
                "type": "Project",
                "id": "auto_project",
                "model": package,
            },
        )


if __name__ == "__main__":
    unittest.main()
