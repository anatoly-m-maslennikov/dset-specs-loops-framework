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
    validate_semantic_classifications,
)
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.yaml_subset import dump, load
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class SemanticTypeCompatibilityTests(unittest.TestCase):
    def test_exact_five_types_and_flat_direct_subtypes(self) -> None:
        self.assertEqual(
            set(SEMANTIC_SUBTYPES),
            {"requirement", "decision", "question", "problem", "qa"},
        )
        self.assertEqual(
            classify_semantic_id("APP-REQUIREMENT-001"), ("requirement", None)
        )
        self.assertEqual(
            classify_semantic_id("APP-CONTRACT-002"),
            ("requirement", "contract"),
        )
        self.assertEqual(
            classify_semantic_id("APP-OPPORTUNITY-002"), ("question", "opportunity")
        )
        self.assertEqual(classify_semantic_id("APP-EVAL-003"), ("qa", "evaluation"))
        self.assertIsNone(classify_semantic_id("APP-TASK-004"))

    def test_repository_legacy_ids_are_classified_without_retyping(self) -> None:
        rows = {item["id"]: item for item in build_semantic_classification_index(ROOT)}

        opportunity = rows["DSET-OPPORTUNITY-GOV-001"]
        self.assertEqual(
            (opportunity["type"], opportunity["subtype"]), ("question", "opportunity")
        )
        self.assertFalse(opportunity["compatibility"])
        evaluation = rows["DSET-EVAL-OPS-001"]
        self.assertEqual(
            (evaluation["type"], evaluation["subtype"]), ("qa", "evaluation")
        )
        self.assertTrue(evaluation["compatibility"])
        compatibility = rows["DSET-REQUIREMENT-GOV-035"]
        self.assertEqual(
            (compatibility["type"], compatibility["subtype"]),
            ("requirement", "none"),
        )
        self.assertTrue(compatibility["compatibility"])
        self.assertEqual(validate_semantic_classifications(ROOT), [])

    def test_carrier_and_id_kind_mismatch_fails_closed(self) -> None:
        with temporary_directory() as raw:
            root = create_adopter(ROOT, Path(raw) / "adopter")
            intake_path = discover_layout(root).intake_path
            intake = load(intake_path)
            assert isinstance(intake, dict)
            items = intake["items"]
            assert isinstance(items, list)
            items.append(
                {
                    "id": "DSET-PROBLEM-GOV-001",
                    "type": "opportunity",
                    "status": "open",
                }
            )
            intake_path.write_text(dump(intake, intake_path), encoding="utf-8")

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
