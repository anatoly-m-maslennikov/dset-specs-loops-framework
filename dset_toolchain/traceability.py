from __future__ import annotations

from pathlib import Path
from typing import Any

from .yaml_subset import dump, load


def build_traceability(root: Path) -> dict[str, Any]:
    root = root.resolve()
    history = load(root / "dset" / "history" / "pull-requests.yaml")
    changes: list[dict[str, Any]] = []
    change_root = root / "dset" / "changes"
    candidates = [
        path
        for path in change_root.iterdir()
        if path.is_dir() and path.name != "archive"
    ]
    archive = change_root / "archive"
    if archive.is_dir():
        candidates.extend(path for path in archive.iterdir() if path.is_dir())
    for path in sorted(candidates, key=lambda item: item.name):
        manifest = path / "change.yaml"
        if not manifest.is_file():
            continue
        data = load(manifest)
        evidence_root = path / "proofs"
        evidence = []
        if evidence_root.is_dir():
            evidence = [
                item.relative_to(root).as_posix()
                for item in sorted(evidence_root.rglob("*"))
                if item.is_file() and item.name != "README.md"
            ]
        pr = data.get("pull_request", {})
        changes.append(
            {
                "id": data["id"],
                "status": data["status"],
                "path": path.relative_to(root).as_posix(),
                "packages": sorted(data.get("packages", [])),
                "requirements": sorted(data.get("requirements", [])),
                "tests": sorted(data.get("tests", [])),
                "evals": sorted(data.get("evals", [])),
                "intake": sorted(data.get("intake", [])),
                "decisions": sorted(data.get("decisions", data.get("adrs", []))),
                "contracts": sorted(data.get("contracts", [])),
                "stories": sorted(data.get("stories", [])),
                "outcomes": sorted(data.get("outcomes", [])),
                "pull_request": pr.get("url", "pending"),
                "evidence": evidence,
            }
        )
    changes.sort(key=lambda item: item["id"])
    return {
        "schema_version": 1.1,
        "repository": history["repository"],
        "changes": changes,
    }


def rendered_traceability(root: Path) -> str:
    return dump(build_traceability(root))


def trace_is_fresh(root: Path) -> bool:
    path = root / "dset" / "traceability.yaml"
    return path.is_file() and path.read_text(encoding="utf-8") == rendered_traceability(
        root
    )


def write_traceability(root: Path) -> Path:
    path = root / "dset" / "traceability.yaml"
    content = rendered_traceability(root)
    temporary = path.with_suffix(".yaml.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return path
