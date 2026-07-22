"""Run the DSET tests run entrypoint.

Invocation: execute this file with optional documented CLI flags.
Inputs and outputs: command arguments in; diagnostics and status out.
Mutable effects: disabled by --dry-run.
Exit statuses: zero succeeds; nonzero reports an actionable failure.
Environment: an isolated supported Python environment.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


def _project_root(start: Path) -> Path:
    for candidate in start.resolve().parents:
        if (candidate / ".dset" / "dset_settings.toml").is_file():
            return candidate
    raise FileNotFoundError("DSET project root is unavailable")


def main() -> int:
    sys.dont_write_bytecode = True
    carrier = Path(__file__).resolve()
    project_root = _project_root(carrier)
    implementation_root = carrier.parents[1]
    installed_python = implementation_root / "100_python"
    installed_tests = carrier.parent / "tests"

    if (installed_python / "dset_toolchain").is_dir() and installed_tests.is_dir():
        package_root = installed_python
        tests_parent = carrier.parent
        tests_root = installed_tests
    else:
        package_root = project_root
        tests_parent = project_root
        tests_root = project_root / "tests"

    import_roots = [str(package_root), str(tests_parent)]
    sys.path[:0] = import_roots
    inherited_pythonpath = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = os.pathsep.join(
        [*import_roots, *([inherited_pythonpath] if inherited_pythonpath else [])]
    )
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    suite = unittest.defaultTestLoader.discover(
        str(tests_root),
        top_level_dir=str(tests_parent),
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
