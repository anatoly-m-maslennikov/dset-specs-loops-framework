from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.validation import validate_change
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "dset" / "fixtures"


class FixtureTests(unittest.TestCase):
    def test_fixture_matrix(self) -> None:
        cases = load(FIXTURES / "cases.yaml")["cases"]
        for case in cases:
            with self.subTest(case=case["id"]), tempfile.TemporaryDirectory() as raw:
                change = self._materialize(case, Path(raw))
                archived = case.get("status") == "archived"
                expected_relative = None
                if archived:
                    expected_relative = f"dset/changes/archive/2026-07-14-{change.name}"
                diagnostics = validate_change(
                    ROOT,
                    change,
                    archived=archived,
                    expected_relative=expected_relative,
                )
                codes = [item.code for item in diagnostics]
                if case["expected"] == "pass":
                    self.assertEqual(codes, [])
                else:
                    self.assertTrue(codes)
                    self.assertEqual(codes[0], case["expected"])

    def _materialize(self, case: dict, target: Path) -> Path:
        source = FIXTURES / "bases" / case["base"]
        data = load(source / "change.yaml")
        change = target / data["id"]
        shutil.copytree(source, change)
        manifest = change / "change.yaml"
        data = load(manifest)
        if "status" in case:
            data["status"] = case["status"]
        if "pull_request_number" in case:
            number = case["pull_request_number"]
            data["pull_request"]["number"] = number
            data["pull_request"]["url"] = (
                f"https://github.com/example/project/pull/{number}"
            )
        if "archive_date" in case:
            date = case["archive_date"]
            data["archive"] = {
                "date": date,
                "path": f"dset/changes/archive/{date}-{data['id']}",
            }
        manifest.write_text(dump(data), encoding="utf-8")
        for relative in case.get("remove", []):
            path = change / relative
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        rename = case.get("rename")
        if rename:
            (change / rename["from"]).rename(change / rename["to"])
        return change


if __name__ == "__main__":
    unittest.main()
