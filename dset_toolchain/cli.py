from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from . import __version__
from .archive import archive_plan, execute_archive
from .diagnostics import Diagnostic
from .errors import DsetCommandError
from .governance import (
    diff_governance,
    find_repository,
    materialize_governance,
    refresh_customization,
    resolve_workflow,
    validate_governance,
)
from .layout import discover_layout
from .scaffold import create_change
from .self_host import run_self_host
from .traceability import (
    rendered_traceability,
    trace_is_fresh,
    write_traceability,
)
from .validation import validate_repository
from .verification import verify_repository
from .yaml_subset import load


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dset")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="validate DSET contracts")
    _root_argument(check)
    check.add_argument("--format", choices=["text", "json"], default="text")

    verify = commands.add_parser("verify", help="run all configured gates")
    _root_argument(verify)
    verify.add_argument("--format", choices=["text", "json"], default="text")

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

    self_host = commands.add_parser(
        "self-host", help="run the bounded DSET release fixed point"
    )
    _root_argument(self_host)
    self_host.add_argument("--work-dir", type=Path)
    self_host.add_argument("--released-ref")

    version = commands.add_parser("version", help="show framework version semantics")
    _root_argument(version)
    version.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "check":
            root = _repository_root(args.root)
            return _report(validate_repository(root), root, args.format)
        if args.command == "verify":
            root = _repository_root(args.root)
            return _report(verify_repository(root), root, args.format)
        if args.command == "new":
            root = _repository_root(args.root)
            path = create_change(
                root,
                args.change_id,
                args.package_id,
                args.profile,
                args.title,
                args.layer,
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
        if args.command == "self-host":
            root = _repository_root(args.root)
            if args.work_dir:
                report = run_self_host(
                    root, args.work_dir, released_ref=args.released_ref
                )
            else:
                with tempfile.TemporaryDirectory() as raw:
                    report = run_self_host(
                        root, Path(raw), released_ref=args.released_ref
                    )
                    report.pop("adopter", None)
            print(json.dumps(report, indent=2))
            return 0
        if args.command == "version":
            root = _repository_root(args.root)
            data = load(discover_layout(root).version_path)
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
    except DsetCommandError as error:
        print(error.render(), file=sys.stderr)
        return 2
    except (FileExistsError, FileNotFoundError, ValueError) as error:
        print(f"DSET-E900: {error}", file=sys.stderr)
        return 2
    return 2


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", nargs="?", type=Path)


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
                print(f"{rule['id']} {rule['path']}")


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
