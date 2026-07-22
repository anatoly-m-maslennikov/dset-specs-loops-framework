from __future__ import annotations

import copy
import json
import subprocess
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.enforcement_profiles import (
    GATE_IDS,
    inspect_target,
    resolve_profile_path,
    validate_profile_data,
    validate_profile_file,
)
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.yaml_subset import dump

ROOT = Path(__file__).resolve().parents[1]
PROFILE = (
    ROOT
    / ".dset/03_layer_tool/templates/enforcement-profiles/typescript-v1-candidate.toml"
)


class EnforcementProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        data, diagnostics = validate_profile_file(PROFILE)
        self.assertEqual(diagnostics, [])
        self.profile = data

    def test_typescript_candidate_is_pinned_and_complete(self) -> None:
        self.assertEqual(self.profile["id"], "typescript-v1-candidate")
        self.assertEqual(self.profile["status"], "candidate")
        self.assertEqual(self.profile["profile_role"], "reference")
        self.assertEqual(self.profile["target_revision_policy"], "exact")
        evidence = cast(dict[str, Any], self.profile["evidence"])
        self.assertEqual(
            evidence["revision"],
            "1c3ede2653245412d4d03067d5b20d9dd228298d",
        )
        self.assertEqual(
            evidence["upstream_revision"],
            "783df1ceb149ac9cd9a00a3444c3dadf83bbacf4",
        )
        gates = cast(list[dict[str, Any]], self.profile["gates"])
        self.assertEqual({item["id"] for item in gates}, set(GATE_IDS))
        self.assertEqual(self.profile["warning_baseline"]["warning_count"], 203)
        self.assertEqual(self.profile["warning_baseline"]["error_count"], 0)
        self.assertIn("OYOHA-DSET-001", self.profile["known_blockers"])
        observed = cast(dict[str, Any], self.profile["observed"])
        ci = cast(dict[str, Any], observed["ci"])
        self.assertEqual(ci["active_workflows"], 0)
        self.assertEqual(ci["candidate_jobs"], ["lint", "typecheck", "test"])

    def test_invalid_profile_boundaries_fail_closed(self) -> None:
        cases: list[tuple[str, Any]] = []

        missing_gate = copy.deepcopy(self.profile)
        missing_gate["gates"].pop()
        cases.append(("all six gates", missing_gate))

        unpinned = copy.deepcopy(self.profile)
        unpinned["evidence"]["revision"] = "main"
        cases.append(("full SHA", unpinned))

        unsafe = copy.deepcopy(self.profile)
        unsafe["scope"]["source_roots"] = ["../src"]
        cases.append(("unsafe profile path", unsafe))

        hard_baseline = copy.deepcopy(self.profile)
        hard_baseline["warning_baseline"]["error_count"] = 1
        cases.append(("Hard errors", hard_baseline))

        inconsistent = copy.deepcopy(self.profile)
        inconsistent["warning_baseline"]["warning_count"] = 204
        cases.append(("per-rule", inconsistent))

        outside_sequence = copy.deepcopy(self.profile)
        outside_sequence["gates"][0]["commands"] = ["npm run unknown"]
        cases.append(("outside canonical sequence", outside_sequence))

        active_blocked = copy.deepcopy(self.profile)
        active_blocked["status"] = "active"
        cases.append(("active profile", active_blocked))

        invalid_revision_policy = copy.deepcopy(self.profile)
        invalid_revision_policy["target_revision_policy"] = "floating"
        cases.append(("target_revision_policy", invalid_revision_policy))

        invalid_role = copy.deepcopy(self.profile)
        invalid_role["profile_role"] = "generic"
        cases.append(("profile_role", invalid_role))

        applied_without_source = copy.deepcopy(self.profile)
        applied_without_source["profile_role"] = "applied"
        cases.append(("derived_from", applied_without_source))

        reference_with_source = copy.deepcopy(self.profile)
        reference_with_source["derived_from"] = "typescript-v1-candidate@0.1"
        cases.append(("cannot set derived_from", reference_with_source))

        for expected, candidate in cases:
            with self.subTest(expected=expected):
                rendered = "\n".join(
                    item.message for item in validate_profile_data(PROFILE, candidate)
                )
                self.assertIn(expected.lower(), rendered.lower())

    def test_target_inspection_is_read_only_and_detects_drift(self) -> None:
        with temporary_directory() as raw:
            target = Path(raw).resolve()
            profile = copy.deepcopy(self.profile)
            scripts = cast(dict[str, str], profile["toolchain"]["scripts"])
            package = {"scripts": scripts}
            (target / "package.json").write_text(json.dumps(package), encoding="utf-8")
            for relative in cast(list[str], profile["scope"]["required_files"]):
                path = target / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_text("{}\n", encoding="utf-8")
            source = target / "src/core"
            tests = target / "tests/unit"
            source.mkdir(parents=True)
            tests.mkdir(parents=True)
            (source / "one.ts").write_text("export const one = 1;\n")
            (source / "two.tsx").write_text("export const two = 2;\n")
            (tests / "one.test.ts").write_text("test('one', () => {});\n")
            self._git(target, "init", "-q")
            self._git(target, "config", "user.name", "DSET Test")
            self._git(target, "config", "user.email", "dset@example.invalid")
            self._git(target, "add", ".")
            self._git(target, "commit", "-qm", "fixture")
            revision = self._git(target, "rev-parse", "HEAD")
            profile["evidence"]["revision"] = revision
            profile["warning_baseline"]["revision"] = revision
            profile["observed"]["file_counts"] = {
                "source_typescript": 2,
                "test_typescript": 1,
                "lint_files": 3,
            }

            before = self._git(target, "status", "--porcelain")
            result = inspect_target(PROFILE, profile, target)
            after = self._git(target, "status", "--porcelain")

            self.assertEqual(result["diagnostics"], [])
            self.assertFalse(result["commands_executed"])
            self.assertFalse(result["promotion_eligible"])
            self.assertEqual(result["profile_role"], "reference")
            self.assertEqual(result["file_counts"]["lint_files"], 3)
            self.assertEqual(before, after)

            profile["toolchain"]["scripts"]["lint"] = "eslint changed"
            drift = inspect_target(PROFILE, profile, target)
            self.assertTrue(
                any(
                    "target script drift: lint" in item for item in drift["diagnostics"]
                )
            )

            original_scripts = cast(
                dict[str, str], self.profile["toolchain"]["scripts"]
            )
            profile["toolchain"]["scripts"]["lint"] = original_scripts["lint"]
            (target / "src/core/three.ts").write_text(
                "export const three = 3;\n", encoding="utf-8"
            )
            self._git(target, "add", ".")
            self._git(target, "commit", "-qm", "descendant")
            profile["observed"]["file_counts"]["source_typescript"] = 3
            profile["observed"]["file_counts"]["lint_files"] = 4

            exact = inspect_target(PROFILE, profile, target)
            self.assertTrue(
                any("target revision drift" in item for item in exact["diagnostics"])
            )
            profile["target_revision_policy"] = "descendant"
            descendant = inspect_target(PROFILE, profile, target)
            self.assertEqual(descendant["diagnostics"], [])

    def test_framework_resolves_the_candidate_template(self) -> None:
        self.assertEqual(resolve_profile_path(ROOT, "typescript-v1-candidate"), PROFILE)

    def test_adopter_cannot_execute_a_framework_reference_as_local_truth(self) -> None:
        with temporary_directory() as raw:
            target = Path(raw).resolve()
            meta = target / "dset/scopes/meta"
            template = (
                target
                / "dset/scopes/tool/templates/enforcement-profiles"
                / PROFILE.name
            )
            for layer in ("meta", "gov", "tool", "skill", "ops"):
                (target / "dset/scopes" / layer).mkdir(parents=True)
            template.parent.mkdir(parents=True)
            manifest = meta / "dset.toml"
            manifest.write_text(
                dump(
                    {
                        "schema_version": "1.2",
                        "project": {
                            "key": "SAMPLE",
                            "repository_role": "adopter",
                        },
                    },
                    manifest,
                ),
                encoding="utf-8",
            )
            template.write_text(PROFILE.read_text(encoding="utf-8"), encoding="utf-8")

            with self.assertRaisesRegex(FileNotFoundError, "project-owned instances"):
                resolve_profile_path(target, "typescript-v1-candidate")

            applied = (
                target / "dset/scopes/tool/profiles" / "typescript-v1-candidate.toml"
            )
            applied.parent.mkdir(parents=True)
            applied_profile = copy.deepcopy(self.profile)
            applied_profile["profile_role"] = "applied"
            applied_profile["derived_from"] = "typescript-v1-candidate@0.1"
            applied.write_text(
                dump(applied_profile, applied),
                encoding="utf-8",
            )
            self.assertEqual(
                resolve_profile_path(target, "typescript-v1-candidate"),
                applied,
            )

    @staticmethod
    def _git(root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()
