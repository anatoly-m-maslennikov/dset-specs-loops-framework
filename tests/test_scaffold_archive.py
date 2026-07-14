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
            self.assertNotIn("{{", (change / "change.yaml").read_text(encoding="utf-8"))
            with self.assertRaises(FileExistsError):
                create_change(target, "add-login", "accounts", "small")

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


if __name__ == "__main__":
    unittest.main()
