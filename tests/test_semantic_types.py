"""Verify DSET semantic types behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.layout import discover_layout
from dset_toolchain.semantic_types import (
    SEMANTIC_SUBTYPES,
    build_semantic_classification_index,
    classify_semantic_id,
    next_semantic_sequence,
    semantic_naming_axis,
    validate_semantic_classifications,
)
from dset_toolchain.temp_paths import temporary_directory
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class SemanticTypeClassificationTests(unittest.TestCase):
    """Verify canonical semantic types across native and historical carriers."""

    def test_exact_four_types_and_flat_direct_subtypes(self) -> None:
        self.assertEqual(
            set(SEMANTIC_SUBTYPES), {"decision", "question", "problem", "qa"}
        )
        self.assertEqual(
            classify_semantic_id("APP-REQUIREMENT-001"), ("decision", "requirement")
        )
        self.assertEqual(
            classify_semantic_id("APP-IMPL-002"),
            ("decision", "implementation_decision"),
        )
        self.assertEqual(
            classify_semantic_id("APP-OPPORTUNITY-002"), ("question", "opportunity")
        )
        self.assertEqual(
            classify_semantic_id("APP-EVAL-PLAN-003"),
            ("qa", "evaluation_plan"),
        )
        self.assertIsNone(classify_semantic_id("APP-TASK-004"))

    def test_naming_mode_selects_one_project_wide_sequence_axis(self) -> None:
        self.assertEqual(
            semantic_naming_axis("decision", "requirement", include_subtype=False),
            "DECISION",
        )
        self.assertEqual(
            semantic_naming_axis("decision", "requirement", include_subtype=True),
            "REQUIREMENT",
        )
        self.assertEqual(
            next_semantic_sequence(
                ROOT,
                "decision",
                "requirement",
                include_subtype=True,
            ),
            63,
        )

    def test_repository_uses_canonical_ids_across_carrier_generations(self) -> None:
        rows = {item["id"]: item for item in build_semantic_classification_index(ROOT)}

        opportunity = rows["DSET-OPPORTUNITY-GOV-001"]
        self.assertEqual(
            (opportunity["type"], opportunity["subtype"]), ("question", "opportunity")
        )
        self.assertFalse(opportunity["historical_carrier"])
        evaluation = rows["DSET-EVAL-PLAN-OPS-001"]
        self.assertEqual(
            (evaluation["type"], evaluation["subtype"]),
            ("qa", "evaluation_plan"),
        )
        self.assertTrue(evaluation["historical_carrier"])
        requirement = rows["DSET-REQUIREMENT-GOV-035"]
        self.assertEqual(
            (requirement["type"], requirement["subtype"]),
            ("decision", "requirement"),
        )
        self.assertFalse(requirement["historical_carrier"])
        self.assertEqual(validate_semantic_classifications(ROOT), [])

    def test_carrier_and_id_kind_mismatch_fails_closed(self) -> None:
        with temporary_directory() as raw:
            root = create_adopter(ROOT, Path(raw) / "adopter")
            carrier = (
                discover_layout(root).project_root
                / "question"
                / "DSET-PROBLEM-GOV-001-mismatched-kind.md"
            )
            carrier.parent.mkdir(parents=True, exist_ok=True)
            carrier.write_text(
                """+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-TEST"
type = "question"
subtype = "opportunity"
semantic_id = "DSET-PROBLEM-GOV-001"
status = "open"
+++

# Deliberately mismatched semantic identity
""",
                encoding="utf-8",
            )

            messages = [
                diagnostic.message
                for diagnostic in validate_semantic_classifications(root)
            ]

            self.assertIn(
                "semantic ID kind disagrees with carrier classification: "
                "DSET-PROBLEM-GOV-001",
                messages,
            )


if __name__ == "__main__":
    unittest.main()
