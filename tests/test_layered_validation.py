from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dset_toolchain.layout import LAYERS
from dset_toolchain.scaffold import create_change
from dset_toolchain.traceability import build_traceability
from dset_toolchain.validation import validate_change, validate_repository
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


class LayeredValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.scopes = self.root / "dset" / "scopes"
        for layer in LAYERS:
            (self.scopes / layer).mkdir(parents=True)
        self._write_project()
        self._write_control_files()
        self._write_fragment("meta", "DSET-REQUIREMENT-001", "DSET-TEST-001")
        self._write_fragment("tool", "DSET-REQUIREMENT-TOOL-001", "DSET-TEST-TOOL-001")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_layered_repository(self) -> None:
        self.assertEqual(validate_repository(self.root), [])

    def test_fragment_ownership_and_cross_fragment_uniqueness(self) -> None:
        path = self._fragment_path("tool")
        data = load(path)
        assert isinstance(data, dict)
        data["requirements"] = ["DSET-REQUIREMENT-001"]
        path.write_text(dump(data), encoding="utf-8")
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
        path.write_text(dump(data), encoding="utf-8")
        self.assertIn(
            "DSET-E145", {item.code for item in validate_repository(self.root)}
        )

    def test_change_layer_and_duplicate_change_ids_are_rejected(self) -> None:
        first = self._write_change("tool", "layered-change")
        self.assertEqual(validate_change(self.root, first, archived=False), [])
        data = load(first / "change.yaml")
        assert isinstance(data, dict)
        data["primary_layer"] = "skill"
        data["affected_layers"] = ["skill"]
        (first / "change.yaml").write_text(dump(data), encoding="utf-8")
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
            (ROOT / "dset/schemas/project.schema.json").read_text(encoding="utf-8")
        )
        fragment = json.loads(
            (ROOT / "dset/schemas/package-fragment.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            project["$defs"]["layered_structure"]["properties"]["layout"]["const"],
            "layered-v1",
        )
        change = json.loads(
            (ROOT / "dset/schemas/change.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            change["$defs"]["workspace"]["properties"]["isolation"]["const"],
            "branch-worktree",
        )
        self.assertEqual(
            change["$defs"]["layered_release_declaration"]["properties"]["policy"][
                "const"
            ],
            "dset/scopes/ops/governance/release.md",
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

    def test_layered_traceability_carries_change_layers(self) -> None:
        self._write_change("tool", "layered-change")

        trace = build_traceability(self.root)

        self.assertEqual(trace["schema_version"], "1.2")
        self.assertEqual(trace["changes"][0]["primary_layer"], "tool")
        self.assertEqual(trace["changes"][0]["affected_layers"], ["tool"])
        self.assertEqual(trace["changes"][0]["slug"], "layered-change")
        self.assertEqual(
            trace["changes"][0]["workspace"]["isolation"], "branch-worktree"
        )

    def test_workspace_and_dependency_currentness_are_enforced(self) -> None:
        change = self._write_change("tool", "layered-change")
        path = change / "change.yaml"
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
        path.write_text(dump(data), encoding="utf-8")
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
        path.write_text(dump(data), encoding="utf-8")
        self.assertEqual(validate_change(self.root, change, archived=False), [])

    def test_scaffold_allocates_stable_change_ids_separately_from_slugs(self) -> None:
        target = self.scopes / "gov" / "templates" / "change"
        shutil.copytree(ROOT / "dset/templates/change", target)

        first = create_change(
            self.root, "portable-cli", "sample", "small", layer="tool"
        )
        second = create_change(
            self.root, "dependency-check", "sample", "small", layer="tool"
        )

        first_data = load(first / "change.yaml")
        second_data = load(second / "change.yaml")
        assert isinstance(first_data, dict)
        assert isinstance(second_data, dict)
        self.assertEqual(first_data["id"], "DSET-CHANGE-TOOL-001")
        self.assertEqual(first_data["slug"], "portable-cli")
        self.assertEqual(second_data["id"], "DSET-CHANGE-TOOL-002")
        self.assertEqual(first_data["workspace"]["isolation"], "branch-worktree")

    def test_workspace_branch_is_unique_only_while_changes_are_active(self) -> None:
        first = self._write_change(
            "tool", "first-change", stable_id="DSET-CHANGE-TOOL-101"
        )
        second = self._write_change(
            "tool", "second-change", stable_id="DSET-CHANGE-TOOL-102"
        )
        second_data = load(second / "change.yaml")
        assert isinstance(second_data, dict)
        second_data["workspace"]["branch"] = "dset/first-change"
        (second / "change.yaml").write_text(dump(second_data), encoding="utf-8")
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
            "release": {"status": "not-applicable", "reason": "fixture"},
            "work_items": {"registry": "dset/scopes/gov/intake.yaml"},
            "structure": {"layout": "layered-v1"},
            "packages": [
                {"id": "sample", "status": "active", "layers": ["meta", "tool"]}
            ],
            "profiles": {
                "runtime_risk": "low",
                "durability_topology": "files",
                "enforcement": "local",
                "delegation_budget": "medium",
            },
            "change_contract": {
                "change_id_format": "project-type-layer-sequence",
                "change_slug_format": "kebab-case",
                "workspace_default": "isolated-branch-worktree-pr",
                "pull_request_required_before_archive": True,
                "archive_requires_fresh_verification": True,
                "keep_pull_request_draft_until_archive_ready": True,
            },
            "verification": {"commands": ["python -m dset_toolchain check ."]},
            "canonical_command": "python -m dset_toolchain check .",
        }
        (self.scopes / "meta" / "dset.yaml").write_text(
            dump(manifest), encoding="utf-8"
        )

    def _write_control_files(self) -> None:
        scopes = [
            {"id": layer, "kind": "layer", "id_segment": layer.upper()}
            for layer in LAYERS
        ]
        (self.scopes / "gov" / "intake.yaml").write_text(
            dump(
                {
                    "schema_version": 1.0,
                    "scope_mode": "multi-scope",
                    "scopes": scopes,
                    "items": [],
                }
            ),
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
            "workspace": {
                "isolation": "branch-worktree",
                "branch": f"dset/{change_slug}",
                "base_ref": "main",
                "base_commit": "pending",
                "head_commit": "pending",
            },
            "dependencies": [],
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

    def _archive_synthetic(self, change: Path, day: str, pr_number: int) -> None:
        path = change / "change.yaml"
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
        path.write_text(dump(data), encoding="utf-8")
        change.replace(destination)


if __name__ == "__main__":
    unittest.main()
