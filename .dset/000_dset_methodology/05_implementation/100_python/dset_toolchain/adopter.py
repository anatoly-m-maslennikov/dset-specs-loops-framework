"""Provide DSET adopter behavior."""

from __future__ import annotations

from pathlib import Path

from .bootstrap import initialize_project


def create_adopter(source_root: Path, destination: Path) -> Path:
    """Create the bounded recursive adopter used by self-host validation."""

    source_root = source_root.resolve()
    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"adopter destination exists: {destination}")
    initialize_project(
        destination,
        project_key="DSET",
        project_id="dset-temporary-adopter",
        project_name="DSET temporary adopter",
        project_license="Apache-2.0",
        package_id="sample",
        source_root=source_root,
        execute=True,
    )
    return destination
