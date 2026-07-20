from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.yaml_subset import loads

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "dset/scopes/ops/templates/release"
PLANNING = ROOT / "dset/scopes/ops/planning"


class ReleaseArtifactTests(unittest.TestCase):
    def test_five_flat_release_templates_have_exact_classification(self) -> None:
        expected = {
            "version-scope.md": ("specification", "version_scope"),
            "roadmap.md": ("plan", "roadmap"),
            "release-plan.md": ("plan", "release_plan"),
            "readiness-record.md": ("readiness_record", None),
            "release-record.md": ("release_record", None),
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
            "DSET-SPECIFICATION-001-0-3-foundation.md": (
                "DSET-SPECIFICATION-001",
                "version_scope",
            ),
            "DSET-SPECIFICATION-002-0-4-self-hosted-core.md": (
                "DSET-SPECIFICATION-002",
                "version_scope",
            ),
            "DSET-SPECIFICATION-003-0-5-adopter-ready.md": (
                "DSET-SPECIFICATION-003",
                "version_scope",
            ),
            "DSET-SPECIFICATION-004-1-0-stable.md": (
                "DSET-SPECIFICATION-004",
                "version_scope",
            ),
            "DSET-PLAN-001-0-4-core-vertical-cut.md": (
                "DSET-PLAN-001",
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
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            raise AssertionError(f"missing frontmatter: {path}")
        end = lines.index("---", 1)
        metadata = loads("\n".join(lines[1:end]))
        if not isinstance(metadata, dict):
            raise AssertionError(f"invalid frontmatter: {path}")
        return metadata


if __name__ == "__main__":
    unittest.main()
