"""Provide DSET temp paths behavior."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def scratch_root(
    *,
    platform_name: str | None = None,
    allow_test_override: bool = True,
) -> Path:
    """Return the host scratch root without trusting a POSIX ambient TMPDIR."""

    if allow_test_override and os.environ.get("DSET_TESTING") == "1":
        test_root = os.environ.get("DSET_TEST_SCRATCH_ROOT")
        if test_root:
            root = Path(test_root).resolve()
            if not root.is_dir():
                raise FileNotFoundError(
                    f"configured DSET test scratch root is unavailable: {root}"
                )
            return root

    platform = os.name if platform_name is None else platform_name
    if platform == "posix":
        return Path("/tmp")
    if platform == "nt":
        return Path(tempfile.gettempdir()).resolve()
    raise OSError(f"unsupported temporary-directory platform: {platform}")


def temporary_directory(
    *,
    prefix: str = "dset-",
    suffix: str | None = None,
) -> tempfile.TemporaryDirectory[str]:
    """Create a fail-loud DSET scratch directory under the host temp root."""

    root = scratch_root()
    if not root.is_dir():
        raise FileNotFoundError(f"temporary root is unavailable: {root}")
    return tempfile.TemporaryDirectory(
        suffix=suffix,
        prefix=prefix,
        dir=root,
        ignore_cleanup_errors=False,
    )
