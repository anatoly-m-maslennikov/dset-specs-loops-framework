from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.layout import discover_layout
from dset_toolchain.yaml_subset import load

ROOT = Path(__file__).resolve().parents[1]
GOV_PACKAGE = ROOT / ".dset" / "gov"
DECISIONS = GOV_PACKAGE / "decision"


class ConflictEntityTests(unittest.TestCase):
    def test_accepted_truth_defines_four_types_and_flat_subtypes(self) -> None:
        domain = (GOV_PACKAGE / "specification-domain.md").read_text(encoding="utf-8")
        spec = (GOV_PACKAGE / "specification-methodology.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("**Decision**", domain)
        self.assertIn("**Problem**", domain)
        self.assertIn("**Question**", domain)
        self.assertIn("**QA**", domain)
        self.assertIn("**Conflict**", domain)
        self.assertIn("direct Question subtype", domain)
        self.assertIn("direct Decision subtype", domain)
        self.assertIn("DSET-INVARIANT-GOV-017", domain)
        self.assertIn("DSET-REQUIREMENT-GOV-027", spec)
        self.assertIn("Four Types use one flat subtype level", spec)
        self.assertIn("never contains another subtype", spec)
        self.assertIn("reviewable primary claim", spec)
        self.assertIn("operator's acceptance is an act", spec)
        self.assertIn("deterministic code executes the method", spec)

    def test_type_is_never_defined_by_workflow_or_location(self) -> None:
        artifacts = (ROOT / "documentation" / "artifact-types.md").read_text(
            encoding="utf-8"
        )
        authoring = (ROOT / "documentation" / "authoring-rules.md").read_text(
            encoding="utf-8"
        )
        rules = (ROOT / ".dset" / "gov" / "specification-work-items.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("never workflow", artifacts)
        self.assertIn("not from a workflow", authoring)
        self.assertIn("Type is determined by meaning", rules)
        normalized_rules = " ".join(rules.split())
        self.assertIn("must not be silently retyped or renamed", normalized_rules)

    def test_conflict_proof_ids_are_registered(self) -> None:
        package = load(
            discover_layout(ROOT).structured_file(GOV_PACKAGE, "package.toml")
        )
        assert isinstance(package, dict)
        self.assertIn("DSET-REQUIREMENT-GOV-027", package["requirements"])
        self.assertIn("DSET-TEST-GOV-027", package["tests"])
        self.assertIn("DSET-EVAL-GOV-017", package["evals"])

    def test_absorbing_decision_preserves_immutable_predecessor(self) -> None:
        predecessor = DECISIONS / (
            "DSET-DECISION-GOV-004-problems-questions-and-conflicts-are-distinct.md"
        )
        successor = DECISIONS / (
            "DSET-DECISION-GOV-005-semantic-artifact-types-and-open-conflicts.md"
        )
        self.assertTrue(predecessor.is_file())
        text = successor.read_text(encoding="utf-8")
        self.assertIn("**Absorbs:** `DSET-DECISION-GOV-004` in full", text)
        self.assertIn("workflow never defines artifact type", text)

        fpf_predecessor = DECISIONS / (
            "DSET-DECISION-GOV-007-flat-canonical-type-and-subtype-model.md"
        )
        fpf_successor = DECISIONS / (
            "DSET-DECISION-GOV-008-fpf-aligned-boundaries-for-the-flat-type-model.md"
        )
        self.assertTrue(fpf_predecessor.is_file())
        fpf_text = fpf_successor.read_text(encoding="utf-8")
        self.assertIn("**Absorbs:** `DSET-DECISION-GOV-007` in full", fpf_text)
        self.assertIn("One atom, one primary governed claim", fpf_text)

    def test_live_and_template_work_item_rules_match(self) -> None:
        live = ROOT / ".dset" / "gov" / "specification-work-items.md"
        template = (
            ROOT
            / ".dset"
            / "gov"
            / "templates"
            / "governance"
            / "core-v1"
            / "work-items.md"
        )
        self.assertEqual(live.read_bytes(), template.read_bytes())
        text = live.read_text(encoding="utf-8")
        for phrase in (
            "independently reviewable primary claim",
            "acceptance is a lifecycle act",
            "Markdown, YAML, database, and hosted records are carriers",
            "Debt must not conceal a Defect or Gap",
            "deterministic code executes the method",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
