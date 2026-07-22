from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dset_toolchain.temp_paths import scratch_root, temporary_directory


class TemporaryPathTests(unittest.TestCase):
    def test_posix_scratch_ignores_ambient_temp_configuration(self) -> None:
        with patch.dict("os.environ", {"TMPDIR": "/repository"}):
            self.assertEqual(
                scratch_root(
                    platform_name="posix",
                    allow_test_override=False,
                ),
                Path("/tmp"),
            )

    def test_scratch_directory_lives_under_root_and_dies_on_exit(self) -> None:
        with temporary_directory(prefix="dset-cleanup-") as raw:
            path = Path(raw)
            self.assertEqual(path.parent, scratch_root())
            self.assertTrue(path.is_dir())
        self.assertFalse(path.exists())

    def test_windows_uses_the_native_system_temp_root(self) -> None:
        native = tempfile.gettempdir()
        with patch(
            "dset_toolchain.temp_paths.tempfile.gettempdir", return_value=native
        ):
            self.assertEqual(
                scratch_root(platform_name="nt", allow_test_override=False),
                Path(native).resolve(),
            )


if __name__ == "__main__":
    unittest.main()
