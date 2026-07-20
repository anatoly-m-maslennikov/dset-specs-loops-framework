from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import cast
from unittest.mock import patch

import dset_toolchain.toml_migration as toml_migration
from dset_toolchain.cli import main
from dset_toolchain.layout import RepositoryLayout
from dset_toolchain.lineage import validate_artifact_relations
from dset_toolchain.toml_codec import loads as load_toml
from dset_toolchain.toml_migration import (
    MigrationPlan,
    apply_toml_migration,
    plan_toml_migration,
    prove_runtime_readiness,
)

ROOT = Path(__file__).resolve().parents[1]


class TomlMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = Path(self.temporary.name) / "fixture"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def standard_fixture(self) -> None:
        self.write(
            "dset/scopes/gov/items.yaml",
            "schema_version: 1.0\nitems:\n  -\n    id: DSET-ITEM-001\n",
        )
        self.write(
            "dset/scopes/gov/index.yaml",
            "schema_version: 1.0\ntarget: items.yaml\n",
        )
        self.write(
            "dset/scopes/gov/record.md",
            "---\nartifact_id: DSET-RECORD-001\nrelations:\n"
            "  - items.yaml\n---\n[items](items.yaml)\n",
        )

    def selector_sealed_package_fixture(self) -> Path:
        for layer in ("meta", "gov", "tool", "skill", "ops"):
            (self.root / f"dset/scopes/{layer}").mkdir(parents=True, exist_ok=True)
        self.write(
            "dset/scopes/meta/dset.yaml",
            'schema_version: "1.2"\n',
        )
        package = self.write(
            "dset/scopes/gov/specs/packages/example/package.yaml",
            'schema_version: "1.2"\n'
            "package_id: example\n"
            "layer: gov\n"
            "requirements:\n"
            "  - DSET-REQUIREMENT-GOV-001\n"
            "tests: []\n"
            "evals: []\n"
            "contracts: []\n"
            "stories: []\n"
            "outcomes: []\n"
            "artifacts:\n"
            "  hub: README.md\n"
            "  domain: domain.md\n"
            "  spec: spec.md\n"
            "  contracts: contracts.md\n"
            "  stories: stories.md\n"
            "  outcomes: outcomes.md\n"
            "  test_plan: test-plan.md\n"
            "  eval_plan: eval-plan.md\n",
        )
        for name in (
            "README.md",
            "domain.md",
            "contracts.md",
            "stories.md",
            "outcomes.md",
            "eval-plan.md",
        ):
            relative = package.parent.relative_to(self.root).as_posix()
            self.write(f"{relative}/{name}", "")
        self.write(
            "dset/scopes/gov/specs/packages/example/spec.md",
            "# DSET-REQUIREMENT-GOV-001\n",
        )
        self.write(
            "dset/scopes/gov/specs/packages/example/test-plan.md",
            "# DSET-TEST-GOV-040\n",
        )
        self.write(
            "dset/scopes/gov/atoms/DSET-ATOMIC-RECORD-061.md",
            "+++\n"
            'artifact_type = "atomic_record"\n'
            'artifact_id = "DSET-ATOMIC-RECORD-061"\n'
            'type = "qa"\n'
            'subtype = "test"\n'
            'semantic_id = "DSET-TEST-GOV-040"\n'
            'status = "accepted"\n'
            'priority = "critical"\n'
            'llm_session_ids = ["codex:test"]\n'
            "+++\n\n# Test\n",
        )
        selector = "requirements:DSET-REQUIREMENT-GOV-001"
        digest = hashlib.sha256(f"{selector}\n".encode()).hexdigest()
        self.write(
            "dset/scopes/gov/governance/legacy-authority.yaml",
            'schema_version: "1.0"\n'
            "records:\n"
            "  -\n"
            "    semantic_id: DSET-REQUIREMENT-GOV-001\n"
            "    fragments:\n"
            "      -\n"
            "        path: dset/scopes/gov/specs/packages/example/package.yaml\n"
            f"        selector: {selector}\n"
            f"        sha256: {digest}\n",
        )
        return package

    def test_dry_run_is_no_write_and_has_complete_digest_and_reference_map(
        self,
    ) -> None:
        self.standard_fixture()
        index = self.root / "dset/scopes/gov/index.yaml"
        before = index.read_text(encoding="utf-8")

        plan = plan_toml_migration(self.root)
        report = plan.report()

        self.assertTrue(plan.ready)
        self.assertEqual(len(plan.entries), 3)
        changes = {
            item["source"]: item
            for item in cast(list[dict[str, str]], report["changes"])
        }
        self.assertEqual(
            changes["dset/scopes/gov/index.yaml"]["before_sha256"],
            hashlib.sha256(before.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(
            changes["dset/scopes/gov/index.yaml"]["target"],
            "dset/scopes/gov/index.toml",
        )
        references = cast(list[dict[str, object]], report["reference_rewrites"])
        self.assertGreaterEqual(len(references), 2)
        counts = cast(dict[str, object], report["counts"])
        self.assertEqual(counts["changes"], 3)
        self.assertEqual(
            counts["changes_by_kind"],
            {"markdown-frontmatter": 1, "structured": 2},
        )
        self.assertTrue(index.exists())
        self.assertFalse(index.with_suffix(".toml").exists())
        self.assertIn("---", (self.root / "dset/scopes/gov/record.md").read_text())

    def test_apply_is_idempotent_and_rewrites_references(self) -> None:
        self.standard_fixture()

        applied = apply_toml_migration(self.root)

        self.assertTrue(applied.ready)
        items = self.root / "dset/scopes/gov/items.toml"
        index = self.root / "dset/scopes/gov/index.toml"
        record = self.root / "dset/scopes/gov/record.md"
        self.assertTrue(items.is_file())
        self.assertFalse(items.with_suffix(".yaml").exists())
        parsed_index = load_toml(index.read_text(encoding="utf-8"))
        self.assertEqual(parsed_index["target"], "items.toml")
        rendered_record = record.read_text(encoding="utf-8")
        self.assertTrue(rendered_record.startswith("+++\n"))
        self.assertIn("items.toml", rendered_record)
        second = apply_toml_migration(self.root)
        self.assertEqual(second.entries, ())

    def test_explicit_exceptions_retain_the_json_schema_contract_boundary(
        self,
    ) -> None:
        self.write(".github/workflows/test.yaml", "name: test\n")
        self.write("skills/dset/agents/openai.yaml", "interface: host\n")
        self.write("skills/dset/SKILL.md", "---\nname: dset\n---\n# DSET\n")
        self.write(
            "dset/scopes/gov/schemas/example.schema.json",
            json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema"}),
        )
        plan = plan_toml_migration(self.root)
        report = plan.report()
        categories = {
            item["category"]
            for item in cast(list[dict[str, str]], report["exceptions"])
        }
        self.assertTrue(
            {
                "github-actions",
                "host-skill-metadata",
                "host-skill-frontmatter",
                "external-json-schema",
            }.issubset(categories)
        )
        self.assertTrue(plan.ready)
        schema = next(
            item
            for item in cast(list[dict[str, object]], report["exceptions"])
            if item["category"] == "external-json-schema"
        )
        self.assertEqual(schema["authority"], "canonical-external-contract")
        self.assertFalse(schema["editable_toml_duplicate"])

    def test_immutable_history_is_never_converted_or_reference_rewritten(
        self,
    ) -> None:
        item = self.write("dset/scopes/gov/items.yaml", "id: current\n")
        atom = self.write(
            "dset/scopes/gov/atoms/DSET-ATOMIC-RECORD-001.md",
            "---\nartifact_id: DSET-ATOMIC-RECORD-001\n---\nSee items.yaml.\n",
        )
        proof = self.write(
            "dset/scopes/gov/changes/example/proofs/result.md",
            "---\nartifact_type: evidence_record\n---\nSee items.yaml.\n",
        )
        decision = self.write(
            "dset/scopes/gov/changes/example/decision-DSET-DECISION-GOV-001.md",
            "# Decision\n\nSee items.yaml.\n",
        )
        decision_digest = hashlib.sha256(decision.read_bytes()).hexdigest()
        self.write(
            "dset/scopes/gov/governance/atoms.yaml",
            "records:\n"
            "  -\n"
            "    semantic_id: DSET-REQUIREMENT-GOV-001\n"
            "    path: dset/scopes/gov/atoms/DSET-ATOMIC-RECORD-001.md\n",
        )
        self.write(
            "dset/scopes/gov/governance/legacy-authority.yaml",
            "records:\n"
            "  -\n"
            "    semantic_id: DSET-DECISION-GOV-001\n"
            "    fragments:\n"
            "      -\n"
            "        path: dset/scopes/gov/changes/example/"
            "decision-DSET-DECISION-GOV-001.md\n"
            "        selector: whole-carrier\n"
            f"        sha256: {decision_digest}\n",
        )
        before = {path: path.read_bytes() for path in (atom, proof, decision)}

        plan = plan_toml_migration(self.root)
        categories = {
            str(item["category"])
            for item in plan.exceptions
            if item["path"]
            in {
                atom.relative_to(self.root).as_posix(),
                proof.relative_to(self.root).as_posix(),
                decision.relative_to(self.root).as_posix(),
            }
        }
        self.assertEqual(
            categories,
            {
                "immutable-sealed-atom",
                "immutable-promoted-proof",
                "immutable-legacy-decision-carrier",
            },
        )

        apply_toml_migration(self.root)

        self.assertFalse(item.is_file())
        self.assertTrue(item.with_suffix(".toml").is_file())
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)

    def test_selector_sealed_package_gets_one_current_native_successor(self) -> None:
        package = self.selector_sealed_package_fixture()
        before = package.read_bytes()
        reference = self.write(
            "README.md",
            "See dset/scopes/gov/specs/packages/example/package.yaml.\n",
        )

        plan = plan_toml_migration(self.root, bypass_runtime_readiness=True)

        self.assertTrue(plan.ready)
        self.assertEqual(len(plan.package_successors), 1)
        self.assertEqual(plan.package_successors[0].status, "pending")
        self.assertNotIn(package, [entry.source for entry in plan.entries])
        apply_toml_migration(self.root, bypass_runtime_readiness=True)

        successor = package.with_suffix(".toml")
        self.assertEqual(package.read_bytes(), before)
        data = load_toml(successor.read_text(encoding="utf-8"))
        self.assertIn("DSET-REQUIREMENT-GOV-001", data["requirements"])
        self.assertIn("DSET-TEST-GOV-040", data["tests"])
        self.assertIn("package.toml", reference.read_text(encoding="utf-8"))
        selected = RepositoryLayout.structured_named_files(self.root, "package")
        self.assertEqual(selected, (successor,))

        second = apply_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertEqual(second.entries, ())
        self.assertEqual(second.references, ())
        self.assertEqual(second.package_successors[0].status, "current")

    def test_registered_snapshot_is_preserved_with_toml_only_current_reads(
        self,
    ) -> None:
        for layer in ("meta", "gov", "tool", "skill", "ops"):
            (self.root / f"dset/scopes/{layer}").mkdir(parents=True, exist_ok=True)
        self.write("dset/scopes/meta/dset.yaml", 'schema_version: "1.2"\n')
        snapshot = self.write(
            "dset/scopes/gov/items.yaml", "schema_version: 1.0\nid: historical\n"
        )
        before = snapshot.read_bytes()
        proof = self.write(
            "dset/scopes/gov/changes/example/proofs/history.md",
            "[historical](../../../items.yaml)\n",
        )
        mutable = self.write("README.md", "[current](dset/scopes/gov/items.yaml)\n")
        digest = hashlib.sha256(before).hexdigest()
        self.write(
            "dset/scopes/gov/artifact-types.yaml",
            'schema_version: "1.0"\n'
            "legacy_structured:\n"
            "  -\n"
            "    path: dset/scopes/gov/items.yaml\n"
            f"    sha256: {digest}\n"
            "    current_owner: dset/scopes/gov/items.toml\n"
            "    artifact_type: implementation\n"
            "    artifact_subtype: configuration\n"
            "    retained_for:\n"
            "      -\n"
            "        carrier_path: dset/scopes/gov/changes/example/proofs/history.md\n"
            "        reason: Immutable history.\n",
        )

        plan = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertTrue(plan.ready, plan.blockers)
        self.assertIn(snapshot, plan.preserved_structured)
        apply_toml_migration(self.root, bypass_runtime_readiness=True)

        owner = snapshot.with_suffix(".toml")
        self.assertEqual(snapshot.read_bytes(), before)
        self.assertTrue(owner.is_file())
        self.assertIn("items.yaml", proof.read_text(encoding="utf-8"))
        self.assertIn("items.toml", mutable.read_text(encoding="utf-8"))
        second = apply_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertEqual(second.entries, ())
        self.assertEqual(second.references, ())

        owner.unlink()
        self.assertEqual(
            RepositoryLayout.structured_file(snapshot.parent, "items.yaml"), owner
        )

    def test_registered_snapshot_digest_drift_blocks_migration(self) -> None:
        snapshot = self.write("dset/scopes/gov/items.yaml", "id: historical\n")
        self.write(
            "dset/scopes/gov/artifact-types.yaml",
            'schema_version: "1.0"\n'
            "legacy_structured:\n"
            "  -\n"
            "    path: dset/scopes/gov/items.yaml\n"
            f"    sha256: {'0' * 64}\n"
            "    current_owner: dset/scopes/gov/items.toml\n"
            "    artifact_type: implementation\n"
            "    artifact_subtype: configuration\n"
            "    retained_for:\n"
            "      -\n"
            "        semantic_id: DSET-REQUIREMENT-GOV-001\n"
            "        reason: Selector seal.\n",
        )
        self.assertTrue(snapshot.is_file())

        plan = plan_toml_migration(self.root, bypass_runtime_readiness=True)

        self.assertTrue(
            any("snapshot digest changed" in item for item in plan.blockers)
        )

    def test_package_successor_rejects_changed_input_and_incomplete_target(
        self,
    ) -> None:
        package = self.selector_sealed_package_fixture()
        package.write_text(
            package.read_text(encoding="utf-8").replace(
                "DSET-REQUIREMENT-GOV-001", "DSET-REQUIREMENT-GOV-999"
            ),
            encoding="utf-8",
        )
        changed = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertTrue(
            any("selector-sealed legacy fragment" in item for item in changed.blockers)
        )

        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = Path(self.temporary.name) / "fixture"
        self.root.mkdir()
        package = self.selector_sealed_package_fixture()
        package.with_suffix(".toml").write_text(
            'schema_version = "1.2"\npackage_id = "example"\nlayer = "gov"\n',
            encoding="utf-8",
        )
        incomplete = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        self.assertIn(
            "package-successor: incomplete current successor: "
            "dset/scopes/gov/specs/packages/example/package.toml",
            incomplete.blockers,
        )

    def test_readiness_binds_preserved_package_and_exact_successor(self) -> None:
        self.selector_sealed_package_fixture()
        (self.root / "dset_toolchain").mkdir()
        preview = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        targets = toml_migration._target_digests(
            self.root,
            list(preview.entries),
            list(preview.references),
            preview.package_successors,
        )
        preserved = toml_migration._preserved_input_digests(
            self.root, preview.package_successors
        )
        evidence = {
            "targets": targets,
            "preserved_inputs": preserved,
            "source_tool_sha256": toml_migration._tool_digest(self.root),
            "source_commit": toml_migration._git_head(self.root),
            "input_sha256": toml_migration._migration_input_digest(
                self.root,
                list(preview.entries),
                list(preview.references),
                list(preview.exceptions),
            ),
        }
        evidence_path = self.write(
            ".dset/toml-migration-runtime-readiness.json",
            json.dumps(evidence),
        )

        current = plan_toml_migration(self.root)
        self.assertEqual(current.runtime_readiness["status"], "current")

        evidence["preserved_inputs"] = {path: "0" * 64 for path in preserved}
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        stale_input = plan_toml_migration(self.root)
        self.assertEqual(stale_input.runtime_readiness["status"], "stale")
        stale_input_items = cast(
            list[str], stale_input.runtime_readiness["missing_or_stale"]
        )
        self.assertTrue(
            any(str(item).startswith("preserved:") for item in stale_input_items)
        )

        evidence["preserved_inputs"] = preserved
        evidence["targets"] = {path: "f" * 64 for path in targets}
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        stale_output = plan_toml_migration(self.root)
        self.assertEqual(stale_output.runtime_readiness["status"], "stale")
        stale_output_items = cast(
            list[str], stale_output.runtime_readiness["missing_or_stale"]
        )
        self.assertTrue(set(targets) & set(stale_output_items))

    def test_inactive_historical_package_id_remains_a_relation_target(self) -> None:
        package = self.selector_sealed_package_fixture()
        package.write_text(
            package.read_text(encoding="utf-8").replace(
                "tests: []",
                "tests:\n  - DSET-TEST-GOV-012",
            ),
            encoding="utf-8",
        )
        atom = self.root / "dset/scopes/gov/atoms/DSET-ATOMIC-RECORD-061.md"
        atom.write_text(
            atom.read_text(encoding="utf-8").replace(
                "+++\n\n# Test",
                '[[relations]]\ntype = "replacement_of"\n'
                'target = "DSET-TEST-GOV-012"\n+++\n\n# Test',
            ),
            encoding="utf-8",
        )
        self.write(
            "dset/scopes/gov/governance/lifecycle.yaml",
            'schema_version: "1.0"\n'
            "events:\n"
            "  -\n"
            "    id: DSET-LIFECYCLE-EVENT-001\n"
            "    atom_id: DSET-TEST-GOV-012\n"
            "    event: absorbed\n"
            "    related:\n"
            "      - DSET-TEST-GOV-040\n",
        )

        apply_toml_migration(self.root, bypass_runtime_readiness=True)

        successor = load_toml(package.with_suffix(".toml").read_text(encoding="utf-8"))
        self.assertNotIn("DSET-TEST-GOV-012", successor["tests"])
        self.assertIn("DSET-TEST-GOV-040", successor["tests"])
        messages = [
            diagnostic.message for diagnostic in validate_artifact_relations(self.root)
        ]
        self.assertFalse(
            any(
                "unresolved relation target: DSET-TEST-GOV-012" in item
                for item in messages
            )
        )

    def test_references_cover_root_relative_bare_and_retained_carriers(self) -> None:
        self.standard_fixture()
        self.write(
            ".github/workflows/dset.yaml",
            "source: dset/scopes/gov/items.yaml\nbare: items.yaml\n",
        )
        self.write(
            "skills/dset/agents/openai.yaml",
            "input: ../../../dset/scopes/gov/items.yaml\n",
        )

        plan = plan_toml_migration(self.root)
        references = {
            (reference.path.relative_to(self.root).as_posix(), reference.source): (
                reference.target
            )
            for reference in plan.references
        }

        self.assertEqual(
            references[(".github/workflows/dset.yaml", "dset/scopes/gov/items.yaml")],
            "dset/scopes/gov/items.toml",
        )
        self.assertEqual(
            references[(".github/workflows/dset.yaml", "items.yaml")],
            "items.toml",
        )
        self.assertEqual(
            references[
                (
                    "skills/dset/agents/openai.yaml",
                    "../../../dset/scopes/gov/items.yaml",
                )
            ],
            "../../../dset/scopes/gov/items.toml",
        )

    def test_shared_bare_filename_is_safe_when_targets_share_a_suffix(self) -> None:
        self.write("dset/scopes/gov/one/shared.yaml", "id: one\n")
        self.write("dset/scopes/gov/two/shared.yaml", "id: two\n")
        self.write("dset/scopes/gov/readme.md", "---\nid: readme\n---\nshared.yaml\n")

        plan = plan_toml_migration(self.root)

        self.assertTrue(plan.ready)
        shared = [
            reference
            for reference in plan.references
            if reference.source == "shared.yaml"
        ]
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0].target, "shared.toml")

    def test_collision_and_unsupported_values_fail_closed(self) -> None:
        self.write("dset/scopes/gov/record.yaml", "id: one\n")
        self.write("dset/scopes/gov/record.json", '{"id": "two"}\n')
        collision = plan_toml_migration(self.root)
        self.assertFalse(collision.ready)
        self.assertIn(
            "target collision dset/scopes/gov/record.toml", collision.blockers[0]
        )

        with tempfile.TemporaryDirectory(dir=ROOT.parent) as raw:
            unsupported_root = Path(raw)
            path = unsupported_root / "dset/scopes/gov/value.yaml"
            path.parent.mkdir(parents=True)
            path.write_text("value: null\n", encoding="utf-8")
            unsupported = plan_toml_migration(unsupported_root)
        self.assertFalse(unsupported.ready)
        self.assertIn("null is not representable", unsupported.blockers[0])

    def test_symlinks_are_retained_and_external_targets_stop_the_plan(self) -> None:
        external = self.root.parent / "external.yaml"
        external.write_text("id: external\n", encoding="utf-8")
        internal = self.write("dset/scopes/gov/internal.yaml", "id: internal\n")
        retained = self.root / "dset/scopes/gov/retained.yaml"
        retained.symlink_to(internal)
        unsafe = self.root / "dset/scopes/gov/unsafe.yaml"
        unsafe.symlink_to(external)

        plan = plan_toml_migration(self.root)
        exceptions = cast(list[dict[str, object]], plan.report()["exceptions"])
        symlinks = [
            item for item in exceptions if item["category"] == "retained-symlink"
        ]

        self.assertEqual(len(symlinks), 2)
        self.assertFalse(plan.ready)
        self.assertTrue(any(item.startswith("path-safety:") for item in plan.blockers))
        self.assertNotIn(retained, [entry.source for entry in plan.entries])
        self.assertNotIn(unsafe, [entry.source for entry in plan.entries])

    def test_null_normalization_is_narrow_and_reported(self) -> None:
        self.write(
            "dset/scopes/gov/intake.yaml",
            "items:\n  -\n    id: ITEM-1\n    decision: null\n",
        )
        self.write(
            "dset/scopes/ops/history/pull-requests.yaml",
            "pull_requests:\n  -\n    number: 1\n    merge_commit: null\n",
        )
        self.write(
            "dset/scopes/gov/record.yaml",
            "promotion:\n  parent_scope: null\n",
        )

        plan = plan_toml_migration(self.root)
        normalizations = cast(list[dict[str, str]], plan.report()["normalizations"])

        self.assertTrue(plan.ready)
        self.assertEqual(
            {(item["source"], item["key_path"]) for item in normalizations},
            {
                ("dset/scopes/gov/intake.yaml", "items.0.decision"),
                ("dset/scopes/gov/record.yaml", "promotion.parent_scope"),
                (
                    "dset/scopes/ops/history/pull-requests.yaml",
                    "pull_requests.0.merge_commit",
                ),
            },
        )

        self.write("dset/scopes/gov/unsupported.yaml", "other: null\n")
        blocked = plan_toml_migration(self.root)
        self.assertFalse(blocked.ready)
        self.assertTrue(
            any(item.startswith("conversion:") for item in blocked.blockers)
        )

    def test_runtime_readiness_and_generated_bundle_are_explicit_gates(self) -> None:
        self.standard_fixture()
        (self.root / "dset_toolchain").mkdir()

        missing = plan_toml_migration(self.root)
        self.assertEqual(missing.runtime_readiness["status"], "missing")
        self.assertTrue(
            any(item.startswith("runtime-readiness:") for item in missing.blockers)
        )

        self.write("dset_toolchain/bootstrap_bundle.json", "{}\n")
        refreshed = plan_toml_migration(self.root)
        targets = toml_migration._target_digests(
            self.root, list(refreshed.entries), list(refreshed.references)
        )
        self.write(
            ".dset/toml-migration-runtime-readiness.json",
            json.dumps(
                {
                    "targets": targets,
                    "source_tool_sha256": toml_migration._tool_digest(self.root),
                    "source_commit": toml_migration._git_head(self.root),
                    "input_sha256": toml_migration._migration_input_digest(
                        self.root,
                        list(refreshed.entries),
                        list(refreshed.references),
                        list(refreshed.exceptions),
                    ),
                }
            ),
        )
        gated = plan_toml_migration(self.root)
        self.assertEqual(gated.runtime_readiness["status"], "current")
        self.assertTrue(gated.ready)

    def test_cli_apply_on_blocked_plan_prints_the_plan_without_applying(self) -> None:
        blocked = MigrationPlan(
            root=ROOT,
            entries=(),
            exceptions=(),
            references=(),
            blockers=("conversion: test blocker",),
            runtime_readiness={"status": "missing"},
        )
        output = StringIO()
        with (
            patch("dset_toolchain.cli.plan_toml_migration", return_value=blocked),
            patch("dset_toolchain.cli.apply_toml_migration") as apply,
            redirect_stdout(output),
        ):
            status = main(["migrate", "toml", str(ROOT), "--apply"])

        self.assertEqual(status, 1)
        self.assertIn("DRY RUN TOML migration blocked", output.getvalue())
        self.assertIn("BLOCKED conversion: test blocker", output.getvalue())
        apply.assert_not_called()

    def test_apply_regenerates_bundle_and_rolls_back_after_runtime_failure(
        self,
    ) -> None:
        self.standard_fixture()
        self.write("dset_toolchain/bootstrap_bundle.json", "old bundle\n")
        self.write("scripts/build_bootstrap_bundle.py", "# builder placeholder\n")
        bundle = self.root / "dset_toolchain/bootstrap_bundle.json"
        original = bundle.read_text(encoding="utf-8")

        with (
            patch(
                "dset_toolchain.toml_migration._render_bootstrap_bundle",
                return_value="new bundle\n",
            ),
            patch(
                "dset_toolchain.toml_migration._validate_migrated_runtime",
                side_effect=ValueError("runtime failed"),
            ),
            self.assertRaisesRegex(ValueError, "rolled back"),
        ):
            apply_toml_migration(self.root, bypass_runtime_readiness=True)

        self.assertTrue((self.root / "dset/scopes/gov/items.yaml").is_file())
        self.assertFalse((self.root / "dset/scopes/gov/items.toml").exists())
        self.assertEqual(bundle.read_text(encoding="utf-8"), original)

    def test_runtime_proof_writes_evidence_without_migrating_the_source(self) -> None:
        self.standard_fixture()
        (self.root / "dset_toolchain").mkdir()
        source = self.root / "dset/scopes/gov/items.yaml"

        with (
            patch("dset_toolchain.toml_migration._validate_migrated_runtime"),
            patch(
                "dset_toolchain.toml_migration._proof_commands",
                return_value=[{"argv": ["test"], "returncode": 0}],
            ),
        ):
            evidence = prove_runtime_readiness(self.root)

        self.assertTrue(source.is_file())
        self.assertFalse(source.with_suffix(".toml").exists())
        stored = json.loads(
            (self.root / ".dset/toml-migration-runtime-readiness.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(stored["targets"], evidence["targets"])

    def test_runtime_mapping_covers_in_place_and_reference_only_writes(self) -> None:
        self.standard_fixture()
        document = self.write(
            "dset/scopes/gov/record.md",
            "---\nid: DSET-ITEM-001\n---\nSee items.yaml.\n",
        )
        reference = self.write("README.md", "See dset/scopes/gov/items.yaml.\n")

        plan = plan_toml_migration(self.root, bypass_runtime_readiness=True)
        targets = toml_migration._target_digests(
            self.root, list(plan.entries), list(plan.references)
        )

        self.assertIn(document.relative_to(self.root).as_posix(), targets)
        self.assertIn(reference.relative_to(self.root).as_posix(), targets)

    def test_full_staged_tree_plans_native_package_successors(self) -> None:
        staged = self.root / "staged"
        excluded = {
            ".git",
            ".venv",
            ".dset",
            ".cache",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
            "build",
            "dist",
        }
        shutil.copytree(
            ROOT,
            staged,
            ignore=lambda _directory, names: set(names) & excluded,
        )
        atom = staged / (
            "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/"
            "DSET-ATOMIC-RECORD-001-artifact-type-name-policy.md"
        )
        before = atom.read_bytes()
        plan = plan_toml_migration(staged, bypass_runtime_readiness=True)

        self.assertTrue(plan.ready)
        self.assertEqual(len(plan.package_successors), 5)
        self.assertTrue(
            all(item.status == "pending" for item in plan.package_successors)
        )
        self.assertNotIn(atom, [entry.source for entry in plan.entries])
        self.assertNotIn(atom, [reference.path for reference in plan.references])
        self.assertEqual(atom.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
