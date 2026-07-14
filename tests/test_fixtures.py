from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, TypedDict, cast

from dset_toolchain.validation import validate_change
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "dset" / "fixtures"


class FixtureCase(TypedDict, total=False):
    id: str
    base: str
    expected: str
    status: str
    pull_request_number: int
    archive_date: str
    remove: list[str]
    rename: dict[str, str]


class FixtureTests(unittest.TestCase):
    def test_fixture_matrix(self) -> None:
        matrix = cast(dict[str, Any], load(FIXTURES / "cases.yaml"))
        cases = cast(list[FixtureCase], matrix["cases"])
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

    def test_legacy_adrs_field_is_accepted_only_for_schema_1_0(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            source = FIXTURES / "bases" / "small"
            change = target / "fixture-small"
            shutil.copytree(source, change)
            manifest = change / "change.yaml"
            data = cast(dict[str, Any], load(manifest))
            data["schema_version"] = 1.0
            for field in ("release", "intake", "decisions", "contracts"):
                data.pop(field, None)
            data["adrs"] = []
            manifest.write_text(dump(data), encoding="utf-8")
            self.assertEqual(validate_change(ROOT, change, archived=False), [])

            data["schema_version"] = 1.1
            data["decisions"] = []
            data["contracts"] = []
            manifest.write_text(dump(data), encoding="utf-8")
            self.assertIn(
                "DSET-E106",
                {item.code for item in validate_change(ROOT, change, archived=False)},
            )

    def _materialize(self, case: FixtureCase, target: Path) -> Path:
        source = FIXTURES / "bases" / case["base"]
        data = cast(dict[str, Any], load(source / "change.yaml"))
        change = target / cast(str, data["id"])
        shutil.copytree(source, change)
        manifest = change / "change.yaml"
        data = cast(dict[str, Any], load(manifest))
        if "status" in case:
            data["status"] = case["status"]
        if "pull_request_number" in case:
            number = case["pull_request_number"]
            pull_request = cast(dict[str, Any], data["pull_request"])
            pull_request["number"] = number
            pull_request["url"] = f"https://github.com/example/project/pull/{number}"
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
