from __future__ import annotations

import sys
from pathlib import Path


def _project_root(start: Path) -> Path:
    for candidate in start.resolve().parents:
        if (candidate / ".dset" / "dset_settings.toml").is_file():
            return candidate
    raise FileNotFoundError("DSET project root is unavailable")


def main() -> int:
    sys.dont_write_bytecode = True
    carrier = Path(__file__).resolve()
    local_package_root = carrier.parent
    project_root = _project_root(carrier)
    package_root = (
        local_package_root
        if (local_package_root / "dset_toolchain").is_dir()
        else project_root
    )
    sys.path.insert(0, str(package_root))

    from dset_toolchain.cli import main as dset_main

    return dset_main()


if __name__ == "__main__":
    raise SystemExit(main())
