from __future__ import annotations

import json
import unittest
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

import dset_toolchain.bootstrap as bootstrap
from dset_toolchain.bootstrap import (
    InitializationError,
    WorkArea,
    bundled_source_digest,
    initialize_project,
    parse_work_area,
)
from dset_toolchain.layout import discover_layout
from dset_toolchain.scaffold import create_change
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.validation import validate_repository
from dset_toolchain.yaml_subset import load
from scripts.build_bootstrap_bundle import render_bundle
from tests.git_fixtures import initialize_exact_git_repository

ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def test_generated_bundle_is_fresh_and_digest_valid(self) -> None:
        bundle_path = ROOT / "dset_toolchain" / "bootstrap_bundle.json"
        committed = bundle_path.read_text(encoding="utf-8")
        self.assertEqual(committed, render_bundle())
        bundle = json.loads(committed)
        self.assertEqual(bundle["sha256"], bundled_source_digest())

    def test_preview_does_not_touch_existing_repository(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "existing").resolve()
            target.mkdir()
            marker = target / "existing.txt"
            marker.write_text("keep", encoding="utf-8")
            result = initialize_project(
                target,
                project_key="APP",
                project_id="sample-app",
                project_name="Sample App",
                project_license="MIT",
                work_areas=(WorkArea("source", "src"),),
            )
            self.assertFalse(result.executed)
            self.assertGreater(len(result.paths), 20)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertFalse((target / "dset").exists())

    def test_execute_initializes_and_validates_nonempty_repository(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "existing").resolve()
            (target / "src").mkdir(parents=True)
            (target / "README.md").write_text("# Existing\n", encoding="utf-8")
            dependency = target / "node_modules/dependency/README.md"
            dependency.parent.mkdir(parents=True)
            dependency.write_text("[missing](./NOT-PACKAGED.md)\n", encoding="utf-8")
            result = initialize_project(
                target,
                project_key="APP",
                project_id="sample-app",
                project_name="Sample App",
                project_license="MIT",
                repository="owner/sample-app",
                work_areas=(WorkArea("source", "src"),),
                execute=True,
            )
            self.assertTrue(result.executed)
            self.assertEqual(validate_repository(target), [])
            self.assertTrue((target / "skills" / "dset" / "SKILL.md").is_file())
            layout = discover_layout(target)
            self.assertEqual(layout.schema_version, "1.3")
            self.assertEqual(
                layout.manifest_path.suffix,
                discover_layout(ROOT).manifest_path.suffix,
            )
            self.assertEqual(
                layout.artifact_type_registry_path.suffix,
                layout.manifest_path.suffix,
            )
            manifest = load(layout.manifest_path)
            self.assertEqual(manifest["project"]["repository_slug"], "sample-app")
            self.assertEqual(
                manifest["work_areas"],
                [{"id": "source", "path": "src"}],
            )
            self.assertNotIn("delegation_budget", manifest["profiles"])
            self.assertNotIn("workspace_default", manifest["change_contract"])
            self.assertTrue(layout.governance_path.is_file())
            self.assertTrue((target / ".dset/dset_settings.toml").is_file())
            self.assertTrue((target / "00_project/README.md").is_file())
            self.assertTrue((target / "10_versions/README.md").is_file())
            self.assertEqual(
                (target / ".dset_runtime/.gitignore").read_text(encoding="utf-8"),
                "*\n!.gitignore\n",
            )
            self.assertFalse((target / ".dset/runtime").exists())
            self.assertFalse((target / "dset_settings.toml").exists())
            self.assertFalse((target / "dset.toml").exists())
            self.assertEqual(
                (target / "README.md").read_text(encoding="utf-8"), "# Existing\n"
            )

            default_change = create_change(
                target,
                "default-workspace",
                "methodology",
                "small",
                layer="tool",
                work_areas=["source"],
            )
            default_data = load(layout.structured_file(default_change, "change.toml"))
            self.assertEqual(default_data["target"]["work_areas"], ["source"])
            self.assertEqual(
                default_data["workspace"]["isolation"],
                "integration-branch",
            )
            self.assertEqual(default_data["workspace"]["branch"], "dev")

            isolated_change = create_change(
                target,
                "isolated-workspace",
                "methodology",
                "small",
                layer="tool",
                workspace_mode="branch-worktree",
            )
            isolated_data = load(layout.structured_file(isolated_change, "change.toml"))
            self.assertEqual(
                isolated_data["workspace"]["isolation"],
                "branch-worktree",
            )
            self.assertEqual(
                isolated_data["workspace"]["branch"],
                "dset/isolated-workspace",
            )
            self.assertEqual(isolated_data["workspace"]["base_ref"], "dev")
            self.assertEqual(validate_repository(target), [])

    def test_execute_detects_hosted_automation_supportability(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "automated").resolve()
            workflow = target / ".github/workflows/ci.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("name: CI\n", encoding="utf-8")

            result = initialize_project(
                target,
                project_key="APP",
                project_id="sample-app",
                project_name="Sample App",
                project_license="MIT",
                execute=True,
            )

            self.assertTrue(result.executed)
            self.assertEqual(validate_repository(target), [])
            manifest = load(discover_layout(target).manifest_path)
            self.assertEqual(manifest["supportability"]["status"], "applicable")
            runbook = (target / ".dset/05_layer_ops/supportability/README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Active hosted automation", runbook)

    def test_execute_ignores_git_ignored_runtime_markdown(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "existing").resolve()
            target.mkdir()
            (target / ".gitignore").write_text("tmp/\n", encoding="utf-8")
            runtime = target / "tmp/runtime/system.md"
            runtime.parent.mkdir(parents=True)
            runtime.write_text("[[host-only-link]]\n", encoding="utf-8")
            initialize_exact_git_repository(target)

            result = initialize_project(
                target,
                project_key="APP",
                project_id="sample-app",
                project_name="Sample App",
                project_license="MIT",
                execute=True,
            )

            self.assertTrue(result.executed)
            self.assertEqual(validate_repository(target), [])

    def test_existing_destination_stops_without_partial_write(self) -> None:
        with temporary_directory() as raw:
            target = (Path(raw) / "existing").resolve()
            manifest = target / ".dset" / "dset_settings.toml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text("existing\n", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                initialize_project(
                    target,
                    project_key="APP",
                    project_id="sample-app",
                    project_name="Sample App",
                    project_license="MIT",
                    execute=True,
                )
            self.assertEqual(manifest.read_text(encoding="utf-8"), "existing\n")
            self.assertFalse((target / "skills").exists())

    def test_work_area_parser_is_platform_neutral(self) -> None:
        self.assertEqual(
            parse_work_area("docs=docs/reference"), WorkArea("docs", "docs/reference")
        )
        for invalid in ("docs", "docs=/absolute", "docs=../outside", "docs=src\\win"):
            with self.subTest(invalid=invalid), self.assertRaises(InitializationError):
                area = parse_work_area(invalid)
                initialize_project(
                    ROOT,
                    project_key="APP",
                    project_id="sample-app",
                    project_name="Sample App",
                    project_license="MIT",
                    work_areas=(area,),
                )

    def test_posix_absolute_work_area_is_rejected_under_windows_semantics(
        self,
    ) -> None:
        with (
            patch.object(bootstrap, "Path", PureWindowsPath),
            self.assertRaisesRegex(
                InitializationError,
                "work-area paths must be repository-relative",
            ),
        ):
            bootstrap._validate_inputs(
                "APP",
                "sample-app",
                "Sample App",
                "MIT",
                "project",
                (WorkArea("docs", "/absolute"),),
            )


if __name__ == "__main__":
    unittest.main()
