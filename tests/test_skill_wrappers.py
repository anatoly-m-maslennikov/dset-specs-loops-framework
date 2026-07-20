from __future__ import annotations

import re
import unittest
from pathlib import Path

from dset_toolchain.skill_catalog import (
    PRE_RESOLUTION_SKILLS,
    PUBLIC_SKILL_WORKFLOWS,
    SKILL_INVOCATION_MARKERS,
)
from dset_toolchain.yaml_subset import load

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class SkillWrapperTests(unittest.TestCase):
    def _skill_text(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_exact_public_catalog_is_thin_and_portable(self) -> None:
        actual = {
            path.parent.name for path in SKILLS.glob("*/SKILL.md") if path.is_file()
        }
        self.assertEqual(actual, set(PUBLIC_SKILL_WORKFLOWS))

        forbidden = ("/Users/", "/tmp/", "~/", "## Workflow", "PowerShell")
        for name, marker in SKILL_INVOCATION_MARKERS.items():
            with self.subTest(skill=name):
                text = self._skill_text(name)
                self.assertLessEqual(len(text.splitlines()), 24)
                self.assertIn(f"name: {name}\n", text)
                self.assertRegex(text, r"(?m)^description: \S")
                self.assertIn(marker, text)
                self.assertEqual(text.count("dset skills context"), 1)
                self.assertIn("installed shared runtime", text)
                self.assertFalse(any(fragment in text for fragment in forbidden))

                metadata = (SKILLS / name / "agents" / "openai.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertIn("display_name:", metadata)
                self.assertIn("short_description:", metadata)
                self.assertIn(f"Use ${name}", metadata)
                match = re.search(r'short_description: "([^"]+)"', metadata)
                self.assertIsNotNone(match)
                assert match is not None
                self.assertGreaterEqual(len(match.group(1)), 25)
                self.assertLessEqual(len(match.group(1)), 64)

    def test_governed_wrappers_fail_closed_after_shared_context(self) -> None:
        for name in PUBLIC_SKILL_WORKFLOWS:
            if name in PRE_RESOLUTION_SKILLS:
                continue
            with self.subTest(skill=name):
                text = self._skill_text(name)
                self.assertIn(
                    f"skills context --skill {name} --target TARGET",
                    text,
                )
                self.assertIn(
                    "resolved repository-local documents own substantive behavior",
                    text,
                )
                self.assertIn("never select an alternate runtime", text)
                self.assertIn("required unavailable conflict coverage", text)
                self.assertNotIn("Walk upward from the target", text)
                self.assertNotIn("rules resolve", text)

                context_at = text.index("dset skills context")
                read_at = text.index("returned project-owned")
                self.assertLess(context_at, read_at)

        registry = load(ROOT / "dset/scopes/gov/governance.yaml")
        workflows = {
            item["id"]: item["rules"] for item in registry["workflows"]
        }
        for name, workflow in PUBLIC_SKILL_WORKFLOWS.items():
            if name in PRE_RESOLUTION_SKILLS or name == "dset":
                continue
            with self.subTest(workflow=workflow):
                self.assertIn("DSET-RULE-LIFECYCLE", workflows[workflow])

    def test_pre_resolution_exceptions_are_bounded(self) -> None:
        initialize = self._skill_text("dset-init")
        self.assertIn("without `--execute`", initialize)
        self.assertIn("With authorization", initialize)
        self.assertIn("never overwrite or merge", initialize)
        self.assertIn("continue into another lifecycle mode", initialize)

        repair = self._skill_text("dset-repair-governance")
        self.assertIn("Require `status: invalid-governance`", repair)
        self.assertIn("Do not resolve substantive rules", repair)
        self.assertIn("Stop before any write", repair)

    def test_primary_and_direct_stop_boundaries_are_distinct(self) -> None:
        primary = self._skill_text("dset")
        self.assertIn("general, multi-stage, or uncertain", primary)
        self.assertNotIn("Route any DSET lifecycle request", primary)
        self.assertNotIn("finite entry-criteria closure", primary)

        boundaries = {
            "dset-decompose": "stop before specification or implementation",
            "dset-clarify": "stop before consequential selection or implementation",
            "dset-diagnose": "stop before implementing a fix",
            "dset-landscape": "stop before a Decision or implementation",
            "dset-prototype": "stop before adoption or promotion",
            "dset-decisions": "before implementation",
            "dset-plan-proof": "stop before implementation or execution",
            "dset-plan-implementation": "stop before implementation",
            "dset-implement": "before claiming verification",
            "dset-verify": "stop before repair or release",
            "dset-triage": "stop before solving the work",
            "dset-release": "Publication requires separate explicit authority",
            "dset-complete": "Stop without creating work",
        }
        for name, boundary in boundaries.items():
            with self.subTest(skill=name):
                self.assertIn(boundary, self._skill_text(name))

    def test_implementation_uses_governed_entry_criteria_closure(self) -> None:
        lifecycle = (
            ROOT
            / "dset/scopes/skill/governance/lifecycle-orchestration.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / "dset/scopes/skill/templates/governance/core-v1/"
            "lifecycle-orchestration.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(lifecycle, template)

        closure = lifecycle.split("The `implement` closure is ordered:", 1)[1]
        closure = closure.split("The `decisions` workflow", 1)[0]
        positions = [
            closure.index(f"`{workflow}`")
            for workflow in (
                "decisions",
                "plan-proof",
                "plan-implementation",
                "implement",
            )
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("every transition must remove a missing criterion", lifecycle)
        self.assertIn("unchanged or repeated state", lifecycle)
        self.assertNotIn("two workflow transitions", lifecycle)

        implement = self._skill_text("dset-implement")
        self.assertNotIn("invoke `dset-decisions` first", implement)
        self.assertNotIn("conditionally invoke proof", implement)


if __name__ == "__main__":
    unittest.main()
