"""DSET toolchain regression tests."""

from __future__ import annotations

from pathlib import Path


def repository_root(carrier: Path) -> Path:
    """Resolve the owning DSET project from root or installed Test carriers."""

    for candidate in carrier.resolve().parents:
        if (candidate / ".dset" / "dset_settings.toml").is_file():
            return candidate
    raise FileNotFoundError("DSET project root is unavailable")


def unique_carrier(root: Path, name: str) -> Path:
    """Resolve one globally unique carrier name inside the project control plane."""

    matches = tuple((root / ".dset").rglob(name))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected one DSET carrier named {name}, found {len(matches)}"
        )
    return matches[0]
