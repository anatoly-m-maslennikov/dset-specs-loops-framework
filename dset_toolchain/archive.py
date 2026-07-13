from __future__ import annotations

from datetime import date
from pathlib import Path

from .validation import validate_change
from .yaml_subset import dump, load


def archive_plan(root: Path, change_id: str, archive_date: date) -> tuple[Path, Path]:
    source = root / "dset" / "changes" / change_id
    destination = (
        root
        / "dset"
        / "changes"
        / "archive"
        / f"{archive_date.isoformat()}-{change_id}"
    )
    if not source.is_dir():
        raise FileNotFoundError(f"active change does not exist: {source}")
    if destination.exists():
        raise FileExistsError(f"archive destination exists: {destination}")
    data = load(source / "change.yaml")
    if data.get("status") != "archive-ready":
        raise ValueError("change status must be archive-ready")
    pr = data.get("pull_request", {})
    if not isinstance(pr.get("number"), int):
        raise ValueError("archive requires a repository-qualified PR")
    diagnostics = validate_change(root, source, archived=False)
    if diagnostics:
        raise ValueError(diagnostics[0].render(root))
    verification = (source / "verification.md").read_text(encoding="utf-8")
    if "Accepted-truth reconciliation: Pass" not in verification:
        raise ValueError("verification must record accepted-truth reconciliation")
    return source, destination


def execute_archive(root: Path, change_id: str, archive_date: date) -> Path:
    source, destination = archive_plan(root, change_id, archive_date)
    manifest_path = source / "change.yaml"
    original = manifest_path.read_text(encoding="utf-8")
    data = load(manifest_path)
    data["status"] = "archived"
    data["archive"] = {
        "date": archive_date.isoformat(),
        "path": destination.relative_to(root).as_posix(),
    }
    temporary = manifest_path.with_suffix(".yaml.tmp")
    temporary.write_text(dump(data), encoding="utf-8")
    temporary.replace(manifest_path)
    try:
        source.replace(destination)
    except Exception:
        manifest_path.write_text(original, encoding="utf-8")
        raise
    return destination
