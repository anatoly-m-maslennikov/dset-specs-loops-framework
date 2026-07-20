from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dset_toolchain.carrier_transitions import (
    decode_historical_envelope,
    load_ledger,
    validate_carrier_transition_ledger,
)
from dset_toolchain.frontmatter import parse as parse_frontmatter
from dset_toolchain.toml_codec import dumps as dump_toml
from dset_toolchain.toml_migration import (
    TomlMigrationError,
    apply_toml_migration,
    plan_toml_migration,
)


class CarrierTransitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self._write(
            "dset/scopes/gov/intake.yaml",
            'schema_version: "1.0"\nitems:\n  - id: DSET-ITEM-001\n'
            "    decision: null\n",
        )
        self.owner = self._write(
            "dset/scopes/gov/intake.toml",
            'schema_version = "1.0"\nitems = []\n',
        )
        self.atom = self._write(
            "dset/scopes/gov/DSET-ATOMIC-RECORD-999-carrier.md",
            "---\n"
            "artifact_type: atomic_record\n"
            "artifact_id: DSET-ATOMIC-RECORD-999\n"
            "type: decision\n"
            "semantic_id: DSET-DECISION-GOV-999\n"
            "status: accepted\n"
            "priority: critical\n"
            "authority: operator:test\n"
            "claim: Preserve this claim.\n"
            "llm_session_ids:\n  - codex:test-session\n"
            "scope:\n  kind: project\n  id: fixture\n"
            "promotion:\n  parent_scope: null\n"
            "---\n"
            "# Immutable body\n\nKeep this byte-for-byte.\n",
        )
        self._write(
            "dset/scopes/gov/migrations/carrier-transitions.toml",
            'schema_version = "1.0"\ntransitions = []\n',
        )
        registry = {
            "schema_version": "1.0",
            "legacy_structured": [
                {
                    "path": self.source.relative_to(self.root).as_posix(),
                    "sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(),
                    "current_owner": self.owner.relative_to(self.root).as_posix(),
                }
            ],
        }
        self._write("dset/scopes/gov/artifact-types.toml", dump_toml(registry))
        subprocess.run(
            ["git", "init", "-q"], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "add", "-A"], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=DSET Test",
                "-c",
                "user.email=dset@example.invalid",
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-q",
                "--no-gpg-sign",
                "-m",
                "fixture",
            ],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_apply_preserves_semantics_git_return_and_is_a_noop(self) -> None:
        original = parse_frontmatter(self.atom.read_text(encoding="utf-8"))
        self.assertIsNotNone(original)
        assert original is not None
        original_body = original[1]
        plan = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertTrue(plan.ready, plan.blockers)
        self.assertEqual(
            {entry.kind for entry in plan.entries},
            {"historical-envelope", "immutable-frontmatter", "transition-registry"},
        )

        apply_toml_migration(self.root, bypass_runtime_readiness=True)

        historical = self.source.with_name("intake.legacy.toml")
        self.assertFalse(self.source.exists())
        self.assertEqual(
            decode_historical_envelope(historical.read_text(encoding="utf-8")),
            {
                "schema_version": "1.0",
                "items": [{"id": "DSET-ITEM-001", "decision": None}],
            },
        )
        parsed = parse_frontmatter(self.atom.read_text(encoding="utf-8"))
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed[2], "toml")
        self.assertEqual(parsed[1], original_body)
        self.assertNotIn("parent_scope", parsed[0]["promotion"])

        ledger = load_ledger(self.root)
        records = ledger["transitions"]
        self.assertEqual(len(records), 2)
        self.assertEqual(validate_carrier_transition_ledger(self.root), [])
        self.assertTrue(all(item["declared_loss"] == [] for item in records))
        self.assertTrue(all(item["source_git_blob"] for item in records))
        self.assertEqual(
            next(item for item in records if item["kind"] == "markdown_frontmatter")[
                "carrier_ids"
            ],
            ["DSET-ATOMIC-RECORD-999"],
        )

        second = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertTrue(second.ready, second.blockers)
        self.assertEqual(second.entries, ())
        self.assertEqual(second.references, ())

    def test_tamper_and_late_failure_fail_closed_with_rollback(self) -> None:
        source_before = self.source.read_bytes()
        atom_before = self.atom.read_bytes()
        registry = self.root / "dset/scopes/gov/artifact-types.toml"
        registry_before = registry.read_bytes()
        ledger_path = self.root / (
            "dset/scopes/gov/migrations/carrier-transitions.toml"
        )
        ledger_before = ledger_path.read_bytes()

        with (
            patch(
                "dset_toolchain.toml_migration._validate_staged_tree",
                side_effect=ValueError("forced late failure"),
            ),
            self.assertRaisesRegex(TomlMigrationError, "rolled back"),
        ):
            apply_toml_migration(self.root, bypass_runtime_readiness=True)

        self.assertEqual(self.source.read_bytes(), source_before)
        self.assertEqual(self.atom.read_bytes(), atom_before)
        self.assertEqual(registry.read_bytes(), registry_before)
        self.assertEqual(ledger_path.read_bytes(), ledger_before)
        self.assertFalse(self.source.with_name("intake.legacy.toml").exists())

        apply_toml_migration(self.root, bypass_runtime_readiness=True)
        historical = self.source.with_name("intake.legacy.toml")
        historical.write_text(
            historical.read_text(encoding="utf-8") + "# tamper\n",
            encoding="utf-8",
        )
        self.assertTrue(validate_carrier_transition_ledger(self.root))


if __name__ == "__main__":
    unittest.main()
