from __future__ import annotations

import json
import unittest
from pathlib import Path

from dset_toolchain.evidence import validate_evidence_records
from dset_toolchain.frontmatter import render
from dset_toolchain.temp_paths import temporary_directory

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / ".dset/02_layer_gov/schemas/evidence-record.schema.json"
TEMPLATE = ROOT / ".dset/02_layer_gov/templates/evidence-record.md"


class EvidenceRecordTests(unittest.TestCase):
    def test_native_toml_record_enforces_the_bounded_core(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            path = root / "APP-EVIDENCE-RECORD-001.md"
            path.write_text(render(self._record(), "\n# Result\n"), encoding="utf-8")
            self.assertEqual(validate_evidence_records(root, [path], frozenset()), [])

            invalid = self._record()
            invalid.pop("reopen_when")
            invalid["polarity"] = "positive"
            path.write_text(render(invalid, "\n# Result\n"), encoding="utf-8")
            messages = [
                item.message
                for item in validate_evidence_records(root, [path], frozenset())
            ]
            self.assertTrue(
                any("missing fields: reopen_when" in item for item in messages)
            )
            self.assertIn("Evidence Record polarity is invalid", messages)

    def test_yaml_is_only_accepted_for_an_exact_legacy_path(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            path = root / "dset/change/proofs/old.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\nartifact_type: evidence_record\n---\nHistorical proof.\n",
                encoding="utf-8",
            )
            self.assertTrue(validate_evidence_records(root, [path], frozenset()))
            relative = path.relative_to(root).as_posix()
            self.assertEqual(
                validate_evidence_records(root, [path], frozenset({relative})), []
            )

    def test_schema_and_template_are_shipped(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["properties"]["artifact_type"]["const"], "evidence_record"
        )
        self.assertTrue(TEMPLATE.read_text(encoding="utf-8").startswith("+++\n"))

    @staticmethod
    def _record() -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "artifact_type": "evidence_record",
            "artifact_subtype": "test_result",
            "artifact_id": "APP-EVIDENCE-RECORD-001",
            "priority": "medium",
            "llm_session_ids": ["codex:test-session"],
            "context": ["repository=owner/repository", "environment=local"],
            "observed_at": "2026-07-20T12:00:00+04:00",
            "evidence_location": "proofs/result.txt",
            "polarity": "supports",
            "currentness": "current",
            "reopen_when": "The subject revision or method changes.",
            "subject": {
                "id": "APP-TEST-001",
                "revision": "0123456789abcdef0123456789abcdef01234567",
                "intended_use": "Support one bounded Verification claim.",
            },
            "producer": {
                "identity": "test-runner",
                "performed_work": "Executed the declared deterministic test.",
            },
            "method": {
                "description": "Run the focused unit test.",
                "setup": "Python 3.14 with locked dependencies.",
            },
            "relations": [{"type": "evidence_for", "target": "APP-TEST-001"}],
        }


if __name__ == "__main__":
    unittest.main()
