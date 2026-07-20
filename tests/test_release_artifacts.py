from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.frontmatter import metadata as frontmatter_metadata

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "dset/scopes/ops/templates/release"
PLANNING = ROOT / "dset/scopes/ops/planning"
CHANGE = ROOT / "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin"


class ReleaseArtifactTests(unittest.TestCase):
    def test_release_templates_share_delivery_classification(self) -> None:
        expected = {
            "version-scope.md": ("delivery", "version_scope"),
            "roadmap.md": ("delivery", "roadmap"),
            "release-plan.md": ("delivery", "release_plan"),
            "readiness-record.md": ("delivery", "readiness_record"),
            "release-record.md": ("delivery", "release_record"),
        }
        self.assertEqual(
            {path.name for path in TEMPLATES.glob("*.md") if path.name != "README.md"},
            set(expected),
        )
        for name, classification in expected.items():
            with self.subTest(name=name):
                metadata = self._frontmatter(TEMPLATES / name)
                self.assertEqual(
                    (metadata["artifact_type"], metadata.get("artifact_subtype")),
                    classification,
                )

    def test_dset_self_applies_type_first_release_names(self) -> None:
        expected = {
            "DSET-DELIVERY-001-0-3-foundation.md": (
                "DSET-DELIVERY-001",
                "version_scope",
            ),
            "DSET-DELIVERY-002-0-4-self-hosted-core.md": (
                "DSET-DELIVERY-002",
                "version_scope",
            ),
            "DSET-DELIVERY-003-0-5-adopter-ready.md": (
                "DSET-DELIVERY-003",
                "version_scope",
            ),
            "DSET-DELIVERY-004-1-0-stable.md": (
                "DSET-DELIVERY-004",
                "version_scope",
            ),
            "DSET-DELIVERY-005-0-4-core-vertical-cut.md": (
                "DSET-DELIVERY-005",
                "roadmap",
            ),
        }
        actual = {
            path.name for path in PLANNING.glob("*.md") if path.name != "README.md"
        }
        self.assertEqual(actual, set(expected))
        for name, (artifact_id, subtype) in expected.items():
            with self.subTest(name=name):
                metadata = self._frontmatter(PLANNING / name)
                self.assertEqual(metadata["artifact_id"], artifact_id)
                self.assertEqual(metadata["artifact_subtype"], subtype)

    def test_dset_delivery_sequence_covers_current_release_carriers(self) -> None:
        expected = {
            CHANGE / "DSET-DELIVERY-006-0-3-1-release.md": (
                "DSET-DELIVERY-006",
                "release_plan",
            ),
            CHANGE / "DSET-DELIVERY-007-0-3-1-readiness.md": (
                "DSET-DELIVERY-007",
                "readiness_record",
            ),
        }
        for path, (artifact_id, subtype) in expected.items():
            with self.subTest(path=path.name):
                metadata = self._frontmatter(path)
                self.assertEqual(metadata["artifact_type"], "delivery")
                self.assertEqual(metadata["artifact_id"], artifact_id)
                self.assertEqual(metadata["artifact_subtype"], subtype)

        all_delivery_ids = [
            self._frontmatter(path)["artifact_id"]
            for path in sorted(PLANNING.glob("DSET-DELIVERY-*.md"))
        ] + [artifact_id for artifact_id, _ in expected.values()]
        self.assertEqual(
            all_delivery_ids,
            [f"DSET-DELIVERY-{sequence:03d}" for sequence in range(1, 8)],
        )

    def test_release_reference_chain_and_gate_boundaries_are_explicit(self) -> None:
        release_plan = (TEMPLATES / "release-plan.md").read_text(encoding="utf-8")
        readiness = (TEMPLATES / "readiness-record.md").read_text(encoding="utf-8")
        release_record = (TEMPLATES / "release-record.md").read_text(encoding="utf-8")
        self.assertIn("version_scope_ref", release_plan)
        self.assertIn("release_plan_ref", readiness)
        self.assertIn("candidate_sha", readiness)
        self.assertIn("Use exactly `ready` or `blocked`", readiness)
        for field in (
            "version_scope_ref",
            "release_plan_ref",
            "readiness_record_ref",
            "Protected merge SHA",
            "Publisher/forge release",
        ):
            self.assertIn(field, release_record)

    def test_milestone_is_only_a_roadmap_entry(self) -> None:
        roadmap = (TEMPLATES / "roadmap.md").read_text(encoding="utf-8")
        self.assertIn("Milestones are entries in this Roadmap", roadmap)
        self.assertEqual(list(TEMPLATES.glob("*milestone*.md")), [])
        self.assertEqual(list(PLANNING.glob("*MILESTONE*.md")), [])

    def test_live_release_rule_matches_distributed_template(self) -> None:
        live = ROOT / "dset/scopes/ops/governance/release.md"
        template = ROOT / "dset/scopes/ops/templates/governance/core-v1/release.md"
        self.assertEqual(
            live.read_text(encoding="utf-8"),
            template.read_text(encoding="utf-8"),
        )

    @staticmethod
    def _frontmatter(path: Path) -> dict[str, Any]:
        metadata = frontmatter_metadata(path)
        if metadata is None:
            raise AssertionError(f"missing frontmatter: {path}")
        return metadata


if __name__ == "__main__":
    unittest.main()
