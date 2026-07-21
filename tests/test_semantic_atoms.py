from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.layout import discover_layout
from dset_toolchain.legacy_authority import (
    legacy_authority_ids,
    validate_legacy_authority_ledger,
)
from dset_toolchain.semantic_atoms import (
    append_lifecycle_event,
    archive_atom,
    build_semantic_atom_index,
    collect_semantic_atoms,
    seal_atom,
    validate_semantic_atoms,
)
from dset_toolchain.semantic_types import build_semantic_classification_index
from dset_toolchain.yaml_subset import dump, load

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
            "legacy-authority-ledger.schema.json",
        )
        for name in schemas:
            with self.subTest(name=name):
                json.loads((schema_root / name).read_text(encoding="utf-8"))

    def test_legacy_authority_fragments_are_immutable(self) -> None:
        package_root = self.root / "dset/specs/packages/sample"
        package = discover_layout(self.root).structured_file(
            package_root, "package.toml"
        )
        data = load(package)
        assert isinstance(data, dict)
        data["contracts"] = []
        package.write_text(dump(data, package), encoding="utf-8")

        messages = [item.message for item in validate_semantic_atoms(self.root)]

        self.assertIn(
            "legacy Decision authority changed without native successors",
            messages,
        )

    def test_legacy_ledger_keeps_historical_yaml_identity_after_toml_cutover(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            root = Path(raw).resolve()
            governance = root / "dset/governance"
            package_root = root / "dset/specs/packages/sample"
            governance.mkdir(parents=True)
            package_root.mkdir(parents=True)
            (root / "dset/dset.yaml").write_text(
                'schema_version: "1.0"\n', encoding="utf-8"
            )
            historical = package_root / "package.yaml"
            historical.write_text(
                "contracts:\n  - DSET-CONTRACT-GOV-001\n",
                encoding="utf-8",
            )
            (package_root / "package.toml").write_text(
                "contracts = []\n", encoding="utf-8"
            )
            selector = "contracts:DSET-CONTRACT-GOV-001"
            digest = hashlib.sha256(f"{selector}\n".encode()).hexdigest()
            (governance / "legacy-authority.yaml").write_text(
                'schema_version: "1.0"\n'
                "records:\n"
                "  -\n"
                "    semantic_id: DSET-CONTRACT-GOV-001\n"
                "    type: decision\n"
                "    subtype: contract\n"
                "    fragments:\n"
                "      -\n"
                "        path: dset/specs/packages/sample/package.yaml\n"
                f"        selector: {selector}\n"
                f"        sha256: {digest}\n",
                encoding="utf-8",
            )

            self.assertEqual(validate_legacy_authority_ledger(root), [])
            self.assertIn("DSET-CONTRACT-GOV-001", legacy_authority_ids(root))
            rows = {
                str(item["id"]): item
                for item in build_semantic_classification_index(root)
            }
            self.assertEqual(rows["DSET-CONTRACT-GOV-001"]["subtype"], "contract")
            self.assertTrue(rows["DSET-CONTRACT-GOV-001"]["compatibility"])

            historical.write_text("contracts: []\n", encoding="utf-8")
            messages = [item.message for item in validate_legacy_authority_ledger(root)]
            self.assertIn(
                "legacy Decision authority changed without native successors",
                messages,
            )

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

    def test_sealing_repeats_repository_backed_emission_gate(self) -> None:
        text = self._write_atom().replace('authority: "operator:test-operator"\n', "")
        self.atom_path.write_text(text, encoding="utf-8")

        with self.assertRaisesRegex(
            ValueError, "artifact emission is blocked: material field"
        ):
            seal_atom(self.root, self.atom_path)

    def test_new_atom_cannot_seal_legacy_child_of(self) -> None:
        text = self._write_atom().replace(
            "promotion:\n  parent_scope: null\n",
            "promotion:\n  parent_scope: null\nchild_of:\n  - DSET-REQUIREMENT-001\n",
        )
        self.atom_path.write_text(text, encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "sealed compatibility input only"):
            seal_atom(self.root, self.atom_path)

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

    def test_second_absorption_successor_is_rejected(self) -> None:
        self._write_atom()
        seal_atom(self.root, self.atom_path)
        for number in (2, 3):
            path = self.root / f"dset/changes/DSET-ATOMIC-RECORD-00{number}.md"
            path.write_text(
                self._atom_text(
                    carrier=f"DSET-ATOMIC-RECORD-00{number}",
                    semantic=f"DSET-CONTRACT-00{number}",
                ),
                encoding="utf-8",
            )
            seal_atom(self.root, path)
        append_lifecycle_event(
            self.root,
            self._event(
                "DSET-LIFECYCLE-EVENT-001",
                "DSET-CONTRACT-001",
                "DSET-CONTRACT-002",
            ),
        )

        with self.assertRaisesRegex(ValueError, "multiple absorption successors"):
            append_lifecycle_event(
                self.root,
                self._event(
                    "DSET-LIFECYCLE-EVENT-002",
                    "DSET-CONTRACT-001",
                    "DSET-CONTRACT-003",
                ),
            )

    def test_terminal_atom_cannot_be_reaccepted(self) -> None:
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

        with self.assertRaisesRegex(ValueError, "terminal atom"):
            append_lifecycle_event(
                self.root,
                {
                    "id": "DSET-LIFECYCLE-EVENT-002",
                    "atom_id": "DSET-CONTRACT-001",
                    "event": "accepted",
                    "occurred_at": "2026-07-20T00:01:00+04:00",
                    "related": [],
                    "llm_session_ids": ["codex:test-session"],
                },
            )

    def test_retired_atom_requires_registered_carrier_transition(self) -> None:
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

        with self.assertRaisesRegex(ValueError, "registered carrier transition"):
            archive_atom(self.root, "DSET-CONTRACT-001")

        self.assertEqual(self.atom_path.read_bytes(), original)
        self.assertEqual(validate_semantic_atoms(self.root), [])
        row = build_semantic_atom_index(self.root)[0]
        self.assertFalse(row["archived"])
        self.assertEqual(row["current_status"], "retired")
        self.assertEqual(row["path"], self.atom_path.relative_to(self.root).as_posix())

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
authority: "operator:test-operator"
claim: "The output contract governs this project."
scope:
  kind: project
  id: dset-temporary-adopter
promotion:
  parent_scope: null
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
