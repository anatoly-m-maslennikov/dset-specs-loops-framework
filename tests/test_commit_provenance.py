from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from dset_toolchain.commit_provenance import (
    CommitRecord,
    validate_commit_history,
    validate_commit_message,
)


class CommitProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.known = {
            "APP-REQUIREMENT-001": ("decision", "requirement"),
            "APP-TEST-001": ("qa", "test"),
            "APP-DEFECT-001": ("problem", "defect"),
        }

    def test_implementation_mode_requires_decision_and_session(self) -> None:
        message = (
            "feat: implement behavior\n\n"
            "Implements: APP-REQUIREMENT-001\n"
            "Resolves: APP-DEFECT-001\n"
            "Session: codex:test-session\n"
        )

        self.assertEqual(validate_commit_message(message, self.known), [])

    def test_evidence_mode_is_distinct(self) -> None:
        message = (
            "test: record proof\n\n"
            "Decision: APP-REQUIREMENT-001\n"
            "Verifies: APP-TEST-001\n"
            "Session: codex:test-session\n"
        )

        self.assertEqual(validate_commit_message(message, self.known), [])

    def test_unknown_nondecision_and_missing_provenance_fail(self) -> None:
        self.assertTrue(validate_commit_message("fix: no trailers", self.known))
        problems = validate_commit_message(
            "fix: wrong\n\n"
            "Implements: APP-TEST-001, APP-UNKNOWN-001\n"
            "Session: codex:test-session\n",
            self.known,
        )
        self.assertIn("Implements must reference a Decision: APP-TEST-001", problems)
        self.assertIn("Implements references unknown ID: APP-UNKNOWN-001", problems)

    def test_exact_correction_revalidates_with_ordinary_rules(self) -> None:
        record = self._record(
            "a" * 40,
            "fix: legacy\n\n"
            "Implements: APP-REQUIREMENT-001, APP-TEST-001\n"
            "Session: codex:test-session\n",
        )
        correction = self._correction(record)

        self.assertEqual(
            validate_commit_history([record], self.known, [correction]), []
        )

    def test_correction_is_bound_to_range_digest_and_unique_commit(self) -> None:
        record = self._record("b" * 40, "fix: no trailers\n")
        wrong_digest = self._correction(record)
        wrong_digest["original_message_sha256"] = "0" * 64

        problems = validate_commit_history([record], self.known, [wrong_digest])

        self.assertIn(
            f"provenance correction message digest mismatch for commit {record.commit}",
            problems,
        )
        correction = self._correction(record)
        duplicate_problems = validate_commit_history(
            [record], self.known, [correction, dict(correction)]
        )
        self.assertIn(
            f"duplicate provenance correction for commit {record.commit}",
            duplicate_problems,
        )
        outside = self._correction(self._record("c" * 40, "fix: absent\n"))
        outside_problems = validate_commit_history([record], self.known, [outside])
        self.assertIn(
            "provenance correction commit is outside the validated range: " + "c" * 40,
            outside_problems,
        )

    def test_correction_cannot_exempt_valid_or_invalid_semantics(self) -> None:
        valid = self._record(
            "d" * 40,
            "feat: valid\n\n"
            "Implements: APP-REQUIREMENT-001\n"
            "Session: codex:test-session\n",
        )
        unnecessary = validate_commit_history(
            [valid], self.known, [self._correction(valid)]
        )
        self.assertIn(
            f"correction for commit {valid.commit} is unnecessary because the "
            "original provenance is valid",
            unnecessary,
        )

        invalid = self._record("e" * 40, "fix: no trailers\n")
        correction = self._correction(invalid)
        correction["decision_ids"] = ["APP-TEST-001"]
        semantic_problems = validate_commit_history(
            [invalid], self.known, [correction]
        )
        self.assertIn(
            f"correction for commit {invalid.commit}: Implements must reference "
            "a Decision: APP-TEST-001",
            semantic_problems,
        )

    def test_project_schema_owns_exact_correction_shape(self) -> None:
        schema = json.loads(
            (
                Path(__file__).parents[1]
                / "dset/scopes/meta/schemas/project.schema.json"
            ).read_text(encoding="utf-8")
        )

        policy = schema["properties"]["commit_provenance"]
        self.assertEqual(
            policy["properties"]["corrections"]["items"]["$ref"],
            "#/$defs/commit_provenance_correction",
        )
        correction = schema["$defs"]["commit_provenance_correction"]
        self.assertEqual(
            set(correction["required"]),
            {
                "commit",
                "original_message_sha256",
                "mode",
                "decision_ids",
                "verifies",
                "resolves",
                "session",
                "rationale",
            },
        )
        self.assertFalse(correction["additionalProperties"])

    @staticmethod
    def _record(commit: str, message: str) -> CommitRecord:
        return CommitRecord(
            commit=commit,
            message=message,
            message_sha256=hashlib.sha256(message.encode()).hexdigest(),
        )

    @staticmethod
    def _correction(record: CommitRecord) -> dict[str, object]:
        return {
            "commit": record.commit,
            "original_message_sha256": record.message_sha256,
            "mode": "implementation",
            "decision_ids": ["APP-REQUIREMENT-001"],
            "verifies": [],
            "resolves": [],
            "session": "codex:test-session",
            "rationale": "Preserve immutable history while correcting provenance.",
        }


if __name__ == "__main__":
    unittest.main()
