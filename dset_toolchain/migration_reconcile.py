"""One-shot reconciliation for a proven DSET authority-format migration.

This module is executed in a fresh interpreter after primary TOML writes land
inside the guarded migration transaction.  Source validation and digest-bound
readiness evidence happen before this step, so rebasing format-sensitive seals
cannot legitimize unrelated source drift.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

from .compilation import compilation_path, write_compilation
from .health import health_path, write_health
from .identity import find_unique_name
from .layout import discover_layout
from .traceability import write_traceability
from .yaml_subset import dump, load


def reconcile_migrated_tree(root: Path) -> tuple[Path, ...]:
    """Rebase format-sensitive seals and refresh existing derived views."""

    root = root.resolve()
    changed: list[Path] = []
    layout = discover_layout(root)
    registry = layout.governance_path
    if registry.is_file():
        _rebase_governance_sources(root, registry)
        changed.append(registry)

    compiled = compilation_path(root)
    if compiled.is_file():
        changed.append(write_compilation(root))

    trace = layout.traceability_path
    if trace.is_file():
        changed.append(write_traceability(root))

    dashboard = health_path(root)
    if dashboard.is_file():
        changed.append(write_health(root))
    return tuple(changed)


def _rebase_governance_sources(root: Path, registry_path: Path) -> None:
    """Handle governance sources using the declared repository contract."""
    data = load(registry_path)
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list):
        raise ValueError("governance registry requires rules")
    for rule in rules:
        if not isinstance(rule, dict) or rule.get("customization") != "unmodified":
            continue
        document = rule.get("document")
        raw_path = rule.get("path")
        source = rule.get("source")
        if not isinstance(source, dict):
            raise ValueError("unmodified governance rule requires a source")
        if isinstance(document, str):
            local = find_unique_name(root, document)
        elif isinstance(raw_path, str):
            local = (root / raw_path).resolve()
        else:
            raise ValueError("unmodified governance rule requires a document")
        if not local.is_file():
            raise ValueError(f"governance rule is missing: {document or raw_path}")
        source["sha256"] = hashlib.sha256(local.read_bytes()).hexdigest()

    wrappers = data.get("wrappers")
    if not isinstance(wrappers, list):
        raise ValueError("governance registry requires wrappers")
    for wrapper in wrappers:
        if not isinstance(wrapper, dict):
            raise ValueError("governance wrapper must be a mapping")
        skill = wrapper.get("skill")
        raw_path = wrapper.get("path")
        if isinstance(skill, str):
            local = (root / "skills" / skill / "SKILL.md").resolve()
        elif isinstance(raw_path, str):
            local = (root / raw_path).resolve()
        else:
            raise ValueError("governance wrapper requires a skill identity")
        if not local.is_file():
            raise ValueError(f"governance wrapper is missing: {skill or raw_path}")
        wrapper["sha256"] = hashlib.sha256(local.read_bytes()).hexdigest()
    _atomic_structured_write(registry_path, data)


def _atomic_structured_write(path: Path, data: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(dump(data, path), encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface and return its exit status."""
    values = sys.argv[1:] if argv is None else argv
    root = Path(values[0] if values else ".")
    reconcile_migrated_tree(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
