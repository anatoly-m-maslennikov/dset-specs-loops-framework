"""Verify Local Python Tools profile enforcement.

Assurance scope: physical-line measurement and self-conformance diagnostics.
Non-obvious fixtures: generated source isolates exclusions without fixture files.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from dset_toolchain.local_python_profile import (
    _measured_function_lines,
    validate_local_python_profile,
)
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


class LocalPythonProfileTests(unittest.TestCase):
    """Verify literal line measurement and checker self-conformance."""

    def test_function_measurement_excludes_signature_docstring_and_comments(
        self,
    ) -> None:
        source = _source_with_body(38)
        node = ast.parse(source).body[0]
        assert isinstance(node, ast.FunctionDef)

        self.assertEqual(_measured_function_lines(source, node), 40)

    def test_nested_function_body_is_measured_independently(self) -> None:
        source = """def outer() -> int:
    def inner() -> int:
        value = 1
        return value
    return inner()
"""
        tree = ast.parse(source)
        outer = tree.body[0]
        assert isinstance(outer, ast.FunctionDef)
        inner = outer.body[0]
        assert isinstance(inner, ast.FunctionDef)

        self.assertEqual(_measured_function_lines(source, outer), 1)
        self.assertEqual(_measured_function_lines(source, inner), 2)

    def test_checker_conforms_to_its_own_static_rules(self) -> None:
        diagnostics = validate_local_python_profile(ROOT)
        local = [
            item for item in diagnostics if item.path.name == "local_python_profile.py"
        ]

        self.assertEqual(local, [])


def _source_with_body(body_lines: int) -> str:
    """Handle with body using the declared repository contract."""
    body = "\n".join("    value += 1" for _ in range(body_lines))
    return f'''def measured(
    initial: int,
) -> int:
    """Return a deliberately long measured body."""
    # This comment is excluded.
    value = initial
{body}
    return value
'''


if __name__ == "__main__":
    unittest.main()
