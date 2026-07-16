from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.runtime import RuntimeStateError, load_invocation
from dset_toolchain.runtime_bridge import (
    checkpoint_runtime,
    finish_runtime,
    read_runtime,
    start_runtime,
)

ROOT = Path(__file__).resolve().parents[1]


class RuntimeBridgeTests(unittest.TestCase):
    def test_host_bridge_spans_process_shaped_calls(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            adopter = Path(raw) / "adopter ünicode"
            create_adopter(ROOT, adopter)
            started = start_runtime(
                adopter,
                public_entrypoint="dset-diagnose",
                workflow_id="diagnosis",
                objective="Diagnose the failing import",
                mode_id="diagnose",
                llm_session_ids=("codex:test-session",),
            )
            run = cast(dict[str, Any], started["run"])
            self.assertIsInstance(run, dict)
            run_id = str(run["run_id"])
            session_id = str(run["session_id"])
            checkpoint = checkpoint_runtime(
                adopter,
                run_id,
                status="paused",
                next_mode="verify",
                next_reason_code="DSET-RUNTIME-EVIDENCE-READY",
            )
            self.assertEqual(checkpoint["status"], "paused")
            self.assertEqual(read_runtime(adopter, session_id=session_id), checkpoint)
            terminal = finish_runtime(
                adopter,
                run_id,
                status="succeeded",
                outputs=("proofs/diagnosis.md",),
                next_signals=("verify",),
            )
            self.assertEqual(terminal["status"], "succeeded")
            self.assertEqual(terminal["persistence"], "persisted")
            with self.assertRaises(RuntimeStateError):
                load_invocation(adopter, run_id)

    def test_bridge_rejects_unknown_workflow_before_run_creation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            adopter = Path(raw) / "adopter"
            create_adopter(ROOT, adopter)
            with self.assertRaises(ValueError):
                start_runtime(
                    adopter,
                    public_entrypoint="dset",
                    workflow_id="not-registered",
                    objective="Do work",
                )
            self.assertFalse((adopter / ".dset" / "runs").exists())


if __name__ == "__main__":
    unittest.main()
