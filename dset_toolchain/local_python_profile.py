"""Validate source carriers against the selected Local Python Tools profile."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic
from .toml_codec import load

# PROFILE_NAME identifies the only current concrete Python profile; methodology owns it.
PROFILE_NAME = "020_dset-implementation-local-python-tools-profile-v1.toml"
# PRIVATE_DOCSTRING_STATEMENT_LIMIT separates trivial helpers from documented behavior.
PRIVATE_DOCSTRING_STATEMENT_LIMIT = 5
# AUTHORITATIVE_PYTHON_ROOTS maps selected work areas to repository-owned source roots.
AUTHORITATIVE_PYTHON_ROOTS = (
    Path("dset_toolchain"),
    Path("tests"),
    Path("15_layer_implementation/100_python"),
    Path("15_layer_implementation/110_tests"),
)


@dataclass(frozen=True)
class PythonProfileLimits:
    """Hold executable size limits loaded from the selected profile."""

    function_exclusive: int
    module_maximum: int


def validate_local_python_profile(root: Path) -> list[Diagnostic]:
    """Validate every authoritative Python carrier for this framework source."""
    root = root.resolve()
    profile_path = _find_profile(root)
    try:
        limits = _load_limits(profile_path)
    except (OSError, TypeError, ValueError) as error:
        return [Diagnostic("DSET-E180", profile_path, str(error))]
    diagnostics: list[Diagnostic] = []
    for path in _python_files(root):
        diagnostics.extend(_validate_file(path, limits))
    return sorted(set(diagnostics))


def _find_profile(root: Path) -> Path:
    """Resolve the one authoritative Local Python Tools profile carrier."""
    matches = sorted(root.rglob(PROFILE_NAME))
    source = [path for path in matches if ".dset" not in path.parts]
    if len(source) == 1:
        return source[0]
    if len(matches) == 1:
        return matches[0]
    raise FileNotFoundError(f"expected one selected profile named {PROFILE_NAME}")


def _load_limits(path: Path) -> PythonProfileLimits:
    """Load mandatory size limits without duplicating their numeric values."""
    data = load(path)
    limits = data.get("limits") if isinstance(data, dict) else None
    if not isinstance(limits, dict):
        raise ValueError("Local Python Tools profile requires a limits table")
    function_limit = limits.get("function_line_limit_exclusive")
    module_limit = limits.get("module_line_limit")
    if not isinstance(function_limit, int) or function_limit < 2:
        raise ValueError("function_line_limit_exclusive must be an integer above one")
    if not isinstance(module_limit, int) or module_limit < function_limit:
        raise ValueError("module_line_limit must be at least the function limit")
    return PythonProfileLimits(function_limit, module_limit)


def _python_files(root: Path) -> tuple[Path, ...]:
    """Enumerate authoritative root Python sources without installed mirrors."""
    paths = {
        path
        for relative in AUTHORITATIVE_PYTHON_ROOTS
        for path in (root / relative).rglob("*.py")
        if "__pycache__" not in path.parts
    }
    return tuple(sorted(paths))


def _validate_file(path: Path, limits: PythonProfileLimits) -> list[Diagnostic]:
    """Parse and validate one source carrier against static profile rules."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, path.as_posix())
    except (OSError, UnicodeError, SyntaxError) as error:
        return [
            _diagnostic("DSET-E180", path, f"Python carrier cannot be read: {error}")
        ]
    diagnostics = _module_diagnostics(path, source, tree, limits)
    diagnostics.extend(_definition_diagnostics(path, source, tree, limits))
    diagnostics.extend(_constant_diagnostics(path, source, tree))
    return diagnostics


def _module_diagnostics(
    path: Path,
    source: str,
    tree: ast.Module,
    limits: PythonProfileLimits,
) -> list[Diagnostic]:
    """Check module documentation, measured size, and indentation."""
    diagnostics: list[Diagnostic] = []
    if ast.get_docstring(tree, clean=False) is None:
        diagnostics.append(
            _diagnostic("DSET-E181", path, "module docstring is missing")
        )
    measured = _measured_module_lines(source, tree)
    if measured > limits.module_maximum:
        diagnostics.append(
            _diagnostic(
                "DSET-E182",
                path,
                f"module has {measured} measured lines; maximum is {limits.module_maximum}",
            )
        )
    if "\t" in source:
        diagnostics.append(
            _diagnostic("DSET-E180", path, "tab indentation is prohibited")
        )
    return diagnostics


def _definition_diagnostics(
    path: Path,
    source: str,
    tree: ast.Module,
    limits: PythonProfileLimits,
) -> list[Diagnostic]:
    """Check classes and functions for size, documentation, and typing."""
    diagnostics: list[Diagnostic] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and ast.get_docstring(node) is None:
            diagnostics.append(
                _at("DSET-E184", path, node, "class docstring is missing")
            )
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        measured = _measured_function_lines(source, node)
        if measured >= limits.function_exclusive:
            diagnostics.append(
                _at(
                    "DSET-E183",
                    path,
                    node,
                    f"function has {measured} measured lines; exclusive limit is {limits.function_exclusive}",
                )
            )
        diagnostics.extend(_function_contract_diagnostics(path, node, measured))
    return diagnostics


