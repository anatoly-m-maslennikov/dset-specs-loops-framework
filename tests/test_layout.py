from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path, PureWindowsPath

from dset_toolchain.layout import LAYERS, _canonical_relative, discover_layout
from dset_toolchain.yaml_subset import dump


class RepositoryLayoutTest(unittest.TestCase):
    def test_legacy_layout_preserves_central_paths(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            dset = root / "dset"
            dset.mkdir()
            (dset / "dset.yaml").write_text(
                dump({"schema_version": 1.1}), encoding="utf-8"
            )

            layout = discover_layout(root)

            self.assertFalse(layout.layered)
            self.assertEqual(layout.schema_version, "1.1")
            self.assertEqual(layout.settings_path, root / "dset_settings.toml")
            self.assertEqual(layout.manifest_path, dset / "dset.yaml")
            self.assertEqual(layout.governance_path, dset / "governance.yaml")
            self.assertEqual(layout.artifact_registry_path, dset / "artifacts.yaml")
            self.assertEqual(
                layout.artifact_type_registry_path, dset / "artifact-types.yaml"
            )
            self.assertEqual(layout.intake_path, dset / "intake.yaml")
            self.assertEqual(layout.version_path, dset / "version.yaml")
            self.assertEqual(layout.history_path, dset / "history/pull-requests.yaml")
            self.assertEqual(layout.traceability_path, dset / "traceability.yaml")
            self.assertEqual(layout.schema_roots, (dset / "schemas",))
            self.assertEqual(layout.template_roots, (dset / "templates",))
            self.assertEqual(layout.active_change_roots, (dset / "changes",))
            self.assertEqual(layout.archive_change_roots, (dset / "changes/archive",))

    def test_layered_layout_discovers_owned_and_distributed_paths(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            scopes = root / "dset" / "scopes"
            for layer in LAYERS:
                (scopes / layer).mkdir(parents=True)
            (scopes / "meta" / "dset.yaml").write_text(
                dump({"schema_version": "1.2"}), encoding="utf-8"
            )
            change = scopes / "tool" / "changes" / "portable-cli"
            change.mkdir(parents=True)
            (change / "change.yaml").write_text(
                dump({"id": "DSET-CHANGE-TOOL-001", "slug": "portable-cli"}),
                encoding="utf-8",
            )
            package = scopes / "skill" / "specs/packages/skills/package.yaml"
            package.parent.mkdir(parents=True)
            package.write_text(dump({"id": "skills"}), encoding="utf-8")
            template = scopes / "gov" / "templates" / "profiles.yaml"
            template.parent.mkdir()
            template.write_text(dump({"profiles": {}}), encoding="utf-8")

            layout = discover_layout(root)

            self.assertTrue(layout.layered)
            self.assertEqual(layout.schema_version, "1.2")
            self.assertEqual(layout.settings_path, root / "dset_settings.toml")
            self.assertEqual(layout.manifest_path, scopes / "meta" / "dset.yaml")
            self.assertEqual(layout.governance_path, scopes / "gov" / "governance.yaml")
            self.assertEqual(
                layout.artifact_registry_path, scopes / "gov" / "artifacts.yaml"
            )
            self.assertEqual(
                layout.artifact_type_registry_path,
                scopes / "gov" / "artifact-types.yaml",
            )
            self.assertEqual(layout.intake_path, scopes / "gov" / "intake.yaml")
            self.assertEqual(layout.provenance_path, scopes / "gov" / "provenance.yaml")
            self.assertEqual(layout.migrations_root, scopes / "gov" / "migrations")
            self.assertEqual(layout.version_path, scopes / "meta" / "version.yaml")
            self.assertEqual(layout.budget_path, scopes / "skill" / "budget.yaml")
            self.assertEqual(
                layout.traceability_path,
                scopes / "gov" / "generated" / "traceability.yaml",
            )
            self.assertEqual(
                layout.history_path, scopes / "ops" / "history/pull-requests.yaml"
            )
            self.assertEqual(
                layout.supportability_root, scopes / "ops" / "supportability"
            )
            self.assertEqual(layout.fixtures_root, scopes / "tool" / "fixtures")
            self.assertEqual(
                layout.schema_roots,
                tuple(scopes / layer / "schemas" for layer in LAYERS),
            )
            self.assertEqual(layout.find_template("profiles.yaml"), template)
            self.assertEqual(layout.find_change("DSET-CHANGE-TOOL-001"), change)
            self.assertEqual(layout.change_layer(change), "tool")
            self.assertEqual(layout.package_fragments(), (package,))

    def test_layout_conflicts_and_unsafe_paths_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            dset = root / "dset"
            (dset / "scopes" / "meta").mkdir(parents=True)
            (dset / "dset.yaml").write_text(
                dump({"schema_version": 1.1}), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "layout conflict"):
                discover_layout(root)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            scopes = root / "dset" / "scopes"
            for layer in LAYERS:
                (scopes / layer).mkdir(parents=True)
            (scopes / "meta" / "dset.yaml").write_text(
                dump({"schema_version": "1.2"}), encoding="utf-8"
            )
            (root / "dset" / "intake.yaml").write_text("items: []\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "authorities coexist"):
                discover_layout(root)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            dset = root / "dset"
            dset.mkdir()
            (dset / "dset.yaml").write_text(
                dump({"schema_version": 1.1}), encoding="utf-8"
            )
            layout = discover_layout(root)
            for unsafe in ("../outside", "/absolute", "C:/drive", "a//b", "a\\b"):
                with (
                    self.subTest(unsafe=unsafe),
                    self.assertRaisesRegex(ValueError, "canonical relative POSIX"),
                ):
                    layout.resolve_dset_path(unsafe)

    def test_archived_change_lookup_uses_manifest_identity(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            dset = root / "dset"
            archive = dset / "changes" / "archive"
            archive.mkdir(parents=True)
            (dset / "dset.yaml").write_text(
                dump({"schema_version": 1.1}), encoding="utf-8"
            )
            false_suffix = archive / "2026-01-01-not-foo"
            false_suffix.mkdir()
            (false_suffix / "change.yaml").write_text(
                dump({"id": "not-foo"}), encoding="utf-8"
            )
            expected = archive / "2026-01-02-foo"
            expected.mkdir()
            (expected / "change.yaml").write_text(dump({"id": "foo"}), encoding="utf-8")

            self.assertEqual(
                discover_layout(root).find_change("foo", archived=True), expected
            )

    def test_distributed_schema_names_are_unique(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            scopes = root / "dset" / "scopes"
            for layer in LAYERS:
                (scopes / layer).mkdir(parents=True)
            (scopes / "meta" / "dset.yaml").write_text(
                dump({"schema_version": "1.2"}), encoding="utf-8"
            )
            for layer in ("meta", "gov"):
                path = scopes / layer / "schemas" / "duplicate.schema.json"
                path.parent.mkdir()
                path.write_text(json.dumps({"type": "object"}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "schema is not unique"):
                tuple(discover_layout(root).schema_paths())

    def test_native_relative_path_serializes_to_posix(self) -> None:
        self.assertEqual(
            _canonical_relative(PureWindowsPath("governance/core-v1/profile.yaml")),
            Path("governance/core-v1/profile.yaml"),
        )
        with self.assertRaisesRegex(ValueError, "canonical relative POSIX"):
            _canonical_relative(r"governance\core-v1\profile.yaml")

    @unittest.skipIf(os.name == "nt", "directory symlink creation is not portable")
    def test_layout_returns_canonical_identity_for_directory_alias(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw).resolve()
            alias = target.parent / f"{target.name}-alias"
            alias.symlink_to(target, target_is_directory=True)
            try:
                dset = alias / "dset"
                dset.mkdir()
                (dset / "dset.yaml").write_text(
                    dump({"schema_version": 1.1}), encoding="utf-8"
                )
                self.assertEqual(discover_layout(alias).root, target)
            finally:
                alias.unlink()


if __name__ == "__main__":
    unittest.main()
