from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.external_review import (
    create_review_packet,
    reconcile_review,
    validate_review_report,
    write_reconciliation,
)
from dset_toolchain.yaml_subset import dump, loads

ROOT = Path(__file__).resolve().parents[1]


class ExternalReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.work = Path(self.temporary.name)
        self.packet = self.work / "review-packet.md"
        create_review_packet(
            ROOT,
            self.packet,
            packet_id="DSET-REVIEW-PACKET-001",
            artifacts=["README.md"],
            criteria=["Check exact behavior against accepted truth"],
            scope="README behavior only",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_packet_binds_exact_commit_inputs_rules_and_read_only_effect(self) -> None:
        metadata = self._metadata(self.packet)
        self.assertEqual(metadata["allowed_effects"], ["read_only_report"])
        self.assertEqual(len(str(metadata["commit"])), 40)
        reviewed = metadata["reviewed_inputs"]
        assert isinstance(reviewed, list)
        self.assertEqual(reviewed[0]["path"], "README.md")
        self.assertTrue(metadata["resolved_rules"])
        with self.assertRaises(FileExistsError):
            create_review_packet(
                ROOT,
                self.packet,
                packet_id="DSET-REVIEW-PACKET-001",
                artifacts=["README.md"],
                criteria=["same"],
                scope="same",
            )

    def test_report_envelope_accepts_free_form_body_and_stable_findings(self) -> None:
        report = self._write_report()
        result = validate_review_report(ROOT, self.packet, report)
        self.assertEqual(result["finding_ids"], ["DSET-REVIEW-FINDING-001"])
        self.assertFalse(result["implementation_authorized"])

    def test_reconciliation_is_complete_explicit_and_never_authorizes_repair(
        self,
    ) -> None:
        report = self._write_report()
        candidate = self.work / "reconcile.json"
        candidate.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "report_id": "DSET-EVIDENCE-RECORD-099",
                    "report_sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
                    "reconciled_at": "2026-07-20T12:00:00+04:00",
                    "llm_session_ids": ["codex:test-session"],
                    "findings": [
                        {
                            "finding_id": "DSET-REVIEW-FINDING-001",
                            "disposition": "route_problem",
                            "rationale": "Observed behavior violates accepted truth.",
                            "target_id": "DSET-PROBLEM-GOV-099",
                            "reopen_proof": ["DSET-TEST-GOV-025"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        result = reconcile_review(ROOT, self.packet, report, candidate)
        self.assertEqual(result["reopen_proof"], ["DSET-TEST-GOV-025"])
        self.assertFalse(result["implementation_authorized"])
        output = self.work / "result.json"
        write_reconciliation(self.work, output, result)
        self.assertTrue(output.is_file())
        with self.assertRaises(FileExistsError):
            write_reconciliation(self.work, output, result)

    def test_report_input_drift_stops(self) -> None:
        report = self._write_report(reviewed_inputs=[])
        with self.assertRaisesRegex(ValueError, "inputs do not match"):
            validate_review_report(ROOT, self.packet, report)

    def _write_report(self, *, reviewed_inputs: object | None = None) -> Path:
        packet = self._metadata(self.packet)
        report = self.work / "review-report.md"
        metadata = {
            "schema_version": "1.0",
            "artifact_type": "evidence_record",
            "artifact_subtype": "review_report",
            "artifact_id": "DSET-EVIDENCE-RECORD-099",
            "packet_id": packet["packet_id"],
            "priority": "high",
            "reviewer": {
                "identity": "independent-reviewer",
                "host": "claude-code",
                "model": "available-model",
                "tool_version": "1.0",
            },
            "llm_session_ids": ["claude:test-session"],
            "reviewed_commit": packet["commit"],
            "reviewed_inputs": (
                packet["reviewed_inputs"]
                if reviewed_inputs is None
                else reviewed_inputs
            ),
            "method": "Independent bounded conformance review",
            "observed_at": "2026-07-20T11:00:00+04:00",
            "limitations": ["No hosted CI access"],
            "findings": [
                {
                    "id": "DSET-REVIEW-FINDING-001",
                    "priority": "high",
                    "evidence": "README line and accepted rule disagree",
                    "confidence": "high",
                    "impact": "Operator may follow stale behavior",
                    "proposed_disposition": "route_problem",
                }
            ],
        }
        report.write_text(
            f"---\n{dump(metadata)}---\n\n# Review report\n\n"
            "Free-form narrative, tables, or host-specific detail may live here.\n",
            encoding="utf-8",
        )
        return report

    @staticmethod
    def _metadata(path: Path) -> dict[str, object]:
        lines = path.read_text(encoding="utf-8").splitlines()
        end = lines.index("---", 1)
        value = loads("\n".join(lines[1:end]))
        assert isinstance(value, dict)
        return value


if __name__ == "__main__":
    unittest.main()
