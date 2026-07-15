from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
WORKFLOWS = {
    "dset": "lifecycle-orchestration",
    "dset-clarify": "domain-clarification",
    "dset-diagnose": "diagnosis",
    "dset-prototype": "prototyping",
    "dset-release": "release",
}


class SkillWrapperTests(unittest.TestCase):
    def _skill_text(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_exactly_five_thin_portable_public_wrappers(self) -> None:
        actual = {
            path.parent.name for path in SKILLS.glob("*/SKILL.md") if path.is_file()
        }
        self.assertEqual(actual, set(WORKFLOWS))

        forbidden = ("/Users/", "/tmp/", "~/", "## Workflow", "PowerShell")
        for name, workflow in WORKFLOWS.items():
            with self.subTest(skill=name):
                text = self._skill_text(name)
                self.assertLessEqual(len(text.splitlines()), 24)
                self.assertIn(f"name: {name}\n", text)
                self.assertRegex(text, r"(?m)^description: \S")
                self.assertIn(
                    f"rules resolve {workflow} --format json",
                    text,
                )
                self.assertIn("Select exactly one available resolver entrypoint", text)
                self.assertIn("Never retry the alternate after a nonzero result", text)
                self.assertIn(
                    "without fallback to the wrapper, memory, installed templates, "
                    "or remote framework prose",
                    text,
                )
                self.assertIn("`conflict_resolution` coverage", text)
                self.assertIn("Empty `conflicts` is unassured", text)
                self.assertIn(
                    "selected rules require unavailable conflict coverage", text
                )
                self.assertIn("`persistence: unavailable`", text)
                self.assertIn("never edit an emitted atomic artifact", text)
                self.assertFalse(any(fragment in text for fragment in forbidden))

                resolve_at = text.index(f"rules resolve {workflow}")
                read_at = text.index("Read the returned rule documents")
                runtime_at = text.index("runtime adapter only when exposed")
                self.assertLess(resolve_at, read_at)
                self.assertLess(read_at, runtime_at)

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

    def test_primary_trigger_is_general_and_specialist_stops_are_distinct(self) -> None:
        primary = self._skill_text("dset")
        self.assertIn("general, multi-stage, or next-action", primary)
        self.assertNotIn("Route any DSET lifecycle request", primary)
        self.assertIn("at most two workflow transitions", primary)

        specialists = {
            "dset-clarify": "stop before consequential selection or implementation",
            "dset-diagnose": "stop before implementing a fix",
            "dset-prototype": "stop before adoption or promotion",
            "dset-release": "Publication requires separate explicit authority",
        }
        for name, boundary in specialists.items():
            with self.subTest(skill=name):
                text = self._skill_text(name)
                self.assertIn(
                    "With no root, return a `$dset` `initialize` handoff", text
                )
                self.assertIn(boundary, text)


if __name__ == "__main__":
    unittest.main()
