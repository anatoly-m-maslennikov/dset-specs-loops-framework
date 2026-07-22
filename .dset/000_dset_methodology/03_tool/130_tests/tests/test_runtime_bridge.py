from __future__ import annotations

import contextlib
import io
import json
import shutil
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.cli import main
from dset_toolchain.layout import discover_layout
from dset_toolchain.runtime import RuntimeStateError, load_invocation
from dset_toolchain.runtime_bridge import (
    advance_runtime_closure,
    checkpoint_runtime,
    finish_runtime,
    handoff_runtime,
    read_runtime,
    start_child_runtime,
    start_runtime,
)
from dset_toolchain.skill_catalog import PUBLIC_SKILL_WORKFLOWS
from dset_toolchain.skill_context import resolve_skill_context
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.yaml_subset import dump
from tests import repository_root

ROOT = repository_root(Path(__file__))


class RuntimeBridgeTests(unittest.TestCase):
    def test_host_bridge_spans_process_shaped_calls(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter ünicode").resolve()
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

    def test_cli_handoff_preserves_explicit_session_until_terminal_finish(
        self,
    ) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            primary = resolve_skill_context(
                adopter,
                skill_id="dset",
                objective="Route the failing import",
                llm_session_ids=("codex:test-session",),
            )
            primary_run = cast(dict[str, Any], primary["run"])
            primary_run_id = str(primary_run["run_id"])
            session_id = str(primary_run["session_id"])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "runtime",
                        "handoff",
                        primary_run_id,
                        str(adopter),
                        "--next-signal",
                        "diagnose",
                    ]
                )
            self.assertEqual(result, 0)
            handed_off = json.loads(output.getvalue())
            self.assertEqual(handed_off["status"], "succeeded")
            self.assertEqual(handed_off["session_id"], session_id)
            checkpoint = read_runtime(adopter, session_id=session_id)
            assert checkpoint is not None
            self.assertEqual(checkpoint["status"], "active")
            self.assertEqual(checkpoint["active_run_ids"], [])

            with self.assertRaisesRegex(ValueError, "requires explicit session ID"):
                resolve_skill_context(
                    adopter,
                    skill_id="dset-diagnose",
                    objective="Do not infer handoff continuity",
                    llm_session_ids=("codex:test-session",),
                )

            specialist = resolve_skill_context(
                adopter,
                skill_id="dset-diagnose",
                objective="Diagnose the failing import",
                session_id=session_id,
                llm_session_ids=("codex:test-session",),
            )
            specialist_run = cast(dict[str, Any], specialist["run"])
            self.assertEqual(specialist_run["session_id"], session_id)
            self.assertEqual(specialist_run["root_run_id"], primary_run_id)
            self.assertEqual(specialist_run["parent_run_id"], primary_run_id)

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main(
                    [
                        "runtime",
                        "finish",
                        str(specialist_run["run_id"]),
                        str(adopter),
                        "--status",
                        "succeeded",
                    ]
                )
            self.assertEqual(result, 0)
            terminal = json.loads(output.getvalue())
            self.assertEqual(terminal["session_id"], session_id)
            checkpoint = read_runtime(adopter, session_id=session_id)
            assert checkpoint is not None
            self.assertEqual(checkpoint["status"], "completed")
            with self.assertRaisesRegex(RuntimeStateError, "session is not active"):
                resolve_skill_context(
                    adopter,
                    skill_id="dset-verify",
                    objective="Do not reopen a completed chain",
                    session_id=session_id,
                    llm_session_ids=("codex:test-session",),
                )

    def test_bridge_rejects_unknown_workflow_before_run_creation(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            with self.assertRaises(ValueError):
                start_runtime(
                    adopter,
                    public_entrypoint="dset",
                    workflow_id="not-registered",
                    objective="Do work",
                )
            self.assertFalse((adopter / ".dset" / "runs").exists())

    def test_public_skill_requires_llm_session_provenance(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            with self.assertRaisesRegex(ValueError, "host-session provenance"):
                start_runtime(
                    adopter,
                    public_entrypoint="dset-diagnose",
                    workflow_id="diagnosis",
                    objective="Diagnose with missing host provenance",
                )
            self.assertFalse((adopter / ".dset" / "runs").exists())

    def test_bridge_accepts_every_catalog_entry_and_rejects_mismatches(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            shutil.copytree(
                ROOT / ".dset",
                adopter / ".dset",
                ignore=shutil.ignore_patterns("runtime"),
            )
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
                    llm_session_ids=("codex:test-session",),
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
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            shutil.copytree(
                ROOT / ".dset",
                adopter / ".dset",
                ignore=shutil.ignore_patterns("runtime"),
            )
            shutil.copytree(ROOT / "skills", adopter / "skills")
            context = resolve_skill_context(
                adopter / "skills" / "dset-implement" / "SKILL.md",
                skill_id="dset-implement",
                objective="Implement the shared runtime",
                session_id="session-context-work-area",
                llm_session_ids=("codex:test-session",),
            )
            self.assertEqual(context["repository_root"], str(adopter))
            self.assertEqual(context["work_area"], "skills")
            self.assertEqual(context["workflow_id"], "implement")
            self.assertEqual(context["artifact_creation_strictness"], "medium")
            self.assertEqual(context["change_workspace_default"], "integration-branch")
            self.assertEqual(context["delegation_budget_profile"], "medium")
            semantic_routing = cast(dict[str, Any], context["semantic_routing"])
            self.assertEqual(
                semantic_routing["types"],
                ["decision", "question", "problem", "qa"],
            )
            self.assertGreater(semantic_routing["classification_count"], 0)
            self.assertEqual(
                semantic_routing["source"],
                ".dset/02_layer_gov/specification-work-items.md",
            )
            self.assertTrue(str(context["ruleset_identity"]).startswith("ruleset:"))
            closure = cast(dict[str, Any], context["closure"])
            self.assertEqual(closure["next_workflow"], "decisions")
            resolved = cast(dict[str, Any], context["resolved"])
            self.assertEqual(resolved["workflow_id"], "implement")
            run = cast(dict[str, Any], context["run"])
            finish_runtime(adopter, str(run["run_id"]), status="succeeded")

    def test_context_applies_strict_implementation_mode_without_prerequisites(
        self,
    ) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            settings = adopter / "dset_settings.toml"
            settings.write_text(
                settings.read_text(encoding="utf-8")
                .replace('mode = "lazy"', 'mode = "strict"')
                .replace(
                    'default_workspace = "integration-branch"',
                    'default_workspace = "branch-worktree"',
                )
                .replace('budget_profile = "medium"', 'budget_profile = "high"'),
                encoding="utf-8",
            )

            context = resolve_skill_context(
                adopter,
                skill_id="dset-implement",
                objective="Implement only from prepared authority",
                session_id="session-context-strict",
                llm_session_ids=("codex:test-session",),
            )

            self.assertEqual(context["implementation_preparation_mode"], "strict")
            self.assertEqual(context["change_workspace_default"], "branch-worktree")
            self.assertEqual(context["delegation_budget_profile"], "high")
            closure = cast(dict[str, Any], context["closure"])
            self.assertEqual(closure["implementation_mode"], "strict")
            self.assertEqual(closure["next_workflow"], "implement")
            with self.assertRaisesRegex(ValueError, "workflow mismatch"):
                start_child_runtime(
                    adopter,
                    session_id="session-context-strict",
                    workflow_id="decisions",
                    objective="Must not repair prerequisites",
                    llm_session_ids=("codex:test-session",),
                )
            run = cast(dict[str, Any], context["run"])
            finish_runtime(adopter, str(run["run_id"]), status="stopped")

    def test_context_returns_rootless_initialization_without_writing(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "new-project").resolve()
            context = resolve_skill_context(
                target,
                skill_id="dset-init",
                objective="Initialize the project",
            )
            self.assertEqual(context["status"], "initialization-required")
            self.assertIsNone(context["repository_root"])
            self.assertFalse(target.exists())

    def test_repair_context_is_bounded_to_governance_diagnostics(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            settings = adopter / "dset_settings.toml"
            settings.write_text("invalid project setting\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "governance is valid"):
                resolve_skill_context(
                    adopter,
                    skill_id="dset-repair-governance",
                    objective="Do not misroute a settings defect",
                )

            registry = discover_layout(adopter).governance_path
            registry.write_text("invalid governance\n", encoding="utf-8")
            context = resolve_skill_context(
                adopter,
                skill_id="dset-repair-governance",
                objective="Return bounded governance diagnostics",
            )
            self.assertEqual(context["status"], "invalid-governance")
            self.assertTrue(context["diagnostics"])

    def test_context_rejects_competing_project_roots(self) -> None:
        with temporary_directory() as raw:
            outer = (Path(raw) / "outer").resolve()
            shutil.copytree(
                ROOT / ".dset",
                outer / ".dset",
                ignore=shutil.ignore_patterns("runtime"),
            )
            nested = outer / "nested"
            manifest = nested / "dset" / "scopes" / "meta" / "dset.toml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                dump({"schema_version": "1.2"}, manifest), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "competing DSET project roots"):
                resolve_skill_context(
                    nested,
                    skill_id="dset-implement",
                    objective="Reject ambiguous authority",
                )

    def test_child_runs_advance_one_persisted_implementation_closure(self) -> None:
        with temporary_directory() as raw:
            adopter = (Path(raw) / "adopter").resolve()
            create_adopter(ROOT, adopter)
            started = start_runtime(
                adopter,
                public_entrypoint="dset-implement",
                workflow_id="implement",
                objective="Implement the bounded change",
                session_id="session-closure",
                llm_session_ids=("codex:test-session",),
            )
            root_run = cast(dict[str, Any], started["run"])
            child = start_child_runtime(
                adopter,
                session_id="session-closure",
                workflow_id="decisions",
                objective="Reconcile accepted directives",
                llm_session_ids=("codex:test-session",),
            )
            child_run = cast(dict[str, Any], child["run"])
            self.assertEqual(child_run["root_run_id"], root_run["run_id"])
            self.assertEqual(child_run["parent_run_id"], root_run["run_id"])
            self.assertEqual(child_run["invocation_source"], "chained-skill")
            handoff_runtime(
                adopter,
                str(child_run["run_id"]),
                next_signals=("plan-proof",),
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
                llm_session_ids=("codex:test-session",),
            )
            second_run = cast(dict[str, Any], second["run"])
            self.assertEqual(second_run["parent_run_id"], child_run["run_id"])
            handoff_runtime(
                adopter,
                str(second_run["run_id"]),
                next_signals=("plan-implementation",),
            )
            terminal = finish_runtime(
                adopter,
                str(root_run["run_id"]),
                status="succeeded",
            )
            self.assertEqual(terminal["status"], "succeeded")
            final_checkpoint = read_runtime(adopter, session_id="session-closure")
            assert final_checkpoint is not None
            self.assertEqual(final_checkpoint["status"], "completed")
            self.assertEqual(final_checkpoint["active_run_ids"], [])


if __name__ == "__main__":
    unittest.main()
