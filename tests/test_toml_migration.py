from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import cast
from unittest.mock import patch

from dset_toolchain.cli import main
from dset_toolchain.toml_codec import loads as load_toml
from dset_toolchain.toml_migration import (
    MigrationPlan,
    apply_toml_migration,
    plan_toml_migration,
)

ROOT = Path(__file__).resolve().parents[1]


class TomlMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = Path(self.temporary.name) / "fixture"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def standard_fixture(self) -> None:
        self.write(
            "dset/scopes/gov/items.yaml",
            "schema_version: 1.0\nitems:\n  -\n    id: DSET-ITEM-001\n",
        )
        self.write(
            "dset/scopes/gov/index.yaml",
            "schema_version: 1.0\ntarget: items.yaml\n",
        )
        self.write(
            "dset/scopes/gov/record.md",
            "---\nartifact_id: DSET-RECORD-001\nrelations:\n"
            "  - items.yaml\n---\n[items](items.yaml)\n",
        )

    def test_dry_run_is_no_write_and_has_complete_digest_and_reference_map(
        self,
    ) -> None:
        self.standard_fixture()
        index = self.root / "dset/scopes/gov/index.yaml"
        before = index.read_text(encoding="utf-8")

        plan = plan_toml_migration(self.root)
        report = plan.report()

        self.assertTrue(plan.ready)
        self.assertEqual(len(plan.entries), 3)
        changes = {
            item["source"]: item
            for item in cast(list[dict[str, str]], report["changes"])
        }
        self.assertEqual(
            changes["dset/scopes/gov/index.yaml"]["before_sha256"],
            hashlib.sha256(before.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(
            changes["dset/scopes/gov/index.yaml"]["target"],
            "dset/scopes/gov/index.toml",
        )
        references = cast(list[dict[str, object]], report["reference_rewrites"])
        self.assertGreaterEqual(len(references), 2)
        counts = cast(dict[str, object], report["counts"])
        self.assertEqual(counts["changes"], 3)
        self.assertEqual(
            counts["changes_by_kind"],
            {"markdown-frontmatter": 1, "structured": 2},
        )
        self.assertTrue(index.exists())
        self.assertFalse(index.with_suffix(".toml").exists())
        self.assertIn("---", (self.root / "dset/scopes/gov/record.md").read_text())

    def test_apply_is_idempotent_and_rewrites_references(self) -> None:
        self.standard_fixture()

        applied = apply_toml_migration(self.root)

        self.assertTrue(applied.ready)
        items = self.root / "dset/scopes/gov/items.toml"
        index = self.root / "dset/scopes/gov/index.toml"
        record = self.root / "dset/scopes/gov/record.md"
        self.assertTrue(items.is_file())
        self.assertFalse(items.with_suffix(".yaml").exists())
        parsed_index = load_toml(index.read_text(encoding="utf-8"))
        self.assertEqual(parsed_index["target"], "items.toml")
        rendered_record = record.read_text(encoding="utf-8")
        self.assertTrue(rendered_record.startswith("+++\n"))
        self.assertIn("items.toml", rendered_record)
        second = apply_toml_migration(self.root)
        self.assertEqual(second.entries, ())

    def test_explicit_exceptions_retain_the_json_schema_contract_boundary(
        self,
    ) -> None:
        self.write(".github/workflows/test.yaml", "name: test\n")
        self.write("skills/dset/agents/openai.yaml", "interface: host\n")
        self.write("skills/dset/SKILL.md", "---\nname: dset\n---\n# DSET\n")
        self.write(
            "dset/scopes/gov/schemas/example.schema.json",
            json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema"}),
        )
        plan = plan_toml_migration(self.root)
        report = plan.report()
        categories = {
            item["category"]
            for item in cast(list[dict[str, str]], report["exceptions"])
        }
        self.assertTrue(
            {
                "github-actions",
                "host-skill-metadata",
                "host-skill-frontmatter",
                "external-json-schema",
            }.issubset(categories)
        )
        self.assertTrue(plan.ready)
        schema = next(
            item
            for item in cast(list[dict[str, object]], report["exceptions"])
            if item["category"] == "external-json-schema"
        )
        self.assertEqual(schema["authority"], "canonical-external-contract")
        self.assertFalse(schema["editable_toml_duplicate"])

    def test_references_cover_root_relative_bare_and_retained_carriers(self) -> None:
        self.standard_fixture()
        self.write(
            ".github/workflows/dset.yaml",
            "source: dset/scopes/gov/items.yaml\nbare: items.yaml\n",
        )
        self.write(
            "skills/dset/agents/openai.yaml",
            "input: ../../../dset/scopes/gov/items.yaml\n",
        )

        plan = plan_toml_migration(self.root)
        references = {
            (reference.path.relative_to(self.root).as_posix(), reference.source): (
                reference.target
            )
            for reference in plan.references
        }

        self.assertEqual(
            references[(".github/workflows/dset.yaml", "dset/scopes/gov/items.yaml")],
            "dset/scopes/gov/items.toml",
        )
        self.assertEqual(
            references[(".github/workflows/dset.yaml", "items.yaml")],
            "items.toml",
        )
        self.assertEqual(
            references[
                (
                    "skills/dset/agents/openai.yaml",
                    "../../../dset/scopes/gov/items.yaml",
                )
            ],
            "../../../dset/scopes/gov/items.toml",
        )

    def test_shared_bare_filename_is_safe_when_targets_share_a_suffix(self) -> None:
        self.write("dset/scopes/gov/one/shared.yaml", "id: one\n")
        self.write("dset/scopes/gov/two/shared.yaml", "id: two\n")
        self.write("dset/scopes/gov/readme.md", "---\nid: readme\n---\nshared.yaml\n")

        plan = plan_toml_migration(self.root)

        self.assertTrue(plan.ready)
        shared = [
            reference
            for reference in plan.references
            if reference.source == "shared.yaml"
        ]
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0].target, "shared.toml")

    def test_collision_and_unsupported_values_fail_closed(self) -> None:
        self.write("dset/scopes/gov/record.yaml", "id: one\n")
        self.write("dset/scopes/gov/record.json", '{"id": "two"}\n')
        collision = plan_toml_migration(self.root)
        self.assertFalse(collision.ready)
        self.assertIn(
            "target collision dset/scopes/gov/record.toml", collision.blockers[0]
        )

        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            unsupported_root = Path(raw)
            path = unsupported_root / "dset/scopes/gov/value.yaml"
            path.parent.mkdir(parents=True)
            path.write_text("value: null\n", encoding="utf-8")
            unsupported = plan_toml_migration(unsupported_root)
        self.assertFalse(unsupported.ready)
        self.assertIn("null is not representable", unsupported.blockers[0])

    def test_symlinks_are_retained_and_external_targets_stop_the_plan(self) -> None:
        external = self.root.parent / "external.yaml"
        external.write_text("id: external\n", encoding="utf-8")
        internal = self.write("dset/scopes/gov/internal.yaml", "id: internal\n")
        retained = self.root / "dset/scopes/gov/retained.yaml"
        retained.symlink_to(internal)
        unsafe = self.root / "dset/scopes/gov/unsafe.yaml"
        unsafe.symlink_to(external)

        plan = plan_toml_migration(self.root)
        exceptions = cast(list[dict[str, object]], plan.report()["exceptions"])
        symlinks = [
            item for item in exceptions if item["category"] == "retained-symlink"
        ]

        self.assertEqual(len(symlinks), 2)
        self.assertFalse(plan.ready)
        self.assertTrue(any(item.startswith("path-safety:") for item in plan.blockers))
        self.assertNotIn(retained, [entry.source for entry in plan.entries])
        self.assertNotIn(unsafe, [entry.source for entry in plan.entries])

    def test_null_normalization_is_narrow_and_reported(self) -> None:
        self.write(
            "dset/scopes/gov/intake.yaml",
            "items:\n  -\n    id: ITEM-1\n    decision: null\n",
        )
        self.write(
            "dset/scopes/ops/history/pull-requests.yaml",
            "pull_requests:\n  -\n    number: 1\n    merge_commit: null\n",
        )
        self.write(
            "dset/scopes/gov/record.yaml",
            "promotion:\n  parent_scope: null\n",
        )

        plan = plan_toml_migration(self.root)
        normalizations = cast(list[dict[str, str]], plan.report()["normalizations"])

        self.assertTrue(plan.ready)
        self.assertEqual(
            {(item["source"], item["key_path"]) for item in normalizations},
            {
                ("dset/scopes/gov/intake.yaml", "items.0.decision"),
                ("dset/scopes/gov/record.yaml", "promotion.parent_scope"),
                (
                    "dset/scopes/ops/history/pull-requests.yaml",
                    "pull_requests.0.merge_commit",
                ),
            },
        )

        self.write("dset/scopes/gov/unsupported.yaml", "other: null\n")
        blocked = plan_toml_migration(self.root)
        self.assertFalse(blocked.ready)
        self.assertTrue(
            any(item.startswith("conversion:") for item in blocked.blockers)
        )

    def test_runtime_readiness_and_generated_bundle_are_explicit_gates(self) -> None:
        self.standard_fixture()
        (self.root / "dset_toolchain").mkdir()

        missing = plan_toml_migration(self.root)
        self.assertEqual(missing.runtime_readiness["status"], "missing")
        self.assertTrue(
            any(item.startswith("runtime-readiness:") for item in missing.blockers)
        )

        targets = {
            entry.target.relative_to(self.root).as_posix(): entry.target_digest
            for entry in missing.entries
            if entry.source != entry.target
        }
        self.write(
            ".dset/toml-migration-runtime-readiness.json",
            json.dumps({"targets": targets}),
        )
        self.write("dset_toolchain/bootstrap_bundle.json", "{}\n")
        gated = plan_toml_migration(self.root)
        self.assertEqual(gated.runtime_readiness["status"], "current")
        self.assertTrue(
            any(item.startswith("regeneration-boundary:") for item in gated.blockers)
        )

    def test_cli_apply_on_blocked_plan_prints_the_plan_without_applying(self) -> None:
        blocked = MigrationPlan(
            root=ROOT,
            entries=(),
            exceptions=(),
            references=(),
            blockers=("conversion: test blocker",),
            runtime_readiness={"status": "missing"},
        )
        output = StringIO()
        with (
            patch("dset_toolchain.cli.plan_toml_migration", return_value=blocked),
            patch("dset_toolchain.cli.apply_toml_migration") as apply,
            redirect_stdout(output),
        ):
            status = main(["migrate", "toml", str(ROOT), "--apply"])

        self.assertEqual(status, 1)
        self.assertIn("DRY RUN TOML migration blocked", output.getvalue())
        self.assertIn("BLOCKED conversion: test blocker", output.getvalue())
        apply.assert_not_called()


if __name__ == "__main__":
    unittest.main()
