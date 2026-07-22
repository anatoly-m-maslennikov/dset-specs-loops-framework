from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dset_toolchain.skill_catalog import PUBLIC_SKILL_WORKFLOWS  # noqa: E402

OUTPUT = ROOT / "dset_toolchain" / "bootstrap_bundle.json"


def selected_files(root: Path = ROOT) -> list[Path]:
    root = root.resolve()
    selected = [root / ".dset" / "dset_settings.toml"]
    for layer in ("meta", "gov", "tool", "skill", "ops"):
        layer_root = root / ".dset" / layer
        for folder in ("schemas", "templates"):
            selected.extend(
                path for path in (layer_root / folder).rglob("*") if path.is_file()
            )
    for skill_id in sorted(PUBLIC_SKILL_WORKFLOWS):
        selected.extend(
            path
            for path in (root / "skills" / skill_id).rglob("*")
            if path.is_file()
            and not any(part.startswith(".") for part in path.relative_to(root).parts)
            and path.suffix in {".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
        )
    return sorted(set(selected))


def render_bundle(root: Path = ROOT) -> str:
    root = root.resolve()
    files = {
        path.relative_to(root).as_posix(): path.read_text(encoding="utf-8")
        for path in selected_files(root)
    }
    encoded_files = json.dumps(
        files, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    bundle = {
        "schema_version": 1,
        "sha256": hashlib.sha256(encoded_files).hexdigest(),
        "files": files,
    }
    return json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_bundle(root: Path = ROOT) -> Path:
    """Render and atomically replace the generated CLI/wire bundle."""

    root = root.resolve()
    output = root / "dset_toolchain" / "bootstrap_bundle.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(render_bundle(root), encoding="utf-8")
    temporary.replace(output)
    return output


def main() -> int:
    output = write_bundle(ROOT)
    print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
