"""Read and write the repository's TOML-only structured-data carriers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .toml_codec import TomlCodecError, dumps, load as load_toml, loads as loads_toml

# STRUCTURED_SUFFIX is the only project-owned structured carrier suffix.
STRUCTURED_SUFFIX = ".toml"


class StructuredDataError(ValueError):
    """Report a non-TOML carrier or a value outside the portable TOML subset."""


def load(path: Path) -> dict[str, Any]:
    """Load one TOML carrier and reject compatibility-format suffixes."""
    _require_toml_path(path)
    try:
        return load_toml(path)
    except (OSError, UnicodeError, TomlCodecError) as error:
        raise StructuredDataError(str(error)) from error


def loads(text: str) -> dict[str, Any]:
    """Load TOML text through the same portable subset as file carriers."""
    try:
        return loads_toml(text)
    except TomlCodecError as error:
        raise StructuredDataError(str(error)) from error


def dump(data: Any, path: Path | None = None) -> str:
    """Render TOML and optionally verify the destination carrier suffix."""
    if path is not None:
        _require_toml_path(path)
    try:
        return dumps(data)
    except TomlCodecError as error:
        raise StructuredDataError(str(error)) from error


def write(path: Path, data: Any) -> None:
    """Write one TOML carrier after creating its parent directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump(data, path), encoding="utf-8")


def _require_toml_path(path: Path) -> None:
    """Reject every project-owned structured carrier suffix except TOML."""
    if path.suffix.lower() != STRUCTURED_SUFFIX:
        raise StructuredDataError(
            f"project-owned structured carrier must use TOML: {path.name}"
        )
