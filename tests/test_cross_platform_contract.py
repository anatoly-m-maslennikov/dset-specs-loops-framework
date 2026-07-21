from __future__ import annotations

import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CrossPlatformContractTests(unittest.TestCase):
    def test_repository_pins_text_worktree_bytes_to_lf(self) -> None:
        paths = (
            "dset_toolchain/validation.py",
            "dset/scopes/ops/governance/release.md",
            "dset/scopes/gov/migrations/carrier-transitions.toml",
            "dset/scopes/gov/generated/traceability.toml",
        )
        for path in paths:
            result = subprocess.run(
                [
                    "git",
                    "-c",
                    "core.autocrlf=true",
                    "check-attr",
                    "eol",
                    "--",
                    path,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            with self.subTest(path=path):
                self.assertEqual(result.stdout.strip(), f"{path}: eol: lf")

    def test_hosted_matrix_covers_linux_macos_and_native_windows(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "dset.yml").read_text(
            encoding="utf-8"
        )
        for runner in ("ubuntu-latest", "macos-latest", "windows-latest"):
            self.assertIn(runner, workflow)
        self.assertNotIn("shell: bash", workflow)
        self.assertNotIn("shell: pwsh", workflow)

    def test_wsl_proof_requires_an_explicit_self_hosted_runner(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "wsl-proof.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch", workflow)
        self.assertIn("runs-on: [self-hosted, windows, x64, wsl]", workflow)
        self.assertIn("shell: wsl.exe bash -e {0}", workflow)

    def test_cli_handles_spaces_and_unicode_without_shell_assumptions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="dset portability ") as raw:
            target = (Path(raw) / "project ünicode").resolve()
            target.mkdir()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(
                    [
                        "init",
                        str(target),
                        "--project-key",
                        "APP",
                        "--project-id",
                        "portable-app",
                        "--name",
                        "Portable App",
                        "--license",
                        "MIT",
                        "--format",
                        "json",
                    ]
                )
            self.assertEqual(status, 0)
            self.assertFalse((target / "dset").exists())

    def test_portable_modules_have_no_machine_paths_or_shell_execution(self) -> None:
        modules = (
            "bootstrap.py",
            "runtime.py",
            "runtime_bridge.py",
            "skill_distribution.py",
            "release.py",
        )
        for name in modules:
            text = (ROOT / "dset_toolchain" / name).read_text(encoding="utf-8")
            with self.subTest(module=name):
                self.assertNotIn("/Users/", text)
                self.assertNotIn("C:\\\\", text)
                self.assertNotIn("shell=True", text)


if __name__ == "__main__":
    unittest.main()
