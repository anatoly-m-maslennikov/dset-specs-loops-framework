from __future__ import annotations

import contextlib
import io
import json
import os
import unittest
from pathlib import Path
from unittest import mock

from dset_toolchain.cli import main
from dset_toolchain.skill_distribution import SKILL_WORKFLOWS
from dset_toolchain.temp_paths import temporary_directory
from tests import repository_root

ROOT = repository_root(Path(__file__))


class EndToEndCliTests(unittest.TestCase):
    def test_initialize_runtime_and_codex_distribution(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "project").resolve()
            (target / "src").mkdir(parents=True)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "init",
                        str(target),
                        "--project-key",
                        "APP",
                        "--project-id",
                        "sample-app",
                        "--name",
                        "Sample App",
                        "--license",
                        "MIT",
                        "--work-area",
                        "source=src",
                        "--execute",
                        "--format",
                        "json",
                    ]
                )
            self.assertEqual(result, 0)
            self.assertTrue(json.loads(output.getvalue())["executed"])

            output = io.StringIO()
            with (
                mock.patch.dict(os.environ, {"PYTHONPATH": str(ROOT)}),
                contextlib.redirect_stdout(output),
            ):
                result = main(["verify", str(target), "--format", "json"])
            self.assertEqual(result, 0)
            self.assertEqual(json.loads(output.getvalue()), [])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "runtime",
                        "start",
                        "diagnosis",
                        str(target),
                        "--entrypoint",
                        "dset-diagnose",
                        "--objective",
                        "Diagnose a failing import",
                        "--mode",
                        "diagnose",
                        "--llm-session-id",
                        "codex:test-session",
                    ]
                )
            self.assertEqual(result, 0)
            started = json.loads(output.getvalue())
            run_id = started["run"]["run_id"]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "runtime",
                        "finish",
                        run_id,
                        str(target),
                        "--status",
                        "succeeded",
                        "--next-signal",
                        "verify",
                    ]
                )
            self.assertEqual(result, 0)
            self.assertEqual(json.loads(output.getvalue())["status"], "succeeded")

            destination = (Path(raw) / "codex-skills").resolve()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "skills",
                        "install",
                        "--host",
                        "codex",
                        "--destination",
                        str(destination),
                        "--apply",
                    ]
                )
            self.assertEqual(result, 0)
            installed = json.loads(output.getvalue())
            self.assertTrue(installed["applied"])
            self.assertEqual(len(installed["proofs"]), len(SKILL_WORKFLOWS))


if __name__ == "__main__":
    unittest.main()
