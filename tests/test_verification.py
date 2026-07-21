from __future__ import annotations

import unittest
from unittest.mock import patch

from dset_toolchain.verification import _verification_args


class VerificationCommandTests(unittest.TestCase):
    def test_python_placeholder_preserves_native_windows_path(self) -> None:
        executable = r"C:\Program Files\Python312\python.exe"

        with patch("dset_toolchain.verification.sys.executable", executable):
            args = _verification_args("{python} -m unittest discover -s tests -v")

        self.assertEqual(
            args,
            [executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        )

    def test_python_placeholder_must_be_an_exact_token(self) -> None:
        with patch("dset_toolchain.verification.sys.executable", "python-native"):
            args = _verification_args("tool-{python} --check")

        self.assertEqual(args, ["tool-{python}", "--check"])


if __name__ == "__main__":
    unittest.main()
