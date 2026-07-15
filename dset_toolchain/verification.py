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


def verify_repository(root: Path) -> list[Diagnostic]:
    diagnostics = validate_repository(root)
    if diagnostics:
        return diagnostics
    layout = discover_layout(root)
    manifest = load(layout.manifest_path)
    verification = manifest.get("verification", {})
    for command in verification.get("commands", []):
        args = shlex.split(str(command).replace("{python}", sys.executable))
        result = subprocess.run(args, cwd=root, check=False)
        if result.returncode:
            diagnostics.append(
                Diagnostic(
                    "DSET-E201",
                    layout.manifest_path,
                    f"verification command failed ({result.returncode}): {command}",
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
