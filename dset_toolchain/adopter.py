from __future__ import annotations

import shutil
from pathlib import Path

from .governance import materialize_governance
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
        write_traceability(destination)
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def _write_adopter_files(source_root: Path, root: Path) -> None:
    dset = root / "dset"
    package = dset / "specs" / "packages" / "sample"
    (dset / "changes" / "archive").mkdir(parents=True)
    package.mkdir(parents=True)
    (dset / "supportability").mkdir()
    shutil.copytree(source_root / "dset" / "schemas", dset / "schemas")
    shutil.copytree(source_root / "dset" / "templates", dset / "templates")
    shutil.copytree(source_root / "dset" / "history", dset / "history")
    (root / "skills").mkdir()
    shutil.copyfile(source_root / "skills" / "README.md", root / "skills" / "README.md")
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
        "verification": {"commands": ["{python} -m dset_toolchain check ."]},
        "canonical_command": "python -m dset_toolchain check .",
    }
    (dset / "dset.yaml").write_text(dump(manifest), encoding="utf-8")
    shutil.copyfile(
        source_root / "dset" / "templates" / "budget.yaml", dset / "budget.yaml"
    )
    shutil.copyfile(
        source_root / "dset" / "templates" / "intake.yaml", dset / "intake.yaml"
    )
    (dset / "provenance.yaml").write_text(
        dump({"schema_version": 1.0, "sources": []}), encoding="utf-8"
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
    (package / "package.yaml").write_text(dump(package_manifest), encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
