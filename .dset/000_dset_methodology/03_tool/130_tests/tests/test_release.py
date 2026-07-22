from __future__ import annotations

import unittest

from dset_toolchain.release import (
    ProductVersion,
    expected_target,
    validate_coordinated_identity,
)


class ReleasePolicyTests(unittest.TestCase):
    def test_transition_matrix(self) -> None:
        cases: tuple[tuple[str, str, bool, str], ...] = (
            ("0.2.4", "small", False, "0.2.5"),
            ("0.2.4", "normal", False, "0.3.0"),
            ("0.9.0", "normal", False, "0.10.0"),
            ("1.4.9", "small", False, "1.4.10"),
            ("1.4.9", "normal", False, "1.5.0"),
            ("1.4.9", "breaking", False, "2.0.0"),
            ("0.9.0", "rc", True, "1.0.0-rc.1"),
            ("1.0.0-rc.4", "rc", False, "1.0.0-rc.5"),
            ("1.0.0-rc.4", "final", True, "1.0.0"),
        )
        for base, release_class, readiness, target in cases:
            with self.subTest(base=base, release_class=release_class):
                self.assertEqual(
                    expected_target(
                        base, release_class, readiness_passed=readiness
                    ).semver,
                    target,
                )

    def test_bootstrap_is_explicit_and_pre_one(self) -> None:
        self.assertEqual(
            expected_target(
                "unversioned", "bootstrap", bootstrap_target="0.3.1"
            ).semver,
            "0.3.1",
        )
        for base, target in (("0.1.0", "0.3.1"), (None, "1.0.0")):
            with self.subTest(base=base, target=target), self.assertRaises(ValueError):
                expected_target(base, "bootstrap", bootstrap_target=target)

    def test_invalid_progressions_fail(self) -> None:
        cases: tuple[tuple[str, str, bool], ...] = (
            ("0.9.0", "rc", False),
            ("1.0.0-rc.1", "small", False),
            ("1.0.0-rc.1", "normal", False),
            ("1.0.0-rc.1", "final", False),
            ("0.4.0", "breaking", False),
            ("1.2.0", "final", True),
        )
        for base, release_class, readiness in cases:
            with (
                self.subTest(base=base, release_class=release_class),
                self.assertRaises(ValueError),
            ):
                expected_target(base, release_class, readiness_passed=readiness)

    def test_rc_identity_has_one_exact_python_mapping(self) -> None:
        version = ProductVersion.parse("1.0.0-rc.12")
        self.assertEqual(version.python, "1.0.0rc12")
        validate_coordinated_identity(version.semver, "1.0.0rc12")
        with self.assertRaises(ValueError):
            validate_coordinated_identity(version.semver, "1.0.0-rc.12")

    def test_semver_parser_rejects_noncanonical_versions(self) -> None:
        for version in ("v1.2.3", "01.2.3", "1.2", "1.0.0-rc0"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                ProductVersion.parse(version)


if __name__ == "__main__":
    unittest.main()
