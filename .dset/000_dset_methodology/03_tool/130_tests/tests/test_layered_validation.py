from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.cli import main
from dset_toolchain.layout import LAYERS, discover_layout
from dset_toolchain.scaffold import create_change
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.traceability import build_traceability
from dset_toolchain.validation import validate_change, validate_repository
from dset_toolchain.yaml_subset import dump, load
from tests import repository_root

ROOT = repository_root(Path(__file__))


class LayeredValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = temporary_directory()
        self.root = Path(self.temporary.name).resolve()
        self.scopes = self.root / "dset" / "scopes"
        for layer in LAYERS:
            (self.scopes / layer).mkdir(parents=True)
        for work_area in ("api", "web", "worker"):
            (self.root / "src" / work_area).mkdir(parents=True)
        self._write_project()
        self._write_control_files()
        self._write_fragment("meta", "DSET-REQUIREMENT-001", "DSET-TEST-001")
        self._write_fragment("tool", "DSET-REQUIREMENT-TOOL-001", "DSET-TEST-TOOL-001")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_layered_repository(self) -> None:
        self.assertEqual(validate_repository(self.root), [])

    def test_change_ids_may_be_owned_by_native_atomic_records(self) -> None:
        change = self._write_change("tool", "native-atoms")
        manifest_path = self._change_manifest(change)
        manifest = load(manifest_path)
        assert isinstance(manifest, dict)
        native_ids = {
            "requirements": "DSET-REQUIREMENT-TOOL-100",
            "tests": "DSET-TEST-TOOL-100",
            "evals": "DSET-EVALUATION-TOOL-100",
        }
        for sequence, (group, identifier) in enumerate(native_ids.items(), start=100):
            values = manifest[group]
            assert isinstance(values, list)
            values.append(identifier)
            carrier = change / f"DSET-ATOMIC-RECORD-{sequence}.md"
            carrier.write_text(f"# Native atom\n\n{identifier}\n", encoding="utf-8")
        manifest_path.write_text(dump(manifest), encoding="utf-8")

        messages = [
            diagnostic.message
            for diagnostic in validate_change(self.root, change, archived=False)
        ]

        for identifier in native_ids.values():
            self.assertNotIn(
                f"{identifier} is not present in its owning artifact", messages
            )

    def test_work_area_registry_requires_unique_safe_existing_directories(self) -> None:
        path = self.scopes / "meta" / "dset.yaml"
        baseline = load(path)
        assert isinstance(baseline, dict)
        valid = baseline["work_areas"]
        (self.root / "src" / "not-directory").write_text("fixture\n", encoding="utf-8")
        invalid_cases = (
            [valid[0], {**valid[1], "id": valid[0]["id"]}],
            [valid[0], {**valid[1], "path": valid[0]["path"]}],
            [{"id": "absolute", "path": "/tmp"}],
            [{"id": "drive", "path": "C:/src"}],
            [{"id": "escape", "path": "../outside"}],
            [{"id": "missing", "path": "src/missing"}],
            [
                {
                    "id": "not-directory",
                    "path": "src/not-directory",
                }
            ],
            [{"id": "windows", "path": "src\\api"}],
            [{"id": "dot", "path": "src/./api"}],
            [{"id": "empty", "path": "src//api"}],
        )
        for work_areas in invalid_cases:
            with self.subTest(work_areas=work_areas):
                manifest = dict(baseline)
                manifest["work_areas"] = work_areas
                path.write_text(dump(manifest), encoding="utf-8")
                self.assertIn(
                    "DSET-E143", {item.code for item in validate_repository(self.root)}
                )
        path.write_text(dump(baseline), encoding="utf-8")
        self.assertEqual(validate_repository(self.root), [])

    def test_intake_derives_layers_and_requires_stable_owner_change(self) -> None:
        path = self.scopes / "gov" / "intake.yaml"
        valid: dict[str, Any] = {
            "id": "DSET-QUESTION-GOV-001",
            "scope": "gov",
            "type": "question",
            "status": "open",
            "title": "Choice",
            "statement": "Which bounded option applies?",
            "owner_change": "DSET-CHANGE-GOV-001",
            "decision": "pending",
            "llm_session_ids": [],
            "external_refs": [],
        }
        baseline: dict[str, Any] = {"schema_version": "1.1", "items": [valid]}
        path.write_text(dump(baseline), encoding="utf-8")
        self.assertNotIn(
            "DSET-E142", {item.code for item in validate_repository(self.root)}
        )

        invalid_cases = (
            {**baseline, "scope_mode": "multi-scope", "scopes": []},
            {**baseline, "schema_version": 1.0},
            {**baseline, "items": [{**valid, "id": "DSET-PROBLEM-GOV-001"}]},
            {**baseline, "items": [{**valid, "scope": "tool"}]},
            {
                **baseline,
                "items": [{**valid, "owner_change": "legacy-change-slug"}],
            },
            {
                **baseline,
                "items": [{**valid, "decision": "DSET-DECISION-TOOL-001"}],
            },
        )
        for invalid in invalid_cases:
            with self.subTest(intake=invalid):
                path.write_text(dump(invalid), encoding="utf-8")
                self.assertIn(
                    "DSET-E142", {item.code for item in validate_repository(self.root)}
                )

    def test_current_intake_uses_flat_question_and_problem_subtypes(self) -> None:
        path = self.scopes / "gov" / "intake.yaml"
        conflict: dict[str, Any] = {
            "id": "DSET-CONFLICT-GOV-001",
            "scope": "gov",
            "type": "question",
            "subtype": "conflict",
            "status": "open",
            "title": "Incompatible authority",
            "statement": "Two applicable claims cannot both hold.",
            "owner_change": "DSET-CHANGE-GOV-001",
            "decision": "pending",
            "llm_session_ids": [],
            "external_refs": [],
        }
        path.write_text(
            dump({"schema_version": "1.2", "items": [conflict]}), encoding="utf-8"
        )

        self.assertNotIn(
            "DSET-E142", {item.code for item in validate_repository(self.root)}
        )

        conflict["type"] = "problem"
        path.write_text(
            dump({"schema_version": "1.2", "items": [conflict]}), encoding="utf-8"
        )
        codes = {item.code for item in validate_repository(self.root)}
        self.assertIn("DSET-E142", codes)
        self.assertIn("DSET-E166", codes)

    def test_atomic_artifacts_require_explicit_session_provenance(self) -> None:
        intake_path = self.scopes / "gov" / "intake.yaml"
        item: dict[str, Any] = {
            "id": "DSET-QUESTION-GOV-001",
            "scope": "gov",
            "type": "question",
            "status": "open",
            "title": "Choice",
            "statement": "Which bounded option applies?",
            "owner_change": "DSET-CHANGE-GOV-001",
            "decision": "pending",
            "external_refs": [],
        }
        intake_path.write_text(
            dump({"schema_version": "1.1", "items": [item]}), encoding="utf-8"
        )
        self.assertIn(
            "DSET-E155", {item.code for item in validate_repository(self.root)}
        )
        item["llm_session_ids"] = []
        intake_path.write_text(
            dump({"schema_version": "1.1", "items": [item]}), encoding="utf-8"
        )

        change = self._write_change("gov", "session-provenance", id_layer="GOV")
        manifest_path = self._change_manifest(change)
        manifest = load(manifest_path)
        assert isinstance(manifest, dict)
        manifest.pop("llm_session_ids")
        manifest_path.write_text(dump(manifest), encoding="utf-8")
        self.assertIn(
            "DSET-E155",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )
        manifest["llm_session_ids"] = ["missing-host-prefix"]
        manifest_path.write_text(dump(manifest), encoding="utf-8")
        self.assertIn(
            "DSET-E155",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )
        manifest["llm_session_ids"] = []
        manifest_path.write_text(dump(manifest), encoding="utf-8")

        decision = change / "decision-DSET-DECISION-GOV-099.md"
        decision.write_text("# Decision\n", encoding="utf-8")
        proof = change / "proofs" / "bounded-proof.md"
        proof.parent.mkdir()
        proof.write_text("# Proof\n", encoding="utf-8")
        self.assertIn(
            "DSET-E155",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )
        for path, title in ((decision, "Decision"), (proof, "Proof")):
            path.write_text(
                f"# {title}\n\n- **LLM session IDs:** none\n", encoding="utf-8"
            )
        self.assertNotIn(
            "DSET-E155",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )

        proof.write_text(
            "+++\n"
            'artifact_type = "evidence_record"\n'
            'artifact_id = "DSET-EVIDENCE-RECORD-099"\n'
            'llm_session_ids = ["codex:session-099"]\n'
            "+++\n\n"
            "# Proof\n",
            encoding="utf-8",
        )
        self.assertNotIn(
            "DSET-E155",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )

    def test_change_target_is_repository_or_declared_work_areas(self) -> None:
        change = self._write_change("tool", "targeted-change")
        path = self._change_manifest(change)
        data = load(path)
        assert isinstance(data, dict)
        self.assertEqual(data["target"], {"repository": True, "work_areas": []})
        self.assertEqual(validate_change(self.root, change, archived=False), [])

        valid_target = {"repository": False, "work_areas": ["api", "web"]}
        data["target"] = valid_target
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertEqual(validate_change(self.root, change, archived=False), [])

        invalid_targets = (
            {"repository": False, "work_areas": ["unknown"]},
            {"repository": True, "work_areas": ["api"]},
            {"repository": False, "work_areas": []},
            {"repository": False, "work_areas": ["api", "api"]},
            {"repository": True},
            None,
        )
        for target in invalid_targets:
            with self.subTest(target=target):
                data["target"] = target
                path.write_text(dump(data, path), encoding="utf-8")
                self.assertIn(
                    "DSET-E148",
                    {
                        item.code
                        for item in validate_change(self.root, change, archived=False)
                    },
                )

    def test_fragment_ownership_and_cross_fragment_uniqueness(self) -> None:
        path = self._fragment_path("tool")
        data = load(path)
        assert isinstance(data, dict)
        data["requirements"] = ["DSET-REQUIREMENT-001"]
        path.write_text(dump(data, path), encoding="utf-8")
        (path.parent / "spec.md").write_text(
            "# DSET-REQUIREMENT-001\n", encoding="utf-8"
        )

        codes = {item.code for item in validate_repository(self.root)}

        self.assertIn("DSET-E146", codes)
        self.assertIn("DSET-E147", codes)

    def test_missing_and_misidentified_fragments_are_distinct(self) -> None:
        self._fragment_path("tool").unlink()
        self.assertIn(
            "DSET-E144", {item.code for item in validate_repository(self.root)}
        )
        self._write_fragment("tool", "DSET-REQUIREMENT-TOOL-001", "DSET-TEST-TOOL-001")
        path = self._fragment_path("tool")
        data = load(path)
        assert isinstance(data, dict)
        data["layer"] = "skill"
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertIn(
            "DSET-E145", {item.code for item in validate_repository(self.root)}
        )

    def test_change_layer_and_duplicate_change_ids_are_rejected(self) -> None:
        first = self._write_change("tool", "layered-change")
        self.assertEqual(validate_change(self.root, first, archived=False), [])
        first_manifest = self._change_manifest(first)
        data = load(first_manifest)
        assert isinstance(data, dict)
        data["primary_layer"] = "skill"
        data["affected_layers"] = ["skill"]
        first_manifest.write_text(dump(data, first_manifest), encoding="utf-8")
        self.assertIn(
            "DSET-E148",
            {item.code for item in validate_change(self.root, first, archived=False)},
        )
        self._write_change(
            "ops",
            "layered-change",
            id_layer="OPS",
            stable_id="DSET-CHANGE-TOOL-099",
        )
        self.assertIn(
            "DSET-E149", {item.code for item in validate_repository(self.root)}
        )

    def test_schema_1_2_shapes_are_explicit(self) -> None:
        project = json.loads(
            (ROOT / ".dset/01_layer_meta/schemas/project.schema.json").read_text(
                encoding="utf-8"
            )
        )
        fragment = json.loads(
            (
                ROOT / ".dset/01_layer_meta/schemas/package-fragment.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertIn(
            "layered-v1",
            project["$defs"]["layered_structure"]["properties"]["layout"]["enum"],
        )
        change = json.loads(
            (ROOT / ".dset/02_layer_gov/schemas/change.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            change["$defs"]["workspace"]["properties"]["isolation"]["enum"],
            ["integration-branch", "branch-worktree"],
        )
        self.assertEqual(
            set(
                change["$defs"]["layered_release_declaration"]["properties"]["policy"][
                    "enum"
                ]
            ),
            {
                "dset/scopes/ops/governance/release.md",
                ".dset/05_layer_ops/procedure-release.md",
            },
        )
        forbidden = project["allOf"][0]["then"]["not"]["anyOf"]
        self.assertEqual(
            {item["required"][0] for item in forbidden},
            {"contracts", "stories", "outcomes"},
        )
        self.assertEqual(
            set(fragment["required"]),
            {
                "schema_version",
                "package_id",
                "layer",
                "requirements",
                "tests",
                "evals",
                "contracts",
                "stories",
                "outcomes",
                "artifacts",
            },
        )

    def test_distributed_schema_ids_match_layer_owned_paths(self) -> None:
        base = (
            "https://raw.githubusercontent.com/anatoly-m-maslennikov/"
            "dset-specs-loops-framework/main/"
        )
        for path in sorted((ROOT / ".dset").glob("*/schemas/*.json")):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    schema["$id"], base + path.relative_to(ROOT).as_posix()
                )

    def test_schema_1_2_work_area_contract_has_two_target_modes(self) -> None:
        project = json.loads(
            (ROOT / ".dset/01_layer_meta/schemas/project.schema.json").read_text(
                encoding="utf-8"
            )
        )
        change = json.loads(
            (ROOT / ".dset/02_layer_gov/schemas/change.schema.json").read_text(
                encoding="utf-8"
            )
        )
        traceability = json.loads(
            (ROOT / ".dset/03_layer_tool/schemas/traceability.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("work_areas", project["allOf"][0]["then"]["required"])
        self.assertEqual(project["allOf"][0]["else"]["not"]["required"], ["work_areas"])
        self.assertNotIn("minItems", project["$defs"]["work_areas"])
        self.assertTrue(project["$defs"]["work_areas"]["uniqueItems"])
        self.assertEqual(
            set(project["$defs"]["work_area"]["required"]),
            {"id", "path"},
        )
        path_pattern = project["$defs"]["repository_relative_path"]["pattern"]
        for valid in ("src", "apps/web-ui", "docs/Product Notes"):
            self.assertIsNotNone(re.fullmatch(path_pattern, valid))
        for invalid in ("/src", "../src", "apps/../src", "apps//src", "C:/src"):
            self.assertIsNone(re.fullmatch(path_pattern, invalid))

        self.assertIn("target", change["allOf"][1]["then"]["required"])
        legacy_only = change["allOf"][1]["else"]["not"]["anyOf"]
        self.assertIn({"required": ["target"]}, legacy_only)
        target = change["$defs"]["target"]
        self.assertEqual(len(target["oneOf"]), 2)
        repository_mode, work_area_mode = target["oneOf"]
        self.assertTrue(repository_mode["properties"]["repository"]["const"])
        self.assertEqual(repository_mode["properties"]["work_areas"]["maxItems"], 0)
        self.assertFalse(work_area_mode["properties"]["repository"]["const"])
        self.assertEqual(work_area_mode["properties"]["work_areas"]["minItems"], 1)
        trace_current = traceability["allOf"][0]["then"]["properties"]["changes"][
            "items"
        ]
        self.assertIn("target", trace_current["required"])
        trace_legacy = traceability["allOf"][0]["else"]["properties"]["changes"][
            "items"
        ]["not"]["anyOf"]
        self.assertIn({"required": ["target"]}, trace_legacy)
        self.assertEqual(traceability["$defs"]["target"]["oneOf"], target["oneOf"])

    def test_layered_traceability_carries_change_layers(self) -> None:
        self._write_change(
            "tool",
            "layered-change",
            target={"repository": False, "work_areas": ["web", "api"]},
        )

        trace = build_traceability(self.root)

        self.assertEqual(trace["schema_version"], "1.3")
        self.assertEqual(trace["changes"][0]["primary_layer"], "tool")
        self.assertEqual(trace["changes"][0]["affected_layers"], ["tool"])
        self.assertEqual(trace["changes"][0]["slug"], "layered-change")
        self.assertEqual(
            trace["changes"][0]["target"],
            {"repository": False, "work_areas": ["api", "web"]},
        )
        self.assertEqual(
            trace["changes"][0]["workspace"]["isolation"], "integration-branch"
        )

    def test_native_atomic_record_can_own_a_change_decision(self) -> None:
        change = self._write_change("tool", "native-decision")
        manifest_path = self._change_manifest(change)
        manifest = load(manifest_path)
        assert isinstance(manifest, dict)
        manifest["decisions"] = ["DSET-DECISION-TOOL-099"]
        manifest_path.write_text(dump(manifest), encoding="utf-8")
        atom = change / "DSET-ATOMIC-RECORD-099-native-decision.md"
        atom.write_text(
            "---\n"
            "artifact_type: atomic_record\n"
            "artifact_id: DSET-ATOMIC-RECORD-099\n"
            "type: decision\n"
            "semantic_id: DSET-DECISION-TOOL-099\n"
            "status: accepted\n"
            "priority: medium\n"
            "llm_session_ids: []\n"
            "---\n\n"
            "# Decision\n",
            encoding="utf-8",
        )

        diagnostics = validate_change(self.root, change, archived=False)

        self.assertNotIn("DSET-E106", {item.code for item in diagnostics})

    def test_workspace_and_dependency_currentness_are_enforced(self) -> None:
        change = self._write_change("tool", "layered-change")
        path = self._change_manifest(change)
        data = load(path)
        assert isinstance(data, dict)
        data["dependencies"] = [
            {
                "change_id": "DSET-CHANGE-GOV-001",
                "pull_request": {
                    "repository": "example/project",
                    "number": "pending",
                    "url": "pending",
                },
                "required_commit": "pending",
                "consumes": ["DSET-CONTRACT-GOV-001"],
                "claim": "The governance contract exists.",
                "use": "Validate the generated tool configuration.",
                "evidence": "proofs/governance-dependency.md",
                "checked_at": "2026-07-15",
                "reopen_when": "The required commit changes.",
                "status": "available",
            }
        ]
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertIn(
            "DSET-E153",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )
        data["dependencies"][0]["pull_request"] = {
            "repository": "example/project",
            "number": 7,
            "url": "https://github.com/example/project/pull/7",
        }
        data["dependencies"][0]["required_commit"] = "a" * 40
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertEqual(validate_change(self.root, change, archived=False), [])

    def test_candidate_must_match_workspace_head_only_when_verified(self) -> None:
        change = self._write_change("tool", "candidate-change")
        path = self._change_manifest(change)
        data = load(path)
        assert isinstance(data, dict)
        data["workspace"]["head_commit"] = "a" * 40
        data["release"] = {
            "policy": "dset/scopes/ops/governance/release.md",
            "class": "small",
            "base": {
                "ref": "main",
                "commit": "b" * 40,
                "version": "0.3.0",
            },
            "target": "0.3.1",
            "readiness": "TEST-READINESS-RECORD-001-release.md",
            "candidate_commit": "c" * 40,
        }
        data["status"] = "in-progress"
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertNotIn(
            "DSET-E152",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )
        data["status"] = "verified"
        path.write_text(dump(data, path), encoding="utf-8")
        self.assertIn(
            "DSET-E152",
            {item.code for item in validate_change(self.root, change, archived=False)},
        )

    def test_scaffold_allocates_stable_change_ids_separately_from_slugs(self) -> None:
        self._install_change_templates()

        first = create_change(
            self.root, "portable-cli", "sample", "small", layer="tool"
        )
        second = create_change(
            self.root, "dependency-check", "sample", "small", layer="tool"
        )

        first_data = load(self._change_manifest(first))
        second_data = load(self._change_manifest(second))
        assert isinstance(first_data, dict)
        assert isinstance(second_data, dict)
        self.assertEqual(first_data["id"], "DSET-CHANGE-TOOL-001")
        self.assertEqual(first_data["slug"], "portable-cli")
        self.assertEqual(second_data["id"], "DSET-CHANGE-TOOL-002")
        self.assertEqual(first_data["workspace"]["isolation"], "integration-branch")
        self.assertEqual(first_data["workspace"]["branch"], "dev")
        self.assertEqual(first_data["workspace"]["base_ref"], "main")
        self.assertEqual(first_data["target"], {"repository": True, "work_areas": []})

        isolated = create_change(
            self.root,
            "isolated-change",
            "sample",
            "small",
            layer="tool",
            workspace_mode="branch-worktree",
        )
        isolated_data = load(self._change_manifest(isolated))
        assert isinstance(isolated_data, dict)
        self.assertEqual(isolated_data["workspace"]["isolation"], "branch-worktree")
        self.assertEqual(isolated_data["workspace"]["branch"], "dset/isolated-change")
        self.assertEqual(isolated_data["workspace"]["base_ref"], "dev")

        (self.root / "dset_settings.toml").write_text(
            "\n".join(
                (
                    'schema_version = "1.2"',
                    "[changes]",
                    'default_workspace = "branch-worktree"',
                    "",
                )
            ),
            encoding="utf-8",
        )
        configured = create_change(
            self.root,
            "settings-isolated-change",
            "sample",
            "small",
            layer="tool",
        )
        configured_data = load(self._change_manifest(configured))
        assert isinstance(configured_data, dict)
        self.assertEqual(configured_data["workspace"]["isolation"], "branch-worktree")
        self.assertEqual(
            configured_data["workspace"]["branch"],
            "dset/settings-isolated-change",
        )

        targeted = create_change(
            self.root,
            "targeted-change",
            "sample",
            "small",
            layer="tool",
            work_areas=["web", "api"],
        )
        targeted_data = load(self._change_manifest(targeted))
        assert isinstance(targeted_data, dict)
        self.assertEqual(
            targeted_data["target"],
            {"repository": False, "work_areas": ["api", "web"]},
        )
        with self.assertRaisesRegex(ValueError, "undeclared work-area"):
            create_change(
                self.root,
                "unknown-target",
                "sample",
                "small",
                layer="tool",
                work_areas=["unknown"],
            )
        with self.assertRaisesRegex(ValueError, "must be unique"):
            create_change(
                self.root,
                "duplicate-target",
                "sample",
                "small",
                layer="tool",
                work_areas=["api", "api"],
            )

    def test_cli_new_accepts_repeatable_work_area_targets(self) -> None:
        self._install_change_templates()
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(
                [
                    "new",
                    "cli-targeted-change",
                    "--root",
                    str(self.root),
                    "--package",
                    "sample",
                    "--profile",
                    "small",
                    "--layer",
                    "TOOL",
                    "--work-area",
                    "web",
                    "--work-area",
                    "api",
                    "--workspace",
                    "branch-worktree",
                ]
            )
        self.assertEqual(result, 0)
        change = self.scopes / "tool" / "changes" / "cli-targeted-change"
        data = load(self._change_manifest(change))
        assert isinstance(data, dict)
        self.assertEqual(
            data["target"],
            {"repository": False, "work_areas": ["api", "web"]},
        )
        self.assertEqual(data["workspace"]["isolation"], "branch-worktree")
        self.assertEqual(data["workspace"]["base_ref"], "dev")

    def test_workspace_branch_is_unique_only_while_changes_are_active(self) -> None:
        first = self._write_change(
            "tool", "first-change", stable_id="DSET-CHANGE-TOOL-101"
        )
        second = self._write_change(
            "tool", "second-change", stable_id="DSET-CHANGE-TOOL-102"
        )
        for change in (first, second):
            manifest = self._change_manifest(change)
            data = load(manifest)
            assert isinstance(data, dict)
            data["pull_request"] = {
                "repository": "example/project",
                "number": 13,
                "url": "https://github.com/example/project/pull/13",
            }
            manifest.write_text(dump(data, manifest), encoding="utf-8")
        self.assertNotIn(
            "DSET-E154", {item.code for item in validate_repository(self.root)}
        )
        first_manifest = self._change_manifest(first)
        second_manifest = self._change_manifest(second)
        first_data = load(first_manifest)
        second_data = load(second_manifest)
        assert isinstance(first_data, dict)
        assert isinstance(second_data, dict)
        first_data["workspace"]["isolation"] = "branch-worktree"
        first_data["workspace"]["branch"] = "dset/first-change"
        first_data["workspace"]["base_ref"] = "dev"
        first_manifest.write_text(dump(first_data, first_manifest), encoding="utf-8")
        second_data["workspace"]["isolation"] = "branch-worktree"
        second_data["workspace"]["branch"] = "dset/first-change"
        second_data["workspace"]["base_ref"] = "dev"
        second_manifest.write_text(dump(second_data, second_manifest), encoding="utf-8")
        self.assertIn(
            "DSET-E154", {item.code for item in validate_repository(self.root)}
        )

        self._archive_synthetic(first, "2026-07-14", 11)
        self._archive_synthetic(second, "2026-07-15", 12)
        self.assertNotIn(
            "DSET-E154", {item.code for item in validate_repository(self.root)}
        )

    def _write_project(self) -> None:
        manifest: dict[str, Any] = {
            "schema_version": "1.2",
            "project": {
                "key": "DSET",
                "id": "layered-fixture",
                "name": "Layered fixture",
                "repository_slug": "layered-fixture",
                "repository_role": "adopter",
            },
            "supportability": {
                "status": "not-applicable",
                "reason": "Synthetic local fixture",
                "authority": "fixture",
                "runbook": "not-applicable",
            },
            "release": {
                "status": "applicable",
                "integration_branch": "dev",
                "protected_branch": "main",
                "publisher": "github",
                "tag_pattern": "v{product_version}",
            },
            "work_items": {"registry": "dset/scopes/gov/intake.yaml"},
            "structure": {"layout": "layered-v1"},
            "work_areas": [
                {"id": "api", "path": "src/api"},
                {"id": "web", "path": "src/web"},
                {"id": "worker", "path": "src/worker"},
            ],
            "packages": [
                {"id": "sample", "status": "active", "layers": ["meta", "tool"]}
            ],
            "profiles": {
                "runtime_risk": "low",
                "durability_topology": "files",
                "enforcement": "local",
            },
            "change_contract": {
                "change_id_format": "project-type-layer-sequence",
                "change_slug_format": "kebab-case",
                "pull_request_required_before_archive": True,
                "archive_requires_fresh_verification": True,
                "keep_pull_request_draft_until_archive_ready": True,
            },
            "commit_provenance": {"start_commit": "manifest-addition"},
            "verification": {"commands": ["python -m dset_toolchain check ."]},
            "canonical_command": "python -m dset_toolchain check .",
        }
        (self.scopes / "meta" / "dset.yaml").write_text(
            dump(manifest), encoding="utf-8"
        )

    def _write_control_files(self) -> None:
        (self.scopes / "gov" / "intake.yaml").write_text(
            dump({"schema_version": "1.1", "items": []}),
            encoding="utf-8",
        )
        (self.scopes / "gov" / "provenance.yaml").write_text(
            dump({"schema_version": 1.0, "sources": []}), encoding="utf-8"
        )
        history = self.scopes / "ops" / "history" / "pull-requests.yaml"
        history.parent.mkdir(parents=True)
        history.write_text(dump({"repository": "example/project"}), encoding="utf-8")
        template = self.scopes / "gov" / "templates" / "profiles.yaml"
        template.parent.mkdir(parents=True)
        template.write_text(
            dump({"schema_version": 1.0, "profiles": {"small": {}}}),
            encoding="utf-8",
        )

    def _fragment_path(self, layer: str) -> Path:
        return self.scopes / layer / "specs/packages/sample/package.yaml"

    def _write_fragment(self, layer: str, requirement: str, test: str) -> None:
        root = self._fragment_path(layer).parent
        root.mkdir(parents=True, exist_ok=True)
        artifacts = {
            "hub": "README.md",
            "domain": "domain.md",
            "spec": "spec.md",
            "contracts": "contracts.md",
            "stories": "stories.md",
            "outcomes": "outcomes.md",
            "test_plan": "test-plan.md",
            "eval_plan": "eval-plan.md",
        }
        data = {
            "schema_version": "1.2",
            "package_id": "sample",
            "layer": layer,
            "requirements": [requirement],
            "tests": [test],
            "evals": [],
            "contracts": [],
            "stories": [],
            "outcomes": [],
            "artifacts": artifacts,
        }
        self._fragment_path(layer).write_text(dump(data), encoding="utf-8")
        for field, filename in artifacts.items():
            content = f"# {field}\n"
            if field == "spec":
                content += f"\n## {requirement}\n"
            elif field == "test_plan":
                content += f"\n## {test}\n"
            (root / filename).write_text(content, encoding="utf-8")

    def _write_change(
        self,
        layer: str,
        change_slug: str,
        *,
        id_layer: str = "TOOL",
        stable_id: str | None = None,
        target: dict[str, object] | None = None,
    ) -> Path:
        root = self.scopes / layer / "changes" / change_slug
        (root / "specs").mkdir(parents=True)
        requirement = f"DSET-REQUIREMENT-{id_layer}-099"
        test = f"DSET-TEST-{id_layer}-099"
        data = {
            "schema_version": "1.2",
            "id": stable_id or f"DSET-CHANGE-{id_layer}-099",
            "slug": change_slug,
            "profile": "small",
            "status": "proposed",
            "primary_layer": layer,
            "affected_layers": [layer],
            "target": target or {"repository": True, "work_areas": []},
            "workspace": {
                "isolation": "integration-branch",
                "branch": "dev",
                "base_ref": "main",
                "base_commit": "pending",
                "head_commit": "pending",
            },
            "dependencies": [],
            "llm_session_ids": [],
            "packages": ["sample"],
            "pull_request": {
                "repository": "example/project",
                "number": "pending",
                "url": "pending",
            },
            "release": {"owner_change": stable_id or f"DSET-CHANGE-{id_layer}-099"},
            "intake": [],
            "requirements": [requirement],
            "tests": [test],
            "evals": [],
            "decisions": [],
            "contracts": [],
            "stories": [],
            "outcomes": [],
        }
        (root / "change.yaml").write_text(dump(data), encoding="utf-8")
        (root / "specs/feature.md").write_text(f"# {requirement}\n", encoding="utf-8")
        (root / "test-plan.md").write_text(f"# {test}\n", encoding="utf-8")
        (root / "eval-plan.md").write_text(
            "# Eval plan\n\nNot applicable to this fixture.\n", encoding="utf-8"
        )
        return root

    def _install_change_templates(self) -> None:
        target = self.scopes / "gov" / "templates" / "change"
        source = (
            discover_layout(ROOT).find_template("change/layered/change.yaml").parents[1]
        )
        shutil.copytree(source, target)

    def _archive_synthetic(self, change: Path, day: str, pr_number: int) -> None:
        path = self._change_manifest(change)
        data = load(path)
        assert isinstance(data, dict)
        layer = str(data["primary_layer"])
        destination = self.scopes / layer / "changes/archive" / f"{day}-{data['slug']}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        data["status"] = "archived"
        data["pull_request"] = {
            "repository": "example/project",
            "number": pr_number,
            "url": f"https://github.com/example/project/pull/{pr_number}",
        }
        data["workspace"]["base_commit"] = "a" * 40
        data["workspace"]["head_commit"] = "b" * 40
        data["archive"] = {
            "date": day,
            "path": destination.relative_to(self.root).as_posix(),
        }
        path.write_text(dump(data, path), encoding="utf-8")
        change.replace(destination)

    def _change_manifest(self, change: Path) -> Path:
        return discover_layout(self.root).structured_file(change, "change.yaml")


if __name__ == "__main__":
    unittest.main()
