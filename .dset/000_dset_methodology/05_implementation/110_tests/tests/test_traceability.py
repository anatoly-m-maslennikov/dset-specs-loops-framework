"""Verify DSET traceability behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import shutil
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.layout import discover_layout
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.traceability import (
    build_traceability,
    trace_is_fresh,
    write_traceability,
)
from dset_toolchain.yaml_subset import load
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


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
        layout = discover_layout(ROOT)
        active_change = layout.find_change(str(current["id"]))
        active_manifest = cast(
            dict[str, Any],
            load(layout.structured_file(active_change, "change.toml")),
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
        relations = trace["relations"]
        legacy = [
            item for item in relations if item["source"] == "DSET-REQUIREMENT-GOV-034"
        ]
        self.assertEqual(legacy[0]["type"], "child_of")
        self.assertEqual(legacy[0]["target"], "DSET-REQUIREMENT-GOV-033")
        self.assertEqual(legacy[0]["origin"], "legacy_child_of")
        self.assertFalse(any("parent_to" in item for item in relations))
        implementation_relations = [
            item for item in relations if item["source_kind"] == "commit"
        ]
        self.assertTrue(implementation_relations)
        self.assertTrue(
            any(
                item["target"] == "DSET-REQUIREMENT-GOV-034"
                for item in implementation_relations
            )
        )
        decision_relations = [
            (item["type"], item.get("target"))
            for item in relations
            if item["source"] == "DSET-DECISION-GOV-013"
        ]
        self.assertIn(("resolution_of", "DSET-QUESTION-GOV-004"), decision_relations)
        self.assertIn(
            ("replacement_of", "DSET-REQUIREMENT-GOV-034"),
            decision_relations,
        )
        projection_ranges = [
            item["range"]
            for item in relations
            if item["source"] == "DSET-SPECIFICATION-001"
            and item["type"] == "projection_of"
        ]
        self.assertEqual(len(projection_ranges), 6)
        self.assertEqual(
            {item["through"] for item in projection_ranges},
            {
                "DSET-ATOMIC-RECORD-113",
                "DSET-ATOMIC-RECORD-114",
                "DSET-ATOMIC-RECORD-115",
                "DSET-ATOMIC-RECORD-078",
                "DSET-ATOMIC-RECORD-079",
                "DSET-ATOMIC-RECORD-080",
            },
        )
        self.assertEqual(
            {
                (item["scope"]["kind"], item["scope"]["id"])
                for item in projection_ranges
            },
            {
                ("project", "dset-specs-loops-framework"),
                ("layer", "gov"),
            },
        )
        atoms = {item["id"]: item for item in trace["semantic_atoms"]}
        self.assertEqual(atoms["DSET-DECISION-GOV-010"]["type"], "decision")
        self.assertEqual(atoms["DSET-DECISION-GOV-010"]["priority"], "high")
        self.assertEqual(atoms["DSET-DECISION-GOV-010"]["current_status"], "accepted")
        self.assertFalse(atoms["DSET-DECISION-GOV-010"]["archived"])
        typed = atoms["DSET-DECISION-GOV-013"]["relations"]
        self.assertTrue(any(item["type"] == "resolution_of" for item in typed))
        classifications = {
            item["id"]: item for item in trace["semantic_classifications"]
        }
        self.assertEqual(
            classifications["DSET-OPPORTUNITY-GOV-001"]["type"], "question"
        )
        self.assertEqual(
            classifications["DSET-OPPORTUNITY-GOV-001"]["subtype"],
            "opportunity",
        )
        self.assertTrue(
            classifications["DSET-OPPORTUNITY-GOV-001"]["historical_carrier"]
        )

    def test_write_is_stable_and_checkable(self) -> None:
        with temporary_directory() as raw:
            target = Path(raw).resolve()
            shutil.copytree(
                ROOT / ".dset",
                target / ".dset",
                ignore=shutil.ignore_patterns("runtime"),
            )
            write_traceability(target)
            trace_path = discover_layout(target).traceability_path
            first = trace_path.read_text(encoding="utf-8")
            write_traceability(target)
            second = trace_path.read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertTrue(trace_is_fresh(target))


if __name__ == "__main__":
    unittest.main()
