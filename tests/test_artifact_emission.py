from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.adopter import create_adopter
from dset_toolchain.artifact_emission import assess_artifact_candidate
from dset_toolchain.cli import main
from dset_toolchain.settings import load_project_settings

ROOT = Path(__file__).resolve().parents[1]


class ArtifactEmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = create_adopter(ROOT, Path(self.temporary.name) / "adopter")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def candidate(self) -> dict[str, Any]:
        return {
            "authority": "operator:test-operator",
            "claim": "The tool writes one deterministic result.",
            "type": "decision",
            "subtype": "requirement",
            "scope": {"kind": "project", "id": "dset-temporary-adopter"},
            "llm_session_ids": ["codex:test-session"],
            "material_links": [],
            "priority": "medium",
            "acceptance": "accepted",
            "promotion": {"parent_scope": None},
            "unknowns": [
                {
                    "field": "rationale",
                    "material": False,
                    "question": "Would rationale help later review?",
                }
            ],
        }

    def enable_high_strictness(self) -> None:
        path = self.root / "dset.toml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'artifact_creation_strictness = "medium"',
                'artifact_creation_strictness = "high"',
            ),
            encoding="utf-8",
        )

    def test_medium_is_default_and_allows_explicit_core_claim(self) -> None:
        settings, issues = load_project_settings(self.root)
        self.assertEqual(issues, ())
        self.assertEqual(settings.artifact_creation_strictness, "medium")
        self.assertEqual(
            settings.priority_scale,
            ("critical", "high", "medium", "low", "deferred"),
        )
        self.assertEqual(settings.default_priority, "medium")

        assessment = assess_artifact_candidate(self.root, self.candidate())

        self.assertTrue(assessment["emission_allowed"])
        self.assertEqual(assessment["strictness"], "medium")
        self.assertEqual(assessment["questions"], [])
        self.assertFalse(assessment["writes_performed"])

    def test_missing_setting_uses_medium_but_invalid_value_stops(self) -> None:
        path = self.root / "dset.toml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'artifact_creation_strictness = "medium"\n', ""
            ),
            encoding="utf-8",
        )
        settings, issues = load_project_settings(self.root)
        self.assertEqual(settings.artifact_creation_strictness, "medium")
        self.assertEqual(issues, ())

        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "artifact_subtype_in_names = false\n",
                "artifact_subtype_in_names = false\n"
                'artifact_creation_strictness = "maximum"\n',
            ),
            encoding="utf-8",
        )
        _settings, issues = load_project_settings(self.root)
        self.assertIn("artifact_creation_strictness must be medium or high", issues)

    def test_high_blocks_until_every_material_field_is_explicit(self) -> None:
        self.enable_high_strictness()

        blocked = assess_artifact_candidate(self.root, self.candidate())

        self.assertFalse(blocked["emission_allowed"])
        missing = {item["field"] for item in blocked["diagnostics"]}
        self.assertEqual(
            missing,
            set(
                (
                    "boundary",
                    "lineage",
                    "conflict_state",
                    "verification_obligation",
                )
            ),
        )
        self.assertEqual(len(blocked["questions"]), 4)

        complete = self.candidate()
        complete.update(
            {
                "boundary": "One repository-local writer only.",
                "priority": "high",
                "lineage": [],
                "acceptance": "accepted",
                "conflict_state": "clear",
                "verification_obligation": "DSET-TEST-TOOL-001",
            }
        )
        allowed = assess_artifact_candidate(self.root, complete)
        self.assertTrue(allowed["emission_allowed"])

    def test_material_unknown_blocks_at_either_strictness(self) -> None:
        candidate = self.candidate()
        candidate["unknowns"] = [
            {
                "field": "authority",
                "material": True,
                "question": "Did the operator accept this directive?",
            }
        ]

        assessment = assess_artifact_candidate(self.root, candidate)

        self.assertFalse(assessment["emission_allowed"])
        self.assertIn(
            "Did the operator accept this directive?", assessment["questions"]
        )

    def test_unknown_repository_scope_is_rejected(self) -> None:
        candidate = self.candidate()
        candidate["scope"] = {"kind": "feature", "id": "unregistered"}

        assessment = assess_artifact_candidate(self.root, candidate)

        self.assertFalse(assessment["emission_allowed"])
        messages = [item["message"] for item in assessment["diagnostics"]]
        self.assertIn(
            "scope is not enabled by the repository manifest",
            messages,
        )

    def test_eligible_promotion_is_proposed_and_never_automatic(self) -> None:
        candidate = self.candidate()
        candidate["scope"] = {"kind": "layer", "id": "tool"}
        candidate["promotion"] = {
            "parent_scope": {
                "kind": "project",
                "id": "dset-specs-loops-framework",
            },
            "applies_unchanged": True,
            "local_context_required": False,
            "affected_children": ["meta", "gov", "tool", "skill", "ops"],
        }

        proposal = assess_artifact_candidate(ROOT, candidate)

        self.assertFalse(proposal["emission_allowed"])
        self.assertEqual(proposal["promotion"]["status"], "proposal-required")
        self.assertTrue(proposal["promotion"]["eligible"])
        self.assertFalse(proposal["promotion"]["automatic"])

        candidate["promotion"]["disposition"] = "keep_local"
        local = assess_artifact_candidate(ROOT, candidate)
        self.assertTrue(local["emission_allowed"])
        self.assertEqual(local["promotion"]["status"], "declined")

        candidate["promotion"]["disposition"] = "promote"
        promote = assess_artifact_candidate(ROOT, candidate)
        self.assertFalse(promote["emission_allowed"])
        self.assertEqual(promote["promotion"]["status"], "promote-before-emission")

    def test_cli_is_read_only_and_returns_blocked_status(self) -> None:
        candidate_path = self.root / "candidate.json"
        candidate = self.candidate()
        candidate.pop("claim")
        candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            status = main(
                [
                    "artifact",
                    "assess",
                    str(self.root),
                    "--candidate",
                    str(candidate_path),
                ]
            )

        self.assertEqual(status, 2)
        result = json.loads(output.getvalue())
        self.assertFalse(result["emission_allowed"])
        self.assertFalse(result["writes_performed"])


if __name__ == "__main__":
    unittest.main()
