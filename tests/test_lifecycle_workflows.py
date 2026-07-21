from __future__ import annotations

import re
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.governance import resolve_workflow
from dset_toolchain.layout import discover_layout
from dset_toolchain.skill_catalog import REGISTERED_SKILL_WORKFLOWS
from dset_toolchain.yaml_subset import load

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = discover_layout(ROOT)
REGISTRY = LAYOUT.governance_path
PROFILE = LAYOUT.find_template("governance/core-v1/profile.toml")
LIFECYCLE = ROOT / "dset/scopes/skill/governance/lifecycle-orchestration.md"

EXCEPTION_MODES = {"initialize", "repair-governance"}
MODE_WORKFLOWS = {
    "decompose": "decompose",
    "diagnose": "diagnosis",
    "clarify": "domain-clarification",
    "landscape": "landscape",
    "prototype": "prototyping",
    "decisions": "decisions",
    "plan-proof": "plan-proof",
    "plan-implementation": "plan-implementation",
    "implement": "implement",
    "verify": "verify",
    "triage-work": "work-triage",
    "release": "release",
    "complete": "complete",
}
PUBLIC_WRAPPER_WORKFLOWS = set(REGISTERED_SKILL_WORKFLOWS.values())
SUPPLEMENTAL_WORKFLOWS = {"overview"}


def _workflow_ids(data: dict[str, Any]) -> set[str]:
    return {
        cast(str, item["id"]) for item in cast(list[dict[str, Any]], data["workflows"])
    }


class LifecycleWorkflowTests(unittest.TestCase):
    def test_every_mode_has_a_registered_or_exception_route(self) -> None:
        registry = cast(dict[str, Any], load(REGISTRY))
        registered = _workflow_ids(registry)
        lifecycle = LIFECYCLE.read_text(encoding="utf-8")
        modes = set(re.findall(r"^\d+\. `([^`]+)`:", lifecycle, flags=re.MULTILINE))

        self.assertEqual(modes, EXCEPTION_MODES | set(MODE_WORKFLOWS))
        self.assertTrue(set(MODE_WORKFLOWS.values()).issubset(registered))
        self.assertTrue(SUPPLEMENTAL_WORKFLOWS.issubset(registered))

    def test_every_governed_mode_resolves_its_public_wrapper(self) -> None:
        registry = cast(dict[str, Any], load(REGISTRY))
        wrappers = cast(list[dict[str, Any]], registry["wrappers"])
        wrapped = {cast(str, item["workflow"]) for item in wrappers}

        self.assertEqual(wrapped, PUBLIC_WRAPPER_WORKFLOWS)
        self.assertEqual(len(wrappers), len(REGISTERED_SKILL_WORKFLOWS))

        for mode, workflow_id in sorted(MODE_WORKFLOWS.items()):
            with self.subTest(mode=mode, workflow=workflow_id):
                resolved, diagnostics = resolve_workflow(ROOT, workflow_id)
                self.assertEqual(diagnostics, [])
                self.assertIsNotNone(resolved)
                assert resolved is not None
                self.assertEqual(resolved["workflow_id"], workflow_id)
                self.assertIsNotNone(resolved["wrapper"])

    def test_distributed_profile_matches_repository_workflows(self) -> None:
        registry = cast(dict[str, Any], load(REGISTRY))
        profile = cast(dict[str, Any], load(PROFILE))

        self.assertEqual(_workflow_ids(profile), _workflow_ids(registry))
        self.assertEqual(profile["workflows"], registry["workflows"])
        profile_wrappers = cast(list[dict[str, Any]], profile["wrappers"])
        self.assertEqual(
            {cast(str, item["workflow"]) for item in profile_wrappers},
            PUBLIC_WRAPPER_WORKFLOWS,
        )
        self.assertEqual(len(profile_wrappers), len(REGISTERED_SKILL_WORKFLOWS))


if __name__ == "__main__":
    unittest.main()
