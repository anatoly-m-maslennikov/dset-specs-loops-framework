from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.git_fixtures import initialize_exact_git_repository


class GitFixtureTests(unittest.TestCase):
    def test_repository_owns_deterministic_newline_policy(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
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
