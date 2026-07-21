from __future__ import annotations

import hashlib
import io
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

from dset_toolchain.adopter import create_adopter
from dset_toolchain.skill_distribution import (
    SKILL_WORKFLOWS,
    SkillDistributionError,
    _launcher_command,
    _render_skill_package,
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
        self.temporary = tempfile.TemporaryDirectory(
            dir=ROOT.parent,
            ignore_cleanup_errors=True,
        )
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

    def install_distribution(
        self,
        host: str,
        destination: Path,
        package: Path | None = None,
    ) -> Path:
        runtime = (
            destination.parent / f".{destination.name}-packages" / "dset"
            if package is None
            else package
        )
        actions = plan_install(self.source, host, destination, runtime)
        runtime_action = plan_runtime_install(
            self.source,
            host,
            runtime,
            wrapper_source=self.source,
            skills_destination=destination,
        )
        apply_install(actions)
        apply_runtime_install(runtime_action)
        return runtime

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
            self.assertNotRegex(wrapper, r"`dset\s")
        self.assertEqual(
            {item.status for item in plan_install(self.source, "codex", destination)},
            {"current"},
        )

    def test_every_installed_wrapper_command_uses_one_runtime_launcher(self) -> None:
        destination = self.root / "installed skills"
        runtime = self.root / "runtime ü & 'quoted';$value" / "dset"
        apply_install(plan_install(self.source, "codex", destination, runtime))
        expected_launcher = _launcher_command(runtime)

        for skill_id in SKILL_WORKFLOWS:
            with self.subTest(skill=skill_id):
                source = (self.source / "skills" / skill_id / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                installed = (destination / skill_id / "SKILL.md").read_text(
                    encoding="utf-8"
                )
                source_commands = re.findall(r"`dset\s", source)
                rendered_commands = re.findall(
                    rf"`{re.escape(expected_launcher)}\s", installed
                )
                self.assertEqual(len(rendered_commands), len(source_commands))
                self.assertNotRegex(installed, r"`dset\s")

    def test_launcher_representation_is_shell_safe_on_posix_and_wsl(self) -> None:
        interpreter = "/opt/Python ü & Co/bin/python's"
        runtime = Path("/mnt/c/Users/Zoë & Team/$DSET;pkg")

        command = _launcher_command(
            runtime,
            platform_name="posix",
            executable=interpreter,
        )

        self.assertEqual(
            shlex.split(command),
            [interpreter, str(runtime / "dset.py")],
        )

    def test_launcher_representation_is_native_powershell(self) -> None:
        interpreter = r"C:\Program Files\Python ü & Co\python.exe"
        runtime = PureWindowsPath(r"C:\Users\Zoë O'Neil\$DSET; package")

        command = _launcher_command(
            runtime,
            platform_name="nt",
            executable=interpreter,
        )

        self.assertEqual(
            command,
            "& 'C:\\Program Files\\Python ü & Co\\python.exe' "
            "'C:\\Users\\Zoë O''Neil\\$DSET; package\\dset.py'",
        )
        self.assertNotIn('"', command)

        rendered = self.root / "rendered-windows-skill"
        _render_skill_package(
            self.source / "skills" / "dset-implement",
            rendered,
            "codex",
            command,
        )
        wrapper = (rendered / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(wrapper.count(f"`{command} "), 3)
        self.assertNotRegex(wrapper, r"`dset\s")

    def test_host_copy_and_default_destinations_are_portable(self) -> None:
        destination = self.root / "claude-skills"
        runtime = self.install_distribution("claude", destination)
        proofs = verify_installation("claude", destination, runtime)
        self.assertEqual(len(proofs), len(SKILL_WORKFLOWS))

        home = self.root / "home"
        self.assertEqual(
            default_destination("codex", environment={}, home=home),
            home / ".agents" / "skills",
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
            home / ".agents" / "skills",
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
        runtime = self.install_distribution("claude", destination)
        receipt = invocation_receipt_template(
            "claude", "dset-diagnose", destination, runtime
        )
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

        verified = verify_invocation_receipt(receipt, "claude", destination, runtime)
        self.assertEqual(verified["status"], "verified")
        self.assertEqual(verified["workflow_id"], "diagnosis")

        receipt["handoff_observed"] = False
        with self.assertRaisesRegex(SkillDistributionError, "handoff_observed"):
            verify_invocation_receipt(receipt, "claude", destination, runtime)

    def test_wrapper_verification_rejects_every_tree_mutation_class(self) -> None:
        destination = self.root / "wrapper-mutation-skills"
        runtime = self.install_distribution("codex", destination)
        skill = destination / "dset-diagnose"
        backup = self.root / "wrapper-backup"
        shutil.copytree(skill, backup)
        mutations = ("changed", "added", "removed", "substituted")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                if mutation == "changed":
                    path = skill / "SKILL.md"
                    path.write_text(
                        path.read_text(encoding="utf-8") + "\nchanged\n",
                        encoding="utf-8",
                    )
                elif mutation == "added":
                    (skill / "unexpected.txt").write_text("added\n", encoding="utf-8")
                elif mutation == "removed":
                    (skill / "agents" / "openai.yaml").unlink()
                else:
                    source = destination / "dset-clarify" / "SKILL.md"
                    (skill / "SKILL.md").write_bytes(source.read_bytes())
                with self.assertRaises(SkillDistributionError):
                    verify_installation("codex", destination, runtime)
                shutil.rmtree(skill)
                shutil.copytree(backup, skill)

    def test_runtime_verification_rejects_every_payload_mutation_class(self) -> None:
        destination = self.root / "runtime-mutation-skills"
        runtime = self.install_distribution("claude", destination)
        backup = self.root / "runtime-backup"
        shutil.copytree(runtime, backup)
        mutations = ("changed", "added", "removed", "substituted")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                target = runtime / "dset_toolchain" / "cli.py"
                if mutation == "changed":
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n# changed\n",
                        encoding="utf-8",
                    )
                elif mutation == "added":
                    (runtime / "unexpected.py").write_text(
                        "# added\n", encoding="utf-8"
                    )
                elif mutation == "removed":
                    target.unlink()
                else:
                    target.write_bytes(
                        (runtime / "dset_toolchain" / "runtime.py").read_bytes()
                    )
                with self.assertRaisesRegex(SkillDistributionError, "runtime payload"):
                    verify_runtime_installation("claude", runtime)
                shutil.rmtree(runtime)
                shutil.copytree(backup, runtime)

    def test_manifest_mutation_removal_and_substitution_are_rejected(self) -> None:
        destination = self.root / "manifest-mutation-skills"
        runtime = self.install_distribution("codex", destination)
        manifest = runtime / "manifest.json"
        original = manifest.read_bytes()
        for mutation in ("changed", "removed", "substituted", "added"):
            with self.subTest(mutation=mutation):
                if mutation == "changed":
                    manifest.write_bytes(manifest.read_bytes() + b" ")
                elif mutation == "removed":
                    manifest.unlink()
                elif mutation == "substituted":
                    replacement = json.loads(original)
                    replacement["installation"]["runtime_destination"] = "substitute"
                    manifest.write_text(
                        json.dumps(replacement, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                else:
                    (runtime / "manifest-copy.json").write_bytes(manifest.read_bytes())
                with self.assertRaises(SkillDistributionError):
                    verify_runtime_installation("codex", runtime)
                with self.assertRaises(SkillDistributionError):
                    verify_installation("codex", destination, runtime)
                manifest.write_bytes(original)
                (runtime / "manifest-copy.json").unlink(missing_ok=True)

    def test_receipt_rejects_post_template_distribution_mutation(self) -> None:
        destination = self.root / "receipt-skills"
        runtime = self.install_distribution("claude", destination)
        receipt = invocation_receipt_template(
            "claude", "dset-diagnose", destination, runtime
        )
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
        wrapper = destination / "dset-diagnose" / "SKILL.md"
        wrapper.write_text(
            wrapper.read_text(encoding="utf-8") + "\nchanged\n",
            encoding="utf-8",
        )
        with self.assertRaises(SkillDistributionError):
            verify_invocation_receipt(receipt, "claude", destination, runtime)

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
        preview = json.loads(output.getvalue())
        self.assertFalse(preview["applied"])
        self.assertEqual(
            set(preview["expected_manifest"]["wrappers"]),
            set(SKILL_WORKFLOWS),
        )
        self.assertEqual(len(preview["expected_manifest_digest"]), 64)

        applied_output = io.StringIO()
        with redirect_stdout(applied_output), redirect_stderr(io.StringIO()):
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
        applied = json.loads(applied_output.getvalue())
        self.assertEqual(
            applied["expected_manifest_digest"],
            hashlib.sha256((package / "manifest.json").read_bytes()).hexdigest(),
        )

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

    def test_combined_install_rolls_back_after_mid_transaction_failure(self) -> None:
        destination = self.root / "codex" / "skills"
        package = self.root / "codex" / "packages" / "dset"

        with (
            patch(
                "dset_toolchain.skill_distribution.apply_runtime_install",
                side_effect=OSError("injected runtime copy failure"),
            ),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
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
        self.assertFalse(package.exists())


if __name__ == "__main__":
    unittest.main()
