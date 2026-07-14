from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from dset_toolchain.errors import DsetCommandError
from dset_toolchain.self_host import run_self_host

ROOT = Path(__file__).resolve().parents[1]


class SelfHostTests(unittest.TestCase):
    def test_hosted_workflow_fetches_released_validator_history(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "dset.yml").read_text(
            encoding="utf-8"
        )
        checkout = workflow.split("uses: actions/checkout@", maxsplit=1)[1]
        checkout = checkout.split("- name: Set up Python", maxsplit=1)[0]
        self.assertIn("fetch-depth: 0", checkout)

    def test_fixed_point_uses_released_and_candidate_validators(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            report = run_self_host(ROOT, Path(raw))
        self.assertEqual(report["released_validator"], "bootstrap-transition")
        self.assertIn(
            "released validator rejected", report["released_validator_diagnostic"]
        )
        self.assertEqual(report["candidate_repository"], "pass")
        self.assertEqual(report["temporary_adopter"], "pass")
        self.assertEqual(report["customization"], "custom")
        self.assertTrue(report["wrapper_unchanged"])
        self.assertTrue(report["recursion_stopped"])

    def test_bad_released_ref_fails_at_first_boundary(self) -> None:
        with (
            tempfile.TemporaryDirectory() as raw,
            self.assertRaises(DsetCommandError) as captured,
        ):
            run_self_host(ROOT, Path(raw), released_ref="0" * 40)
        self.assertEqual(captured.exception.code, "DSET-E140")

    def test_bad_candidate_command_fails_before_adopter(self) -> None:
        with (
            tempfile.TemporaryDirectory() as raw,
            self.assertRaises(DsetCommandError) as captured,
        ):
            run_self_host(
                ROOT,
                Path(raw),
                candidate_command=["missing-dset-candidate"],
            )
        self.assertEqual(captured.exception.code, "DSET-E141")

    def test_parallel_cli_runs_keep_temporary_adopters_outside_repository(self) -> None:
        environment = dict(os.environ)
        environment["TMPDIR"] = str(ROOT)
        command = [sys.executable, "-m", "dset_toolchain", "self-host", str(ROOT)]

        def execute() -> subprocess.CompletedProcess[str]:
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


if __name__ == "__main__":
    unittest.main()
