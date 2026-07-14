from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DsetCommandError(ValueError):
    code: str
    path: Path
    message: str

    def render(self, root: Path | None = None) -> str:
        path = self.path
        if root is not None:
            with contextlib.suppress(ValueError):
                path = path.relative_to(root)
        return f"{self.code} {path.as_posix()}: {self.message}"
