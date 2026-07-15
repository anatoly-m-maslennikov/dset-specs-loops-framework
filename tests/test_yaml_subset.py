from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.layout import discover_layout
from dset_toolchain.yaml_subset import dump, load, loads

ROOT = Path(__file__).resolve().parents[1]


class YamlSubsetTests(unittest.TestCase):
    def test_parses_repository_manifests(self) -> None:
        layout = discover_layout(ROOT)
        provenance = load(layout.provenance_path)
        cases = load(layout.fixtures_root / "cases.yaml")
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

    def test_host_prefixed_ids_round_trip_as_list_scalars(self) -> None:
        value = {
            "llm_session_ids": ["codex:session-001", "claude:session-002"],
            "external_refs": ["https://example.com/evidence"],
        }

        self.assertEqual(loads(dump(value)), value)


if __name__ == "__main__":
    unittest.main()
