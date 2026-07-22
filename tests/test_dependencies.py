"""Verify DSET dependencies behavior.

Assurance scope: deterministic behavior owned by this module.
Non-obvious fixtures: documented by the fixture that owns them.
Host requirements: an isolated supported Python environment.
"""

from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path

from dset_toolchain.dependencies import validate_dependency_policy
from dset_toolchain.temp_paths import temporary_directory
from dset_toolchain.yaml_subset import dump


class DependencyPolicyTests(unittest.TestCase):
    """Verify dependency policy behavior."""

    def test_exact_lock_registry_license_and_provenance_pass(self) -> None:
        with temporary_directory() as raw:
            root, policy = self._project(Path(raw))
            self.assertEqual(
                validate_dependency_policy(
                    root, policy_path=policy, today=date(2026, 7, 20)
                ),
                [],
            )

    def test_unlisted_denied_registry_drift_and_expiry_fail_closed(self) -> None:
        mutations = {
            "unlisted": lambda data: data["allow"].clear(),
            "denied": lambda data: data["deny"].append(
                {
                    "ecosystem": "python-uv",
                    "name": "example",
                    "rationale": "Disallowed package",
                }
            ),
            "registry": lambda data: data["allow"][0].update(
                {"registry": "https://private.example/simple"}
            ),
            "expired": lambda data: data["exceptions"].append(
                {
                    "id": "APP-DEPENDENCY-EXCEPTION-001",
                    "ecosystem": "python-uv",
                    "name": "other",
                    "version": "1.0.0",
                    "registry": "https://pypi.org/simple",
                    "license": "MIT",
                    "provenance": "https://pypi.org/project/other/1.0.0/",
                    "authority": "maintainers",
                    "expires_on": "2026-07-19",
                    "rationale": "Temporary compatibility bridge",
                }
            ),
        }
        expected = {
            "unlisted": "not allowed exactly",
            "denied": "denied dependency",
            "registry": "registry drift",
            "expired": "exception expired",
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), temporary_directory() as raw:
                root, policy = self._project(Path(raw), mutate=mutate)
                messages = [
                    item.message
                    for item in validate_dependency_policy(
                        root, policy_path=policy, today=date(2026, 7, 20)
                    )
                ]
                self.assertTrue(
                    any(expected[name] in item for item in messages), messages
                )

    @staticmethod
    def _project(root: Path, *, mutate: object | None = None) -> tuple[Path, Path]:
        """Handle project using the declared repository contract."""
        (root / "pyproject.toml").write_text(
            '[project]\nname = "app"\nversion = "1.0.0"\n', encoding="utf-8"
        )
        (root / "uv.lock").write_text(
            '[[package]]\nname = "app"\nversion = "1.0.0"\n'
            'source = { editable = "." }\n\n'
            '[[package]]\nname = "example"\nversion = "2.0.0"\n'
            'source = { registry = "https://pypi.org/simple" }\n',
            encoding="utf-8",
        )
        data = {
            "schema_version": "1.0",
            "policy_id": "APP-DEPENDENCY-POLICY-001",
            "version": "1.0",
            "authority": "maintainers",
            "exception_authority": "maintainers",
            "ecosystems": [
                {
                    "id": "python-uv",
                    "manifest": "pyproject.toml",
                    "lockfile": "uv.lock",
                    "registry": "https://pypi.org/simple",
                }
            ],
            "allow": [
                {
                    "ecosystem": "python-uv",
                    "name": "example",
                    "version": "2.0.0",
                    "registry": "https://pypi.org/simple",
                    "license": "MIT",
                    "provenance": "https://pypi.org/project/example/2.0.0/",
                    "rationale": "Required test dependency",
                }
            ],
            "deny": [],
            "exceptions": [],
        }
        if callable(mutate):
            mutate(data)
        policy = root / "dependency-policy.yaml"
        policy.write_text(dump(data), encoding="utf-8")
        return root, policy


if __name__ == "__main__":
    unittest.main()
