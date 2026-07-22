from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from .layout import METHODOLOGY_ROOT, discover_layout

SOURCE_TO_INSTALLED = (
    ("10_project", "00_project"),
    ("11_layer_meta", "01_meta"),
    ("12_layer_gov", "02_gov"),
    ("13_layer_tool", "03_tool"),
    ("14_layer_skill", "04_skill"),
    ("15_layer_ops", "05_ops"),
)
EXECUTABLE_SOURCE_TO_INSTALLED = (
    ("dset_toolchain", "03_tool/120_python/dset_toolchain"),
    ("tests", "03_tool/130_tests/tests"),
)
EXECUTABLE_SOURCE_NAMES = frozenset(
    source for source, _installed in EXECUTABLE_SOURCE_TO_INSTALLED
)
ALL_SOURCE_TO_INSTALLED = SOURCE_TO_INSTALLED + EXECUTABLE_SOURCE_TO_INSTALLED
TOOL_EXECUTABLE_SUBTREES = (
    Path("120_python/dset_toolchain"),
    Path("130_tests/tests"),
)
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
    for source_name, installed_name in ALL_SOURCE_TO_INSTALLED:
        source_root = root / source_name
        installed_root = target / installed_name
        _require_directory(source_root, source_name)
        executable_source = source_name in EXECUTABLE_SOURCE_NAMES
        if not installed_root.is_dir() and not executable_source:
            _require_directory(installed_root, installed_name)
        source_files = _files(source_root)
        installed_files = (
            _files(
                installed_root,
                excluded=TOOL_EXECUTABLE_SUBTREES
                if source_name == "13_layer_tool"
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
    unexpected = [item.carrier for item in drift if item.status == "unexpected"]
    if unexpected:
        raise ValueError(
            "installed methodology contains source-less carriers: "
            + ", ".join(unexpected)
        )
    changed = tuple(item.carrier for item in drift)
    if not execute:
        return changed
    target = _installed_root(root)
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
