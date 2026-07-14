from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.traceability import (
    build_traceability,
    trace_is_fresh,
    write_traceability,
)

ROOT = Path(__file__).resolve().parents[1]


class TraceabilityTests(unittest.TestCase):
    def test_real_history_maps_archives_and_active_change(self) -> None:
        trace = build_traceability(ROOT)
        ids = [item["id"] for item in trace["changes"]]
        self.assertEqual(ids, sorted(ids))
        self.assertIn("bootstrap-dset-project-structure", ids)
        self.assertIn("make-supportability-first-class", ids)
        self.assertIn("operationalize-dset-v1", ids)
        toolchain = next(
            item for item in trace["changes"] if item["id"] == "operationalize-dset-v1"
        )
        self.assertTrue(toolchain["pull_request"].endswith("/pull/7"))
        artifacts = next(
            item
            for item in trace["changes"]
            if item["id"] == "add-artifact-governance-profile"
        )
        self.assertTrue(artifacts["pull_request"].endswith("/pull/8"))

    def test_write_is_stable_and_checkable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw)
            shutil.copytree(ROOT / "dset", target / "dset")
            write_traceability(target)
            first = (target / "dset" / "traceability.yaml").read_text(encoding="utf-8")
            write_traceability(target)
            second = (target / "dset" / "traceability.yaml").read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertTrue(trace_is_fresh(target))


if __name__ == "__main__":
    unittest.main()
