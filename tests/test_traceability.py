from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.layout import discover_layout
from dset_toolchain.traceability import (
    build_traceability,
    trace_is_fresh,
    write_traceability,
)
from dset_toolchain.yaml_subset import load

ROOT = Path(__file__).resolve().parents[1]


class TraceabilityTests(unittest.TestCase):
    def test_real_history_maps_archives_and_active_change(self) -> None:
        trace = build_traceability(ROOT)
        ids = [item["id"] for item in trace["changes"]]
        self.assertEqual(ids, sorted(ids))
        slugs = [item["slug"] for item in trace["changes"]]
        self.assertIn("bootstrap-dset-project-structure", slugs)
        self.assertIn("make-supportability-first-class", slugs)
        self.assertIn("operationalize-dset-v1", slugs)
        toolchain = next(
            item
            for item in trace["changes"]
            if item["slug"] == "operationalize-dset-v1"
        )
        self.assertTrue(toolchain["pull_request"].endswith("/pull/7"))
        artifacts = next(
            item
            for item in trace["changes"]
            if item["slug"] == "add-artifact-governance-profile"
        )
        self.assertTrue(artifacts["pull_request"].endswith("/pull/8"))
        current = next(
            item
            for item in trace["changes"]
            if item["slug"] == "make-dset-self-hosting-and-skills-thin"
        )
        active_manifest = cast(
            dict[str, Any],
            load(discover_layout(ROOT).find_change(str(current["id"])) / "change.yaml"),
        )
        self.assertEqual(current["intake"], sorted(active_manifest["intake"]))
        self.assertEqual(current["decisions"], sorted(active_manifest["decisions"]))
        self.assertEqual(current["contracts"], sorted(active_manifest["contracts"]))
        self.assertEqual(current["stories"], sorted(active_manifest.get("stories", [])))
        self.assertEqual(
            current["outcomes"], sorted(active_manifest.get("outcomes", []))
        )
        self.assertTrue(
            all(item["contracts"] == [] for item in trace["changes"] if item != current)
        )
        self.assertTrue(
            all(item["stories"] == [] for item in trace["changes"] if item != current)
        )
        self.assertTrue(
            all(item["outcomes"] == [] for item in trace["changes"] if item != current)
        )

    def test_write_is_stable_and_checkable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            shutil.copytree(ROOT / "dset", target / "dset")
            write_traceability(target)
            trace_path = discover_layout(target).traceability_path
            first = trace_path.read_text(encoding="utf-8")
            write_traceability(target)
            second = trace_path.read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertTrue(trace_is_fresh(target))


if __name__ == "__main__":
    unittest.main()