def _function_contract_diagnostics(
    path: Path,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    measured: int,
) -> list[Diagnostic]:
    """Check one function's documentation and complete annotations."""
    diagnostics: list[Diagnostic] = []
    if _requires_docstring(path, node, measured) and ast.get_docstring(node) is None:
        diagnostics.append(
            _at("DSET-E184", path, node, "function docstring is missing")
        )
    arguments = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    if node.args.vararg is not None:
        arguments.append(node.args.vararg)
    if node.args.kwarg is not None:
        arguments.append(node.args.kwarg)
    missing = [
        argument.arg
        for argument in arguments
        if argument.arg not in {"self", "cls"} and argument.annotation is None
    ]
    if missing or node.returns is None:
        details = ", ".join(missing) if missing else "return"
        diagnostics.append(
            _at("DSET-E185", path, node, f"annotations missing: {details}")
        )
    return diagnostics


def _requires_docstring(
    path: Path,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    measured: int,
) -> bool:
    """Return whether a function is public or nontrivial enough to document."""
    if path.parent.name == "tests" and node.name.startswith("test_"):
        return False
    if node.name.startswith("_"):
        return measured > PRIVATE_DOCSTRING_STATEMENT_LIMIT
    return True


def _constant_diagnostics(
    path: Path, source: str, tree: ast.Module
) -> list[Diagnostic]:
    """Check module constant placement and adjacent responsibility comments."""
    lines = source.splitlines()
    diagnostics: list[Diagnostic] = []
    declarations_ended = False
    for node in tree.body:
        if _is_import_or_docstring(node):
            continue
        names = _constant_names(node)
        if names:
            previous = lines[node.lineno - 2].strip() if node.lineno > 1 else ""
            if not previous.startswith("#"):
                diagnostics.append(
                    _at("DSET-E186", path, node, "constant lacks documentation")
                )
            if declarations_ended:
                diagnostics.append(
                    _at(
                        "DSET-E186",
                        path,
                        node,
                        "constant follows executable declarations",
                    )
                )
            continue
        declarations_ended = True
    return diagnostics


def _is_import_or_docstring(node: ast.stmt) -> bool:
    """Recognize declarations that may precede module constants."""
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return True
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _constant_names(node: ast.stmt) -> tuple[str, ...]:
    """Return upper-case names assigned by one top-level statement."""
    targets: Iterable[ast.expr]
    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, ast.AnnAssign):
        targets = (node.target,)
    else:
        return ()
    return tuple(
        target.id
        for target in targets
        if isinstance(target, ast.Name) and target.id.isupper()
    )


def _measured_module_lines(source: str, tree: ast.Module) -> int:
    """Count physical module code lines after profile exclusions."""
    excluded = _docstring_lines(tree)
    return _count_code_lines(source, 1, len(source.splitlines()), excluded)


def _measured_function_lines(
    source: str,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> int:
    """Count physical function body lines after profile exclusions."""
    if not node.body:
        return 0
    excluded: set[int] = set()
    docstring = _leading_docstring(node.body)
    if docstring is not None:
        excluded.update(_node_line_range(docstring))
    for nested in _nested_definitions(node.body):
        excluded.update(_node_line_range(nested))
        for decorator in nested.decorator_list:
            excluded.update(_node_line_range(decorator))
    start = node.body[0].lineno
    end = node.end_lineno or node.body[-1].end_lineno or node.body[-1].lineno
    return _count_code_lines(source, start, end, excluded)


def _leading_docstring(body: list[ast.stmt]) -> ast.Expr | None:
    """Return the leading string expression for a definition body."""
    if not body:
        return None
    first = body[0]
    if _is_import_or_docstring(first) and isinstance(first, ast.Expr):
        return first
    return None


def _docstring_lines(tree: ast.Module) -> set[int]:
    """Return every definition docstring line excluded from module size."""
    lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            docstring = _leading_docstring(node.body)
            if docstring is not None:
                lines.update(_node_line_range(docstring))
    return lines


def _nested_definitions(
    body: list[ast.stmt],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, ...]:
    """Return nested definitions whose bodies are measured independently."""
    nested: list[ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef] = []

    def visit(node: ast.AST) -> None:
        """Collect definitions without descending into their owned bodies."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                nested.append(child)
                continue
            visit(child)

    for statement in body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nested.append(statement)
        else:
            visit(statement)
    return tuple(nested)


def _node_line_range(node: ast.AST) -> range:
    """Return the inclusive physical line range owned by an AST node."""
    start = getattr(node, "lineno", 1)
    end = getattr(node, "end_lineno", start) or start
    return range(start, end + 1)


def _count_code_lines(
    source: str,
    start: int,
    end: int,
    excluded: set[int],
) -> int:
    """Count nonblank, non-comment physical lines outside exclusions."""
    lines = source.splitlines()
    return sum(
        1
        for number in range(start, min(end, len(lines)) + 1)
        if number not in excluded
        and lines[number - 1].strip()
        and not lines[number - 1].lstrip().startswith("#")
    )


def _diagnostic(code: str, path: Path, message: str) -> Diagnostic:
    """Build a profile diagnostic for a whole source carrier."""
    return Diagnostic(code, path, message)


def _at(code: str, path: Path, node: ast.AST, message: str) -> Diagnostic:
    """Build a profile diagnostic anchored to one AST node line."""
    return _diagnostic(code, path, f"line {getattr(node, 'lineno', 1)}: {message}")
