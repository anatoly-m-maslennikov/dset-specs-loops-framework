from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.adopter import create_adopter
from dset_toolchain.conflicts import (
    ROLES,
    conflict_result_is_fresh,
    emit_conflict_atom,
    resolve_conflict,
    write_conflict_result,
)
from dset_toolchain.semantic_atoms import (
    append_lifecycle_event,
    collect_semantic_atoms,
    seal_atom,
)

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
        assurance = resolve_conflict(ROOT, self._candidate("atomic_authority", "qa"))
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

    def test_every_role_pair_has_a_deterministic_nonempty_disposition(self) -> None:
        for left in sorted(ROLES):
            for right in sorted(ROLES):
                with self.subTest(left=left, right=right):
                    candidate = self._candidate(left, right)
                    candidate["left"]["id"] = f"APP-LEFT-{left.upper()}-001"
                    candidate["right"]["id"] = f"APP-RIGHT-{right.upper()}-002"
                    result = resolve_conflict(ROOT, candidate)
                    self.assertTrue(result["conflict_class"])
                    self.assertTrue(result["disposition"])
                    if result["conflict_atom_required"]:
                        self.assertTrue(
                            {left, right}.issubset(
                                {"atomic_authority", "external_authority"}
                            )
                        )

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

    def test_first_class_conflict_is_assessed_emitted_and_sealed(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = create_adopter(ROOT, Path(raw) / "adopter")
            self._seed_parties(root)
            candidate = self._emission_candidate()
            output = root / "dset/changes/DSET-ATOMIC-RECORD-003-conflict.md"

            path, result = emit_conflict_atom(root, output, candidate)

            atoms, diagnostics = collect_semantic_atoms(root)
            self.assertEqual(diagnostics, [])
            self.assertEqual(path, output)
            self.assertTrue(result["conflict_atom_required"])
            self.assertEqual(atoms["DSET-CONFLICT-003"].subtype, "conflict")
            self.assertEqual(
                atoms["DSET-CONFLICT-003"].child_of,
                ("DSET-DECISION-001", "DSET-CONTRACT-002"),
            )

    def test_priority_change_invalidates_recorded_conflict_result(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = create_adopter(ROOT, Path(raw) / "adopter")
            self._seed_parties(root)
            candidate = self._emission_candidate()
            recorded = resolve_conflict(root, candidate)
            self.assertTrue(conflict_result_is_fresh(root, candidate, recorded))

            append_lifecycle_event(
                root,
                {
                    "id": "DSET-LIFECYCLE-EVENT-001",
                    "atom_id": "DSET-DECISION-001",
                    "event": "priority_changed",
                    "occurred_at": "2026-07-20T00:00:00+04:00",
                    "priority": "critical",
                    "related": [],
                    "llm_session_ids": ["codex:test-session"],
                },
            )

            self.assertFalse(conflict_result_is_fresh(root, candidate, recorded))

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

    @classmethod
    def _emission_candidate(cls) -> dict[str, Any]:
        candidate = cls._candidate("atomic_authority", "atomic_authority")
        candidate["left"]["id"] = "DSET-DECISION-001"
        candidate["right"]["id"] = "DSET-CONTRACT-002"
        candidate["conflict_atom"] = {
            "artifact_id": "DSET-ATOMIC-RECORD-003",
            "semantic_id": "DSET-CONFLICT-003",
            "authority": "operator:test-operator",
            "claim": "The two active authority claims cannot both govern this scope.",
            "scope": {
                "kind": "project",
                "id": "dset-temporary-adopter",
            },
            "llm_session_ids": ["codex:test-session"],
            "material_links": ["DSET-DECISION-001", "DSET-CONTRACT-002"],
            "promotion": {"parent_scope": None},
            "acceptance": "proposed",
            "priority": "high",
            "lineage": ["DSET-DECISION-001", "DSET-CONTRACT-002"],
            "rationale": "Preserve the unresolved specification-level incompatibility.",
        }
        return candidate

    @staticmethod
    def _seed_parties(root: Path) -> None:
        for carrier, semantic, subtype, priority in (
            ("001", "DSET-DECISION-001", None, "medium"),
            ("002", "DSET-CONTRACT-002", "contract", "high"),
        ):
            path = root / f"dset/changes/DSET-ATOMIC-RECORD-{carrier}-party.md"
            subtype_line = f"subtype: {subtype}\n" if subtype else ""
            path.write_text(
                "---\n"
                "artifact_type: atomic_record\n"
                f"artifact_id: DSET-ATOMIC-RECORD-{carrier}\n"
                "type: decision\n"
                f"{subtype_line}"
                f"semantic_id: {semantic}\n"
                "status: accepted\n"
                f"priority: {priority}\n"
                'authority: "operator:test-operator"\n'
                'claim: "This authority claim governs the fixture."\n'
                "scope:\n"
                "  kind: project\n"
                "  id: dset-temporary-adopter\n"
                "promotion:\n"
                "  parent_scope: null\n"
                "llm_session_ids:\n"
                '  - "codex:test-session"\n'
                "---\n\n# Authority\n",
                encoding="utf-8",
            )
            seal_atom(root, path)


if __name__ == "__main__":
    unittest.main()
