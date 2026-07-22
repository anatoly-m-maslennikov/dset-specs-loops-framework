"""Verify DSET fixtures behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path
from typing import Any, TypedDict, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.layout import discover_layout
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.validation import validate_change
from dset_toolchain.yaml_subset import dump, load
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))
# LAYOUT defines layout; this module owns the default.
LAYOUT = discover_layout(ROOT)
# FIXTURES defines fixtures; this module owns the default.
FIXTURES = LAYOUT.fixtures_root


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
        matrix = cast(
            dict[str, Any], load(LAYOUT.structured_file(FIXTURES, "cases.toml"))
        )
        cases = cast(list[FixtureCase], matrix["cases"])
        for case in cases:
            with self.subTest(case=case["id"]), temporary_directory() as raw:
                project = (Path(raw) / "legacy-adopter").resolve()
                create_adopter(ROOT, project)
                change = self._materialize(case, project / "cases")
                archived = case.get("status") == "archived"
                expected_relative = None
                if archived:
                    expected_relative = f"dset/changes/archive/2026-07-14-{change.name}"
                diagnostics = validate_change(
                    project,
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
        with temporary_directory() as raw:
            project = (Path(raw) / "legacy-adopter").resolve()
            create_adopter(ROOT, project)
            target = project / "cases"
            target.mkdir()
            source = FIXTURES / "bases" / "small"
            change = target / "fixture-small"
            shutil.copytree(source, change)
            manifest = discover_layout(project).structured_file(change, "change.toml")
            data = cast(dict[str, Any], load(manifest))
            data["schema_version"] = 1.0
            for field in ("release", "intake", "decisions", "contracts"):
                data.pop(field, None)
            data["adrs"] = []
            manifest.write_text(dump(data, manifest), encoding="utf-8")
            self.assertEqual(validate_change(project, change, archived=False), [])

            data["schema_version"] = 1.1
            data["decisions"] = []
            data["contracts"] = []
            manifest.write_text(dump(data, manifest), encoding="utf-8")
            self.assertIn(
                "DSET-E106",
                {
                    item.code
                    for item in validate_change(project, change, archived=False)
                },
            )

    def _materialize(self, case: FixtureCase, target: Path) -> Path:
        source = FIXTURES / "bases" / case["base"]
        data = cast(dict[str, Any], load(LAYOUT.structured_file(source, "change.toml")))
        change = target / cast(str, data["id"])
        shutil.copytree(source, change)
        manifest = LAYOUT.structured_file(change, "change.toml")
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
        manifest.write_text(dump(data, manifest), encoding="utf-8")
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
