"""Read and render TOML frontmatter for DSET-owned Markdown carriers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .toml_codec import TomlCodecError
from .toml_codec import dumps as dump_toml
from .toml_codec import loads as load_toml


class FrontmatterError(ValueError):
    """A Markdown frontmatter envelope is malformed or unsupported."""


def parse(text: str) -> tuple[dict[str, Any], str, str] | None:
    """Return ``(metadata, body, format)`` or ``None`` without frontmatter."""

    lines = text.splitlines(keepends=True)
    if not lines:
        return None
    delimiter = lines[0].strip()
    if delimiter != "+++":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() != delimiter:
            continue
        payload = "".join(lines[1:index])
        try:
            value = load_toml(payload)
        except TomlCodecError as error:
            raise FrontmatterError(str(error)) from error
        if not isinstance(value, dict):
            raise FrontmatterError("frontmatter root must be a mapping")
        return (
            value,
            "".join(lines[index + 1 :]),
            "toml",
        )
    raise FrontmatterError("frontmatter opening delimiter has no closing delimiter")


def load(path: Path) -> tuple[dict[str, Any], str, str] | None:
    """Read frontmatter from a Markdown path."""

    return parse(path.read_text(encoding="utf-8"))


def metadata(path: Path) -> dict[str, Any] | None:
    """Read only a frontmatter mapping, returning ``None`` when absent."""

    parsed = load(path)
    return parsed[0] if parsed is not None else None


def format_for_path(path: Path, *, default: str = "toml") -> str:
    """Preserve an existing envelope during compatibility-mode regeneration."""

    try:
        parsed = load(path)
    except (OSError, UnicodeError, FrontmatterError):
        return default
    return parsed[2] if parsed is not None else default


def render(metadata: dict[str, Any], body: str, *, format: str = "toml") -> str:
    """Render a complete Markdown envelope in the requested format."""

    if format == "toml":
        return f"+++\n{dump_toml(metadata)}+++\n{body}"
    raise FrontmatterError(f"unsupported frontmatter format: {format}")
