from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from . import __version__
from .archive import archive_plan, execute_archive
from .artifact_emission import assess_artifact_candidate
from .bootstrap import initialize_project, parse_work_area
from .compilation import (
    compilation_is_fresh,
    compilation_path,
    rendered_compilation,
    write_compilation,
)
from .conflicts import (
    conflict_result_is_fresh,
    emit_conflict_atom,
    resolve_conflict,
    write_conflict_result,
)
from .dependencies import dependency_summary
from .diagnostics import Diagnostic
from .enforcement_profiles import (
    inspect_target,
    resolve_profile_path,
    validate_profile_file,
)
from .errors import DsetCommandError
from .external_review import (
    create_review_packet,
    reconcile_review,
    validate_review_report,
    write_reconciliation,
)
from .governance import (
    diff_governance,
    find_repository,
    materialize_governance,
    refresh_customization,
    resolve_workflow,
    validate_governance,
)
from .health import health_is_fresh, health_path, render_health, write_health
from .layout import discover_layout
from .methodology_sync import methodology_drift, sync_methodology
from .project_data import project_section
from .release import check_release, plan_release, prepare_release
from .runtime_bridge import (
    advance_runtime_closure,
    checkpoint_runtime,
    finish_runtime,
    handoff_runtime,
    read_runtime,
    start_child_runtime,
    start_runtime,
)
from .scaffold import create_change
from .self_host import run_self_host
from .semantic_atoms import append_lifecycle_event, archive_atom, seal_atom
from .skill_catalog import PUBLIC_SKILL_WORKFLOWS
from .skill_distribution import main as skill_distribution_main
from .temp_paths import temporary_directory
from .toml_migration import (
    MigrationPlan,
    apply_toml_migration,
    plan_toml_migration,
    prove_runtime_readiness,
)
from .traceability import (
    rendered_traceability,
    trace_is_fresh,
    write_traceability,
)
from .validation import validate_repository
from .verification import verify_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dset")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser(
        "init", help="preview or execute rootless DSET initialization"
    )
    initialize.add_argument("target", type=Path)
    initialize.add_argument("--project-key", required=True)
    initialize.add_argument("--project-id", required=True)
    initialize.add_argument("--name", required=True, dest="project_name")
    initialize.add_argument("--license", required=True, dest="project_license")
    initialize.add_argument("--package", default="project", dest="package_id")
    initialize.add_argument("--repository")
    initialize.add_argument("--work-area", action="append", default=[])
    initialize.add_argument("--profile", default="core-v1")
    initialize.add_argument("--source", type=Path)
    initialize.add_argument("--execute", action="store_true")
    initialize.add_argument("--format", choices=["text", "json"], default="text")

    check = commands.add_parser("check", help="validate DSET contracts")
    _root_argument(check)
    check.add_argument("--format", choices=["text", "json"], default="text")

    verify = commands.add_parser("verify", help="run all configured gates")
    _root_argument(verify)
    verify.add_argument("--format", choices=["text", "json"], default="text")

    profile = commands.add_parser(
        "profile", help="validate an applied enforcement profile"
    )
    profile_commands = profile.add_subparsers(dest="profile_command", required=True)
    profile_check = profile_commands.add_parser(
        "check", help="inspect a profile and pinned target without executing it"
    )
    _root_argument(profile_check)
    profile_check.add_argument("--profile", required=True, dest="profile_id")
    profile_check.add_argument("--target", type=Path)
    profile_check.add_argument("--format", choices=["text", "json"], default="text")

    new = commands.add_parser("new", help="create a change from templates")
    new.add_argument("change_id")
    new.add_argument("--root", type=Path, default=Path.cwd())
    new.add_argument("--package", required=True, dest="package_id")
    new.add_argument(
        "--profile",
        choices=["small", "standard", "large", "defect", "adoption"],
        default="standard",
    )
    new.add_argument("--title")
    new.add_argument("--layer", choices=["META", "GOV", "TOOL", "SKILL", "OPS"])
    new.add_argument("--work-area", action="append", dest="work_areas", default=[])
    new.add_argument(
        "--workspace",
        choices=["integration-branch", "branch-worktree"],
        dest="workspace_mode",
        help="override the project default; branch-worktree is optional isolation",
    )

    trace = commands.add_parser("trace", help="generate PR traceability")
    _root_argument(trace)
    mode = trace.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")

    archive = commands.add_parser("archive", help="guard and move a change")
    archive.add_argument("change_id")
    archive.add_argument("--root", type=Path, default=Path.cwd())
    archive.add_argument("--date", default=date.today().isoformat())
    archive.add_argument("--execute", action="store_true")

    rules = commands.add_parser("rules", help="resolve repository governing rules")
    rule_commands = rules.add_subparsers(dest="rules_command", required=True)
    rules_check = rule_commands.add_parser("check", help="validate local governance")
    _root_argument(rules_check)
    rules_check.add_argument("--format", choices=["text", "json"], default="text")
    resolve = rule_commands.add_parser("resolve", help="resolve a governed workflow")
    resolve.add_argument("workflow_id")
    _root_argument(resolve)
    resolve.add_argument("--format", choices=["text", "json"], default="text")
    materialize = rule_commands.add_parser(
        "materialize", help="copy project-owned rules from a framework profile"
    )
    materialize.add_argument("target", type=Path)
    materialize.add_argument("--source", type=Path)
    materialize.add_argument("--profile", default="core-v1")
    materialize.add_argument("--install-wrappers", action="store_true")
    refresh = rule_commands.add_parser(
        "refresh", help="record explicit local customization state"
    )
    _root_argument(refresh)
    compare = rule_commands.add_parser(
        "diff", help="compare local rules with framework templates"
    )
    _root_argument(compare)
    compare.add_argument("--source", type=Path, required=True)

    methodology = commands.add_parser(
        "methodology", help="manage the installed project-local methodology"
    )
    methodology_commands = methodology.add_subparsers(
        dest="methodology_command", required=True
    )
    methodology_check = methodology_commands.add_parser(
        "check", help="compare reusable source with the installed methodology"
    )
    _root_argument(methodology_check)
    methodology_check.add_argument("--format", choices=["text", "json"], default="text")
    methodology_sync = methodology_commands.add_parser(
        "sync", help="materialize reusable source into the installed methodology"
    )
    _root_argument(methodology_sync)
    methodology_sync.add_argument("--execute", action="store_true")
    methodology_sync.add_argument("--format", choices=["text", "json"], default="text")

    self_host = commands.add_parser(
        "self-host", help="run the bounded DSET release fixed point"
    )
    _root_argument(self_host)
    self_host.add_argument("--work-dir", type=Path)
    self_host.add_argument("--released-ref")

    migrate = commands.add_parser(
        "migrate", help="preview or apply a deterministic DSET format migration"
    )
    migrate_commands = migrate.add_subparsers(dest="migration_command", required=True)
    migrate_toml = migrate_commands.add_parser(
        "toml", help="preview canonical TOML conversion; writes require --apply"
    )
    _root_argument(migrate_toml)
    migration_mode = migrate_toml.add_mutually_exclusive_group()
    migration_mode.add_argument("--apply", action="store_true")
    migration_mode.add_argument(
        "--prove-runtime-readiness",
        action="store_true",
        help=(
            "prove the preview in a disposable migrated copy and write "
            "digest-only evidence"
        ),
    )
    migrate_toml.add_argument("--format", choices=["text", "json"], default="text")

    version = commands.add_parser("version", help="show framework version semantics")
    _root_argument(version)
    version.add_argument("--format", choices=["text", "json"], default="text")

    release = commands.add_parser("release", help="guard the release transaction")
    release_commands = release.add_subparsers(dest="release_command", required=True)
    release_plan = release_commands.add_parser(
        "plan", help="render the committed release transition"
    )
    _root_argument(release_plan)
    release_plan.add_argument("--format", choices=["text", "json"], default="text")
    release_check = release_commands.add_parser(
        "check", help="check synchronized prepared release identity"
    )
    _root_argument(release_check)
    release_check.add_argument("--format", choices=["text", "json"], default="text")
    release_prepare = release_commands.add_parser(
        "prepare", help="synchronize version surfaces after explicit authorization"
    )
    _root_argument(release_prepare)
    release_prepare.add_argument("--execute", action="store_true")
    release_prepare.add_argument("--format", choices=["text", "json"], default="text")

    artifact = commands.add_parser(
        "artifact", help="assess immutable artifact emission"
    )
    artifact_commands = artifact.add_subparsers(dest="artifact_command", required=True)
    artifact_assess = artifact_commands.add_parser(
        "assess", help="check ambiguity and broader-scope eligibility"
    )
    _root_argument(artifact_assess)
    artifact_assess.add_argument("--candidate", type=Path, required=True)

    atom = commands.add_parser("atom", help="seal atoms and append lifecycle events")
    atom_commands = atom.add_subparsers(dest="atom_command", required=True)
    atom_seal = atom_commands.add_parser("seal", help="seal an emitted atom carrier")
    _root_argument(atom_seal)
    atom_seal.add_argument("--file", type=Path, required=True)
    atom_event = atom_commands.add_parser(
        "event", help="append a validated immutable-atom lifecycle event"
    )
    _root_argument(atom_event)
    atom_event.add_argument("--candidate", type=Path, required=True)
    atom_archive = atom_commands.add_parser(
        "archive", help="move a fully retired atom while preserving its lookup"
    )
    _root_argument(atom_archive)
    atom_archive.add_argument("--id", required=True)

    conflict = commands.add_parser(
        "conflict", help="classify governed artifact incompatibilities"
    )
    _root_argument(conflict)
    conflict.add_argument("--candidate", type=Path, required=True)
    conflict_mode = conflict.add_mutually_exclusive_group()
    conflict_mode.add_argument("--output", type=Path)
    conflict_mode.add_argument("--emit", type=Path)
    conflict_mode.add_argument("--check-result", type=Path)

    health = commands.add_parser("health", help="render derived project health")
    _root_argument(health)
    health_mode = health.add_mutually_exclusive_group()
    health_mode.add_argument("--write", action="store_true")
    health_mode.add_argument("--check", action="store_true")

    compilation = commands.add_parser(
        "compile", help="seal active Decision authority into evergreen projections"
    )
    _root_argument(compilation)
    compilation_mode = compilation.add_mutually_exclusive_group()
    compilation_mode.add_argument("--write", action="store_true")
    compilation_mode.add_argument("--check", action="store_true")

    dependencies = commands.add_parser(
        "dependencies", help="enforce exact dependency policy and lock authority"
    )
    _root_argument(dependencies)
    dependencies.add_argument("--format", choices=["text", "json"], default="text")

    review = commands.add_parser("review", help="exchange bounded external reviews")
    review_commands = review.add_subparsers(dest="review_command", required=True)
    review_packet = review_commands.add_parser(
        "packet", help="create an exact read-only review packet"
    )
    _root_argument(review_packet)
    review_packet.add_argument("--output", type=Path, required=True)
    review_packet.add_argument("--packet-id", required=True)
    review_packet.add_argument("--artifact", action="append", default=[])
    review_packet.add_argument("--criterion", action="append", default=[])
    review_packet.add_argument("--scope", required=True)
    review_validate = review_commands.add_parser(
        "validate", help="validate a report against its exact packet"
    )
    _root_argument(review_validate)
    review_validate.add_argument("--packet", type=Path, required=True)
    review_validate.add_argument("--report", type=Path, required=True)
    review_reconcile = review_commands.add_parser(
        "reconcile", help="validate explicit dispositions for every finding"
    )
    _root_argument(review_reconcile)
    review_reconcile.add_argument("--packet", type=Path, required=True)
    review_reconcile.add_argument("--report", type=Path, required=True)
    review_reconcile.add_argument("--candidate", type=Path, required=True)
    review_reconcile.add_argument("--output", type=Path)

    runtime = commands.add_parser("runtime", help="bridge host skill run state")
    runtime_commands = runtime.add_subparsers(dest="runtime_command", required=True)
    runtime_start = runtime_commands.add_parser("start")
    runtime_start.add_argument("workflow_id")
    _root_argument(runtime_start)
    runtime_start.add_argument(
        "--entrypoint",
        choices=sorted(PUBLIC_SKILL_WORKFLOWS),
        required=True,
    )
    runtime_start.add_argument("--objective", required=True)
    runtime_start.add_argument("--mode")
    runtime_start.add_argument("--session-id")
    runtime_start.add_argument("--llm-session-id", action="append", default=[])
    runtime_resume = runtime_commands.add_parser("resume")
    _root_argument(runtime_resume)
    runtime_resume.add_argument("--session-id")
    runtime_checkpoint = runtime_commands.add_parser("checkpoint")
    runtime_checkpoint.add_argument("run_id")
    _root_argument(runtime_checkpoint)
    runtime_checkpoint.add_argument(
        "--status",
        choices=["active", "paused", "completed", "stopped"],
        default="active",
    )
    runtime_checkpoint.add_argument("--objective")
    runtime_checkpoint.add_argument("--next-mode")
    runtime_checkpoint.add_argument("--reason-code")
    runtime_checkpoint.add_argument(
        "--requires-authorization",
        choices=["none", "repository-write", "external-write", "publication"],
    )
    runtime_handoff = runtime_commands.add_parser(
        "handoff", help="finish one run while keeping its DSET session active"
    )
    runtime_handoff.add_argument("run_id")
    _root_argument(runtime_handoff)
    runtime_handoff.add_argument("--output", action="append", default=[])
    runtime_handoff.add_argument("--diagnostic", action="append", default=[])
    runtime_handoff.add_argument("--next-signal", action="append", required=True)
    runtime_finish = runtime_commands.add_parser("finish")
    runtime_finish.add_argument("run_id")
    _root_argument(runtime_finish)
    runtime_finish.add_argument(
        "--status",
        choices=["succeeded", "failed", "stopped", "interrupted"],
        required=True,
    )
    runtime_finish.add_argument("--output", action="append", default=[])
    runtime_finish.add_argument("--diagnostic", action="append", default=[])
    runtime_finish.add_argument("--next-signal", action="append", default=[])
    runtime_child = runtime_commands.add_parser("child")
    runtime_child.add_argument("session_id")
    runtime_child.add_argument("workflow_id")
    _root_argument(runtime_child)
    runtime_child.add_argument("--objective", required=True)
    runtime_child.add_argument("--llm-session-id", action="append", default=[])
    runtime_closure = runtime_commands.add_parser("closure")
    runtime_closure.add_argument("session_id")
    _root_argument(runtime_closure)
    runtime_closure.add_argument("--workflow")
    runtime_closure.add_argument(
        "--status",
        choices=["succeeded", "failed", "stopped", "ambiguous"],
        default="succeeded",
    )
    runtime_closure.add_argument("--criterion", action="append", default=[])

    skills = commands.add_parser(
        "skills",
        help="install or verify portable Codex and Claude skill distributions",
        add_help=False,
    )
    skills.add_argument("skills_args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            initialization = initialize_project(
                args.target,
                project_key=args.project_key,
                project_id=args.project_id,
                project_name=args.project_name,
                project_license=args.project_license,
                package_id=args.package_id,
                repository=args.repository,
                work_areas=tuple(parse_work_area(item) for item in args.work_area),
                profile=args.profile,
                source_root=args.source,
                execute=args.execute,
            )
            if args.format == "json":
                print(json.dumps(initialization.as_dict(), indent=2, sort_keys=True))
            else:
                label = "INITIALIZED" if initialization.executed else "DRY RUN"
                print(f"{label} {initialization.target} source={initialization.source}")
                for relative_path in initialization.paths:
                    print(relative_path)
            return 0
        if args.command == "check":
            root = _repository_root(args.root)
            return _report(validate_repository(root), root, args.format)
        if args.command == "verify":
            root = _repository_root(args.root)
            return _report(verify_repository(root), root, args.format)
        if args.command == "profile":
            root = _repository_root(args.root)
            profile_path = resolve_profile_path(root, args.profile_id)
            profile_data, diagnostics = validate_profile_file(profile_path)
            target = root if args.target is None else args.target
            if diagnostics:
                return _report(diagnostics, root, args.format)
            if profile_data.get("id") != args.profile_id:
                raise ValueError("profile ID does not match the selected name")
            inspection = inspect_target(profile_path, profile_data, target)
            if args.format == "json":
                print(json.dumps(inspection, indent=2, sort_keys=True))
            else:
                print(
                    f"PROFILE {inspection['profile']} "
                    f"status={inspection['profile_status']}"
                )
                print(f"target_revision={inspection['target_revision']}")
                print(f"file_counts={inspection['file_counts']}")
                print(f"known_blockers={len(inspection['known_blockers'])}")
                for diagnostic in inspection["diagnostics"]:
                    print(diagnostic)
            return 0 if not inspection["diagnostics"] else 1
        if args.command == "new":
            root = _repository_root(args.root)
            path = create_change(
                root,
                args.change_id,
                args.package_id,
                args.profile,
                args.title,
                args.layer,
                work_areas=args.work_areas,
                workspace_mode=args.workspace_mode,
            )
            print(path.relative_to(root).as_posix())
            return 0
        if args.command == "trace":
            root = _repository_root(args.root)
            if args.check:
                if trace_is_fresh(root):
                    print("DSET traceability is fresh")
                    return 0
                path = discover_layout(root).traceability_path.relative_to(root)
                print(f"DSET-E111 {path}: traceability is stale")
                return 1
            if args.write:
                path = write_traceability(root)
                print(path.relative_to(root).as_posix())
                return 0
            sys.stdout.write(rendered_traceability(root))
            return 0
        if args.command == "archive":
            root = _repository_root(args.root)
            archive_date = date.fromisoformat(args.date)
            if args.execute:
                destination = execute_archive(root, args.change_id, archive_date)
                print(destination.relative_to(root).as_posix())
            else:
                source, destination = archive_plan(root, args.change_id, archive_date)
                print(
                    f"DRY RUN {source.relative_to(root).as_posix()} -> "
                    f"{destination.relative_to(root).as_posix()}"
                )
            return 0
        if args.command == "rules":
            if args.rules_command == "materialize":
                source = _repository_root(args.source)
                path = materialize_governance(
                    source,
                    args.target,
                    args.profile,
                    install_wrappers=args.install_wrappers,
                )
                print(path.relative_to(args.target.resolve()).as_posix())
                return 0
            root = _repository_root(args.root)
            if args.rules_command == "check":
                return _report(validate_governance(root), root, args.format)
            if args.rules_command == "resolve":
                resolved, diagnostics = resolve_workflow(root, args.workflow_id)
                if diagnostics:
                    return _report(diagnostics, root, args.format)
                assert resolved is not None
                if args.format == "json":
                    print(json.dumps(resolved, indent=2))
                else:
                    _print_resolved(resolved)
                return 0
            if args.rules_command == "refresh":
                path = refresh_customization(root)
                print(path.relative_to(root).as_posix())
                return 0
            if args.rules_command == "diff":
                sys.stdout.write(diff_governance(root, args.source))
                return 0
        if args.command == "methodology":
            root = _repository_root(args.root)
            if args.methodology_command == "check":
                drift = methodology_drift(root)
                methodology_report = {
                    "status": "current" if not drift else "stale",
                    "carriers": [
                        {"name": item.carrier, "status": item.status} for item in drift
                    ],
                }
                if args.format == "json":
                    print(json.dumps(methodology_report, indent=2, sort_keys=True))
                elif drift:
                    for item in drift:
                        print(f"{item.status.upper()} {item.carrier}")
                else:
                    print("Installed methodology is current")
                return 1 if drift else 0
            changed = sync_methodology(root, execute=args.execute)
            sync_report = {
                "status": "synchronized" if args.execute else "preview",
                "carriers": list(changed),
            }
            if args.format == "json":
                print(json.dumps(sync_report, indent=2, sort_keys=True))
            else:
                label = "SYNCHRONIZED" if args.execute else "DRY RUN"
                print(f"{label} carriers={len(changed)}")
                for carrier in changed:
                    print(carrier)
            return 0
        if args.command == "self-host":
            root = _repository_root(args.root)
            if args.work_dir:
                report = run_self_host(
                    root, args.work_dir, released_ref=args.released_ref
                )
            else:
                with temporary_directory(prefix="dset-self-host-") as raw:
                    report = run_self_host(
                        root, Path(raw), released_ref=args.released_ref
                    )
                    report.pop("adopter", None)
            print(json.dumps(report, indent=2))
            return 0
        if args.command == "version":
            root = _repository_root(args.root)
            data = project_section(root, "version_registry")
            if args.format == "json":
                print(json.dumps(data, indent=2))
            else:
                framework = data["framework"]
                toolchain = data["python_package"]
                schemas = data["schemas"]
                print(f"product: {framework['version']} (coordinated)")
                print(f"python package: {toolchain['version']} (coordinated)")
                print(f"schemas: {schemas['version']} (independent)")
            return 0
        if args.command == "release":
            root = _repository_root(args.root)
            if args.release_command == "plan":
                plan = plan_release(root)
                _print_release(plan.to_dict(), args.format, "RELEASE PLAN")
                return 0
            if args.release_command == "check":
                plan = check_release(root)
                _print_release(plan.to_dict(), args.format, "RELEASE CHECK PASSED")
                return 0
            if args.release_command == "prepare":
                preparation = prepare_release(root, execute=args.execute)
                label = "RELEASE PREPARED" if args.execute else "DRY RUN"
                _print_release(preparation.to_dict(), args.format, label)
                return 0
        if args.command == "artifact":
            root = _repository_root(args.root)
            candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
            if not isinstance(candidate, dict):
                raise ValueError("artifact candidate must be a JSON object")
            assessment = assess_artifact_candidate(root, candidate)
            print(json.dumps(assessment, indent=2, sort_keys=True))
            return 0 if assessment["emission_allowed"] is True else 2
        if args.command == "atom":
            root = _repository_root(args.root)
            if args.atom_command == "seal":
                path = seal_atom(root, args.file)
            elif args.atom_command == "event":
                event = json.loads(args.candidate.read_text(encoding="utf-8"))
                if not isinstance(event, dict):
                    raise ValueError("lifecycle candidate must be a JSON object")
                path = append_lifecycle_event(root, event)
            else:
                path = archive_atom(root, args.id)
            print(path.relative_to(root).as_posix())
            return 0
        if args.command == "conflict":
            root = _repository_root(args.root)
            candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
            if not isinstance(candidate, dict):
                raise ValueError("conflict candidate must be a JSON object")
            if args.emit is not None:
                path, _ = emit_conflict_atom(root, args.emit, candidate)
                print(path.relative_to(root).as_posix())
                return 0
            if args.check_result is not None:
                recorded = json.loads(args.check_result.read_text(encoding="utf-8"))
                if not isinstance(recorded, dict):
                    raise ValueError("recorded conflict result must be a JSON object")
                if conflict_result_is_fresh(root, candidate, recorded):
                    print("DSET conflict result is fresh")
                    return 0
                print("DSET-E165 recorded conflict result is stale")
                return 1
            result = resolve_conflict(root, candidate)
            if args.output is not None:
                path = write_conflict_result(root, args.output, result)
                print(path)
            else:
                print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.command == "health":
            root = _repository_root(args.root)
            if args.check:
                if health_is_fresh(root):
                    print("DSET project health is fresh")
                    return 0
                path = health_path(root).relative_to(root)
                print(f"DSET-E162 {path}: project health is stale")
                return 1
            if args.write:
                path = write_health(root)
                print(path.relative_to(root).as_posix())
                return 0
            sys.stdout.write(render_health(root))
            return 0
        if args.command == "compile":
            root = _repository_root(args.root)
            if args.check:
                if compilation_is_fresh(root):
                    print("DSET active authority compilation is fresh")
                    return 0
                path = compilation_path(root).relative_to(root)
                print(f"DSET-E164 {path}: compilation is stale or incomplete")
                return 1
            if args.write:
                path = write_compilation(root)
                print(path.relative_to(root).as_posix())
                return 0
            sys.stdout.write(rendered_compilation(root))
            return 0
        if args.command == "dependencies":
            root = _repository_root(args.root)
            result = dependency_summary(root)
            if args.format == "json":
                print(json.dumps(result, indent=2, sort_keys=True))
            else:
                print(
                    f"DEPENDENCIES {result['status']} "
                    f"allow={result['allowed']} deny={result['denied']} "
                    f"exceptions={result['exceptions']}"
                )
                for diagnostic in result["diagnostics"]:
                    print(diagnostic)
            return 0 if result["status"] == "pass" else 1
        if args.command == "migrate":
            root = _repository_root(args.root)
            migration_plan = plan_toml_migration(root)
            if args.prove_runtime_readiness:
                try:
                    prove_runtime_readiness(root)
                except ValueError as error:
                    print(f"TOML runtime readiness proof failed: {error}")
                    return 1
                migration_plan = plan_toml_migration(root)
                _print_migration_report(migration_plan, args.format, applied=False)
                return 0 if migration_plan.ready else 1
            if not migration_plan.ready:
                _print_migration_report(migration_plan, args.format, applied=False)
                return 1
            if args.apply:
                migration_plan = apply_toml_migration(root)
            _print_migration_report(
                migration_plan,
                args.format,
                applied=bool(args.apply),
            )
            return 0
        if args.command == "review":
            root = _repository_root(args.root)
            if args.review_command == "packet":
                path = create_review_packet(
                    root,
                    args.output,
                    packet_id=args.packet_id,
                    artifacts=args.artifact,
                    criteria=args.criterion,
                    scope=args.scope,
                )
                print(path)
                return 0
            if args.review_command == "validate":
                result = validate_review_report(root, args.packet, args.report)
            else:
                result = reconcile_review(
                    root, args.packet, args.report, args.candidate
                )
                if args.output is not None:
                    path = write_reconciliation(root, args.output, result)
                    print(path.relative_to(root).as_posix())
                    return 0
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.command == "runtime":
            root = _repository_root(args.root)
            runtime_result: object
            if args.runtime_command == "start":
                runtime_result = start_runtime(
                    root,
                    public_entrypoint=args.entrypoint,
                    workflow_id=args.workflow_id,
                    objective=args.objective,
                    mode_id=args.mode,
                    session_id=args.session_id,
                    llm_session_ids=args.llm_session_id,
                )
            elif args.runtime_command == "resume":
                runtime_result = read_runtime(root, session_id=args.session_id)
            elif args.runtime_command == "checkpoint":
                runtime_result = checkpoint_runtime(
                    root,
                    args.run_id,
                    status=args.status,
                    objective=args.objective,
                    next_mode=args.next_mode,
                    next_reason_code=args.reason_code,
                    requires_authorization=args.requires_authorization,
                )
            elif args.runtime_command == "handoff":
                runtime_result = handoff_runtime(
                    root,
                    args.run_id,
                    outputs=args.output,
                    diagnostics=args.diagnostic,
                    next_signals=args.next_signal,
                )
            elif args.runtime_command == "finish":
                runtime_result = finish_runtime(
                    root,
                    args.run_id,
                    status=args.status,
                    outputs=args.output,
                    diagnostics=args.diagnostic,
                    next_signals=args.next_signal,
                )
            elif args.runtime_command == "child":
                runtime_result = start_child_runtime(
                    root,
                    session_id=args.session_id,
                    workflow_id=args.workflow_id,
                    objective=args.objective,
                    llm_session_ids=args.llm_session_id,
                )
            else:
                runtime_result = advance_runtime_closure(
                    root,
                    session_id=args.session_id,
                    workflow_id=args.workflow,
                    child_status=args.status,
                    observations=_parse_criteria(args.criterion),
                )
            print(json.dumps(runtime_result, indent=2, sort_keys=True))
            return 0
        if args.command == "skills":
            return skill_distribution_main(args.skills_args)
    except DsetCommandError as error:
        print(error.render(), file=sys.stderr)
        return 2
    except (FileExistsError, FileNotFoundError, ValueError) as error:
        print(f"DSET-E900: {error}", file=sys.stderr)
        return 2
    return 2


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", nargs="?", type=Path)


