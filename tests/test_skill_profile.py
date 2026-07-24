"""Verify the provider-neutral DSET Agent Skills profile.

Parameters: repository skills and isolated malformed package fixtures.
Effects: read-only checks plus temporary copied fixtures outside the repository.
Errors: profile violations must fail before distribution or publication.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.skill_catalog import PUBLIC_SKILL_WORKFLOWS
from dset_toolchain.skill_distribution import SkillDistributionError, plan_install
from dset_toolchain.skill_quality import audit_skill_catalog, audit_skill_package
from tests import repository_root

# ROOT locates the repository fixture from test module identity.
ROOT = repository_root(Path(__file__))
# SKILLS locates the public reusable skill catalog.
SKILLS = ROOT / "skills"
# CASES locates the provider-neutral trigger Evaluation definitions.
CASES = (
    ROOT
    / "15_layer_implementation"
    / "120_evaluations"
    / "030_dset-implementation-evaluations-skill-cases.toml"
)


class SkillProfileTests(unittest.TestCase):
    """Verify mandatory create/update and distribution profile gates."""

    def test_repository_catalog_and_case_matrix_pass(self) -> None:
        summary = audit_skill_catalog(
            SKILLS,
            expected_skills=set(PUBLIC_SKILL_WORKFLOWS),
            case_catalog=CASES,
        )
        self.assertEqual(summary.skill_count, len(PUBLIC_SKILL_WORKFLOWS))
        self.assertEqual(summary.case_count, len(PUBLIC_SKILL_WORKFLOWS) * 3)

    def test_description_requires_usage_boundary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dset-skill-profile-") as raw:
            skill = Path(raw) / "example-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: example-skill\n"
                "description: Perform example work.\n---\n\n# Example\n",
                encoding="utf-8",
            )
            issues = audit_skill_package(skill)
        self.assertTrue(any("when to use" in issue for issue in issues))

    def test_distribution_rejects_profile_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dset-skill-distribution-") as raw:
            root = Path(raw)
            copied = root / "skills"
            shutil.copytree(SKILLS, copied)
            target = copied / "dset" / "SKILL.md"
            text = target.read_text(encoding="utf-8")
            target.write_text(text.replace("Use when", "Apply if"), encoding="utf-8")
            with self.assertRaisesRegex(SkillDistributionError, "when to use"):
                plan_install(
                    copied,
                    "claude",
                    root / "installed-skills",
                    root / "installed-package",
                )


if __name__ == "__main__":
    unittest.main()
