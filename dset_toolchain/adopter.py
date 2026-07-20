from __future__ import annotations

import shutil
from pathlib import Path

from .governance import materialize_governance
from .layout import RepositoryLayout, discover_layout
from .legacy_authority import write_legacy_authority_ledger
from .traceability import write_traceability
from .yaml_subset import dump


def create_adopter(source_root: Path, destination: Path) -> Path:
    source_root = source_root.resolve()
    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"adopter destination exists: {destination}")
    destination.mkdir(parents=True)
    try:
        _write_adopter_files(source_root, destination)
        materialize_governance(
            source_root,
            destination,
            "core-v1",
            install_wrappers=True,
        )
        write_legacy_authority_ledger(destination)
        _write_legacy_governance_readme(
            destination / "dset" / "governance" / "README.md"
        )
        write_traceability(destination)
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def _write_adopter_files(source_root: Path, root: Path) -> None:
    source_layout = discover_layout(source_root)
    dset = root / "dset"
    package = dset / "specs" / "packages" / "sample"
    (dset / "changes" / "archive").mkdir(parents=True)
    package.mkdir(parents=True)
    (dset / "supportability").mkdir()
    _copy_schemas(source_layout, dset / "schemas")
    _copy_templates(source_layout, dset / "templates")
    shutil.copytree(source_layout.history_root, dset / "history")
    (root / "skills").mkdir()
    shutil.copyfile(source_root / "skills" / "README.md", root / "skills" / "README.md")
    shutil.copyfile(
        source_root / "skills" / "host-distribution.md",
        root / "skills" / "host-distribution.md",
    )
    manifest = {
        "schema_version": 1.1,
        "project": {
            "key": "DSET",
            "id": "dset-temporary-adopter",
            "name": "DSET temporary adopter",
            "repository_slug": "dset-temporary-adopter",
            "repository_role": "adopter-fixture",
        },
        "supportability": {
            "status": "not-applicable",
            "reason": "ephemeral local validation fixture with no production runtime",
            "authority": "local-process",
            "runbook": "supportability/README.md",
        },
        "release": {
            "status": "not-applicable",
            "reason": "ephemeral fixture has no protected publication path",
        },
        "work_items": {"registry": "dset/intake.yaml"},
        "contracts": ["DSET-CONTRACT-001"],
        "stories": [],
        "outcomes": [],
        "structure": {
            "mode": "single-package",
            "accepted_truth_root": "specs/packages",
            "active_changes_root": "changes",
            "archive_root": "changes/archive",
            "global_truth_root": None,
        },
        "packages": [
            {"id": "sample", "path": "specs/packages/sample", "status": "active"}
        ],
        "profiles": {
            "runtime_risk": "non-production",
            "durability_topology": "files",
            "enforcement": "none",
            "artifact": None,
            "repository_governance": "core-v1",
            "delegation_budget": "medium",
        },
        "change_contract": {
            "change_id_format": "kebab-case",
            "pull_request_required_before_archive": True,
            "archive_requires_fresh_verification": True,
            "keep_pull_request_draft_until_archive_ready": True,
        },
        "commit_provenance": {"start_commit": "manifest-addition"},
        "verification": {"commands": ["{python} -m dset_toolchain check ."]},
        "canonical_command": "python -m dset_toolchain check .",
    }
    manifest_path = dset / "dset.yaml"
    manifest_path.write_text(dump(manifest, manifest_path), encoding="utf-8")
    shutil.copyfile(source_layout.find_template("dset.toml"), root / "dset.toml")
    shutil.copyfile(
        source_layout.find_template("artifact-types.yaml"),
        dset / "artifact-types.yaml",
    )
    shutil.copyfile(source_layout.find_template("budget.yaml"), dset / "budget.yaml")
    _write_legacy_intake(dset / "intake.yaml")
    provenance_path = dset / "provenance.yaml"
    provenance_path.write_text(
        dump({"schema_version": 1.0, "sources": []}, provenance_path), encoding="utf-8"
    )
    _write(
        root / "README.md",
        """# DSET temporary adopter

## Purpose

Exercise the public DSET bootstrap and governance contracts.

## Boundaries

This fixture is ephemeral and has no production authority.

## Repository areas

- [DSET project control](dset/README.md)
- [Workflow skills](skills/README.md)
""",
    )
    _write(
        dset / "README.md",
        """# DSET project control

## Purpose

Own accepted sample truth and repository-local governance.

## Boundaries

The temporary adopter never becomes framework truth.

## Start here

- [Governance](governance/README.md)
- [Project intake](intake.yaml)
- [Delegation budget](budget.yaml)
- [Accepted sample package](specs/packages/sample/README.md)
- [Active changes](changes/README.md)
- [Templates](templates/README.md)
- [Schemas](schemas/README.md)
""",
    )
    _write(
        dset / "changes" / "README.md",
        "# Active changes\n\nNo active changes in the temporary adopter.\n",
    )
    _write(
        dset / "changes" / "archive" / "README.md",
        "# Change archive\n\nNo archived changes in the temporary adopter.\n",
    )
    _write(
        dset / "supportability" / "README.md",
        "# Supportability\n\nNot applicable: this adopter is an ephemeral fixture.\n",
    )
    _write(
        package / "README.md",
        """# Sample package

## Purpose

Provide accepted truth for the bootstrap fixture.

## Boundaries

No production behavior or external effects.

## Start here

- [Domain](domain.md)
- [Specification](spec.md)
- [Contracts](contracts.md)
- [User Stories](stories.md)
- [Outcomes](outcomes.md)
- [Test plan](test-plan.md)
- [Eval plan](eval-plan.md)
""",
    )
    _write(package / "domain.md", "# Sample domain\n\nOne stable fixture entity.\n")
    _write(
        package / "spec.md",
        """# Sample specification

## DSET-REQUIREMENT-001 — Validation is read-only

The temporary adopter must pass DSET validation without external effects.
""",
    )
    _write(
        package / "contracts.md",
        "# Sample contracts\n\n"
        "## DSET-CONTRACT-001 — Validator invocation boundary\n\n"
        "The canonical validation command is the authoritative fixture boundary.\n",
    )
    _write(
        package / "stories.md",
        "# Sample stories\n\n"
        "Not applicable: this infrastructure fixture has no meaningful actor story.\n",
    )
    _write(
        package / "outcomes.md",
        "# Sample outcomes\n\n"
        "Not applicable: this fixture owns validation output, not a measurable "
        "state change.\n",
    )
    _write(
        package / "test-plan.md",
        "# Sample deterministic test plan\n\n- **DSET-TEST-001:** Run `dset check`.\n",
    )
    _write(
        package / "eval-plan.md",
        "# Sample eval plan\n\nNot applicable: the fixture has one exact outcome.\n",
    )
    package_manifest = {
        "schema_version": 1.0,
        "id": "sample",
        "status": "active",
        "requirements": ["DSET-REQUIREMENT-001"],
        "tests": ["DSET-TEST-001"],
        "evals": [],
        "contracts": ["DSET-CONTRACT-001"],
        "stories": [],
        "outcomes": [],
        "artifacts": {
            "domain": "domain.md",
            "spec": "spec.md",
            "contracts": "contracts.md",
            "stories": "stories.md",
            "outcomes": "outcomes.md",
            "test_plan": "test-plan.md",
            "eval_plan": "eval-plan.md",
        },
    }
    package_path = package / "package.yaml"
    package_path.write_text(dump(package_manifest, package_path), encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _copy_schemas(source: RepositoryLayout, destination: Path) -> None:
    destination.mkdir()
    for path in source.schema_paths():
        shutil.copyfile(path, destination / path.name)
    _write(
        destination / "README.md",
        "# DSET schemas\n\nAggregated for the temporary schema 1.1 adopter.\n",
    )


def _copy_templates(source: RepositoryLayout, destination: Path) -> None:
    destination.mkdir()
    copied: dict[Path, Path] = {}
    for template_root in source.template_roots:
        if not template_root.is_dir():
            continue
        for path in sorted(template_root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(template_root)
            if relative == Path("README.md"):
                continue
            previous = copied.get(relative)
            if previous is not None:
                raise ValueError(
                    "template is not unique: "
                    f"{relative.as_posix()} ({previous.as_posix()}, {path.as_posix()})"
                )
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            copied[relative] = path
    _write(
        destination / "README.md",
        "# DSET templates\n\nAggregated for the temporary schema 1.1 adopter.\n",
    )
    _write_legacy_governance_readme(
        destination / "governance" / "core-v1" / "README.md"
    )


def _write_legacy_intake(destination: Path) -> None:
    scopes = (
        ("meta", "Project metadata and accepted truth", "dset"),
        ("gov", "Governance and lifecycle policy", "dset/governance"),
        ("tool", "Executable toolchain", "dset_toolchain"),
        ("skill", "User-facing skills", "skills"),
        ("ops", "Operations and supportability", "dset/supportability"),
    )
    destination.write_text(
        dump(
            {
                "schema_version": 1.0,
                "scope_mode": "multi-scope",
                "scopes": [
                    {
                        "id": identifier,
                        "id_segment": identifier.upper(),
                        "kind": "layer",
                        "name": name,
                        "path": path,
                    }
                    for identifier, name, path in scopes
                ],
                "items": [],
            },
            destination,
        ),
        encoding="utf-8",
    )


def _write_legacy_governance_readme(destination: Path) -> None:
    _write(
        destination,
        """# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their
selected rules.

## Boundaries

This hub owns navigation only. `governance.yaml` owns machine-readable resolution
metadata, and each linked document owns its registered normative rule IDs. Source
templates are provenance after materialization, not live rule authorities.

## Start here

- [Architecture and bootstrap](architecture.md)
- [Build rules](build-rules.md)
- [Domain and specification authoring](domain-spec-authoring.md)
- [Deterministic test planning](test-planning.md)
- [Qualitative and probabilistic eval planning](eval-planning.md)
- [Diagnosis](diagnosis.md)
- [Prototyping](prototyping.md)
- [Supportability](supportability.md)
- [Artifact maintenance](artifact-maintenance.md)
- [Lifecycle orchestration](lifecycle-orchestration.md)
- [Skill-run records](skill-runs.md)
- [Delegation budgets](delegation-budget.md)
- [Release transaction](release.md)
- [Problem, opportunity, and question intake](work-items.md)

Use `dset rules check` to validate ownership and `dset rules resolve <workflow-id>`
to obtain the ordered rule set. Use `dset rules refresh` only after an intentional
local edit, and review `dset rules diff --source <framework-root>` before adopting
later framework changes.
""",
    )
