from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from dset_toolchain.skill_distribution import (
    SKILL_WORKFLOWS,
    SkillDistributionError,
    apply_install,
    default_destination,
    invocation_receipt_template,
    main,
    plan_install,
    verify_installation,
    verify_invocation_receipt,
)

ROOT = Path(__file__).resolve().parents[1]


class SkillDistributionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        shutil.copytree(ROOT / "skills", self.source / "skills")

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
            default_destination(
                "claude",
                environment={"CLAUDE_CONFIG_DIR": str(configured)},
                home=home,
            ),
            configured / "skills",
        )

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

        with redirect_stdout(io.StringIO()):
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


if __name__ == "__main__":
    unittest.main()
