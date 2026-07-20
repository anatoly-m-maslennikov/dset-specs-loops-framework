from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from dset_toolchain.adopter import create_adopter
from dset_toolchain.skill_distribution import (
    SKILL_WORKFLOWS,
    SkillDistributionError,
    apply_install,
    apply_runtime_install,
    default_destination,
    default_package_destination,
    invocation_receipt_template,
    main,
    plan_install,
    plan_runtime_install,
    verify_installation,
    verify_invocation_receipt,
    verify_runtime_installation,
)

ROOT = Path(__file__).resolve().parents[1]


class SkillDistributionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        shutil.copytree(ROOT / "skills", self.source / "skills")
        shutil.copytree(
            ROOT / "dset_toolchain",
            self.source / "dset_toolchain",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_install_is_dry_run_then_copies_all_public_codex_skills(self) -> None:
        destination = self.root / "codex-skills"
        actions = plan_install(self.source, "codex", destination)

        self.assertEqual(len(actions), len(SKILL_WORKFLOWS))
        self.assertEqual({item.status for item in actions}, {"create"})
        self.assertFalse(destination.exists())

        proofs = apply_install(actions)

        self.assertEqual({item.skill_id for item in proofs}, set(SKILL_WORKFLOWS))
        self.assertTrue(all(item.copied_folder for item in proofs))
        self.assertTrue(all(item.discoverable for item in proofs))
        self.assertTrue(all(item.invocation_contract for item in proofs))
        for skill_id in SKILL_WORKFLOWS:
            installed = destination / skill_id
            self.assertTrue(installed.is_dir())
            self.assertFalse(installed.is_symlink())
            self.assertTrue((installed / "agents" / "openai.yaml").is_file())
            wrapper = (installed / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                str(destination.parent / "packages" / "dset" / "dset.py"),
                wrapper,
            )
            self.assertNotIn("`dset skills context", wrapper)
        self.assertEqual(
            {item.status for item in plan_install(self.source, "codex", destination)},
            {"current"},
        )

    def test_claude_copy_and_default_destinations_are_portable(self) -> None:
        destination = self.root / "claude-skills"
        apply_install(plan_install(self.source / "skills", "claude", destination))
        proofs = verify_installation("claude", destination)
        self.assertEqual(len(proofs), len(SKILL_WORKFLOWS))

        home = self.root / "home"
        self.assertEqual(
            default_destination("codex", environment={}, home=home),
            home / ".codex" / "skills",
        )
        self.assertEqual(
            default_destination("claude", environment={}, home=home),
            home / ".claude" / "skills",
        )
        configured = self.root / "configured"
        self.assertEqual(
            default_destination(
                "codex", environment={"CODEX_HOME": str(configured)}, home=home
            ),
            configured / "skills",
        )
        self.assertEqual(
            default_package_destination("codex", environment={}, home=home),
            home / ".codex" / "packages" / "dset",
        )
        self.assertEqual(
            default_package_destination(
                "claude",
                environment={"CLAUDE_CONFIG_DIR": str(configured)},
                home=home,
            ),
            configured / "packages" / "dset",
        )
        self.assertEqual(
            default_destination(
                "claude",
                environment={"CLAUDE_CONFIG_DIR": str(configured)},
                home=home,
            ),
            configured / "skills",
        )

    def test_shared_runtime_package_is_copied_and_executable(self) -> None:
        destination = self.root / "codex" / "packages" / "dset"
        action = plan_runtime_install(ROOT, "codex", destination)

        self.assertEqual(action.status, "create")
        self.assertFalse(destination.exists())
        proof = apply_runtime_install(action)

        self.assertEqual(proof.destination, str(destination))
        self.assertTrue(proof.copied_package)
        self.assertTrue(proof.manifest_current)
        self.assertEqual(proof.portable_launcher, "dset.py")
        self.assertEqual(
            verify_runtime_installation("codex", destination).digest,
            proof.digest,
        )
        completed = subprocess.run(
            [sys.executable, str(destination / "dset.py"), "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "0.3.1")
        self.assertEqual(
            plan_runtime_install(ROOT, "codex", destination).status,
            "current",
        )

    def test_installed_runtime_resolves_explicit_project_target(self) -> None:
        package = self.root / "codex" / "packages" / "dset"
        apply_runtime_install(plan_runtime_install(ROOT, "codex", package))
        project = self.root / "project"
        create_adopter(ROOT, project)
        target = project / "src" / "nested"
        target.mkdir(parents=True)

        completed = subprocess.run(
            [
                sys.executable,
                str(package / "dset.py"),
                "skills",
                "context",
                "--skill",
                "dset-implement",
                "--target",
                str(target),
                "--objective",
                "Resolve from the installed host package",
                "--llm-session-id",
                "codex:test-session",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        context = json.loads(completed.stdout)
        self.assertEqual(context["repository_root"], str(project))
        self.assertEqual(context["skill_id"], "dset-implement")
        self.assertEqual(context["workflow_id"], "implement")
        self.assertTrue(str(context["ruleset_identity"]).startswith("ruleset:"))
        terminal = subprocess.run(
            [
                sys.executable,
                str(package / "dset.py"),
                "runtime",
                "finish",
                str(context["run"]["run_id"]),
                str(project),
                "--status",
                "succeeded",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(terminal.returncode, 0, terminal.stderr)
        self.assertEqual(json.loads(terminal.stdout)["status"], "succeeded")

    def test_runtime_package_conflict_stops_without_overwrite(self) -> None:
        destination = self.root / "claude" / "packages" / "dset"
        apply_runtime_install(plan_runtime_install(ROOT, "claude", destination))
        launcher = destination / "dset.py"
        launcher.write_text("operator content\n", encoding="utf-8")

        action = plan_runtime_install(ROOT, "claude", destination)
        self.assertEqual(action.status, "conflict")
        with self.assertRaisesRegex(
            SkillDistributionError, "runtime destination differs"
        ):
            apply_runtime_install(action)
        self.assertEqual(launcher.read_text(encoding="utf-8"), "operator content\n")

    def test_conflicting_destination_stops_without_overwrite(self) -> None:
        destination = self.root / "codex-skills"
        apply_install(plan_install(self.source, "codex", destination))
        skill = destination / "dset" / "SKILL.md"
        skill.write_text("local operator content\n", encoding="utf-8")

        actions = plan_install(self.source, "codex", destination)
        self.assertIn("conflict", {item.status for item in actions})
        with self.assertRaisesRegex(SkillDistributionError, "destination differs"):
            apply_install(actions)
        self.assertEqual(skill.read_text(encoding="utf-8"), "local operator content\n")

    def test_source_with_an_extra_public_skill_is_rejected(self) -> None:
        extra = self.source / "skills" / "dset-extra"
        extra.mkdir()
        (extra / "SKILL.md").write_text(
            "---\nname: dset-extra\ndescription: extra\n---\n", encoding="utf-8"
        )

        with self.assertRaisesRegex(
            SkillDistributionError, "public DSET skill catalog"
        ):
            plan_install(self.source, "codex", self.root / "target")

    def test_invocation_receipt_requires_real_host_observations(self) -> None:
        destination = self.root / "claude-skills"
        apply_install(plan_install(self.source, "claude", destination))
        receipt = invocation_receipt_template("claude", "dset-diagnose", destination)
        receipt.update(
            {
                "host_version": "test-host-1",
                "repository_identity": "fixture-repository@abc123",
                "host_session_id": "claude:test-session",
                "discovered": True,
                "loaded": True,
                "invoked": True,
                "local_rules_resolved": True,
                "handoff_observed": True,
                "stop_boundary_observed": True,
            }
        )

        verified = verify_invocation_receipt(receipt, "claude", destination)
        self.assertEqual(verified["status"], "verified")
        self.assertEqual(verified["workflow_id"], "diagnosis")

        receipt["handoff_observed"] = False
        with self.assertRaisesRegex(SkillDistributionError, "handoff_observed"):
            verify_invocation_receipt(receipt, "claude", destination)

    def test_cli_install_defaults_to_dry_run_and_requires_apply(self) -> None:
        destination = self.root / "codex-skills"
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(
                [
                    "install",
                    "--host",
                    "codex",
                    "--source",
                    str(self.source),
                    "--destination",
                    str(destination),
                ]
            )
        self.assertEqual(status, 0)
        self.assertFalse(destination.exists())
        self.assertFalse(json.loads(output.getvalue())["applied"])

        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            status = main(
                [
                    "install",
                    "--host",
                    "codex",
                    "--source",
                    str(self.source),
                    "--destination",
                    str(destination),
                    "--apply",
                ]
            )
        self.assertEqual(status, 0)
        self.assertTrue((destination / "dset" / "SKILL.md").is_file())
        package = destination.parent / "packages" / "dset"
        self.assertTrue((package / "dset.py").is_file())

    def test_combined_install_preflights_runtime_conflict_before_writes(self) -> None:
        destination = self.root / "codex" / "skills"
        package = self.root / "codex" / "packages" / "dset"
        package.mkdir(parents=True)
        (package / "dset.py").write_text("operator runtime\n", encoding="utf-8")

        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            status = main(
                [
                    "install",
                    "--host",
                    "codex",
                    "--source",
                    str(self.source),
                    "--destination",
                    str(destination),
                    "--package-destination",
                    str(package),
                    "--apply",
                ]
            )

        self.assertEqual(status, 2)
        self.assertFalse(destination.exists())
        self.assertEqual(
            (package / "dset.py").read_text(encoding="utf-8"),
            "operator runtime\n",
        )


if __name__ == "__main__":
    unittest.main()
