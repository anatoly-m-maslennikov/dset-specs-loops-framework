"""Verify DSET methodology sync behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

from dset_toolchain.methodology_sync import methodology_drift
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))
# METHODOLOGY defines methodology; this module owns the default.
METHODOLOGY = ROOT / ".dset" / "000_dset_methodology"


def _unique_carrier(name: str) -> Path:
    matches = tuple(METHODOLOGY.rglob(name))
    if len(matches) != 1:
        raise AssertionError(f"expected one {name}, found {len(matches)}")
    return matches[0]


class MethodologySyncTests(unittest.TestCase):
    """Verify methodology sync behavior."""

    def test_installed_methodology_matches_all_registered_sources(self) -> None:
        self.assertEqual(methodology_drift(ROOT), ())

    def test_installed_executables_are_real_files_without_symlinks(self) -> None:
        carriers = (
            _unique_carrier("010_dset-tool-python-run.py"),
            _unique_carrier("010_dset-tool-tests-run.py"),
            _unique_carrier("010_dset-tool-evaluations-independent-review.md"),
            _unique_carrier("020_dset-tool-evaluations-result-reconciliation.md"),
        )
        for carrier in carriers:
            with self.subTest(carrier=carrier.name):
                self.assertTrue(carrier.is_file())
                self.assertFalse(carrier.is_symlink())

    def test_installed_python_launcher_uses_the_local_package(self) -> None:
        launcher = _unique_carrier("010_dset-tool-python-run.py")
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, str(launcher), "--version"],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout.strip(), r"^0\.3\.1$")

    def test_evaluation_implementations_preserve_qa_boundaries(self) -> None:
        independent = _unique_carrier(
            "010_dset-tool-evaluations-independent-review.md"
        ).read_text(encoding="utf-8")
        reconciliation = _unique_carrier(
            "020_dset-tool-evaluations-result-reconciliation.md"
        ).read_text(encoding="utf-8")

        self.assertRegex(independent, r"exactly one accepted Evaluation\s+ID")
        self.assertIn("pass, fail, or inconclusive", independent)
        self.assertRegex(
            reconciliation,
            r"without rerunning the\s+Evaluation",
        )
        self.assertIn("Do not convert evidence into authority", reconciliation)


if __name__ == "__main__":
    unittest.main()
