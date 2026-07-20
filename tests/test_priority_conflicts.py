from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.conflicts import resolve_conflict, write_conflict_result

ROOT = Path(__file__).resolve().parents[1]


class PriorityConflictTests(unittest.TestCase):
    def test_source_beats_projection_before_priority(self) -> None:
        candidate = self._candidate("atomic_authority", "evergreen_projection")
        candidate["relation"] = "source_projection"
        candidate["left"]["priority"] = "low"
        candidate["right"]["priority"] = "critical"

        result = resolve_conflict(ROOT, candidate)

        self.assertEqual(result["conflict_class"], "source_projection_drift")
        self.assertEqual(result["disposition"], "recompile_projection")
        self.assertEqual(result["selected_id"], "APP-DECISION-001")
        self.assertFalse(result["conflict_atom_required"])

    def test_assurance_and_implementation_differences_are_not_conflicts(self) -> None:
        assurance = resolve_conflict(
            ROOT, self._candidate("atomic_authority", "qa")
        )
        conformance = resolve_conflict(
            ROOT, self._candidate("atomic_authority", "implementation")
        )

        self.assertEqual(assurance["disposition"], "update_assurance_and_relying_gate")
        self.assertEqual(conformance["disposition"], "route_problem_defect")
        self.assertFalse(assurance["conflict_atom_required"])
        self.assertFalse(conformance["conflict_atom_required"])

    def test_selectable_policy_uses_precedence_then_priority(self) -> None:
        candidate = self._candidate("atomic_authority", "atomic_authority")
        candidate["selectable"] = True
        candidate["left"]["priority"] = "low"
        candidate["right"]["priority"] = "high"

        priority = resolve_conflict(ROOT, candidate)
        candidate["precedence"] = "APP-DECISION-001"
        precedence = resolve_conflict(ROOT, candidate)

        self.assertEqual(priority["selected_id"], "APP-CONTRACT-001")
        self.assertEqual(priority["disposition"], "selected_by_priority")
        self.assertEqual(precedence["selected_id"], "APP-DECISION-001")
        self.assertEqual(precedence["disposition"], "selected_by_precedence")
        self.assertTrue(priority["conflict_atom_required"])
        self.assertTrue(priority["resolution_event_required"])

    def test_equal_or_immutable_unsatisfiable_authority_stops(self) -> None:
        equal = self._candidate("atomic_authority", "atomic_authority")
        equal["selectable"] = True
        equal["left"]["priority"] = "high"
        equal["right"]["priority"] = "high"
        stopped = resolve_conflict(ROOT, equal)

        immutable = self._candidate("external_authority", "external_authority")
        immutable["left"].update({"immutable": True, "external": True})
        immutable["right"].update({"immutable": True, "external": True})
        unsatisfiable = resolve_conflict(ROOT, immutable)

        self.assertIn("stop_on_equal", stopped["disposition"])
        self.assertEqual(
            unsatisfiable["conflict_class"],
            "unsatisfiable_immutable_authority",
        )
        self.assertIsNone(unsatisfiable["selected_id"])

    def test_inapplicable_candidate_does_not_emit_conflict(self) -> None:
        candidate = self._candidate("atomic_authority", "atomic_authority")
        candidate["context"]["applicable"] = False

        result = resolve_conflict(ROOT, candidate)

        self.assertEqual(result["conflict_class"], "not_a_conflict")
        self.assertFalse(result["conflict_atom_required"])

    def test_explicit_result_write_refuses_external_or_existing_path(self) -> None:
        result = resolve_conflict(
            ROOT, self._candidate("atomic_authority", "atomic_authority")
        )
        with tempfile.TemporaryDirectory(dir=ROOT) as raw:
            root = Path(raw)
            output = root / "result.json"
            self.assertEqual(write_conflict_result(root, output, result), output)
            with self.assertRaises(FileExistsError):
                write_conflict_result(root, output, result)
            with self.assertRaisesRegex(ValueError, "inside the repository"):
                write_conflict_result(root, ROOT.parent / "outside.json", result)

    @staticmethod
    def _candidate(left_role: str, right_role: str) -> dict[str, Any]:
        return {
            "left": {
                "id": "APP-DECISION-001",
                "role": left_role,
                "priority": "medium",
                "priority_source": "atom:APP-DECISION-001",
                "immutable": False,
                "external": False,
            },
            "right": {
                "id": "APP-CONTRACT-001",
                "role": right_role,
                "priority": "medium",
                "priority_source": "atom:APP-CONTRACT-001",
                "immutable": False,
                "external": False,
            },
            "context": {
                "applicable": True,
                "same_scope": True,
                "same_concern": True,
                "same_effective_time": True,
            },
            "relation": "none",
            "selectable": False,
        }


if __name__ == "__main__":
    unittest.main()
