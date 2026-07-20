from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from dset_toolchain.bootstrap import (
    InitializationError,
    WorkArea,
    bundled_source_digest,
    initialize_project,
    parse_work_area,
)
from dset_toolchain.validation import validate_repository
from dset_toolchain.yaml_subset import load
from scripts.build_bootstrap_bundle import render_bundle

ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def test_generated_bundle_is_fresh_and_digest_valid(self) -> None:
        bundle_path = ROOT / "dset_toolchain" / "bootstrap_bundle.json"
        committed = bundle_path.read_text(encoding="utf-8")
        self.assertEqual(committed, render_bundle())
        bundle = json.loads(committed)
        self.assertEqual(bundle["sha256"], bundled_source_digest())

    def test_preview_does_not_touch_existing_repository(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "existing"
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
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "existing"
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
            manifest = load(target / "dset" / "scopes" / "meta" / "dset.yaml")
            self.assertEqual(manifest["project"]["repository_slug"], "sample-app")
            self.assertTrue((target / "dset/scopes/gov/artifact-types.yaml").is_file())
            self.assertTrue((target / "dset.toml").is_file())
            self.assertEqual(
                (target / "README.md").read_text(encoding="utf-8"), "# Existing\n"
            )

    def test_execute_detects_hosted_automation_supportability(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "automated"
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
            manifest = load(target / "dset/scopes/meta/dset.yaml")
            self.assertEqual(manifest["supportability"]["status"], "applicable")
            runbook = (target / "dset/scopes/ops/supportability/README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Active hosted automation", runbook)

    def test_execute_ignores_git_ignored_runtime_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "existing"
            target.mkdir()
            (target / ".gitignore").write_text("tmp/\n", encoding="utf-8")
            runtime = target / "tmp/runtime/system.md"
            runtime.parent.mkdir(parents=True)
            runtime.write_text("[[host-only-link]]\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=target, check=True)

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
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "existing"
            manifest = target / "dset" / "scopes" / "meta" / "dset.yaml"
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


if __name__ == "__main__":
    unittest.main()
