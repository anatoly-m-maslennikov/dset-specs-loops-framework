from __future__ import annotations

import hashlib
import json
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
from dset_toolchain.temp_paths import temporary_directory

ROOT = Path(__file__).resolve().parents[1]


class PriorityConflictTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = temporary_directory()
        self.root = Path(self.temporary.name).resolve()
        (self.root / "README.md").write_text("# Conflict evidence\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_source_projection_relation_is_derived_before_priority(self) -> None:
        root = create_adopter(ROOT, self.root / "adopter")
        self._seed_parties(root)
        projection = self._write_fact(
            root,
            "DSET-SPECIFICATION-099",
            artifact_type="specification",
            priority="critical",
            scope={"kind": "project", "id": "dset-temporary-adopter"},
            relations=[{"type": "projection_of", "target": "DSET-DECISION-001"}],
        )
        candidate = self._atomic_candidate(root)
        candidate["right"] = {
            "id": "DSET-SPECIFICATION-099",
            "source": projection,
        }

        result = resolve_conflict(root, candidate)

        self.assertEqual(result["conflict_class"], "source_projection_drift")
        self.assertEqual(result["disposition"], "recompile_projection")
        self.assertEqual(result["selected_id"], "DSET-DECISION-001")
        self.assertEqual(result["left"]["role"], "atomic_authority")
        self.assertEqual(result["right"]["role"], "evergreen_projection")

    def test_assurance_and_implementation_differences_are_not_conflicts(self) -> None:
        assurance = resolve_conflict(
            self.root, self._candidate("atomic_authority", "qa")
        )
        conformance = resolve_conflict(
            self.root, self._candidate("atomic_authority", "implementation")
        )

        self.assertEqual(assurance["disposition"], "update_assurance_and_relying_gate")
        self.assertEqual(conformance["disposition"], "route_problem_defect")
        self.assertFalse(assurance["conflict_atom_required"])
        self.assertFalse(conformance["conflict_atom_required"])

    def test_selectable_policy_uses_registered_precedence_then_priority(self) -> None:
        priority_candidate = self._candidate(
            "atomic_authority",
            "atomic_authority",
            left_priority="low",
            right_priority="high",
            selectable=True,
        )
        priority = resolve_conflict(self.root, priority_candidate)

        rules = self.root / "rules"
        rules.mkdir()
        (rules / "left.md").write_text("# Left rule\n", encoding="utf-8")
        (rules / "right.md").write_text("# Right rule\n", encoding="utf-8")
        governance = self.root / "dset/governance.yaml"
        governance.parent.mkdir(parents=True)
        governance.write_text(
            "schema_version: 1.0\n"
            "rules:\n"
            "  - id: APP-RULE-LEFT-001\n"
            "    path: rules/left.md\n"
            "    applicability: applicable\n"
            "    precedence_over:\n"
            "      - APP-RULE-RIGHT-002\n"
            "  - id: APP-RULE-RIGHT-002\n"
            "    path: rules/right.md\n"
            "    applicability: applicable\n"
            "    precedence_over: []\n",
            encoding="utf-8",
        )
        precedence_candidate = {
            "left": {"id": "APP-RULE-LEFT-001"},
            "right": {"id": "APP-RULE-RIGHT-002"},
            "context": self._context(self.root),
            "selectable": True,
        }
        precedence = resolve_conflict(self.root, precedence_candidate)

        self.assertEqual(priority["selected_id"], "APP-RIGHT-002")
        self.assertEqual(priority["disposition"], "selected_by_priority")
        self.assertEqual(precedence["selected_id"], "APP-RULE-LEFT-001")
        self.assertEqual(precedence["disposition"], "selected_by_precedence")
        self.assertTrue(priority["resolution_event_required"])

    def test_equal_or_immutable_unsatisfiable_authority_stops(self) -> None:
        equal = resolve_conflict(
            self.root,
            self._candidate(
                "atomic_authority",
                "atomic_authority",
                left_priority="high",
                right_priority="high",
                selectable=True,
            ),
        )
        immutable = resolve_conflict(
            self.root,
            self._candidate(
                "external_authority",
                "external_authority",
                left_immutable=True,
                right_immutable=True,
                left_external=True,
                right_external=True,
            ),
        )

        self.assertIn("stop_on_equal", equal["disposition"])
        self.assertEqual(
            immutable["conflict_class"], "unsatisfiable_immutable_authority"
        )
        self.assertIsNone(immutable["selected_id"])

    def test_inapplicable_state_is_derived(self) -> None:
        candidate = self._candidate(
            "atomic_authority", "atomic_authority", left_applicable=False
        )

        result = resolve_conflict(self.root, candidate)

        self.assertEqual(result["conflict_class"], "not_a_conflict")
        self.assertFalse(result["conflict_atom_required"])

    def test_unresolved_party_and_fabricated_facts_are_rejected(self) -> None:
        candidate = self._candidate(
            "atomic_authority", "atomic_authority", left_immutable=True
        )
        candidate["left"]["immutable"] = False
        with self.assertRaisesRegex(ValueError, "mismatches repository truth"):
            resolve_conflict(self.root, candidate)

        candidate["left"] = {"id": "APP-UNKNOWN-099"}
        with self.assertRaisesRegex(ValueError, "party source requires"):
            resolve_conflict(self.root, candidate)

    def test_stale_party_and_context_evidence_are_rejected(self) -> None:
        candidate = self._candidate("atomic_authority", "atomic_authority")
        recorded = resolve_conflict(self.root, candidate)
        left_path = self.root / str(candidate["left"]["source"]["path"])
        left_path.write_text("{}\n", encoding="utf-8")
        self.assertFalse(conflict_result_is_fresh(self.root, candidate, recorded))
        with self.assertRaisesRegex(ValueError, "party source is stale"):
            resolve_conflict(self.root, candidate)

        candidate = self._candidate("atomic_authority", "atomic_authority")
        recorded = resolve_conflict(self.root, candidate)
        (self.root / "README.md").write_text("# Changed evidence\n", encoding="utf-8")
        self.assertFalse(conflict_result_is_fresh(self.root, candidate, recorded))
        with self.assertRaisesRegex(ValueError, "context evidence is stale"):
            resolve_conflict(self.root, candidate)

    def test_relation_and_precedence_assertion_mismatches_are_rejected(self) -> None:
        candidate = self._candidate("atomic_authority", "atomic_authority")
        candidate["relation"] = "absorption"
        candidate["relation_winner"] = "APP-LEFT-001"
        with self.assertRaisesRegex(ValueError, "relation assertion mismatches"):
            resolve_conflict(self.root, candidate)

        candidate = self._candidate("atomic_authority", "atomic_authority")
        candidate["precedence"] = "APP-LEFT-001"
        with self.assertRaisesRegex(ValueError, "precedence assertion mismatches"):
            resolve_conflict(self.root, candidate)

    def test_conflict_party_priority_must_use_the_project_vocabulary(self) -> None:
        candidate = self._candidate(
            "atomic_authority",
            "atomic_authority",
            left_priority="unregistered",
        )

        with self.assertRaisesRegex(ValueError, "not in the project scale"):
            resolve_conflict(self.root, candidate)

    def test_every_role_pair_has_a_deterministic_nonempty_disposition(self) -> None:
        for left in sorted(ROLES):
            for right in sorted(ROLES):
                with self.subTest(left=left, right=right):
                    result = resolve_conflict(self.root, self._candidate(left, right))
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
            self.root, self._candidate("atomic_authority", "atomic_authority")
        )
        output = self.root / "result.json"
        self.assertEqual(write_conflict_result(self.root, output, result), output)
        with self.assertRaises(FileExistsError):
            write_conflict_result(self.root, output, result)
        with self.assertRaisesRegex(ValueError, "inside the repository"):
            write_conflict_result(
                self.root, self.root.parent / "outside-conflict-result.json", result
            )

    def test_first_class_conflict_is_assessed_emitted_and_sealed(self) -> None:
        root = create_adopter(ROOT, self.root / "adopter")
        self._seed_parties(root)
        candidate = self._emission_candidate(root)
        output = root / "dset/changes/DSET-ATOMIC-RECORD-003-conflict.md"

        path, result = emit_conflict_atom(root, output, candidate)

        atoms, diagnostics = collect_semantic_atoms(root)
        self.assertEqual(diagnostics, [])
        self.assertEqual(path, output)
        self.assertTrue(result["conflict_atom_required"])
        self.assertEqual(atoms["DSET-CONFLICT-003"].subtype, "conflict")

    def test_absorption_and_priority_lifecycle_are_repository_derived(self) -> None:
        root = create_adopter(ROOT, self.root / "adopter")
        self._seed_parties(root, replacement=True)
        candidate = self._atomic_candidate(root)
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

        append_lifecycle_event(
            root,
            {
                "id": "DSET-LIFECYCLE-EVENT-002",
                "atom_id": "DSET-DECISION-001",
                "event": "absorbed",
                "occurred_at": "2026-07-20T01:00:00+04:00",
                "related": ["DSET-CONTRACT-002"],
                "llm_session_ids": ["codex:test-session"],
            },
        )
        candidate["context"]["applicable"] = False
        absorbed = resolve_conflict(root, candidate)
        self.assertEqual(absorbed["conflict_class"], "absorption")
        self.assertEqual(absorbed["selected_id"], "DSET-CONTRACT-002")

    def _candidate(
        self,
        left_role: str,
        right_role: str,
        *,
        left_priority: str = "medium",
        right_priority: str = "medium",
        left_immutable: bool = False,
        right_immutable: bool = False,
        left_external: bool = False,
        right_external: bool = False,
        left_applicable: bool = True,
        right_applicable: bool = True,
        selectable: bool = False,
    ) -> dict[str, Any]:
        left = self._write_fact(
            self.root,
            "APP-LEFT-001",
            conflict_role=left_role,
            priority=left_priority,
            immutable=left_immutable,
            external=left_external,
            applicability=left_applicable,
        )
        right = self._write_fact(
            self.root,
            "APP-RIGHT-002",
            conflict_role=right_role,
            priority=right_priority,
            immutable=right_immutable,
            external=right_external,
            applicability=right_applicable,
        )
        context = self._context(self.root)
        context["applicable"] = left_applicable and right_applicable
        return {
            "left": {"id": "APP-LEFT-001", "source": left},
            "right": {"id": "APP-RIGHT-002", "source": right},
            "context": context,
            "selectable": selectable,
        }

    @staticmethod
    def _write_fact(
        root: Path,
        identifier: str,
        **facts: Any,
    ) -> dict[str, str]:
        directory = root / "conflict-facts"
        directory.mkdir(exist_ok=True)
        path = directory / f"{identifier.lower()}.json"
        metadata = {
            "artifact_id": identifier,
            "artifact_type": "conflict_party_fact",
            "scope": {"kind": "project", "id": "conflict-fixture"},
            "current_status": "accepted",
            **facts,
        }
        path.write_text(json.dumps(metadata, sort_keys=True) + "\n", encoding="utf-8")
        return PriorityConflictTests._identity(root, path)

    @staticmethod
    def _context(root: Path) -> dict[str, Any]:
        evidence_path = root / "README.md"
        return {
            "applicable": True,
            "same_scope": True,
            "same_concern": True,
            "same_effective_time": True,
            "evidence": [PriorityConflictTests._identity(root, evidence_path)],
        }

    @staticmethod
    def _identity(root: Path, path: Path) -> dict[str, str]:
        return {
            "path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    @classmethod
    def _atomic_candidate(cls, root: Path) -> dict[str, Any]:
        return {
            "left": {"id": "DSET-DECISION-001"},
            "right": {"id": "DSET-CONTRACT-002"},
            "context": cls._context(root),
            "selectable": False,
        }

    @classmethod
    def _emission_candidate(cls, root: Path) -> dict[str, Any]:
        candidate = cls._atomic_candidate(root)
        candidate["conflict_atom"] = {
            "artifact_id": "DSET-ATOMIC-RECORD-003",
            "semantic_id": "DSET-CONFLICT-003",
            "authority": "operator:test-operator",
            "claim": "The two active authority claims cannot both govern this scope.",
            "scope": {"kind": "project", "id": "dset-temporary-adopter"},
            "llm_session_ids": ["codex:test-session"],
            "material_links": ["DSET-DECISION-001", "DSET-CONTRACT-002"],
            "promotion": {"parent_scope": None},
            "acceptance": "proposed",
            "priority": "high",
            "lineage": ["DSET-DECISION-001", "DSET-CONTRACT-002"],
            "rationale": "Preserve the unresolved incompatibility.",
        }
        return candidate

    @staticmethod
    def _seed_parties(root: Path, *, replacement: bool = False) -> None:
        for carrier, semantic, subtype, priority in (
            ("001", "DSET-DECISION-001", None, "medium"),
            ("002", "DSET-CONTRACT-002", "contract", "high"),
        ):
            path = root / f"dset/changes/DSET-ATOMIC-RECORD-{carrier}-party.md"
            subtype_line = f"subtype: {subtype}\n" if subtype else ""
            relation = (
                "relations:\n  - type: replacement_of\n    target: DSET-DECISION-001\n"
                if replacement and semantic == "DSET-CONTRACT-002"
                else ""
            )
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
                f"{relation}"
                "llm_session_ids:\n"
                '  - "codex:test-session"\n'
                "---\n\n# Authority\n",
                encoding="utf-8",
            )
            seal_atom(root, path)


if __name__ == "__main__":
    unittest.main()
