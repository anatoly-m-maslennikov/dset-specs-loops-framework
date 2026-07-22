"""Verify DSET governance behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import shutil
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.adopter import create_adopter
from dset_toolchain.cli import main
from dset_toolchain.errors import DsetCommandError
from dset_toolchain.governance import (
    diff_governance,
    find_repository,
    materialize_governance,
    refresh_customization,
    resolve_workflow,
    validate_governance,
)
from dset_toolchain.layout import discover_layout
from dset_toolchain.legacy_authority import write_legacy_authority_ledger
from dset_toolchain.skill_catalog import REGISTERED_SKILL_WORKFLOWS
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.validation import validate_repository
from dset_toolchain.yaml_subset import dump, load
from tests import repository_root

# ROOT locates the repository fixture; repository layout is authoritative.
ROOT = repository_root(Path(__file__))


def _framework_schema(name: str) -> Path:
    return next(
        path for path in discover_layout(ROOT).schema_paths() if path.name == name
    )


class GovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = temporary_directory()
        self.root = (Path(self.temporary.name) / "adopter").resolve()
        create_adopter(ROOT, self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_registry_resolves_stable_order(self) -> None:
        self.assertEqual(validate_governance(self.root), [])
        registry = cast(
            dict[str, Any], load(discover_layout(self.root).governance_path)
        )
        self.assertEqual(registry["schema_version"], 1.1)
        self.assertTrue(
            all(
                "precedence_over" in rule
                for rule in cast(list[dict[str, Any]], registry["rules"])
            )
        )
        resolved, diagnostics = resolve_workflow(self.root, "domain-clarification")
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved["workflow_id"], "domain-clarification")
        self.assertEqual(resolved["customization"], "unmodified")
        self.assertGreater(len(cast(list[Any], resolved["rules"])), 3)
        self.assertTrue(
            all(
                "precedence_over" in rule
                for rule in cast(list[dict[str, Any]], resolved["rules"])
            )
        )

    def test_find_repository_walks_upward(self) -> None:
        nested = self.root / "src" / "feature"
        nested.mkdir(parents=True)
        self.assertEqual(find_repository(nested), self.root)

    def test_cli_resolve_reports_rule_identity(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(
                [
                    "rules",
                    "resolve",
                    "domain-clarification",
                    str(self.root),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(result, 0)
        output = stream.getvalue()
        self.assertIn('"workflow_id": "domain-clarification"', output)
        self.assertIn('"customization": "unmodified"', output)
        self.assertIn('"status": "unavailable"', output)
        self.assertIn("DSET-CONFLICT-RESOLUTION-UNAVAILABLE", output)

    def test_empty_conflicts_do_not_claim_resolution_coverage(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "diagnosis")
        self.assertEqual(diagnostics, [])
        assert resolved is not None
        self.assertEqual(resolved["conflicts"], [])
        self.assertEqual(
            resolved["conflict_resolution"],
            {
                "status": "unavailable",
                "coverage": [],
                "reason_code": "DSET-CONFLICT-RESOLUTION-UNAVAILABLE",
            },
        )

    def test_resolution_is_stable_and_read_only(self) -> None:
        registry = discover_layout(self.root).governance_path
        before = hashlib.sha256(registry.read_bytes()).hexdigest()
        first, first_diagnostics = resolve_workflow(self.root, "diagnosis")
        second, second_diagnostics = resolve_workflow(self.root, "diagnosis")
        self.assertEqual(first_diagnostics, [])
        self.assertEqual(second_diagnostics, [])
        self.assertEqual(first, second)
        self.assertEqual(hashlib.sha256(registry.read_bytes()).hexdigest(), before)

    def test_registry_failure_codes_are_stable(self) -> None:
        cases = {
            "missing-registry": ("DSET-E130", self._remove_registry),
            "missing-owner": ("DSET-E131", self._missing_owner),
            "duplicate-owner": ("DSET-E132", self._duplicate_owner),
            "missing-document": ("DSET-E133", self._missing_document),
            "outside-root": ("DSET-E134", self._outside_root),
            "dependency-cycle": ("DSET-E135", self._dependency_cycle),
            "precedence-cycle": ("DSET-E150", self._precedence_cycle),
            "missing-precedence": ("DSET-E150", self._missing_precedence),
            "missing-precedence-owner": (
                "DSET-E150",
                self._missing_precedence_owner,
            ),
            "backward-dependency": ("DSET-E151", self._backward_dependency),
            "backward-precedence": ("DSET-E151", self._backward_precedence),
            "incompatible-profile": ("DSET-E137", self._incompatible_profile),
            "wrapper-mismatch": ("DSET-E138", self._wrapper_mismatch),
        }
        for name, (expected, mutation) in cases.items():
            with self.subTest(case=name), temporary_directory() as raw:
                target = (Path(raw) / "adopter").resolve()
                create_adopter(ROOT, target)
                mutation(target)
                codes = {item.code for item in validate_governance(target)}
                self.assertIn(expected, codes)

    def test_unknown_workflow_is_stable(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "unknown-workflow")
        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["DSET-E136"])

    def test_irreducible_backward_authority_proposes_features(self) -> None:
        self._backward_dependency(self.root)
        diagnostic = next(
            item for item in validate_governance(self.root) if item.code == "DSET-E151"
        )
        self.assertIn(
            "converting irreducible peer layers to features", diagnostic.message
        )
        self.assertIn("horizontal Contracts", diagnostic.message)

    def test_deprecated_grill_workflow_is_not_registered(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "domain-grilling")
        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["DSET-E136"])

    def test_customization_changes_rules_not_wrapper(self) -> None:
        wrapper = self.root / "skills" / "dset-clarify" / "SKILL.md"
        before = hashlib.sha256(wrapper.read_bytes()).hexdigest()
        rule = self.root / "dset" / "governance" / "domain-spec-authoring.md"
        rule.write_text(
            rule.read_text(encoding="utf-8") + "\nLocal output rule.\n",
            encoding="utf-8",
        )
        self.assertIn(
            "DSET-E139", {item.code for item in validate_governance(self.root)}
        )
        refresh_customization(self.root)
        self.assertEqual(validate_governance(self.root), [])
        resolved, diagnostics = resolve_workflow(self.root, "domain-clarification")
        self.assertEqual(diagnostics, [])
        assert resolved is not None
        self.assertEqual(resolved["customization"], "custom")
        self.assertEqual(hashlib.sha256(wrapper.read_bytes()).hexdigest(), before)
        self.assertIn("Local output rule.", diff_governance(self.root, ROOT))

    def test_same_wrappers_resolve_each_projects_local_governance(self) -> None:
        results: dict[str, dict[str, object]] = {}
        with temporary_directory() as raw:
            parent = Path(raw).resolve()
            for label in ("project-a", "project-b"):
                project = parent / label
                create_adopter(ROOT, project)
                rule = project / "dset" / "governance" / "domain-spec-authoring.md"
                marker = f"{label} local output rule."
                rule.write_text(
                    rule.read_text(encoding="utf-8") + f"\n{marker}\n",
                    encoding="utf-8",
                )
                refresh_customization(project)

                nested_target = project / "src" / "feature"
                nested_target.mkdir(parents=True)
                discovered = find_repository(nested_target)
                resolved, diagnostics = resolve_workflow(
                    discovered, "domain-clarification"
                )
                self.assertEqual(diagnostics, [])
                assert resolved is not None
                local_rule = next(
                    item
                    for item in cast(list[dict[str, Any]], resolved["rules"])
                    if item["id"] == "DSET-RULE-DOMAIN-SPEC"
                )
                wrapper = project / "skills" / "dset-clarify" / "SKILL.md"
                results[label] = {
                    "root": discovered,
                    "wrapper_sha": hashlib.sha256(wrapper.read_bytes()).hexdigest(),
                    "rule_sha": local_rule["sha256"],
                    "customization": resolved["customization"],
                    "rule_text": (project / str(local_rule["path"])).read_text(
                        encoding="utf-8"
                    ),
                }

        first = results["project-a"]
        second = results["project-b"]
        self.assertNotEqual(first["root"], second["root"])
        self.assertEqual(first["wrapper_sha"], second["wrapper_sha"])
        self.assertNotEqual(first["rule_sha"], second["rule_sha"])
        self.assertEqual(first["customization"], "custom")
        self.assertEqual(second["customization"], "custom")
        self.assertIn("project-a local output rule.", str(first["rule_text"]))
        self.assertNotIn("project-b local output rule.", str(first["rule_text"]))
        self.assertIn("project-b local output rule.", str(second["rule_text"]))
        self.assertNotIn("project-a local output rule.", str(second["rule_text"]))

    def test_materialized_rules_do_not_read_changed_source_template(self) -> None:
        with temporary_directory() as raw:
            source = (Path(raw) / "framework").resolve()
            source.mkdir()
            for name in (".dset", "skills"):
                source_path = ROOT / name
                target_path = source / name
                shutil.copytree(source_path, target_path)
            target = (Path(raw) / "materialized-adopter").resolve()
            create_adopter(source, target)
            template = discover_layout(source).find_template(
                "governance/core-v1/domain-spec-authoring.md"
            )
            template.write_text("# Replaced source template\n", encoding="utf-8")
            resolved, diagnostics = resolve_workflow(target, "domain-clarification")
            self.assertEqual(diagnostics, [])
            assert resolved is not None
            local_rule = next(
                item
                for item in cast(list[dict[str, Any]], resolved["rules"])
                if item["id"] == "DSET-RULE-DOMAIN-SPEC"
            )
            local = target / str(local_rule["path"])
            self.assertIn("Establish ubiquitous language", local.read_text())
            self.assertNotIn("Replaced source template", local.read_text())

    def test_generated_wrappers_match_canonical_sources(self) -> None:
        registry = cast(
            dict[str, Any], load(discover_layout(self.root).governance_path)
        )
        for wrapper in cast(list[dict[str, Any]], registry["wrappers"]):
            with self.subTest(workflow=wrapper["workflow"]):
                generated = self.root / str(wrapper["path"])
                canonical = ROOT / str(wrapper["path"])
                self.assertEqual(generated.read_bytes(), canonical.read_bytes())
                self.assertEqual(
                    wrapper["sha256"],
                    hashlib.sha256(canonical.read_bytes()).hexdigest(),
                )

    def test_release_applicable_adopter_installs_all_registered_wrappers(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "release-adopter").resolve()
            (target / "dset").mkdir(parents=True)
            manifest_path = target / "dset" / "dset.toml"
            manifest_path.write_text(
                dump(
                    {
                        "schema_version": 1.1,
                        "profiles": {"repository_governance": "core-v1"},
                        "release": {"status": "applicable"},
                    },
                    manifest_path,
                ),
                encoding="utf-8",
            )
            materialize_governance(ROOT, target, install_wrappers=True)
            self.assertEqual(validate_governance(target), [])
            for workflow in REGISTERED_SKILL_WORKFLOWS.values():
                with self.subTest(workflow=workflow):
                    resolved, diagnostics = resolve_workflow(target, workflow)
                    self.assertEqual(diagnostics, [])
                    self.assertIsNotNone(resolved)

    def test_justified_unselected_non_applicability_is_valid(self) -> None:
        path, registry = self._registry(self.root)
        rule = registry["rules"][-1]
        rule["applicability"] = "not-applicable"
        rule["reason"] = "prototype workflow is not selected in this fixture"
        registry["workflows"] = [
            workflow
            for workflow in registry["workflows"]
            if workflow["id"] != "prototyping"
        ]
        registry["wrappers"] = [
            wrapper
            for wrapper in registry["wrappers"]
            if wrapper["workflow"] != "prototyping"
        ]
        path.write_text(dump(registry, path), encoding="utf-8")
        self.assertEqual(validate_governance(self.root), [])

    def test_materialization_refuses_existing_destination(self) -> None:
        with self.assertRaises(FileExistsError):
            materialize_governance(ROOT, self.root)

    def test_profile_assigns_every_rule_to_a_stable_layer(self) -> None:
        profile = cast(
            dict[str, Any],
            load(
                discover_layout(ROOT).find_template("governance/core-v1/profile.toml")
            ),
        )
        self.assertEqual(profile["schema_version"], 1.1)
        self.assertEqual(profile["version"], "0.3")
        actual = {item["id"]: item["layer"] for item in profile["rules"]}
        self.assertEqual(
            actual,
            {
                "DSET-RULE-ARCHITECTURE": "GOV",
                "DSET-RULE-ARTIFACT-CLASSIFICATION": "GOV",
                "DSET-RULE-BUILD": "TOOL",
                "DSET-RULE-DOMAIN-SPEC": "META",
                "DSET-RULE-TEST-PLAN": "META",
                "DSET-RULE-EVAL-PLAN": "META",
                "DSET-RULE-SUPPORTABILITY": "OPS",
                "DSET-RULE-ARTIFACT-MAINTENANCE": "GOV",
                "DSET-RULE-WORK-ITEMS": "GOV",
                "DSET-RULE-DELEGATION-BUDGET": "SKILL",
                "DSET-RULE-SKILL-RUNS": "SKILL",
                "DSET-RULE-RELEASE": "OPS",
                "DSET-RULE-LIFECYCLE": "SKILL",
                "DSET-RULE-DIAGNOSIS": "SKILL",
                "DSET-RULE-PROTOTYPING": "SKILL",
            },
        )

    def test_schema_12_materializes_rules_into_their_owning_layers(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "layered-adopter").resolve()
            self._make_layered_project(target)
            registry_path = materialize_governance(ROOT, target)
            self.assertEqual(
                registry_path,
                discover_layout(target).governance_path,
            )
            registry = cast(dict[str, Any], load(registry_path))
            for rule in cast(list[dict[str, Any]], registry["rules"]):
                with self.subTest(rule=rule["id"]):
                    expected_prefix = (
                        Path("dset")
                        / "scopes"
                        / str(rule["layer"]).lower()
                        / "governance"
                    )
                    self.assertEqual(Path(str(rule["path"])).parent, expected_prefix)
                    self.assertTrue((target / str(rule["path"])).is_file())
            self.assertTrue(
                (
                    target / "dset" / "scopes" / "gov" / "governance" / "README.md"
                ).is_file()
            )
            self.assertEqual(validate_governance(target), [])

    def test_layered_source_templates_are_resolved_across_all_roots(self) -> None:
        with temporary_directory() as raw:
            source = (Path(raw) / "layered-framework").resolve()
            target = (Path(raw) / "layered-adopter").resolve()
            self._make_layered_project(source)
            self._make_layered_project(target)
            layout = discover_layout(ROOT)
            profile_path = layout.find_template("governance/core-v1/profile.toml")
            profile = cast(dict[str, Any], load(profile_path))
            profile_root = (
                source
                / "dset"
                / "scopes"
                / "tool"
                / "templates"
                / "governance"
                / "core-v1"
            )
            profile_root.mkdir(parents=True)
            shutil.copyfile(profile_path, profile_root / profile_path.name)
            shutil.copyfile(
                layout.find_template("governance/core-v1/README.md"),
                profile_root / "README.md",
            )
            for rule in cast(list[dict[str, Any]], profile["rules"]):
                distributed = (
                    source
                    / "dset"
                    / "scopes"
                    / str(rule["layer"]).lower()
                    / "templates"
                    / "governance"
                    / "core-v1"
                    / str(rule["template"])
                )
                distributed.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(
                    layout.find_template(f"governance/core-v1/{rule['template']}"),
                    distributed,
                )

            registry_path = materialize_governance(source, target)
            registry = cast(dict[str, Any], load(registry_path))
            for rule in cast(list[dict[str, Any]], registry["rules"]):
                with self.subTest(rule=rule["id"]):
                    self.assertIn(
                        f"dset/scopes/{str(rule['layer']).lower()}/templates/",
                        rule["source"]["template"],
                    )
            self.assertEqual(validate_governance(target), [])

    def test_product_and_package_versions_are_coordinated(self) -> None:
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = main(["version", str(ROOT)])
        self.assertEqual(result, 0)
        output = stream.getvalue()
        self.assertIn("product: 0.3.1 (coordinated)", output)
        self.assertIn("python package: 0.3.1 (coordinated)", output)
        self.assertIn("schemas: 1.2 (independent)", output)

    def test_bootstrap_release_target_is_explicit_not_framework_hard_coded(
        self,
    ) -> None:
        release = (ROOT / ".dset/05_layer_ops/procedure-release.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("explicit first `0.Y.Z` target", release)
        self.assertNotIn(
            "| no activated product version | `bootstrap` | `0.3.0` |", release
        )

    def test_temporary_adopter_materializes_current_project_inputs(self) -> None:
        layout = discover_layout(self.root)
        manifest = cast(dict[str, Any], load(layout.manifest_path))
        self.assertEqual(manifest["schema_version"], 1.1)
        self.assertEqual(manifest["project"]["key"], "DSET")
        self.assertEqual(manifest["contracts"], ["DSET-CONTRACT-001"])
        self.assertEqual(manifest["stories"], [])
        self.assertEqual(manifest["outcomes"], [])
        self.assertNotIn("delegation_budget", manifest["profiles"])
        self.assertEqual(manifest["release"]["status"], "not-applicable")
        self.assertEqual(manifest["work_items"]["registry"], "dset/intake.toml")
        self.assertTrue((self.root / "dset_settings.toml").is_file())
        self.assertFalse((self.root / "dset.toml").exists())
        self.assertTrue(layout.artifact_type_registry_path.is_file())
        self.assertTrue(layout.budget_path.is_file())
        self.assertTrue(layout.intake_path.is_file())
        package_root = self.root / "dset" / "specs" / "packages" / "sample"
        package_path = layout.structured_file(package_root, "package.toml")
        package = cast(
            dict[str, Any],
            load(package_path),
        )
        self.assertEqual(package["contracts"], ["DSET-CONTRACT-001"])
        self.assertEqual(package["stories"], [])
        self.assertEqual(package["outcomes"], [])
        self.assertTrue(
            (
                self.root / "dset" / "specs" / "packages" / "sample" / "stories.md"
            ).is_file()
        )
        self.assertTrue(
            (
                self.root / "dset" / "specs" / "packages" / "sample" / "outcomes.md"
            ).is_file()
        )
        registry = cast(dict[str, Any], load(layout.governance_path))
        release = next(
            rule
            for rule in cast(list[dict[str, Any]], registry["rules"])
            if rule["id"] == "DSET-RULE-RELEASE"
        )
        self.assertEqual(release["applicability"], "not-applicable")
        workflows = cast(list[dict[str, Any]], registry["workflows"])
        self.assertNotIn("release", {item["id"] for item in workflows})
        wrappers = cast(list[dict[str, Any]], registry["wrappers"])
        self.assertNotIn("release", {item["workflow"] for item in wrappers})
        self.assertFalse((self.root / "skills" / "dset-release").exists())
        self.assertTrue(
            all(
                "DSET-RULE-RELEASE" not in cast(list[str], item["rules"])
                for item in workflows
            )
        )

    def test_current_schema_suite_preserves_legacy_change_shape(self) -> None:
        change_schema = json.loads(_framework_schema("change.schema.json").read_text())
        current = change_schema["allOf"][0]
        self.assertEqual(current["then"]["required"], ["adrs"])
        self.assertEqual(current["then"]["not"]["required"], ["decisions"])
        self.assertEqual(
            current["else"]["required"],
            ["release", "intake", "decisions", "contracts", "llm_session_ids"],
        )
        self.assertEqual(current["else"]["not"]["required"], ["adrs"])
        release_variants = change_schema["$defs"]["release"]["oneOf"]
        self.assertEqual(len(release_variants), 2)
        intake_schema = json.loads(_framework_schema("intake.schema.json").read_text())
        for item_name in ("legacy_item", "layered_item"):
            self.assertIn(
                "llm_session_ids", intake_schema["$defs"][item_name]["required"]
            )

    def test_atomic_rationale_is_supported_but_optional(self) -> None:
        change_schema = json.loads(_framework_schema("change.schema.json").read_text())
        self.assertIn("rationale", change_schema["properties"])
        self.assertNotIn("rationale", change_schema["required"])
        self.assertEqual(change_schema["$defs"]["rationale"]["minLength"], 1)

        intake_schema = json.loads(_framework_schema("intake.schema.json").read_text())
        for item_name in ("legacy_item", "layered_item"):
            item = intake_schema["$defs"][item_name]
            self.assertIn("rationale", item["properties"])
            self.assertNotIn("rationale", item["required"])
        self.assertEqual(intake_schema["$defs"]["rationale"]["minLength"], 1)

        for schema_path in (
            ROOT / ".dset/04_layer_skill/schemas/skill-run.schema.json",
            ROOT / ".dset/04_layer_skill/schemas/session-checkpoint.schema.json",
        ):
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            self.assertIn("rationale", schema["properties"])
            self.assertNotIn("rationale", schema["required"])
            self.assertEqual(schema["$defs"]["rationale"]["minLength"], 1)

        for name in ("decision.md", "adoption-decision.md"):
            decision_template = (
                ROOT / ".dset/02_layer_gov/templates/change" / name
            ).read_text(encoding="utf-8")
            self.assertIn("Rationale (recommended, optional)", decision_template)
            self.assertIn("Omission alone does", decision_template)
            self.assertIn("not invalidate the Decision", decision_template)

        rule = (
            ROOT / ".dset/02_layer_gov/specification-artifact-maintenance.md"
        ).read_text(encoding="utf-8")
        self.assertIn("absence alone never invalidates", rule)
        self.assertIn("not hidden authority", rule)

    def test_trace_id_schemas_are_type_first_and_layer_bounded(self) -> None:
        change_schema = json.loads(_framework_schema("change.schema.json").read_text())
        patterns = change_schema["$defs"]
        complete_pattern = patterns["trace_id"]["pattern"]
        for valid in (
            "DSET-SCENARIO-META-001",
            "DSET-INVARIANT-001",
            "DSET-TASK-TOOL-001",
            "DSET-CONTRACT-OPS-001",
            "ACME-STORY-SKILL-001",
            "ACME-OUTCOME-OPS-001",
            "ACME-CHANGE-SKILL-001",
        ):
            self.assertIsNotNone(re.fullmatch(complete_pattern, valid))
        self.assertIsNotNone(
            re.fullmatch(
                patterns["requirement_ids"]["items"]["pattern"],
                "DSET-REQUIREMENT-GOV-001",
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                patterns["contract_ids"]["items"]["pattern"],
                "ACME-CONTRACT-TOOL-002",
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                patterns["story_ids"]["items"]["pattern"],
                "ACME-STORY-SKILL-001",
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                patterns["outcome_ids"]["items"]["pattern"],
                "ACME-OUTCOME-OPS-001",
            )
        )
        for invalid in (
            "REQUIREMENT-DSET-GOV-001",
            "DSET-REQ-GOV-001",
            "DSET-REQUIREMENT-GLOBAL-001",
            "DSET-ADR-GOV-001",
        ):
            self.assertIsNone(
                re.fullmatch(patterns["requirement_ids"]["items"]["pattern"], invalid)
            )

    def test_validator_uses_the_manifest_project_key(self) -> None:
        layout = discover_layout(self.root)
        manifest_path = layout.manifest_path
        manifest = cast(dict[str, Any], load(manifest_path))
        manifest["project"]["key"] = "ACME"
        manifest["contracts"] = ["ACME-CONTRACT-001"]
        manifest_path.write_text(dump(manifest, manifest_path), encoding="utf-8")

        package_root = self.root / "dset" / "specs" / "packages" / "sample"
        package_path = layout.structured_file(package_root, "package.toml")
        package = cast(dict[str, Any], load(package_path))
        package["requirements"] = ["ACME-REQUIREMENT-001"]
        package["tests"] = ["ACME-TEST-001"]
        package["contracts"] = ["ACME-CONTRACT-001"]
        package_path.write_text(dump(package, package_path), encoding="utf-8")
        for filename in ("spec.md", "test-plan.md", "contracts.md"):
            path = package_root / filename
            path.write_text(
                path.read_text(encoding="utf-8").replace("DSET-", "ACME-"),
                encoding="utf-8",
            )
        write_legacy_authority_ledger(self.root)
        self.assertEqual(validate_repository(self.root), [])

    def test_validator_ignores_machine_local_cache_documents(self) -> None:
        cache = self.root / ".cache" / "vendor"
        cache.mkdir(parents=True)
        (cache / "README.md").write_text(
            "[generated missing link](not-present.md)\n", encoding="utf-8"
        )

        self.assertEqual(validate_repository(self.root), [])

    def test_legacy_intake_enforces_type_and_registered_layer(self) -> None:
        path = discover_layout(self.root).intake_path
        baseline = cast(dict[str, Any], load(path))
        valid: dict[str, Any] = {
            "id": "DSET-QUESTION-GOV-001",
            "scope": "gov",
            "type": "question",
            "status": "open",
            "title": "Choice",
            "statement": "Which bounded option applies?",
            "owner_change": "pending",
            "decision": "pending",
            "llm_session_ids": [],
            "external_refs": [],
        }
        baseline["items"] = [valid]
        path.write_text(dump(baseline, path), encoding="utf-8")
        self.assertNotIn(
            "DSET-E142", {item.code for item in validate_repository(self.root)}
        )
        invalid_cases = (
            {**valid, "id": "DSET-PROBLEM-GOV-001"},
            {**valid, "id": "DSET-QUESTION-GLOBAL-001"},
            {**valid, "scope": "tool"},
            {**valid, "decision": "DSET-DECISION-TOOL-001"},
        )
        for invalid in invalid_cases:
            with self.subTest(identifier=invalid["id"], scope=invalid["scope"]):
                baseline["items"] = [invalid]
                path.write_text(dump(baseline, path), encoding="utf-8")
                self.assertIn(
                    "DSET-E142", {item.code for item in validate_repository(self.root)}
                )

    def test_contract_template_requires_real_host_and_ci_proof(self) -> None:
        layout = discover_layout(ROOT)
        text = layout.find_template("package/contracts.md").read_text()
        self.assertIn("Markdown validity is not host proof", text)
        self.assertIn("allowlists, denylists, and enforcement metadata", text)
        self.assertIn("real GitHub Actions workflow artifacts", text)
        contract_ids = sorted(
            identifier
            for path in layout.package_fragments()
            for identifier in cast(dict[str, Any], load(path))["contracts"]
        )
        self.assertEqual(
            contract_ids,
            [
                "DSET-CONTRACT-META-001",
                "DSET-CONTRACT-OPS-001",
                "DSET-CONTRACT-SKILL-001",
                "DSET-CONTRACT-SKILL-002",
                "DSET-CONTRACT-TOOL-001",
                "DSET-CONTRACT-TOOL-002",
            ],
        )

    def test_story_and_outcome_templates_preserve_semantic_boundaries(self) -> None:
        layout = discover_layout(ROOT)
        stories = layout.find_template("package/stories.md").read_text()
        self.assertIn("Actor or stakeholder", stories)
        self.assertIn("Desired capability or outcome", stories)
        self.assertIn("Linked Requirements", stories)
        self.assertIn("Linked Scenarios", stories)
        self.assertIn("not an intake queue", stories)
        self.assertIn("does not replace normative Requirements", stories)

        outcomes = layout.find_template("package/outcomes.md").read_text()
        self.assertIn("Baseline", outcomes)
        self.assertIn("Target", outcomes)
        self.assertIn("Observation method/source", outcomes)
        self.assertIn("Evaluation window", outcomes)
        self.assertIn("Linked Problems/Opportunities", outcomes)
        self.assertIn("Linked User Stories", outcomes)
        self.assertIn("Linked Evals", outcomes)
        self.assertIn("deliverable, or feature is not itself an Outcome", outcomes)

    def test_story_and_outcome_records_require_structured_fields(self) -> None:
        package_root = self.root / "dset" / "specs" / "packages" / "sample"
        manifest_path = discover_layout(self.root).structured_file(
            package_root, "package.toml"
        )
        manifest = cast(dict[str, Any], load(manifest_path))
        manifest["stories"] = ["DSET-STORY-001"]
        manifest["outcomes"] = ["DSET-OUTCOME-001"]
        manifest_path.write_text(dump(manifest, manifest_path), encoding="utf-8")
        (package_root / "stories.md").write_text(
            "# User Stories\n\n## DSET-STORY-001 — Incomplete\n\nActor only.\n",
            encoding="utf-8",
        )
        (package_root / "outcomes.md").write_text(
            "# Outcomes\n\n## DSET-OUTCOME-001 — Incomplete\n\nTarget only.\n",
            encoding="utf-8",
        )
        self.assertIn(
            "DSET-E117", {item.code for item in validate_repository(self.root)}
        )

        (package_root / "stories.md").write_text(
            """# User Stories

