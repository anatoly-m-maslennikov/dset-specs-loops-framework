from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.semantic_atoms import (
    append_lifecycle_event,
    archive_atom,
    build_semantic_atom_index,
    collect_semantic_atoms,
    seal_atom,
    validate_semantic_atoms,
)

ROOT = Path(__file__).resolve().parents[1]


class SemanticAtomTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = create_adopter(ROOT, Path(self.temporary.name) / "adopter")
        self.atom_path = (
            self.root / "dset/changes/DSET-ATOMIC-RECORD-001-output-contract.md"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_repository_ledger_lifecycle_and_schemas_are_valid(self) -> None:
        self.assertEqual(validate_semantic_atoms(ROOT), [])
        schema_root = ROOT / "dset/scopes/gov/schemas"
        schemas = (
            "atom.schema.json",
            "atom-ledger.schema.json",
            "conflict-candidate.schema.json",
            "conflict-result.schema.json",
            "lifecycle.schema.json",
        )
        for name in schemas:
            with self.subTest(name=name):
                json.loads((schema_root / name).read_text(encoding="utf-8"))

    def test_four_type_atom_is_sealed_and_later_mutation_fails(self) -> None:
        self._write_atom()

        seal_atom(self.root, self.atom_path)

        atoms, diagnostics = collect_semantic_atoms(self.root)
        self.assertEqual(diagnostics, [])
        self.assertEqual(atoms["DSET-CONTRACT-001"].semantic_type, "decision")
        self.assertEqual(atoms["DSET-CONTRACT-001"].subtype, "contract")
        self.assertEqual(validate_semantic_atoms(self.root), [])

        self.atom_path.write_text(
            self.atom_path.read_text(encoding="utf-8") + "Changed.\n",
            encoding="utf-8",
        )
        messages = [item.message for item in validate_semantic_atoms(self.root)]
        self.assertIn(
            "sealed atom sha256 changed: DSET-CONTRACT-001",
            messages,
        )

    def test_invalid_nested_or_qa_empty_subtype_fails(self) -> None:
        self._write_atom()
        self.atom_path.write_text(
            self.atom_path.read_text(encoding="utf-8").replace(
                "type: decision\nsubtype: contract",
                "type: qa\nsubtype: requirement/test",
            ),
            encoding="utf-8",
        )

        messages = [item.message for item in validate_semantic_atoms(self.root)]

        self.assertIn("atom has an invalid direct subtype", messages)

    def test_lifecycle_is_append_only_and_absorption_cycles_stop(self) -> None:
        self._write_atom()
        seal_atom(self.root, self.atom_path)
        second = self.root / "dset/changes/DSET-ATOMIC-RECORD-002-format.md"
        second.write_text(
            self._atom_text(
                carrier="DSET-ATOMIC-RECORD-002",
                semantic="DSET-CONTRACT-002",
            ),
            encoding="utf-8",
        )
        seal_atom(self.root, second)
        append_lifecycle_event(
            self.root,
            self._event(
                "DSET-LIFECYCLE-EVENT-001",
                "DSET-CONTRACT-001",
                "DSET-CONTRACT-002",
            ),
        )

        with self.assertRaisesRegex(ValueError, "absorption cycle"):
            append_lifecycle_event(
                self.root,
                self._event(
                    "DSET-LIFECYCLE-EVENT-002",
                    "DSET-CONTRACT-002",
                    "DSET-CONTRACT-001",
                ),
            )

    def test_retired_atom_moves_byte_for_byte_with_stable_lookup(self) -> None:
        original = self._write_atom().encode()
        seal_atom(self.root, self.atom_path)
        append_lifecycle_event(
            self.root,
            {
                "id": "DSET-LIFECYCLE-EVENT-001",
                "atom_id": "DSET-CONTRACT-001",
                "event": "retired",
                "occurred_at": "2026-07-20T00:00:00+04:00",
                "related": [],
                "llm_session_ids": ["codex:test-session"],
            },
        )

        archived = archive_atom(self.root, "DSET-CONTRACT-001")

        self.assertEqual(archived.read_bytes(), original)
        self.assertFalse(self.atom_path.exists())
        self.assertEqual(validate_semantic_atoms(self.root), [])
        row = build_semantic_atom_index(self.root)[0]
        self.assertTrue(row["archived"])
        self.assertEqual(row["current_status"], "retired")
        self.assertEqual(row["path"], archived.relative_to(self.root).as_posix())

    def _write_atom(self) -> str:
        text = self._atom_text(
            carrier="DSET-ATOMIC-RECORD-001",
            semantic="DSET-CONTRACT-001",
        )
        self.atom_path.write_text(text, encoding="utf-8")
        return text

    @staticmethod
    def _atom_text(*, carrier: str, semantic: str) -> str:
        return f"""---
artifact_type: atomic_record
artifact_id: {carrier}
type: decision
subtype: contract
semantic_id: {semantic}
status: accepted
priority: high
llm_session_ids:
  - "codex:test-session"
---

# Contract
"""

    @staticmethod
    def _event(event_id: str, atom_id: str, successor: str) -> dict[str, object]:
        return {
            "id": event_id,
            "atom_id": atom_id,
            "event": "absorbed",
            "occurred_at": "2026-07-20T00:00:00+04:00",
            "related": [successor],
            "llm_session_ids": ["codex:test-session"],
        }


if __name__ == "__main__":
    unittest.main()
