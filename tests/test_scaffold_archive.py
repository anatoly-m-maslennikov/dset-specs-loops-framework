from __future__ import annotations

import shutil
import unittest
from datetime import date
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.archive import archive_plan, execute_archive
from dset_toolchain.layout import discover_layout
from dset_toolchain.scaffold import create_change
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = discover_layout(ROOT).fixtures_root


class ScaffoldArchiveTests(unittest.TestCase):
    def test_new_creates_profile_without_overwrite(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "adopter").resolve()
            self._copy_support(target)
            change = create_change(
                target, "add-login", "accounts", "small", "Add login"
            )
            self.assertTrue((change / "test-plan.md").is_file())
            self.assertTrue((change / "eval-plan.md").is_file())
            self.assertFalse((change / "design.md").exists())
            manifest_path = discover_layout(target).structured_file(
                change, "change.toml"
            )
            manifest = manifest_path.read_text(encoding="utf-8")
            self.assertNotIn("{{", manifest)
            self.assertIn("DSET-REQUIREMENT-001", manifest)
            self.assertIn("DSET-CONTRACT-001", manifest)
            self.assertEqual(load(manifest_path)["stories"], [])
            self.assertEqual(load(manifest_path)["outcomes"], [])
            with self.assertRaises(FileExistsError):
                create_change(target, "add-login", "accounts", "small")

    def test_new_uses_only_registered_optional_layers(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "adopter").resolve()
            self._copy_support(target)
            change = create_change(
                target, "govern-login", "accounts", "small", layer="GOV"
            )
            manifest = (
                discover_layout(target)
                .structured_file(change, "change.toml")
                .read_text(encoding="utf-8")
            )
            self.assertIn("DSET-REQUIREMENT-GOV-001", manifest)
            self.assertIn("DSET-CONTRACT-GOV-001", manifest)
            with self.assertRaisesRegex(ValueError, "unknown ID layer"):
                create_change(
                    target, "global-login", "accounts", "small", layer="GLOBAL"
                )
            with self.assertRaisesRegex(ValueError, "require schema 1.2"):
                create_change(
                    target,
                    "work-area-login",
                    "accounts",
                    "small",
                    work_areas=["api"],
                )

    def test_new_uses_a_generic_project_prefix(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "adopter").resolve()
            self._copy_support(target)
            manifest_path = discover_layout(target).manifest_path
            manifest = load(manifest_path)
            manifest["project"]["key"] = "ACME"
            manifest_path.write_text(dump(manifest, manifest_path), encoding="utf-8")
            change = create_change(
                target, "govern-login", "accounts", "small", layer="GOV"
            )
            rendered = (
                discover_layout(target)
                .structured_file(change, "change.toml")
                .read_text(encoding="utf-8")
            )
            self.assertIn("ACME-REQUIREMENT-GOV-001", rendered)
            self.assertIn("ACME-CONTRACT-GOV-001", rendered)
            specification = (change / "specs" / "accounts.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("ACME-STORY-GOV-001", specification)
            self.assertIn("ACME-OUTCOME-GOV-001", specification)

    def test_archive_is_dry_run_then_guarded_move(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "adopter").resolve()
            self._copy_support(target)
            source = target / "dset" / "changes" / "fixture-standard"
            shutil.copytree(FIXTURES / "bases" / "standard", source)
            manifest_path = discover_layout(target).structured_file(
                source, "change.yaml"
            )
            data = load(manifest_path)
            data["status"] = "archive-ready"
            data["pull_request"]["number"] = 42
            data["pull_request"]["url"] = "https://github.com/example/project/pull/42"
            manifest_path.write_text(dump(data, manifest_path), encoding="utf-8")
            with (source / "verification.md").open("a", encoding="utf-8") as file:
                file.write("\nAccepted-truth reconciliation: Pass\n")
            source_path, destination = archive_plan(
                target, "fixture-standard", date(2026, 7, 14)
            )
            self.assertEqual(source_path, source)
            self.assertFalse(destination.exists())
            result = execute_archive(target, "fixture-standard", date(2026, 7, 14))
            self.assertTrue(result.is_dir())
            self.assertFalse(source.exists())
            archived = load(
                discover_layout(target).structured_file(result, "change.yaml")
            )
            self.assertEqual(archived["status"], "archived")

    def _copy_support(self, target: Path) -> None:
        create_adopter(ROOT, target)


if __name__ == "__main__":
    unittest.main()