## DSET-STORY-001 — Contributor can validate

- **Actor or stakeholder:** Contributor
- **Desired capability or outcome:** Validate locally
- **Value or purpose:** Catch errors early
- **Linked Requirements:** DSET-REQUIREMENT-001
- **Linked Scenarios:** Validation succeeds without external effects
""",
            encoding="utf-8",
        )
        (package_root / "outcomes.md").write_text(
            """# Outcomes

## DSET-OUTCOME-001 — Earlier feedback

- **Baseline:** Errors are found after review.
- **Target:** Errors are found before review.
- **Observation method/source:** Review and local validation timestamps.
- **Evaluation window:** The next ten changes.
- **Linked Problems/Opportunities:** Local feedback opportunity.
- **Linked User Stories:** DSET-STORY-001.
- **Linked Evals:** Review timing eval.
""",
            encoding="utf-8",
        )
        self.assertNotIn(
            "DSET-E117", {item.code for item in validate_repository(self.root)}
        )

    def test_wrappers_are_thin_and_registered(self) -> None:
        workflows = {
            "lifecycle-orchestration": "dset",
            "domain-clarification": "dset-clarify",
            "diagnosis": "dset-diagnose",
            "prototyping": "dset-prototype",
            "release": "dset-release",
            "work-triage": "dset-triage",
            "decompose": "dset-decompose",
            "landscape": "dset-landscape",
            "decisions": "dset-decisions",
            "plan-proof": "dset-plan-proof",
            "plan-implementation": "dset-plan-implementation",
            "implement": "dset-implement",
            "verify": "dset-verify",
            "complete": "dset-complete",
        }
        registry = cast(
            dict[str, Any],
            load(discover_layout(ROOT).governance_path),
        )
        registered = {
            item["workflow"]: item["path"]
            for item in cast(list[dict[str, Any]], registry["wrappers"])
        }
        resolved_workflows = {
            item["id"]: set(cast(list[str], item["rules"]))
            for item in cast(list[dict[str, Any]], registry["workflows"])
        }
        for workflow, skill in workflows.items():
            with self.subTest(workflow=workflow):
                path = ROOT / "skills" / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 24)
                self.assertIn(f"skills context --skill {skill} --target TARGET", text)
                self.assertNotIn("## Workflow", text)
                self.assertNotIn("git bisect", text)
                self.assertNotIn("proofs/<candidate>-fit", text)
                self.assertEqual(
                    registered[workflow], path.relative_to(ROOT).as_posix()
                )
                metadata = cast(
                    dict[str, Any],
                    load(ROOT / "skills" / skill / "agents" / "openai.yaml"),
                )
                interface = cast(dict[str, Any], metadata["interface"])
                self.assertTrue(interface["display_name"])
                self.assertIn(f"${skill}", interface["default_prompt"])
                self.assertIn("DSET-RULE-SKILL-RUNS", resolved_workflows[workflow])
                self.assertIn("DSET-RULE-LIFECYCLE", resolved_workflows[workflow])

    def test_manifest_and_template_boundaries_are_stable(self) -> None:
        with self.assertRaises(DsetCommandError) as captured:
            materialize_governance(ROOT, self.root, "missing-profile")
        self.assertEqual(captured.exception.code, "DSET-E140")
        discover_layout(self.root).manifest_path.unlink()
        self.assertEqual(validate_repository(self.root)[0].code, "DSET-E001")

    def test_comparison_and_decision_templates_separate_selection(self) -> None:
        layout = discover_layout(ROOT)
        landscape = layout.find_template("change/solution-landscape.md").read_text(
            encoding="utf-8"
        )
        candidates, decision = landscape.split("## Decision", maxsplit=1)
        self.assertIn("Compared with / criteria", candidates)
        self.assertIn("Evidence eligibility", candidates)
        self.assertNotIn("**Adopt", candidates)
        self.assertNotIn("**Reject", candidates)
        self.assertIn("Record adopt, adapt, or reject only", decision)

        decision_template = layout.find_template("change/decision.md").read_text(
            encoding="utf-8"
        )
        for field in (
            "Decision ID",
            "Decision date",
            "Resolves Question",
            "Absorbs",
            "Replaces claims",
            "Priority",
            "Expected confirmation evidence",
            "Known counter-evidence",
            "If reopened, retain",
            "If reopened, withdraw",
            "Retirement condition",
        ):
            self.assertIn(field, decision_template)

        active = (ROOT / "00_project/analysis-solution-landscape.md").read_text(
            encoding="utf-8"
        )
        active_candidates, _ = active.split("## Decision", maxsplit=1)
        self.assertNotIn("**Adopt", active_candidates)
        self.assertNotIn("**Reject", active_candidates)

    def test_distributed_manifest_templates_are_schema_specific(self) -> None:
        layout = discover_layout(ROOT)
        legacy_change = cast(
            dict[str, Any], load(layout.find_template("change/legacy/change.yaml"))
        )
        layered_change = cast(
            dict[str, Any], load(layout.find_template("change/layered/change.yaml"))
        )
        legacy_package = cast(
            dict[str, Any], load(layout.find_template("package/legacy/package.yaml"))
        )
        layered_package = cast(
            dict[str, Any], load(layout.find_template("package/layered/package.yaml"))
        )

        self.assertEqual(legacy_change["schema_version"], 1.1)
        self.assertEqual(legacy_change["release"]["policy"], "pending")
        self.assertEqual(layered_change["schema_version"], "1.2")
        self.assertEqual(
            layered_change["release"]["policy"],
            "dset/scopes/ops/governance/release.md",
        )
        self.assertEqual(legacy_package["schema_version"], 1.0)
        self.assertEqual(layered_package["schema_version"], "1.2")
        self.assertIn("layer", layered_package)

    def test_fpf_provenance_bounds_each_adaptation(self) -> None:
        provenance = cast(dict[str, Any], load(discover_layout(ROOT).provenance_path))
        fpf = next(
            source
            for source in cast(list[dict[str, Any]], provenance["sources"])
            if source["id"] == "fpf"
        )
        for mapping in cast(list[dict[str, Any]], fpf["mappings"]):
            with self.subTest(pattern=mapping["pattern"]):
                self.assertTrue(mapping["adaptation_scope"])
                self.assertTrue(mapping["exclusions"])
        patterns = {
            mapping["pattern"]
            for mapping in cast(list[dict[str, Any]], fpf["mappings"])
        }
        self.assertTrue(
            {
                "FPF-A.07",
                "FPF-A.11",
                "FPF-A.02.09",
                "FPF-C.32.PAD",
                "FPF-E.17.AUD",
            }.issubset(patterns)
        )

    def test_health_review_and_ranking_rules_are_compiled(self) -> None:
        live = (
            ROOT / ".dset/02_layer_gov/specification-artifact-maintenance.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT
            / ".dset/02_layer_gov/templates/governance/core-v1/artifact-maintenance.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(live, template)
        for phrase in (
            "numerator, denominator, exclusions",
            "mandatory envelope",
            "findings body may be free-form",
            "authorize repair",
            "transactional context/evidence, and implementation",
            "priority orders remediation or escalation",
            "otherwise, higher effective priority wins",
            "resolver accepts every governed artifact pairing",
            "evidence never rewrites authority",
            "Atomic artifacts are immutable",
            "registered carrier transition",
        ):
            self.assertIn(phrase, live)

        architecture = (
            ROOT / ".dset/02_layer_gov/specification-architecture.md"
        ).read_text(encoding="utf-8")
        architecture_template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/architecture.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(architecture, architecture_template)
        for phrase in (
            "Atomic authority sources",
            "Later state is an append-only lifecycle event",
            "active atom wins over a stale compiled projection",
            "lossless carrier transition",
            "smallest independently reviewable primary project claim",
            "acceptance act grants authority to Decision",
            "QA atom defines a check",
        ):
            self.assertIn(phrase, architecture)

        work_items = (
            ROOT / ".dset/02_layer_gov/specification-work-items.md"
        ).read_text(encoding="utf-8")
        work_items_template = (
            ROOT / ".dset/02_layer_gov/templates/governance/core-v1/work-items.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(work_items, work_items_template)
        self.assertIn("one Type and at most one direct subtype", work_items)
        self.assertIn("sibling Requirement subtypes", work_items)
        self.assertIn("never edits the Question atom", work_items)
        self.assertIn("QA always has one of its two", work_items)
        self.assertIn("append-only", work_items)

        for name in ("decision.md", "adoption-decision.md"):
            decision_template = (
                ROOT / ".dset/02_layer_gov/templates/change" / name
            ).read_text(encoding="utf-8")
            self.assertIn("**Absorbs:**", decision_template)
            self.assertNotIn("**Superseded by:**", decision_template)
            self.assertIn("emitted Decision", decision_template)

        gov = (ROOT / ".dset/02_layer_gov/specification-methodology.md").read_text(
            encoding="utf-8"
        )
        tool = (ROOT / ".dset/03_layer_tool/specification-methodology.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("DSET-REQUIREMENT-GOV-024", gov)
        self.assertIn("DSET-REQUIREMENT-GOV-025", gov)
        self.assertIn("DSET-REQUIREMENT-GOV-026", gov)
        self.assertIn("DSET-REQUIREMENT-TOOL-018", tool)
        self.assertIn("DSET-REQUIREMENT-TOOL-019", tool)
        self.assertIn("portable Markdown", tool)

        archived_ids: set[str] = set()
        layout = discover_layout(ROOT)
        archived_manifests = (
            path
            for root in layout.archive_change_roots
            for path in layout.structured_named_files(root, "change")
        )
        for path in archived_manifests:
            manifest = cast(dict[str, Any], load(path))
            for group in ("requirements", "tests", "evals"):
                archived_ids.update(cast(list[str], manifest.get(group, [])))
        self.assertTrue(
            {
                "DSET-REQUIREMENT-TOOL-018",
                "DSET-REQUIREMENT-TOOL-019",
                "DSET-TEST-TOOL-018",
                "DSET-TEST-TOOL-019",
            }.isdisjoint(archived_ids)
        )

    @staticmethod
    def _make_layered_project(root: Path) -> None:
        scopes = root / "dset" / "scopes"
        for layer in ("meta", "gov", "tool", "skill", "ops"):
            (scopes / layer).mkdir(parents=True)
        manifest_path = scopes / "meta" / "dset.toml"
        manifest_path.write_text(
            dump(
                {
                    "schema_version": "1.2",
                    "profiles": {"repository_governance": "core-v1"},
                },
                manifest_path,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _registry(root: Path) -> tuple[Path, dict[str, Any]]:
        path = discover_layout(root).governance_path
        return path, cast(dict[str, Any], load(path))

    @classmethod
    def _write_registry(cls, root: Path, data: dict[str, Any]) -> None:
        path, _ = cls._registry(root)
        path.write_text(dump(data, path), encoding="utf-8")

    @staticmethod
    def _remove_registry(root: Path) -> None:
        discover_layout(root).governance_path.unlink()

    @classmethod
    def _missing_owner(cls, root: Path) -> None:
        _, data = cls._registry(root)
        del data["rules"][0]["owner"]
        cls._write_registry(root, data)

    @classmethod
    def _duplicate_owner(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"].append(dict(data["rules"][0]))
        cls._write_registry(root, data)

    @classmethod
    def _missing_document(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"][0]["path"] = "dset/governance/missing.md"
        cls._write_registry(root, data)

    @classmethod
    def _outside_root(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"][0]["path"] = "../outside.md"
        cls._write_registry(root, data)

    @classmethod
    def _dependency_cycle(cls, root: Path) -> None:
        _, data = cls._registry(root)
        first = data["rules"][0]
        second = data["rules"][1]
        first["depends_on"] = [second["id"]]
        second["depends_on"] = [first["id"]]
        cls._write_registry(root, data)

    @classmethod
    def _precedence_cycle(cls, root: Path) -> None:
        _, data = cls._registry(root)
        first = data["rules"][0]
        second = data["rules"][1]
        first["precedence_over"] = [second["id"]]
        second["precedence_over"] = [first["id"]]
        cls._write_registry(root, data)

    @classmethod
    def _missing_precedence(cls, root: Path) -> None:
        _, data = cls._registry(root)
        del data["rules"][0]["precedence_over"]
        cls._write_registry(root, data)

    @classmethod
    def _missing_precedence_owner(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["rules"][0]["precedence_over"] = ["DSET-RULE-MISSING"]
        cls._write_registry(root, data)

    @classmethod
    def _backward_dependency(cls, root: Path) -> None:
        _, data = cls._registry(root)
        meta = next(rule for rule in data["rules"] if rule["layer"] == "META")
        ops = next(rule for rule in data["rules"] if rule["layer"] == "OPS")
        meta["depends_on"] = [ops["id"]]
        cls._write_registry(root, data)

    @classmethod
    def _backward_precedence(cls, root: Path) -> None:
        _, data = cls._registry(root)
        meta = next(rule for rule in data["rules"] if rule["layer"] == "META")
        ops = next(rule for rule in data["rules"] if rule["layer"] == "OPS")
        ops["precedence_over"] = [meta["id"]]
        cls._write_registry(root, data)

    @classmethod
    def _incompatible_profile(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["profile"]["id"] = "other-profile"
        cls._write_registry(root, data)

    @classmethod
    def _wrapper_mismatch(cls, root: Path) -> None:
        _, data = cls._registry(root)
        data["wrappers"][0]["sha256"] = "0" * 64
        cls._write_registry(root, data)


if __name__ == "__main__":
    unittest.main()
