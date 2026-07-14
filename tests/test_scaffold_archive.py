from __future__ import annotations

import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

from dset_toolchain.archive import archive_plan, execute_archive
from dset_toolchain.scaffold import create_change
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


class ScaffoldArchiveTests(unittest.TestCase):
    def test_new_creates_profile_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            self._copy_support(target)
            change = create_change(
                target, "add-login", "accounts", "small", "Add login"
            )
            self.assertTrue((change / "test-plan.md").is_file())
            self.assertTrue((change / "eval-plan.md").is_file())
            self.assertFalse((change / "design.md").exists())
            manifest = (change / "change.yaml").read_text(encoding="utf-8")
            self.assertNotIn("{{", manifest)
            self.assertIn("DSET-REQUIREMENT-001", manifest)
            self.assertIn("DSET-CONTRACT-001", manifest)
            self.assertIn("stories: []", manifest)
            self.assertIn("outcomes: []", manifest)
            with self.assertRaises(FileExistsError):
                create_change(target, "add-login", "accounts", "small")

    def test_new_uses_only_registered_optional_layers(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            self._copy_support(target)
            change = create_change(
                target, "govern-login", "accounts", "small", layer="GOV"
            )
            manifest = (change / "change.yaml").read_text(encoding="utf-8")
            self.assertIn("DSET-REQUIREMENT-GOV-001", manifest)
            self.assertIn("DSET-CONTRACT-GOV-001", manifest)
            with self.assertRaisesRegex(ValueError, "unknown ID layer"):
                create_change(
                    target, "global-login", "accounts", "small", layer="GLOBAL"
                )

    def test_new_uses_a_generic_project_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            self._copy_support(target)
            manifest_path = target / "dset" / "dset.yaml"
            manifest = load(manifest_path)
            manifest["project"]["key"] = "ACME"
            manifest_path.write_text(dump(manifest), encoding="utf-8")
            change = create_change(
                target, "govern-login", "accounts", "small", layer="GOV"
            )
            rendered = (change / "change.yaml").read_text(encoding="utf-8")
            self.assertIn("ACME-REQUIREMENT-GOV-001", rendered)
            self.assertIn("ACME-CONTRACT-GOV-001", rendered)
            specification = (change / "specs" / "accounts.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("ACME-STORY-GOV-001", specification)
            self.assertIn("ACME-OUTCOME-GOV-001", specification)

    def test_archive_is_dry_run_then_guarded_move(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            self._copy_support(target)
            source = target / "dset" / "changes" / "fixture-standard"
            shutil.copytree(ROOT / "dset" / "fixtures" / "bases" / "standard", source)
            data = load(source / "change.yaml")
            data["status"] = "archive-ready"
            data["pull_request"]["number"] = 42
            data["pull_request"]["url"] = "https://github.com/example/project/pull/42"
            (source / "change.yaml").write_text(dump(data), encoding="utf-8")
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
            archived = load(result / "change.yaml")
            self.assertEqual(archived["status"], "archived")

    def _copy_support(self, target: Path) -> None:
        (target / "dset" / "changes" / "archive").mkdir(parents=True)
        shutil.copytree(ROOT / "dset" / "templates", target / "dset" / "templates")
        shutil.copytree(ROOT / "dset" / "history", target / "dset" / "history")
        shutil.copyfile(ROOT / "dset" / "dset.yaml", target / "dset" / "dset.yaml")
        shutil.copyfile(ROOT / "dset" / "intake.yaml", target / "dset" / "intake.yaml")


if __name__ == "__main__":
    unittest.main()
