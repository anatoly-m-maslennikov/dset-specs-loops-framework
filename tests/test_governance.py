from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import shutil
import tempfile
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
from dset_toolchain.validation import validate_repository
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


def _framework_schema(name: str) -> Path:
    return next(
        path for path in discover_layout(ROOT).schema_paths() if path.name == name
    )


class GovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "adopter"
        create_adopter(ROOT, self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_registry_resolves_stable_order(self) -> None:
        self.assertEqual(validate_governance(self.root), [])
        resolved, diagnostics = resolve_workflow(self.root, "domain-clarification")
        self.assertEqual(diagnostics, [])
        self.assertIsNotNone(resolved)
        assert resolved is not None
        self.assertEqual(resolved["workflow_id"], "domain-clarification")
        self.assertEqual(resolved["customization"], "unmodified")
        self.assertGreater(len(cast(list[Any], resolved["rules"])), 3)

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

    def test_resolution_is_stable_and_read_only(self) -> None:
        registry = self.root / "dset" / "governance.yaml"
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
            "incompatible-profile": ("DSET-E137", self._incompatible_profile),
            "wrapper-mismatch": ("DSET-E138", self._wrapper_mismatch),
        }
        for name, (expected, mutation) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as raw:
                target = Path(raw) / "adopter"
                create_adopter(ROOT, target)
                mutation(target)
                codes = {item.code for item in validate_governance(target)}
                self.assertIn(expected, codes)

    def test_unknown_workflow_is_stable(self) -> None:
        resolved, diagnostics = resolve_workflow(self.root, "unknown-workflow")
        self.assertIsNone(resolved)
        self.assertEqual([item.code for item in diagnostics], ["DSET-E136"])

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

    def test_materialized_rules_do_not_read_changed_source_template(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / "framework"
            source.mkdir()
            for name in ("dset", "skills"):
                source_path = ROOT / name
                target_path = source / name
                shutil.copytree(source_path, target_path)
            target = Path(raw) / "materialized-adopter"
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
        registry = cast(dict[str, Any], load(self.root / "dset" / "governance.yaml"))
        for wrapper in cast(list[dict[str, Any]], registry["wrappers"]):
            with self.subTest(workflow=wrapper["workflow"]):
                generated = self.root / str(wrapper["path"])
                canonical = ROOT / str(wrapper["path"])
                self.assertEqual(generated.read_bytes(), canonical.read_bytes())
                self.assertEqual(
                    wrapper["sha256"],
                    hashlib.sha256(canonical.read_bytes()).hexdigest(),
                )

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
        path.write_text(dump(registry), encoding="utf-8")
        self.assertEqual(validate_governance(self.root), [])

    def test_materialization_refuses_existing_destination(self) -> None:
        with self.assertRaises(FileExistsError):
            materialize_governance(ROOT, self.root)

    def test_profile_assigns_every_rule_to_a_stable_layer(self) -> None:
        profile = cast(
            dict[str, Any],
            load(
                discover_layout(ROOT).find_template("governance/core-v1/profile.yaml")
            ),
        )
        actual = {item["id"]: item["layer"] for item in profile["rules"]}
        self.assertEqual(
            actual,
            {
                "DSET-RULE-ARCHITECTURE": "GOV",
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
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "layered-adopter"
            self._make_layered_project(target)
            registry_path = materialize_governance(ROOT, target)
            self.assertEqual(
                registry_path,
                target / "dset" / "scopes" / "gov" / "governance.yaml",
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
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / "layered-framework"
            target = Path(raw) / "layered-adopter"
            self._make_layered_project(source)
            self._make_layered_project(target)
            layout = discover_layout(ROOT)
            profile_path = layout.find_template("governance/core-v1/profile.yaml")
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
            shutil.copyfile(profile_path, profile_root / "profile.yaml")
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
        release = (ROOT / "dset/scopes/ops/governance/release.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("explicit first `0.Y.Z` target", release)
        self.assertNotIn(
            "| no activated product version | `bootstrap` | `0.3.0` |", release
        )

    def test_temporary_adopter_materializes_current_project_inputs(self) -> None:
        manifest = cast(dict[str, Any], load(self.root / "dset" / "dset.yaml"))
        self.assertEqual(manifest["schema_version"], 1.1)
        self.assertEqual(manifest["project"]["key"], "DSET")
        self.assertEqual(manifest["contracts"], ["DSET-CONTRACT-001"])
        self.assertEqual(manifest["stories"], [])
        self.assertEqual(manifest["outcomes"], [])
        self.assertEqual(manifest["profiles"]["delegation_budget"], "medium")
        self.assertEqual(manifest["release"]["status"], "not-applicable")
        self.assertEqual(manifest["work_items"]["registry"], "dset/intake.yaml")
        self.assertTrue((self.root / "dset" / "budget.yaml").is_file())
        self.assertTrue((self.root / "dset" / "intake.yaml").is_file())
        package = cast(
            dict[str, Any],
            load(self.root / "dset" / "specs" / "packages" / "sample" / "package.yaml"),
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
        registry = cast(dict[str, Any], load(self.root / "dset" / "governance.yaml"))
        release = next(
            rule
            for rule in cast(list[dict[str, Any]], registry["rules"])
            if rule["id"] == "DSET-RULE-RELEASE"
        )
        self.assertEqual(release["applicability"], "not-applicable")
        workflows = cast(list[dict[str, Any]], registry["workflows"])
        self.assertNotIn("release", {item["id"] for item in workflows})
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
            ["release", "intake", "decisions", "contracts"],
        )
        self.assertEqual(current["else"]["not"]["required"], ["adrs"])
        release_variants = change_schema["$defs"]["release"]["oneOf"]
        self.assertEqual(len(release_variants), 2)

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
        manifest_path = self.root / "dset" / "dset.yaml"
        manifest = cast(dict[str, Any], load(manifest_path))
        manifest["project"]["key"] = "ACME"
        manifest["contracts"] = ["ACME-CONTRACT-001"]
        manifest_path.write_text(dump(manifest), encoding="utf-8")

        package_root = self.root / "dset" / "specs" / "packages" / "sample"
        package_path = package_root / "package.yaml"
        package = cast(dict[str, Any], load(package_path))
        package["requirements"] = ["ACME-REQUIREMENT-001"]
        package["tests"] = ["ACME-TEST-001"]
        package["contracts"] = ["ACME-CONTRACT-001"]
        package_path.write_text(dump(package), encoding="utf-8")
        for filename in ("spec.md", "test-plan.md", "contracts.md"):
            path = package_root / filename
            path.write_text(
                path.read_text(encoding="utf-8").replace("DSET-", "ACME-"),
                encoding="utf-8",
            )
        self.assertEqual(validate_repository(self.root), [])

    def test_legacy_intake_enforces_type_and_registered_layer(self) -> None:
        path = self.root / "dset" / "intake.yaml"
        baseline = cast(dict[str, Any], load(path))
        valid: dict[str, Any] = {
            "id": "DSET-QUESTION-GOV-001",
            "scope": "gov",
            "type": "question",
            "status": "open",
            "title": "Choice",
            "statement": "Which bounded option applies?",
            "owner_change": None,
            "decision": "pending",
            "external_refs": [],
        }
        baseline["items"] = [valid]
        path.write_text(dump(baseline), encoding="utf-8")
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
                path.write_text(dump(baseline), encoding="utf-8")
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
        manifest_path = package_root / "package.yaml"
        manifest = cast(dict[str, Any], load(manifest_path))
        manifest["stories"] = ["DSET-STORY-001"]
        manifest["outcomes"] = ["DSET-OUTCOME-001"]
        manifest_path.write_text(dump(manifest), encoding="utf-8")
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
            "domain-clarification": "dset-clarify",
            "diagnosis": "dset-diagnose",
            "prototyping": "dset-prototype",
        }
        for workflow, skill in workflows.items():
            with self.subTest(workflow=workflow):
                path = ROOT / "skills" / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 24)
                self.assertIn(f"rules resolve {workflow}", text)
                self.assertNotIn("## Workflow", text)
                self.assertNotIn("git bisect", text)
                self.assertNotIn("proofs/<candidate>-fit", text)

    def test_manifest_and_template_boundaries_are_stable(self) -> None:
        with self.assertRaises(DsetCommandError) as captured:
            materialize_governance(ROOT, self.root, "missing-profile")
        self.assertEqual(captured.exception.code, "DSET-E140")
        (self.root / "dset" / "dset.yaml").unlink()
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
            "Confirmation evidence",
            "Violation or counter-evidence",
            "If reopened, retain",
            "If reopened, withdraw",
            "Successor or retirement",
        ):
            self.assertIn(field, decision_template)

        active = (
            ROOT / "dset/scopes/skill/changes/"
            "make-dset-self-hosting-and-skills-thin/solution-landscape.md"
        ).read_text(encoding="utf-8")
        active_candidates, _ = active.split("## Decision", maxsplit=1)
        self.assertNotIn("**Adopt", active_candidates)
        self.assertNotIn("**Reject", active_candidates)

    def test_fpf_provenance_bounds_each_adaptation(self) -> None:
        provenance = cast(
            dict[str, Any], load(ROOT / "dset/scopes/gov/provenance.yaml")
        )
        fpf = next(
            source
            for source in cast(list[dict[str, Any]], provenance["sources"])
            if source["id"] == "fpf"
        )
        for mapping in cast(list[dict[str, Any]], fpf["mappings"]):
            with self.subTest(pattern=mapping["pattern"]):
                self.assertTrue(mapping["adaptation_scope"])
                self.assertTrue(mapping["exclusions"])

    @staticmethod
    def _make_layered_project(root: Path) -> None:
        scopes = root / "dset" / "scopes"
        for layer in ("meta", "gov", "tool", "skill", "ops"):
            (scopes / layer).mkdir(parents=True)
        (scopes / "meta" / "dset.yaml").write_text(
            dump(
                {
                    "schema_version": "1.2",
                    "profiles": {"repository_governance": "core-v1"},
                }
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _registry(root: Path) -> tuple[Path, dict[str, Any]]:
        path = root / "dset" / "governance.yaml"
        return path, cast(dict[str, Any], load(path))

    @classmethod
    def _write_registry(cls, root: Path, data: dict[str, Any]) -> None:
        path, _ = cls._registry(root)
        path.write_text(dump(data), encoding="utf-8")

    @staticmethod
    def _remove_registry(root: Path) -> None:
        (root / "dset" / "governance.yaml").unlink()

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
