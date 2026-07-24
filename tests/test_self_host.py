"""Verify DSET self host behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dset_toolchain.errors import DsetCommandError
from dset_toolchain.self_host import run_self_host
from dset_toolchain.temp_paths import temporary_directory
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class SelfHostTests(unittest.TestCase):
    """Verify self host behavior."""

    def test_hosted_workflow_fetches_released_validator_history(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "dset.yml").read_text(
            encoding="utf-8"
        )
        checkout = workflow.split("uses: actions/checkout@", maxsplit=1)[1]
        checkout = checkout.split("- name: Set up Python", maxsplit=1)[0]
        self.assertIn("fetch-depth: 0", checkout)

    def test_fixed_point_uses_released_and_candidate_validators(self) -> None:
        with temporary_directory() as raw:
            report = run_self_host(ROOT, Path(raw))
        self.assertEqual(report["released_validator"], "bootstrap-transition")
        self.assertIn(
            "released validator rejected", report["released_validator_diagnostic"]
        )
        self.assertEqual(report["candidate_repository"], "pass")
        self.assertEqual(report["temporary_adopter"], "pass")
        self.assertEqual(report["customization"], "custom")
        self.assertEqual(
            report["workflows_resolved"],
            [
                "lifecycle-orchestration",
                "domain-clarification",
                "diagnosis",
                "prototyping",
                "work-triage",
                "decompose",
                "landscape",
                "decisions",
                "plan-proof",
                "plan-implementation",
                "implement",
                "verify",
                "complete",
                "overview",
            ],
        )
        self.assertTrue(report["wrappers_unchanged"])
        self.assertTrue(report["wrapper_unchanged"])
        self.assertTrue(report["recursion_stopped"])

    def test_bad_released_ref_fails_at_first_boundary(self) -> None:
        with (
            temporary_directory() as raw,
            self.assertRaises(DsetCommandError) as captured,
        ):
            run_self_host(ROOT, Path(raw), released_ref="0" * 40)
        self.assertEqual(captured.exception.code, "DSET-E140")

    def test_bad_candidate_command_fails_before_adopter(self) -> None:
        with (
            temporary_directory() as raw,
            self.assertRaises(DsetCommandError) as captured,
        ):
            run_self_host(
                ROOT,
                Path(raw),
                candidate_command=["missing-dset-candidate"],
            )
        self.assertEqual(captured.exception.code, "DSET-E141")

    def test_parallel_cli_runs_keep_temporary_adopters_outside_repository(self) -> None:
        patterns = ("dset-init-*", "dset-source-*", "dset-self-host-*")
        before = {
            path.resolve()
            for pattern in patterns
            for path in ROOT.glob(pattern)
            if path.is_dir()
        }
        environment = dict(os.environ)
        environment["TMPDIR"] = str(ROOT)
        command = [sys.executable, "-m", "dset_toolchain", "self-host", str(ROOT)]

        def execute() -> subprocess.CompletedProcess[str]:
            """Handle execute using the declared repository contract."""
            return subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: execute(), range(2)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = {
            path.resolve()
            for pattern in patterns
            for path in ROOT.glob(pattern)
            if path.is_dir()
        }
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
