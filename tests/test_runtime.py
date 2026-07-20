from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dset_toolchain.runtime import (
    MAX_RECORD_BYTES,
    MAX_RUN_BYTES,
    AmbiguousSessionError,
    RunFinishedError,
    finish_run,
    resume_checkpoint,
    start_run,
    update_checkpoint,
)

ROOT = Path(__file__).resolve().parents[1]


class RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        manifest = self.root / "dset" / "scopes" / "meta" / "dset.yaml"
        manifest.parent.mkdir(parents=True)
        manifest.write_text('schema_version: "1.2"\n', encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_run_and_checkpoint_lifecycle_is_atomic_and_schema_shaped(self) -> None:
        invocation = start_run(
            self.root,
            public_entrypoint="dset",
            objective="Route the active change",
            workflow_id="lifecycle-orchestration",
            mode_id="verify",
            llm_session_ids=["codex:session-001"],
            next_mode="verify",
            next_reason_code="DSET-RUNTIME-VERIFY",
        )

        self.assertEqual(invocation.run["schema_version"], "1.2")
        self.assertEqual(invocation.run["status"], "running")
        self.assertEqual(invocation.run["persistence"], "persisted")
        self.assertIn("workspace", invocation.run["scope"])
        self.assertIsNotNone(invocation.running_path)
        assert invocation.running_path is not None
        self.assertTrue(invocation.running_path.is_file())
        checkpoint_path = (
            self.root / ".dset" / "sessions" / f"{invocation.session_id}.json"
        )
        first_checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        self.assertEqual(first_checkpoint["schema_version"], "1.2")
        self.assertEqual(first_checkpoint["latest_run_id"], invocation.run_id)
        self.assertIn("closure", first_checkpoint)

        updated = update_checkpoint(
            invocation,
            ruleset_identity="ruleset-001",
            completed=[
                {"kind": "workflow", "id": "verify", "path": None},
            ],
            pending=[
                {
                    "kind": "proof",
                    "id": "DSET-TEST-SKILL-009",
                    "path": "proofs/session.json",
                }
            ],
            touched_paths=["tests/test_runtime.py"],
            next_mode="complete",
            next_reason_code="DSET-RUNTIME-COMPLETE",
        )
        self.assertEqual(updated["sequence"], 1)
        self.assertEqual(updated["ruleset_identity"], "ruleset-001")

        terminal = finish_run(
            invocation,
            status="succeeded",
            outputs=["proofs/session.json"],
            next_signals=["complete"],
        )
        self.assertEqual(terminal["schema_version"], "1.2")
        self.assertEqual(terminal["status"], "succeeded")
        self.assertEqual(terminal["persistence"], "persisted")
        self.assertIsNotNone(terminal["finished_at"])
        self.assertFalse(invocation.running_path.is_file())
        terminals = [
            path
            for path in (self.root / ".dset" / "runs").glob("*.json")
            if not path.name.startswith(".")
        ]
        self.assertEqual(len(terminals), 1)
        persisted = json.loads(terminals[0].read_text(encoding="utf-8"))
        self.assertEqual(persisted, terminal)
        run_schema = json.loads(
            (ROOT / "dset/scopes/skill/schemas/skill-run.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(persisted), set(run_schema["required"]))
        self.assertLessEqual(terminals[0].stat().st_size, MAX_RECORD_BYTES)
        final_checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        checkpoint_schema = json.loads(
            (
                ROOT / "dset/scopes/skill/schemas/session-checkpoint.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(set(final_checkpoint), set(checkpoint_schema["required"]))
        self.assertEqual(final_checkpoint["status"], "completed")
        self.assertEqual(final_checkpoint["sequence"], 2)

        with self.assertRaises(RunFinishedError):
            finish_run(invocation, status="failed")
        self.assertEqual(
            json.loads(terminals[0].read_text(encoding="utf-8")), persisted
        )

    def test_resume_requires_one_compatible_active_checkpoint(self) -> None:
        scope = {
            "project": "dset",
            "change": "DSET-CHANGE-SKILL-001",
            "target": {"repository": True, "work_areas": []},
        }
        first = start_run(
            self.root,
            public_entrypoint="dset",
            objective="First session",
            workflow_id="lifecycle-orchestration",
            scope=scope,
        )
        explicit = resume_checkpoint(self.root, session_id=first.session_id)
        self.assertIsNotNone(explicit)
        assert explicit is not None
        self.assertEqual(explicit["session_id"], first.session_id)
        implicit = resume_checkpoint(self.root, scope=scope)
        self.assertIsNotNone(implicit)
        assert implicit is not None
        self.assertEqual(implicit["session_id"], first.session_id)

        second = start_run(
            self.root,
            public_entrypoint="dset-clarify",
            objective="Second session",
            workflow_id="domain-clarification",
            session_id="session-second",
            scope=scope,
        )
        self.assertNotEqual(first.session_id, second.session_id)
        with self.assertRaises(AmbiguousSessionError):
            resume_checkpoint(self.root, scope=scope)

        resumed = start_run(
            self.root,
            public_entrypoint="dset-diagnose",
            objective="Continue first session",
            workflow_id="diagnosis",
            session_id=first.session_id,
            scope=scope,
        )
        self.assertEqual(resumed.session_id, first.session_id)
        self.assertEqual(resumed.run["root_run_id"], first.run["root_run_id"])
        self.assertEqual(resumed.run["parent_run_id"], first.run_id)

    def test_absent_or_non_dset_root_never_creates_project_state(self) -> None:
        absent = self.root / "missing-project"
        invocation = start_run(
            absent,
            public_entrypoint="dset",
            objective="Explain initialization",
            workflow_id=None,
            next_mode="initialize",
            next_reason_code="DSET-RUNTIME-INITIALIZE",
        )
        terminal = finish_run(invocation, status="stopped", next_signals=["initialize"])
        self.assertEqual(terminal["persistence"], "unavailable")
        self.assertIsNone(terminal["checkpoint"])
        self.assertFalse(absent.exists())

        ordinary = self.root / "ordinary"
        ordinary.mkdir()
        second = start_run(
            ordinary,
            public_entrypoint="dset",
            objective="No implicit adoption",
            workflow_id=None,
            next_mode="initialize",
        )
        finish_run(second, status="stopped")
        self.assertFalse((ordinary / ".dset").exists())

    def test_retention_enforces_age_count_and_total_bytes(self) -> None:
        runs = self.root / ".dset" / "runs"
        seed = start_run(
            self.root,
            public_entrypoint="dset",
            objective="Create runtime directories",
            workflow_id="lifecycle-orchestration",
        )
        finish_run(seed, status="succeeded")
        old = runs / "old-run.json"
        old.write_text("{}\n", encoding="utf-8")
        old_time = (datetime.now(timezone.utc) - timedelta(days=31)).timestamp()
        os.utime(old, (old_time, old_time))
        for index in range(205):
            (runs / f"count-{index:03d}.json").write_text("{}\n", encoding="utf-8")
        for index in range(170):
            (runs / f"large-{index:03d}.json").write_bytes(b"x" * 130_000)

        trigger = start_run(
            self.root,
            public_entrypoint="dset",
            objective="Apply retention",
            workflow_id="lifecycle-orchestration",
            session_id="retention-session",
        )
        finish_run(trigger, status="succeeded")

        remaining = [
            path
            for path in runs.glob("*.json")
            if path.is_file() and not path.name.startswith(".")
        ]
        self.assertFalse(old.exists())
        self.assertLessEqual(len(remaining), 200)
        self.assertLessEqual(
            sum(path.stat().st_size for path in remaining), MAX_RUN_BYTES
        )


if __name__ == "__main__":
    unittest.main()
