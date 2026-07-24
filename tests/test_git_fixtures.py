"""Verify DSET git fixtures behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

from dset_toolchain.temp_paths import temporary_directory
from tests.git_fixtures import initialize_exact_git_repository


class GitFixtureTests(unittest.TestCase):
    """Verify git fixture behavior."""

    def test_repository_owns_deterministic_newline_policy(self) -> None:
        with temporary_directory() as raw:
            root = Path(raw).resolve()
            initialize_exact_git_repository(root)

            values = {
                key: subprocess.run(
                    ["git", "config", "--local", "--get", key],
                    cwd=root,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                for key in ("core.autocrlf", "core.eol")
            }

            self.assertEqual(values, {"core.autocrlf": "false", "core.eol": "lf"})


if __name__ == "__main__":
    unittest.main()
