from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path

from dset_toolchain.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_trace_prints_without_writing(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(["trace", str(ROOT)])
        self.assertEqual(result, 0)
        self.assertIn("operationalize-dset-v1", stream.getvalue())

    def test_check_passes_current_project_contract(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(["check", str(ROOT)])
        self.assertEqual(result, 0)
        self.assertIn("DSET validation passed", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
