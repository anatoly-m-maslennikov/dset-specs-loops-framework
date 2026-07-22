"""Provide DSET methodology sync behavior."""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from .layout import METHODOLOGY_ROOT, discover_layout

# SOURCE_TO_INSTALLED defines source to installed; this module owns the default.
SOURCE_TO_INSTALLED = (
    ("10_project", "00_project"),
    ("11_layer_meta", "01_meta"),
    ("12_layer_gov", "02_gov"),
    ("13_layer_tool", "03_tool"),
    ("14_layer_skill", "04_skill"),
    ("15_layer_implementation", "05_implementation"),
    ("16_layer_ops", "06_ops"),
)
# EXECUTABLE_SOURCE_TO_INSTALLED defines executable source to installed; this module owns the default.
EXECUTABLE_SOURCE_TO_INSTALLED = (
    ("dset_toolchain", "05_implementation/100_python/dset_toolchain"),
    ("tests", "05_implementation/110_tests/tests"),
)
# ALL_SOURCE_TO_INSTALLED defines all source to installed; this module owns the default.
ALL_SOURCE_TO_INSTALLED = SOURCE_TO_INSTALLED + EXECUTABLE_SOURCE_TO_INSTALLED
# IMPLEMENTATION_EXECUTABLE_SUBTREES defines implementation executable subtrees; this module owns the default.
IMPLEMENTATION_EXECUTABLE_SUBTREES = (
    Path("100_python/dset_toolchain"),
    Path("110_tests/tests"),
)
# SOURCE_ONLY_CARRIERS defines source only carriers; this module owns the default.
SOURCE_ONLY_CARRIERS = frozenset({"000_dset-project-hub.md"})


@dataclass(frozen=True)
class MethodologyDrift:
    carrier: str
    status: str


def methodology_drift(root: Path) -> tuple[MethodologyDrift, ...]:
    """Compare reusable source with the installed project-local methodology."""

    root = root.resolve()
    target = _installed_root(root)
    drift: list[MethodologyDrift] = []
    expected_roots = {name.split("/", 1)[0] for _, name in ALL_SOURCE_TO_INSTALLED}
    if target.is_dir():
        for child in sorted(target.iterdir()):
            if child.is_dir() and child.name not in expected_roots:
                drift.append(MethodologyDrift(child.name, "unexpected"))
    for source_name, installed_name in ALL_SOURCE_TO_INSTALLED:
        source_root = root / source_name
        installed_root = target / installed_name
        _require_directory(source_root, source_name)
        source_files = _files(source_root)
        installed_files = (
            _files(
                installed_root,
                excluded=IMPLEMENTATION_EXECUTABLE_SUBTREES
                if source_name == "15_layer_implementation"
                else (),
            )
            if installed_root.is_dir()
            else {}
        )
        for relative, source in source_files.items():
            if source.name in SOURCE_ONLY_CARRIERS:
                continue
            destination = installed_root / relative
            if not destination.is_file():
                drift.append(MethodologyDrift(source.name, "missing"))
            elif _sha256(source) != _sha256(destination):
                drift.append(MethodologyDrift(source.name, "changed"))
        for relative, installed in installed_files.items():
            if installed.name in SOURCE_ONLY_CARRIERS:
                continue
            if relative not in source_files:
                drift.append(MethodologyDrift(installed.name, "unexpected"))
    return tuple(sorted(drift, key=lambda item: (item.carrier, item.status)))


def sync_methodology(root: Path, *, execute: bool = False) -> tuple[str, ...]:
    """Preview or materialize source carriers into the installed methodology."""

    root = root.resolve()
    drift = methodology_drift(root)
    changed = tuple(item.carrier for item in drift)
    if not execute:
        return changed
    target = _installed_root(root)
    _remove_source_less_carriers(root, target)
    for source_name, installed_name in ALL_SOURCE_TO_INSTALLED:
        source_root = root / source_name
        installed_root = target / installed_name
        installed_root.mkdir(parents=True, exist_ok=True)
        for relative, source in _files(source_root).items():
            if source.name in SOURCE_ONLY_CARRIERS:
                continue
            destination = installed_root / relative
            if destination.is_file() and _sha256(source) == _sha256(destination):
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    if methodology_drift(root):
        raise ValueError("installed methodology remains out of sync")
    return changed


def _remove_source_less_carriers(root: Path, target: Path) -> None:
    expected_roots = {name.split("/", 1)[0] for _, name in ALL_SOURCE_TO_INSTALLED}
    for child in sorted(target.iterdir()):
        if child.is_dir() and child.name not in expected_roots:
            shutil.rmtree(child)
    for source_name, installed_name in ALL_SOURCE_TO_INSTALLED:
        source_root = root / source_name
        installed_root = target / installed_name
        if not installed_root.is_dir():
            continue
        excluded = (
            IMPLEMENTATION_EXECUTABLE_SUBTREES
            if source_name == "15_layer_implementation"
            else ()
        )
        source_files = _files(source_root)
        installed_files = _files(installed_root, excluded=excluded)
        for relative, installed in installed_files.items():
            if relative not in source_files:
                installed.unlink()
        for directory in sorted(installed_root.rglob("*"), reverse=True):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()


def _installed_root(root: Path) -> Path:
    layout = discover_layout(root)
    if not layout.separated:
        raise ValueError("methodology synchronization requires schema 1.5")
    return layout.dset_root / METHODOLOGY_ROOT


def _files(
    root: Path,
    *,
    excluded: tuple[Path, ...] = (),
) -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if (
            path.name.startswith(".")
            or path.suffix == ".pyc"
            or "__pycache__" in relative.parts
            or any(relative.is_relative_to(prefix) for prefix in excluded)
        ):
            continue
        files[relative] = path
    return files


def _require_directory(path: Path, identity: str) -> None:
    if not path.is_dir():
        raise FileNotFoundError(f"methodology area is missing: {identity}")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
