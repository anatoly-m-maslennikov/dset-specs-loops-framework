from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.runtime import RuntimeStateError, load_invocation
from dset_toolchain.runtime_bridge import (
    advance_runtime_closure,
    checkpoint_runtime,
    finish_runtime,
    read_runtime,
    start_child_runtime,
    start_runtime,
)
from dset_toolchain.skill_catalog import PUBLIC_SKILL_WORKFLOWS
from dset_toolchain.skill_context import resolve_skill_context

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

    def test_bridge_accepts_every_catalog_entry_and_rejects_mismatches(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            adopter = Path(raw) / "adopter"
            shutil.copytree(ROOT / "dset", adopter / "dset")
            shutil.copytree(ROOT / "skills", adopter / "skills")
            for skill_id, workflow_id in PUBLIC_SKILL_WORKFLOWS.items():
                if skill_id in {"dset-init", "dset-repair-governance"}:
                    continue
                started = start_runtime(
                    adopter,
                    public_entrypoint=skill_id,
                    workflow_id=workflow_id,
                    objective=f"Run {skill_id}",
                    session_id=f"session-{skill_id}",
                )
                run = cast(dict[str, Any], started["run"])
                self.assertEqual(run["skill_id"], skill_id)
            with self.assertRaisesRegex(ValueError, "workflow mismatch"):
                start_runtime(
                    adopter,
                    public_entrypoint="dset-release",
                    workflow_id="diagnosis",
                    objective="Wrong pair",
                )

    def test_context_resolves_explicit_nested_work_area_target(self) -> None:
        context = resolve_skill_context(
            ROOT / "skills" / "dset-implement" / "SKILL.md",
            skill_id="dset-implement",
            objective="Implement the shared runtime",
            session_id="session-context-work-area",
            llm_session_ids=("codex:test-session",),
        )
        self.assertEqual(context["repository_root"], str(ROOT))
        self.assertEqual(context["work_area"], "skills")
        self.assertEqual(context["workflow_id"], "implement")
        self.assertEqual(context["artifact_creation_strictness"], "medium")
        semantic_routing = cast(dict[str, Any], context["semantic_routing"])
        self.assertEqual(
            semantic_routing["types"], ["decision", "question", "problem", "qa"]
        )
        self.assertGreater(semantic_routing["classification_count"], 0)
        self.assertEqual(
            semantic_routing["source"],
            "dset/scopes/gov/governance/work-items.md",
        )
        self.assertTrue(str(context["ruleset_identity"]).startswith("ruleset:"))
        closure = cast(dict[str, Any], context["closure"])
        self.assertEqual(closure["next_workflow"], "decisions")
        resolved = cast(dict[str, Any], context["resolved"])
        self.assertEqual(resolved["workflow_id"], "implement")

    def test_context_returns_rootless_initialization_without_writing(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            target = Path(raw) / "new-project"
            context = resolve_skill_context(
                target,
                skill_id="dset-init",
                objective="Initialize the project",
            )
            self.assertEqual(context["status"], "initialization-required")
            self.assertIsNone(context["repository_root"])
            self.assertFalse(target.exists())

    def test_repair_context_is_bounded_to_governance_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            adopter = Path(raw) / "adopter"
            create_adopter(ROOT, adopter)
            settings = adopter / "dset.toml"
            settings.write_text("invalid project setting\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "governance is valid"):
                resolve_skill_context(
                    adopter,
                    skill_id="dset-repair-governance",
                    objective="Do not misroute a settings defect",
                )

            registry = adopter / "dset" / "governance.yaml"
            registry.write_text("invalid governance\n", encoding="utf-8")
            context = resolve_skill_context(
                adopter,
                skill_id="dset-repair-governance",
                objective="Return bounded governance diagnostics",
            )
            self.assertEqual(context["status"], "invalid-governance")
            self.assertTrue(context["diagnostics"])

    def test_context_rejects_competing_project_roots(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            outer = Path(raw) / "outer"
            shutil.copytree(ROOT / "dset", outer / "dset")
            nested = outer / "nested"
            manifest = nested / "dset" / "scopes" / "meta" / "dset.yaml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text('schema_version: "1.2"\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "competing DSET project roots"):
                resolve_skill_context(
                    nested,
                    skill_id="dset-implement",
                    objective="Reject ambiguous authority",
                )

    def test_child_runs_advance_one_persisted_implementation_closure(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            adopter = Path(raw) / "adopter"
            create_adopter(ROOT, adopter)
            started = start_runtime(
                adopter,
                public_entrypoint="dset-implement",
                workflow_id="implement",
                objective="Implement the bounded change",
                session_id="session-closure",
            )
            root_run = cast(dict[str, Any], started["run"])
            child = start_child_runtime(
                adopter,
                session_id="session-closure",
                workflow_id="decisions",
                objective="Reconcile accepted directives",
            )
            child_run = cast(dict[str, Any], child["run"])
            self.assertEqual(child_run["root_run_id"], root_run["run_id"])
            self.assertEqual(child_run["parent_run_id"], root_run["run_id"])
            self.assertEqual(child_run["invocation_source"], "chained-skill")
            finish_runtime(
                adopter,
                str(child_run["run_id"]),
                status="succeeded",
                session_status="active",
            )

            checkpoint = advance_runtime_closure(
                adopter,
                session_id="session-closure",
                workflow_id="decisions",
                observations={
                    "proof_plan_complete": False,
                    "implementation_plan_complete": False,
                    "implementation_authorized": False,
                },
            )
            self.assertEqual(checkpoint["closure"]["next_workflow"], "plan-proof")
            second = start_child_runtime(
                adopter,
                session_id="session-closure",
                workflow_id="plan-proof",
                objective="Complete proof plans",
            )
            second_run = cast(dict[str, Any], second["run"])
            self.assertEqual(second_run["parent_run_id"], child_run["run_id"])


if __name__ == "__main__":
    unittest.main()
