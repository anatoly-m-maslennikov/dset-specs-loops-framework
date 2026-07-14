from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.yaml_subset import dump, load, loads

ROOT = Path(__file__).resolve().parents[1]


class YamlSubsetTests(unittest.TestCase):
    def test_parses_repository_manifests(self) -> None:
        provenance = load(ROOT / "dset" / "provenance.yaml")
        cases = load(ROOT / "dset" / "fixtures" / "cases.yaml")
        self.assertEqual(provenance["project_license"], "Apache-2.0")
        self.assertEqual(cases["cases"][0]["id"], "valid-small-fix")

    def test_round_trip_nested_data(self) -> None:
        value = {
            "version": 1.0,
            "items": [
                {"id": "one", "enabled": True, "tags": ["a", "b"]},
                {"id": "two", "value": None},
            ],
        }
        self.assertEqual(loads(dump(value)), value)


if __name__ == "__main__":
    unittest.main()
