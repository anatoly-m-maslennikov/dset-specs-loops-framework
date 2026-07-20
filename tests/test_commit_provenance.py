from __future__ import annotations

import unittest

from dset_toolchain.commit_provenance import validate_commit_message


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


if __name__ == "__main__":
    unittest.main()
