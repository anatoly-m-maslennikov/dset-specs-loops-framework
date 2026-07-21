from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

from .diagnostics import Diagnostic
from .layout import discover_layout
from .traceability import trace_is_fresh
from .validation import validate_repository
from .yaml_subset import load


def _verification_args(command: object) -> list[str]:
    """Expand exact command placeholders without reparsing native paths."""

    args = shlex.split(str(command))
    return [sys.executable if arg == "{python}" else arg for arg in args]


def verify_repository(root: Path) -> list[Diagnostic]:
    diagnostics = validate_repository(root)
    if diagnostics:
        return diagnostics
    layout = discover_layout(root)
    manifest = load(layout.manifest_path)
    verification = manifest.get("verification", {})
    for command in verification.get("commands", []):
        args = _verification_args(command)
        result = subprocess.run(
            args,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip()
            suffix = f"; output: {detail[-2000:]}" if detail else ""
            diagnostics.append(
                Diagnostic(
                    "DSET-E201",
                    layout.manifest_path,
                    "verification command failed "
                    f"({result.returncode}): {command}{suffix}",
                )
            )
            return diagnostics
    if not trace_is_fresh(root):
        diagnostics.append(
            Diagnostic(
                "DSET-E111",
                layout.traceability_path,
                "traceability is missing or stale; run dset trace --write",
            )
        )
    return diagnostics