def _parse_criteria(values: Sequence[str]) -> dict[str, bool | None]:
    parsed: dict[str, bool | None] = {}
    for raw in values:
        name, separator, value = raw.partition("=")
        if not separator or not name or name in parsed:
            raise ValueError(f"criterion must be unique NAME=VALUE: {raw}")
        if value == "true":
            parsed[name] = True
        elif value == "false":
            parsed[name] = False
        elif value == "unknown":
            parsed[name] = None
        else:
            raise ValueError(f"criterion value must be true, false, or unknown: {raw}")
    return parsed


def _print_migration_report(
    plan: MigrationPlan,
    output_format: str,
    *,
    applied: bool,
) -> None:
    """Render one preview or blocked migration plan without raising to the host."""

    report = plan.report()
    report["applied"] = applied
    if output_format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    label = "APPLIED" if applied else "DRY RUN"
    print(
        f"{label} TOML migration {report['status']} "
        f"changes={len(plan.entries)} references={len(plan.references)} "
        f"exceptions={len(plan.exceptions)}"
    )
    for blocker in plan.blockers:
        print(f"BLOCKED {blocker}")


def _repository_root(raw: Path | None) -> Path:
    return find_repository(raw or Path.cwd())


def _print_resolved(data: dict[str, object]) -> None:
    print(
        f"workflow={data['workflow_id']} profile={data['profile']}@"
        f"{data['profile_version']} customization={data['customization']}"
    )
    rules = data.get("rules")
    if isinstance(rules, list):
        for rule in rules:
            if isinstance(rule, dict):
                print(f"{rule['id']} {rule['document']}")


def _print_release(data: dict[str, object], output_format: str, label: str) -> None:
    if output_format == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    print(
        f"{label} {data['owner_change']} {data['release_class']} "
        f"{data['target']} tag={data['tag']}"
    )
    changes = data.get("changes")
    if isinstance(changes, list):
        for path in changes:
            print(path)


def _report(diagnostics: Sequence[Diagnostic], root: Path, output_format: str) -> int:
    if output_format == "json":
        print(
            json.dumps(
                [
                    {
                        "code": item.code,
                        "path": _relative(item.path, root),
                        "message": item.message,
                    }
                    for item in diagnostics
                ],
                indent=2,
            )
        )
    elif diagnostics:
        for item in diagnostics:
            print(item.render(root))
    else:
        print("DSET validation passed")
    return 1 if diagnostics else 0


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
