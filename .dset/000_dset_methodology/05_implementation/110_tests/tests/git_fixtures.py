"""Verify DSET git fixtures behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def initialize_exact_git_repository(root: Path) -> None:
    """Initialize a fixture repository with deterministic text-byte policy."""
    subprocess.run(
        ["git", "init", "-q"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    for key, value in (("core.autocrlf", "false"), ("core.eol", "lf")):
        subprocess.run(
            ["git", "config", "--local", key, value],
            cwd=root,
            check=True,
            capture_output=True,
        )
