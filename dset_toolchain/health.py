from __future__ import annotations

import hashlib
import os
import re
import subprocess
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .compilation import active_authority_ids
from .layout import discover_layout
from .semantic_atoms import collect_semantic_atoms, effective_priority
from .settings import load_project_settings
from .yaml_subset import YamlSubsetError, load, loads

ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-[0-9]{3,}\b")
DECISION_KINDS = frozenset(
    {
        "DECISION",
        "REQUIREMENT",
        "CONSTRAINT",
        "CONTRACT",
        "STORY",
        "OUTCOME",
        "SCENARIO",
        "INVARIANT",
    }
)
QA_KINDS = frozenset({"TEST", "EVAL", "EVALUATION"})
IGNORED_PARTS = frozenset(
    {
        ".git",
        ".cache",
        ".dset",
        ".venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "dist",
    }
)


@dataclass(frozen=True)
class Coverage:
    name: str
    numerator: int
    denominator: int
    excluded: int
    not_applicable: int
    unknown: int
    stale: int
    gaps: tuple[str, ...]


def build_health_model(root: Path) -> dict[str, Any]:
    root = root.resolve()
    layout = discover_layout(root)
    settings, issues = load_project_settings(root)
    if issues:
        raise ValueError(issues[0])
    artifacts = _classified_artifacts(root)
    atoms, atom_diagnostics = collect_semantic_atoms(root)
    if atom_diagnostics:
        raise ValueError(atom_diagnostics[0].message)
    lifecycle = _lifecycle_events(root)
    intake = _intake_items(root, layout.intake_path, lifecycle)
    authorities = active_authority_ids(root)
    modern_authorities = {
        atom.semantic_id
        for atom in atoms.values()
        if atom.semantic_type == "decision"
        and atom.emission_status == "accepted"
        and atom.semantic_id in authorities
    }
    qa_ids = _qa_ids(root, atoms)
    projections = _evergreen_text(root)
    commit_edges = _commit_implements(root)
    proof_text = _proof_text(root)
    qa_plan_text = _qa_plan_text(root)

    compiled = _coverage_compiled(authorities, projections)
    implemented = _coverage_implemented(authorities, modern_authorities, commit_edges)
    qa_coverage = _coverage_qa(authorities, qa_plan_text)
    proof_coverage = _coverage_proof(qa_ids, proof_text)

    type_counts = Counter(item["artifact_type"] for item in artifacts)
    subtype_counts = Counter(
        str(item["artifact_subtype"])
        for item in artifacts
        if item["artifact_subtype"] is not None
    )
    layer_counts = Counter(str(item["layer"]) for item in artifacts)
    role_counts = Counter(_role(str(item["artifact_type"])) for item in artifacts)
    priority_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    atom_rows: list[dict[str, Any]] = []
    for atom in atoms.values():
        priority, source = effective_priority(root, atom)
        priority_counts[priority] += 1
        status_counts[
            _current_status(atom.semantic_id, atom.emission_status, lifecycle)
        ] += 1
        atom_rows.append(
            {
                "id": atom.semantic_id,
                "type": atom.semantic_type,
                "subtype": atom.subtype or "none",
                "status": _current_status(
                    atom.semantic_id, atom.emission_status, lifecycle
                ),
                "priority": priority,
                "priority_source": source,
                "path": atom.path,
            }
        )
    priority_counts[settings.default_priority] += max(0, len(artifacts) - len(atoms))
    status_counts.update(str(item["effective_status"]) for item in intake)
    status_counts.update(_change_statuses(root))
    work_areas = _work_area_counts(root, artifacts)
    packages = _package_counts(root, artifacts)
    unresolved = [item for item in intake if item["effective_status"] == "open"]
    resolved_conflicts = [
        event
        for event in lifecycle
        if event.get("event") == "resolved"
        and "CONFLICT" in str(event.get("atom_id", "")).split("-")
    ]
    return {
        "schema_version": "1.0",
        "source_digest": _source_digest(root),
        "artifact_counts": {
            "total": len(artifacts),
            "by_role": dict(sorted(role_counts.items())),
            "by_type": dict(sorted(type_counts.items())),
            "by_subtype": dict(sorted(subtype_counts.items())),
            "by_layer": dict(sorted(layer_counts.items())),
            "by_priority": dict(sorted(priority_counts.items())),
            "by_status": dict(sorted(status_counts.items())),
        },
        "atoms": sorted(atom_rows, key=lambda item: str(item["id"])),
        "unresolved": unresolved,
        "resolved_conflicts": resolved_conflicts,
        "coverage": [compiled, implemented, qa_coverage, proof_coverage],
        "packages": packages,
        "work_areas": work_areas,
        "canonical_returns": {
            "manifest": layout.manifest_path.relative_to(root).as_posix(),
            "governance": layout.governance_path.relative_to(root).as_posix(),
            "intake": layout.intake_path.relative_to(root).as_posix(),
            "traceability": layout.traceability_path.relative_to(root).as_posix(),
        },
    }


