"""Configure optional DSET governance surfaces.

Commands inspect or preview one repository-local ``dset_settings.toml``.
Writes require an explicit execute flag and preserve unrelated TOML text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .errors import DsetCommandError
from .settings import GOVERNANCE_SURFACE_KEYS, selected_settings_path
from .toml_codec import TomlCodecError
from .toml_codec import load as load_toml

# SURFACE_IDS maps readable CLI identities to canonical TOML keys.
SURFACE_IDS = {
    key.replace("_", "-"): key for key in GOVERNANCE_SURFACE_KEYS
}
# _TABLE_HEADER recognizes the one owned settings table.
_TABLE_HEADER = re.compile(r"^\s*\[governance_surfaces\]\s*(?:#.*)?$")
# _ANY_TABLE_HEADER recognizes the boundary of the next TOML table.
_ANY_TABLE_HEADER = re.compile(r"^\s*\[\[?[A-Za-z0-9_.\"'-]+\]?\]\s*(?:#.*)?$")


@dataclass(frozen=True)
class SurfaceChange:
    """Describe one previewed governance-surface state change."""

    settings_path: Path
    surface_id: str
    before: bool
    after: bool
    changed: bool

    def as_dict(self) -> dict[str, str | bool]:
        """Return a stable command-facing representation."""
        return {
            "settings_path": self.settings_path.as_posix(),
            "surface": self.surface_id,
            "before": self.before,
            "after": self.after,
            "changed": self.changed,
        }


def surface_states(root: Path) -> dict[str, bool]:
    """Return all registered surface states, defaulting missing keys to false."""
    path, table = _surface_table(root)
    unknown = sorted(set(table) - set(GOVERNANCE_SURFACE_KEYS))
    if unknown:
        raise _settings_error(
            path,
            "unknown governance surface: " + ", ".join(unknown),
        )
    states: dict[str, bool] = {}
    for surface_id, key in SURFACE_IDS.items():
        value = table.get(key, False)
        if not isinstance(value, bool):
            raise _settings_error(path, f"governance_surfaces.{key} must be boolean")
        states[surface_id] = value
    return states


def plan_surface_change(
    root: Path,
    surface_id: str,
    *,
    active: bool,
) -> SurfaceChange:
    """Preview one activation or deactivation without changing the repository."""
    canonical_id = _surface_id(surface_id)
    states = surface_states(root)
    before = states[canonical_id]
    return SurfaceChange(
        settings_path=selected_settings_path(root),
        surface_id=canonical_id,
        before=before,
        after=active,
        changed=before != active,
    )


def execute_surface_change(change: SurfaceChange) -> None:
    """Apply a previewed change while preserving unrelated TOML text."""
    if not change.changed:
        return
    path = change.settings_path
    text = path.read_text(encoding="utf-8")
    updated = _updated_settings_text(
        text,
        SURFACE_IDS[change.surface_id],
        change.after,
    )
    path.write_text(updated, encoding="utf-8")


def surface_recommendations(root: Path) -> tuple[dict[str, str], ...]:
    """Recommend only reactivation supported by an existing retained carrier."""
    states = surface_states(root)
    recommendations: list[dict[str, str]] = []
    for surface_id, active in states.items():
        if active:
            continue
        carriers = _matching_carriers(root, surface_id)
        if carriers:
            recommendations.append(
                {
                    "surface": surface_id,
                    "reason": "inactive surface has retained carrier",
                    "evidence": carriers[0],
                }
            )
    return tuple(recommendations)


def _surface_table(root: Path) -> tuple[Path, dict[str, object]]:
    """Read the selected settings carrier and its optional surface table."""
    path = selected_settings_path(root)
    if not path.is_file():
        raise _settings_error(path, "DSET settings carrier does not exist")
    try:
        raw = load_toml(path)
    except (OSError, UnicodeError, TomlCodecError) as error:
        raise _settings_error(path, f"cannot read settings: {error}") from error
    table = raw.get("governance_surfaces", {})
    if not isinstance(table, dict):
        raise _settings_error(path, "governance_surfaces must be a TOML table")
    return path, table


def _surface_id(value: str) -> str:
    """Normalize and validate one operator-facing surface identity."""
    normalized = value.replace("_", "-")
    if normalized not in SURFACE_IDS:
        raise ValueError(
            "surface must be one of: " + ", ".join(SURFACE_IDS)
        )
    return normalized


def _updated_settings_text(text: str, key: str, active: bool) -> str:
    """Update one key and materialize explicit defaults for missing peers."""
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    table_start = _table_start(lines)
    rendered = "true" if active else "false"
    if table_start is None:
        separator = "" if not text or text.endswith(("\n", "\r")) else newline
        entries = [
            f"{name} = {rendered if name == key else 'false'}{newline}"
            for name in GOVERNANCE_SURFACE_KEYS
        ]
        return (
            text
            + separator
            + f"{newline}[governance_surfaces]{newline}"
            + "".join(entries)
        )

    table_end = _table_end(lines, table_start)
    found: set[str] = set()
    for index in range(table_start + 1, table_end):
        for name in GOVERNANCE_SURFACE_KEYS:
            pattern = re.compile(
                rf"^(\s*{re.escape(name)}\s*=\s*)(true|false)(\s*(?:#.*)?)(\r?\n)?$"
            )
            match = pattern.match(lines[index])
            if match is None:
                continue
            found.add(name)
            if name == key:
                ending = match.group(4) or ""
                lines[index] = (
                    f"{match.group(1)}{rendered}{match.group(3)}{ending}"
                )
            break
    missing = [
        f"{name} = {rendered if name == key else 'false'}{newline}"
        for name in GOVERNANCE_SURFACE_KEYS
        if name not in found
    ]
    lines[table_end:table_end] = missing
    return "".join(lines)


def _table_start(lines: list[str]) -> int | None:
    """Locate the optional surface table."""
    for index, line in enumerate(lines):
        if _TABLE_HEADER.match(line.rstrip("\r\n")):
            return index
    return None


def _table_end(lines: list[str], table_start: int) -> int:
    """Locate the first table after the surface table."""
    for index in range(table_start + 1, len(lines)):
        if _ANY_TABLE_HEADER.match(lines[index].rstrip("\r\n")):
            return index
    return len(lines)


def _matching_carriers(root: Path, surface_id: str) -> list[str]:
    """Return bounded retained carrier evidence for one inactive surface."""
    tokens = {
        "evergreen-specification": ("specification",),
        "test-plan": ("test-plan",),
        "evaluation-plan": ("eval-plan", "evaluation-plan"),
        "implementation-plan": ("implementation-plan",),
        "project-overview": ("overview", "project-health"),
        "architecture-view": ("architecture",),
    }[surface_id]
    matches: list[str] = []
    for path in sorted((root / ".dset").rglob("*")):
        if (
            not path.is_file()
            or ".dset_runtime" in path.parts
            or "000_dset_methodology" in path.parts
        ):
            continue
        lowered = path.name.lower()
        if any(token in lowered for token in tokens):
            matches.append(path.relative_to(root).as_posix())
            if len(matches) == 3:
                break
    return matches


def _settings_error(path: Path, message: str) -> DsetCommandError:
    """Build a stable configuration diagnostic."""
    return DsetCommandError("DSET-E173", path, message)
