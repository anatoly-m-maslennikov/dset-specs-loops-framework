from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, cast

from dset_toolchain.cli import main
from dset_toolchain.layout import discover_layout
from dset_toolchain.release import (
    ReleaseError,
    check_release,
    plan_release,
    prepare_release,
)
from dset_toolchain.yaml_subset import dump, load

ROOT = Path(__file__).resolve().parents[1]


class ReleaseIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.change = self._write_project()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_plan_prepare_check_and_repeat_are_deterministic(self) -> None:
        before = self._surface_bytes()
        plan = plan_release(self.root)
        self.assertEqual(plan.owner_change, "TEST-CHANGE-OPS-001")
        self.assertEqual(plan.release_class, "normal")
        self.assertEqual(plan.target, "0.4.0")
        self.assertEqual(plan.python_target, "0.4.0")
        self.assertEqual(plan.tag, "v0.4.0")
        version_path = discover_layout(self.root).version_path
        self.assertEqual(
            set(plan.changes),
            {
                version_path.relative_to(self.root).as_posix(),
                "dset_toolchain/__init__.py",
                "pyproject.toml",
            },
        )

        preview = prepare_release(self.root)
        self.assertFalse(preview.executed)
        self.assertEqual(preview.changed, ())
        self.assertEqual(self._surface_bytes(), before)
        with self.assertRaises(ReleaseError):
            check_release(self.root)

        prepared = prepare_release(self.root, execute=True)
        self.assertTrue(prepared.executed)
        self.assertEqual(set(prepared.changed), set(plan.changes))
        self.assertEqual(check_release(self.root).target, "0.4.0")
        version = load(version_path)
        self.assertEqual(version["framework"]["version"], "0.4.0")
        self.assertEqual(version["python_package"]["version"], "0.4.0")
        self.assertIn('version = "0.4.0"', (self.root / "pyproject.toml").read_text())
        self.assertIn(
            '__version__ = "0.4.0"',
            (self.root / "dset_toolchain/__init__.py").read_text(),
        )

        repeated = prepare_release(self.root, execute=True)
        self.assertEqual(repeated.changed, ())
        self.assertTrue(repeated.plan.to_dict()["prepared"])

    def test_cli_defaults_prepare_to_read_only_and_emits_json(self) -> None:
        before = self._surface_bytes()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["release", "prepare", str(self.root), "--format", "json"])
        self.assertEqual(result, 0)
        data = json.loads(output.getvalue())
        self.assertFalse(data["executed"])
        self.assertFalse(data["prepared"])
        self.assertEqual(self._surface_bytes(), before)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    "release",
                    "prepare",
                    str(self.root),
                    "--execute",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(result, 0)
        self.assertTrue(json.loads(output.getvalue())["prepared"])

    def test_invalid_target_or_multiple_release_owners_stop(self) -> None:
        layout = discover_layout(self.root)
        manifest = layout.structured_file(self.change, "change.toml")
        data = cast(dict[str, Any], load(manifest))
        release = cast(dict[str, Any], data["release"])
        release["target"] = "0.3.2"
        manifest.write_text(dump(data, manifest), encoding="utf-8")
        with self.assertRaisesRegex(ReleaseError, "declared target"):
            plan_release(self.root)

        release["target"] = "0.4.0"
        manifest.write_text(dump(data, manifest), encoding="utf-8")
        duplicate = self.root / "dset/scopes/tool/changes/duplicate"
        duplicate.mkdir(parents=True)
        (duplicate / "verification.md").write_text("ready\n", encoding="utf-8")
        (duplicate / "TEST-DELIVERY-003-release.md").write_text(
            (self.change / "TEST-DELIVERY-003-release.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        duplicate_manifest = layout.structured_file(duplicate, "change.toml")
        duplicate_data = cast(dict[str, Any], load(manifest))
        duplicate_data["id"] = "TEST-CHANGE-TOOL-001"
        duplicate_manifest.write_text(
            dump(duplicate_data, duplicate_manifest), encoding="utf-8"
        )
        with self.assertRaisesRegex(ReleaseError, "exactly one owner"):
            plan_release(self.root)

    def test_readiness_record_is_the_only_release_gate_authority(self) -> None:
        readiness = self.change / "TEST-DELIVERY-003-release.md"
        ready_text = readiness.read_text(encoding="utf-8")
        readiness.write_text(
            ready_text.replace("disposition: ready", "disposition: blocked"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ReleaseError, "blocks this release"):
            plan_release(self.root)

        readiness.write_text(
            ready_text.replace(
                'candidate_sha: "2222222222222222222222222222222222222222"',
                'candidate_sha: "3333333333333333333333333333333333333333"',
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ReleaseError, "candidate does not match"):
            plan_release(self.root)

        readiness.write_text("# Verification says ready\n", encoding="utf-8")
        with self.assertRaisesRegex(ReleaseError, "YAML frontmatter"):
            plan_release(self.root)

    def test_archived_prepared_owner_remains_publishable(self) -> None:
        prepare_release(self.root, execute=True)
        archive = self.root / "dset/scopes/ops/changes/archive/release"
        archive.parent.mkdir()
        self.change.rename(archive)
        plan = check_release(self.root)
        self.assertEqual(plan.owner_change, "TEST-CHANGE-OPS-001")
        self.assertEqual(plan.target, "0.4.0")

    def test_publisher_is_exact_merge_idempotent_and_collision_guarded(self) -> None:
        workflow = (ROOT / ".github/workflows/publish-release.yml").read_text(
            encoding="utf-8"
        )
        version_relative = (
            discover_layout(ROOT).version_path.relative_to(ROOT).as_posix()
        )
        for phrase in (
            "paths:",
            version_relative,
            "ref: ${{ github.sha }}",
            'test "$(git rev-parse HEAD)" = "$MERGE_SHA"',
            "release check . --format json",
            '"publish": str(prior_version != version).lower()',
            "if: steps.release.outputs.publish == 'true'",
            "git/matching-refs/tags/$TAG",
            "git/tags/$object_sha",
            'test "$object_sha" = "$MERGE_SHA"',
            'test "$prerelease" = "$PRERELEASE"',
            'if [ "$count" = "0" ]',
            "repos/$GITHUB_REPOSITORY/git/refs",
            "repos/$GITHUB_REPOSITORY/releases",
        ):
            self.assertIn(phrase, workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("--force", workflow)

    def _write_project(self) -> Path:
        scopes = self.root / "dset" / "scopes"
        for layer in ("meta", "gov", "tool", "skill", "ops"):
            (scopes / layer / "changes").mkdir(parents=True)
        manifest_path = scopes / "meta" / "dset.toml"
        manifest_path.write_text(
            dump(
                {
                    "schema_version": "1.2",
                    "release": {
                        "status": "applicable",
                        "integration_branch": "dev",
                        "protected_branch": "main",
                        "publisher": "github",
                        "tag_pattern": "v{product_version}",
                    },
                },
                manifest_path,
            ),
            encoding="utf-8",
        )
        version_path = scopes / "meta" / "version.toml"
        version_path.write_text(
            dump(
                {
                    "schema_version": "1.2",
                    "framework": {
                        "version": "0.3.1",
                        "versioning": "coordinated-product-package",
                    },
                    "python_package": {
                        "name": "dset-spec-loops",
                        "version": "0.3.1",
                        "versioning": "coordinated-product-package",
                    },
                    "schemas": {"version": "1.2", "versioning": "independent"},
                },
                version_path,
            ),
            encoding="utf-8",
        )
        (self.root / "pyproject.toml").write_text(
            """[build-system]
requires = ["setuptools>=68"]

[project]
name = "dset-spec-loops"
version = "0.3.1"

[tool.example]
version = "independent"
""",
            encoding="utf-8",
        )
        package = self.root / "dset_toolchain"
        package.mkdir()
        (package / "__init__.py").write_text(
            '__version__ = "0.3.1"\n', encoding="utf-8"
        )
        change = scopes / "ops" / "changes" / "release"
        change.mkdir()
        (change / "verification.md").write_text("# Verification\n", encoding="utf-8")
        (change / "TEST-DELIVERY-003-release.md").write_text(
            """---
artifact_type: delivery
artifact_subtype: readiness_record
artifact_id: TEST-DELIVERY-003
version_scope_ref: TEST-DELIVERY-001
release_plan_ref: TEST-DELIVERY-002
candidate_sha: "2222222222222222222222222222222222222222"
disposition: ready
llm_session_ids: []
---

# Readiness Record
""",
            encoding="utf-8",
        )
        change_manifest = change / "change.toml"
        change_manifest.write_text(
            dump(
                {
                    "schema_version": "1.2",
                    "id": "TEST-CHANGE-OPS-001",
                    "status": "in-progress",
                    "release": {
                        "policy": "dset/scopes/ops/governance/release.md",
                        "class": "normal",
                        "base": {
                            "ref": "main",
                            "commit": "1111111111111111111111111111111111111111",
                            "version": "0.3.1",
                        },
                        "target": "0.4.0",
                        "readiness": "TEST-DELIVERY-003-release.md",
                        "candidate_commit": (
                            "2222222222222222222222222222222222222222"
                        ),
                    },
                },
                change_manifest,
            ),
            encoding="utf-8",
        )
        return change

    def _surface_bytes(self) -> dict[str, bytes]:
        version_path = discover_layout(self.root).version_path
        version_relative = version_path.relative_to(self.root).as_posix()
        return {
            path: (self.root / path).read_bytes()
            for path in (
                version_relative,
                "pyproject.toml",
                "dset_toolchain/__init__.py",
            )
        }


if __name__ == "__main__":
    unittest.main()