def render_health(root: Path) -> str:
    root = root.resolve()
    model = build_health_model(root)
    layout = discover_layout(root)
    output_dir = health_path(root).parent
    project = load(layout.manifest_path)["project"]
    project_key = str(project["key"])
    lines = [
        "---",
        "artifact_type: derived_view",
        "artifact_subtype: health_dashboard",
        f"artifact_id: {project_key}-DERIVED-VIEW-001",
        "priority: low",
        "llm_session_ids: []",
        "---",
        "",
        f"# {project_key} project health",
        "",
        "> [!NOTE]",
        "> This generated view is not authority. Follow each link to its canonical",
        "> owner and refresh explicitly after source changes.",
        "",
        f"- **Source digest:** `{model['source_digest']}`",
        "- **Renderer:** `dset health` schema 1.0",
        "",
        "## Coverage",
        "",
        "| Closure | Numerator | Denominator | Excluded | N/A | Unknown | Stale |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for coverage in model["coverage"]:
        lines.append(
            f"| {coverage.name} | {coverage.numerator} | {coverage.denominator} | "
            f"{coverage.excluded} | {coverage.not_applicable} | "
            f"{coverage.unknown} | {coverage.stale} |"
        )
    lines.extend(["", "### Coverage gaps", ""])
    for coverage in model["coverage"]:
        if not coverage.gaps:
            lines.append(f"- **{coverage.name}:** none")
            continue
        links = ", ".join(f"`{identifier}`" for identifier in coverage.gaps)
        lines.append(f"- **{coverage.name}:** {links}")

    counts = model["artifact_counts"]
    lines.extend(
        [
            "",
            "## Artifact inventory",
            "",
            f"- **Governed artifacts:** {counts['total']}",
            f"- **By role:** {_counter_text(counts['by_role'])}",
            f"- **By type:** {_counter_text(counts['by_type'])}",
            f"- **By subtype:** {_counter_text(counts['by_subtype'])}",
            f"- **By layer:** {_counter_text(counts['by_layer'])}",
            f"- **By effective priority:** {_counter_text(counts['by_priority'])}",
            f"- **By status:** {_counter_text(counts['by_status'])}",
            "",
            "## Unresolved work",
            "",
        ]
    )
    unresolved = model["unresolved"]
    if unresolved:
        for item in unresolved:
            link = _link(root, output_dir, str(item["path"]))
            subtype = f"/{item['subtype']}" if item["subtype"] else ""
            lines.append(
                f"- [`{item['id']}`]({link}) — {item['type']}{subtype}: {item['title']}"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Drill-downs", ""])
    lines.append(f"- **Packages:** {_counter_text(model['packages'])}")
    lines.append(f"- **Work Areas:** {_counter_text(model['work_areas'])}")
    lines.extend(["", "## Canonical return paths", ""])
    for name, path in model["canonical_returns"].items():
        link = _link(root, output_dir, path)
        lines.append(f"- [{name}]({link})")
    lines.extend(
        [
            "",
            "## Boundaries",
            "",
            "Counts are descriptive, not targets. Missing links remain gaps; the",
            "renderer never creates Decisions, implementation, Tests, Evaluations, or",
            "evidence to improve a ratio. `unknown`, `not applicable`, exclusions, and",
            "staleness remain separate dispositions.",
            "",
        ]
    )
    return "\n".join(lines)


def health_is_fresh(root: Path) -> bool:
    path = health_path(root)
    return path.is_file() and path.read_text(encoding="utf-8") == render_health(root)


def write_health(root: Path) -> Path:
    path = health_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".md.tmp")
    temporary.write_text(render_health(root), encoding="utf-8")
    temporary.replace(path)
    return path


def health_path(root: Path) -> Path:
    layout = discover_layout(root)
    project = load(layout.manifest_path)["project"]
    key = str(project["key"])
    generated = (
        layout.traceability_path.parent
        if layout.layered
        else layout.dset_root / "generated"
    )
    return generated / f"{key}-DERIVED-VIEW-001-project-health.md"


def _classified_artifacts(root: Path) -> list[dict[str, Any]]:
    layout = discover_layout(root)
    registry = load(layout.artifact_type_registry_path)
    rules = registry.get("path_rules", []) if isinstance(registry, dict) else []
    artifacts: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _relative_ignored(relative) or not _in_project_scope(root, relative):
            continue
        if "generated" in relative.parts:
            continue
        direct = _frontmatter(path)
        artifact_type = direct.get("artifact_type") if direct else None
        artifact_subtype = direct.get("artifact_subtype") if direct else None
        if artifact_type is None:
            matches = [
                item
                for item in rules
                if isinstance(item, dict)
                and _matches(relative.as_posix(), str(item.get("pattern", "")))
            ]
            if len(matches) == 1:
                artifact_type = matches[0].get("artifact_type")
                artifact_subtype = matches[0].get("artifact_subtype")
        if artifact_type is None:
            artifact_type, artifact_subtype = _implementation_class(relative)
        if artifact_type is None:
            continue
        artifacts.append(
            {
                "path": relative.as_posix(),
                "artifact_type": str(artifact_type),
                "artifact_subtype": (
                    str(artifact_subtype) if artifact_subtype is not None else None
                ),
                "layer": _layer(relative),
            }
        )
    artifacts.append(
        {
            "path": health_path(root).relative_to(root).as_posix(),
            "artifact_type": "derived_view",
            "artifact_subtype": "health_dashboard",
            "layer": "gov",
        }
    )
    return artifacts


def _qa_ids(root: Path, atoms: dict[str, Any]) -> set[str]:
    identifiers = {
        atom.semantic_id for atom in atoms.values() if atom.semantic_type == "qa"
    }
    for path in root.rglob("package.yaml"):
        if not _canonical_package_manifest(root, path):
            continue
        try:
            data = load(path)
        except (OSError, UnicodeError, YamlSubsetError):
            continue
        if not isinstance(data, dict):
            continue
        for field in ("tests", "evals"):
            values = data.get(field, [])
            if isinstance(values, list):
                identifiers.update(
                    str(item) for item in values if isinstance(item, str)
                )
    return identifiers


def _coverage_compiled(authorities: set[str], text: str) -> Coverage:
    covered = {identifier for identifier in authorities if identifier in text}
    gaps = tuple(sorted(authorities - covered))
    return Coverage(
        "Decision authority compiled into evergreen truth",
        len(covered),
        len(authorities),
        0,
        0,
        len(gaps),
        0,
        gaps,
    )


def _coverage_implemented(
    authorities: set[str], modern_authorities: set[str], commit_edges: set[str]
) -> Coverage:
    covered = modern_authorities & commit_edges
    gaps = tuple(sorted(modern_authorities - covered))
    excluded = authorities - modern_authorities
    return Coverage(
        "Decision authority linked from implementation commits",
        len(covered),
        len(modern_authorities),
        len(excluded),
        0,
        len(gaps),
        0,
        gaps,
    )


def _coverage_qa(authorities: set[str], plan_text: str) -> Coverage:
    covered: set[str] = set()
    not_applicable: set[str] = set()
    for line in plan_text.splitlines():
        ids = set(ID_RE.findall(line))
        owners = ids & authorities
        if not owners:
            continue
        if "not applicable" in line.lower():
            not_applicable.update(owners)
        elif any(_kind(identifier) in QA_KINDS for identifier in ids):
            covered.update(owners)
    gaps = tuple(sorted(authorities - covered - not_applicable))
    denominator = len(authorities) - len(not_applicable)
    return Coverage(
        "Applicable authority connected to Test or Evaluation",
        len(covered),
        denominator,
        0,
        len(not_applicable),
        len(gaps),
        0,
        gaps,
    )


def _coverage_proof(qa_ids: set[str], proof_text: str) -> Coverage:
    covered: set[str] = set()
    stale: set[str] = set()
    for identifier in qa_ids:
        positions = [line for line in proof_text.splitlines() if identifier in line]
        if any(
            "stale" in line.lower() or "historical" in line.lower()
            for line in positions
        ):
            stale.add(identifier)
        elif positions:
            covered.add(identifier)
    gaps = tuple(sorted(qa_ids - covered - stale))
    return Coverage(
        "QA definitions connected to current evidence",
        len(covered),
        len(qa_ids),
        0,
        0,
        len(gaps),
        len(stale),
        gaps,
    )


def _evergreen_text(root: Path) -> str:
    paths = [
        path
        for path in root.rglob("*.md")
        if not _path_ignored(root, path)
        and _in_project_scope(root, path.relative_to(root))
        and ("specs" in path.parts or "governance" in path.parts)
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(paths))


def _qa_plan_text(root: Path) -> str:
    paths = [
        path
        for path in root.rglob("*.md")
        if not _path_ignored(root, path)
        and _in_project_scope(root, path.relative_to(root))
        and path.name in {"test-plan.md", "eval-plan.md"}
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(paths))


def _proof_text(root: Path) -> str:
    paths = [
        path
        for path in root.rglob("*.md")
        if not _path_ignored(root, path)
        and _in_project_scope(root, path.relative_to(root))
        and "proofs" in path.parts
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in sorted(paths))


def _commit_implements(root: Path) -> set[str]:
    try:
        completed = subprocess.run(
            ["git", "log", "--format=%B%x00"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    identifiers: set[str] = set()
    for line in completed.stdout.splitlines():
        if line.startswith("Implements:"):
            identifiers.update(ID_RE.findall(line))
    return identifiers


def _lifecycle_events(root: Path) -> list[dict[str, Any]]:
    path = discover_layout(root).governance_root / "lifecycle.yaml"
    if not path.is_file():
        return []
    data = load(path)
    events = data.get("events", []) if isinstance(data, dict) else []
    return [dict(item) for item in events if isinstance(item, dict)]


def _intake_items(
    root: Path, path: Path, lifecycle: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    data = load(path)
    raw = data.get("items", []) if isinstance(data, dict) else []
    latest = {str(item.get("atom_id")): str(item.get("event")) for item in lifecycle}
    items: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("id"))
        semantic_type, subtype = _legacy_intake_type(identifier, str(item.get("type")))
        status = str(item.get("status"))
        if latest.get(identifier) in {"answered", "resolved", "rejected", "retired"}:
            status = "resolved"
        items.append(
            {
                "id": identifier,
                "type": semantic_type,
                "subtype": subtype,
                "title": str(item.get("title", "untitled")),
                "effective_status": status,
                "path": path.relative_to(root).as_posix(),
            }
        )
    return items


def _current_status(identifier: str, emitted: str, events: list[dict[str, Any]]) -> str:
    status = emitted
    for event in events:
        if event.get("atom_id") == identifier:
            status = str(event.get("event"))
    return status


def _work_area_counts(root: Path, artifacts: list[dict[str, Any]]) -> dict[str, int]:
    manifest = load(discover_layout(root).manifest_path)
    raw = manifest.get("work_areas", []) if isinstance(manifest, dict) else []
    counts: dict[str, int] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("id"))
        area_path = str(item.get("path", ""))
        counts[identifier] = sum(
            1 for artifact in artifacts if str(artifact["path"]).startswith(area_path)
        )
    return counts


def _package_counts(root: Path, artifacts: list[dict[str, Any]]) -> dict[str, int]:
    manifest = load(discover_layout(root).manifest_path)
    raw = manifest.get("packages", []) if isinstance(manifest, dict) else []
    counts: dict[str, int] = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("id"))
        counts[identifier] = sum(
            1
            for artifact in artifacts
            if f"/packages/{identifier}/" in str(artifact["path"])
        )
    return counts


def _change_statuses(root: Path) -> list[str]:
    statuses: list[str] = []
    for path in root.rglob("change.yaml"):
        relative = path.relative_to(root)
        if (
            _path_ignored(root, path)
            or not _in_project_scope(root, relative)
            or "templates" in relative.parts
            or "fixtures" in relative.parts
        ):
            continue
        try:
            data = load(path)
        except (OSError, UnicodeError, YamlSubsetError):
            continue
        if isinstance(data, dict) and isinstance(data.get("status"), str):
            statuses.append(str(data["status"]))
    return statuses


def _canonical_package_manifest(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return (
        not _path_ignored(root, path)
        and _in_project_scope(root, relative)
        and "specs" in relative.parts
        and "packages" in relative.parts
        and "templates" not in relative.parts
        and "fixtures" not in relative.parts
    )


def _source_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if _relative_ignored(relative) or not _in_project_scope(root, relative):
            continue
        if "generated" in relative.parts or relative.parts[0] == ".dset":
            continue
        digest.update(relative.as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _frontmatter(path: Path) -> dict[str, Any] | None:
    if path.suffix.lower() != ".md":
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        end = lines.index("---", 1)
        data = loads("\n".join(lines[1:end])) if lines[0] == "---" else None
    except (OSError, UnicodeError, ValueError, YamlSubsetError, IndexError):
        return None
    return data if isinstance(data, dict) else None


def _implementation_class(relative: Path) -> tuple[str | None, str | None]:
    if (
        relative.parts
        and relative.parts[0] == "dset_toolchain"
        and relative.suffix == ".py"
    ):
        return "implementation", "source_code"
    if relative.parts and relative.parts[0] == "tests" and relative.suffix == ".py":
        return "implementation", "test_implementation"
    if relative.parts and relative.parts[0] == "skills":
        return "implementation", "documentation"
    return None, None


def _matches(relative: str, pattern: str) -> bool:
    path = PurePosixPath(relative)
    return path.match(pattern) or (
        pattern.startswith("**/") and path.match(pattern.removeprefix("**/"))
    )


def _layer(relative: Path) -> str:
    parts = relative.parts
    if len(parts) >= 3 and parts[:2] == ("dset", "scopes"):
        return parts[2]
    if parts and parts[0] in {"dset_toolchain", "tests"}:
        return "tool"
    if parts and parts[0] == "skills":
        return "skill"
    return "repository"


def _role(artifact_type: str) -> str:
    if artifact_type == "atomic_record":
        return "atomic"
    if artifact_type in {"specification", "plan", "procedure"}:
        return "evergreen"
    if artifact_type == "implementation":
        return "implementation"
    if artifact_type in {"evidence_record", "change"}:
        return "transactional"
    return "derived_or_navigation"


def _kind(identifier: str) -> str:
    for part in identifier.split("-"):
        if part in DECISION_KINDS or part in QA_KINDS:
            return part
    return "UNKNOWN"


def _legacy_intake_type(identifier: str, legacy_type: str) -> tuple[str, str | None]:
    if "OPPORTUNITY" in identifier.split("-") or legacy_type == "opportunity":
        return "question", "opportunity"
    if "CONFLICT" in identifier.split("-"):
        return "question", "conflict"
    return legacy_type, None


def _counter_text(value: dict[str, int]) -> str:
    if not value:
        return "none"
    return ", ".join(f"{key}={count}" for key, count in sorted(value.items()))


def _link(root: Path, from_dir: Path, target: str) -> str:
    return Path(os.path.relpath(root / target, from_dir)).as_posix()


def _path_ignored(root: Path, path: Path) -> bool:
    return _relative_ignored(path.relative_to(root))


def _relative_ignored(relative: Path) -> bool:
    return any(
        part in IGNORED_PARTS or (part.startswith(".") and part != ".github")
        for part in relative.parts
    )


def _in_project_scope(root: Path, relative: Path) -> bool:
    """Keep derived health inside declared project ownership boundaries."""
    if len(relative.parts) == 1:
        return True
    layout = discover_layout(root)
    if relative.is_relative_to(layout.dset_root.relative_to(root)):
        return True
    manifest = load(layout.manifest_path)
    work_areas = manifest.get("work_areas", []) if isinstance(manifest, dict) else []
    for item in work_areas:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        area = Path(str(item["path"]))
        if area.parts and relative.is_relative_to(area):
            return True
    return False
