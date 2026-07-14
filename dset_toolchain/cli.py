from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from . import __version__
from .archive import archive_plan, execute_archive
from .diagnostics import Diagnostic
from .scaffold import create_change
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "check":
            return _report(validate_repository(root), root, args.format)
        if args.command == "verify":
            return _report(verify_repository(root), root, args.format)
        if args.command == "new":
            path = create_change(
                root,
                args.change_id,
                args.package_id,
                args.profile,
                args.title,
            )
            print(path.relative_to(root).as_posix())
            return 0
        if args.command == "trace":
            if args.check:
                if trace_is_fresh(root):
                    print("DSET traceability is fresh")
                    return 0
                print("DSET-E111 dset/traceability.yaml: traceability is stale")
                return 1
            if args.write:
                path = write_traceability(root)
                print(path.relative_to(root).as_posix())
                return 0
            sys.stdout.write(rendered_traceability(root))
            return 0
        if args.command == "archive":
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
    except (FileExistsError, FileNotFoundError, ValueError) as error:
        print(f"DSET-E900: {error}", file=sys.stderr)
        return 2
    return 2


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())


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
