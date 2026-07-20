from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .yaml_subset import YamlSubsetError, load

LAYERS: Final[tuple[str, ...]] = ("meta", "gov", "tool", "skill", "ops")
LEGACY_SCHEMA_VERSIONS: Final[frozenset[str]] = frozenset({"1.0", "1.1"})
LAYERED_SCHEMA_VERSION: Final[str] = "1.2"
LEGACY_AUTHORITY_PATHS: Final[tuple[str, ...]] = (
    "artifact-types.toml",
    "artifact-types.yaml",
    "artifacts.toml",
    "artifacts.yaml",
    "budget.toml",
    "budget.yaml",
    "changes",
    "fixtures",
    "governance",
    "governance.toml",
    "governance.yaml",
    "history",
    "intake.toml",
    "intake.yaml",
    "migrations",
    "provenance.toml",
    "provenance.yaml",
    "schemas",
    "specs",
    "supportability",
    "templates",
    "traceability.toml",
    "traceability.yaml",
    "version.toml",
    "version.yaml",
)


@dataclass(frozen=True)
class RepositoryLayout:
    """Canonical path authority for one DSET repository.

    Schema 1.0 and 1.1 use the central ``dset/`` layout. Schema 1.2 uses
    layer-owned roots below ``dset/scopes/``. Detection is based on the
    manifest location and, when readable, its declared schema version.
    """

    root: Path
    schema_version: str | None
    layered: bool

    @property
    def dset_root(self) -> Path:
        return self.root / "dset"

    @property
    def settings_path(self) -> Path:
        return self.root / "dset_settings.toml"

    @property
    def scopes_root(self) -> Path:
        return self.dset_root / "scopes"

    def layer_root(self, layer: str) -> Path:
        normalized = layer.lower()
        if normalized not in LAYERS:
            raise ValueError(f"unknown DSET layer: {layer}")
        return self.scopes_root / normalized

    @property
    def layer_roots(self) -> dict[str, Path]:
        return {layer: self.layer_root(layer) for layer in LAYERS}

    @property
    def manifest_path(self) -> Path:
        if self.layered:
            return self.structured_file(self.layer_root("meta"), "dset.toml")
        return self.structured_file(self.dset_root, "dset.toml")

    @property
    def governance_path(self) -> Path:
        return self._owned_file("gov", self._preferred_name("governance"))

    @property
    def governance_root(self) -> Path:
        return self._owned_directory("gov", "governance")

    @property
    def artifact_registry_path(self) -> Path:
        return self._owned_file("gov", self._preferred_name("artifacts"))

    @property
    def artifact_type_registry_path(self) -> Path:
        return self._owned_file("gov", self._preferred_name("artifact-types"))

    @property
    def intake_path(self) -> Path:
        return self._owned_file("gov", self._preferred_name("intake"))

    @property
    def provenance_path(self) -> Path:
        return self._owned_file("gov", self._preferred_name("provenance"))

    @property
    def traceability_path(self) -> Path:
        if self.layered:
            return self.structured_file(
                self.layer_root("gov") / "generated",
                self._preferred_name("traceability"),
            )
        return self.structured_file(
            self.dset_root, self._preferred_name("traceability")
        )

    @property
    def migrations_root(self) -> Path:
        return self._owned_directory("gov", "migrations")

    @property
    def version_path(self) -> Path:
        return self._owned_file("meta", self._preferred_name("version"))

    @property
    def budget_path(self) -> Path:
        return self._owned_file("skill", self._preferred_name("budget"))

    @property
    def history_root(self) -> Path:
        return self._owned_directory("ops", "history")

    @property
    def history_path(self) -> Path:
        return self.structured_file(
            self.history_root, self._preferred_name("pull-requests")
        )

    @property
    def supportability_root(self) -> Path:
        return self._owned_directory("ops", "supportability")

    @property
    def fixtures_root(self) -> Path:
        return self._owned_directory("tool", "fixtures")

    @property
    def schema_roots(self) -> tuple[Path, ...]:
        if self.layered:
            return tuple(self.layer_root(layer) / "schemas" for layer in LAYERS)
        return (self.dset_root / "schemas",)

    @property
    def template_roots(self) -> tuple[Path, ...]:
        if self.layered:
            return tuple(self.layer_root(layer) / "templates" for layer in LAYERS)
        return (self.dset_root / "templates",)

    @property
    def active_change_roots(self) -> tuple[Path, ...]:
        if self.layered:
            return tuple(self.layer_root(layer) / "changes" for layer in LAYERS)
        return (self.dset_root / "changes",)

    @property
    def archive_change_roots(self) -> tuple[Path, ...]:
        return tuple(path / "archive" for path in self.active_change_roots)

    @property
    def package_roots(self) -> tuple[Path, ...]:
        if self.layered:
            return tuple(
                self.layer_root(layer) / "specs" / "packages" for layer in LAYERS
            )
        return (self.dset_root / "specs" / "packages",)

    def schema_paths(self) -> Iterator[Path]:
        seen: dict[str, Path] = {}
        for root in self.schema_roots:
            if root.is_dir():
                for path in sorted(root.glob("*.json")):
                    previous = seen.get(path.name)
                    if previous is not None:
                        raise ValueError(
                            "schema is not unique: "
                            f"{path.name} ({previous.as_posix()}, {path.as_posix()})"
                        )
                    seen[path.name] = path
                    yield path

    def find_template(self, relative: str | Path) -> Path:
        return self._find_unique(self.template_roots, relative, "template")

    def package_fragments(self) -> tuple[Path, ...]:
        fragments: list[Path] = []
        for root in self.package_roots:
            if root.is_dir():
                fragments.extend(self.structured_named_files(root, "package"))
        return tuple(sorted(fragments))

    @staticmethod
    def structured_file(directory: Path, name: str) -> Path:
        """Resolve canonical TOML with explicit legacy YAML read fallback."""

        requested = directory / name
        if requested.suffix.lower() not in {".toml", ".yaml", ".yml"}:
            return requested
        stem = requested.with_suffix("")
        canonical = stem.with_suffix(".toml")
        legacy = (stem.with_suffix(".yaml"), stem.with_suffix(".yml"))
        if canonical.is_file():
            return canonical
        for candidate in legacy:
            if candidate.is_file():
                if _registered_snapshot_after_cutover(candidate):
                    return canonical
                return candidate
        return canonical if requested.suffix.lower() == ".toml" else requested

    @staticmethod
    def structured_named_files(root: Path, stem: str) -> tuple[Path, ...]:
        """Return one TOML-preferred carrier per directory for a basename."""

        by_parent: dict[Path, list[Path]] = {}
        for suffix in (".toml", ".yaml", ".yml"):
            for path in root.rglob(f"{stem}{suffix}"):
                by_parent.setdefault(path.parent, []).append(path)
        selected: list[Path] = []
        for parent, candidates in sorted(by_parent.items()):
            canonical = parent / f"{stem}.toml"
            selected.append(
                canonical if canonical in candidates else sorted(candidates)[0]
            )
        return tuple(selected)

    def active_change_root(self, layer: str | None = None) -> Path:
        if not self.layered:
            return self.active_change_roots[0]
        if layer is None:
            raise ValueError("schema 1.2 changes require an owning DSET layer")
        return self.layer_root(layer) / "changes"

    def archive_change_root(self, layer: str | None = None) -> Path:
        return self.active_change_root(layer) / "archive"

    def find_change(self, change_id: str, *, archived: bool = False) -> Path:
        roots = self.archive_change_roots if archived else self.active_change_roots
        matches: list[Path] = []
        for root in roots:
            if not root.is_dir():
                continue
            if archived or self.layered:
                for path in root.iterdir():
                    manifest = self.structured_file(path, "change.yaml")
                    if not path.is_dir() or not manifest.is_file():
                        continue
                    try:
                        data = load(manifest)
                    except (OSError, ValueError, YamlSubsetError):
                        continue
                    if isinstance(data, dict) and data.get("id") == change_id:
                        matches.append(path)
            else:
                candidate = root / change_id
                if candidate.is_dir():
                    matches.append(candidate)
        if not matches:
            state = "archived" if archived else "active"
            raise FileNotFoundError(f"{state} change does not exist: {change_id}")
        if len(matches) > 1:
            rendered = ", ".join(
                path.relative_to(self.root).as_posix() for path in matches
            )
            raise ValueError(f"change ID is not unique: {change_id} ({rendered})")
        return matches[0]

    def change_layer(self, change: Path) -> str | None:
        resolved = change.resolve()
        if not self.layered:
            return None
        for layer, root in self.layer_roots.items():
            try:
                resolved.relative_to(root / "changes")
            except ValueError:
                continue
            return layer
        raise ValueError(f"change is outside the DSET layout: {change}")

    def resolve_dset_path(self, relative: str | Path) -> Path:
        return self.dset_root / _canonical_relative(relative)

    def _owned_file(self, layer: str, name: str) -> Path:
        base = self.layer_root(layer) if self.layered else self.dset_root
        return self.structured_file(base, name)

    def _owned_directory(self, layer: str, name: str) -> Path:
        return self._owned_file(layer, name)

    def _preferred_name(self, stem: str) -> str:
        suffix = ".toml" if self.manifest_path.suffix == ".toml" else ".yaml"
        return f"{stem}{suffix}"

    @staticmethod
    def _find_unique(roots: tuple[Path, ...], relative: str | Path, kind: str) -> Path:
        normalized = _canonical_relative(relative)
        candidates: list[Path] = []
        for root in roots:
            requested = root / normalized
            if requested.suffix.lower() in {".toml", ".yaml", ".yml"}:
                stem = requested.with_suffix("")
                candidates.extend(
                    stem.with_suffix(suffix) for suffix in (".toml", ".yaml", ".yml")
                )
            else:
                candidates.append(requested)
        matches = [path for path in candidates if path.is_file()]
        if not matches:
            raise FileNotFoundError(f"{kind} is missing: {relative}")
        if len(matches) > 1:
            rendered = ", ".join(path.as_posix() for path in matches)
            raise ValueError(f"{kind} is not unique: {relative} ({rendered})")
        return matches[0]


def discover_layout(root: Path) -> RepositoryLayout:
    """Discover a DSET layout, defaulting missing repositories to legacy paths."""

    root = root.resolve()
    legacy = _manifest_candidate(root / "dset" / "dset.yaml")
    layered = _manifest_candidate(root / "dset" / "scopes" / "meta" / "dset.yaml")
    if legacy.is_file() and layered.is_file():
        raise ValueError(
            "DSET project has both legacy and schema 1.2 manifests: "
            f"{legacy}, {layered}"
        )
    manifest = layered if layered.is_file() else legacy
    is_layered = layered.is_file()
    version = _schema_version(manifest) if manifest.is_file() else None
    if is_layered and version != LAYERED_SCHEMA_VERSION:
        raise ValueError(f"layered DSET manifest must declare schema 1.2: {layered}")
    if not is_layered and version is not None and version not in LEGACY_SCHEMA_VERSIONS:
        raise ValueError(
            f"central DSET manifest must declare schema 1.0 or 1.1: {legacy}"
        )
    scopes = root / "dset" / "scopes"
    if is_layered:
        actual_layers = {path.name for path in scopes.iterdir() if path.is_dir()}
        if actual_layers != set(LAYERS):
            raise ValueError(
                "layered DSET project must contain exactly the fixed layer roots: "
                f"{', '.join(LAYERS)}"
            )
        conflicts = [
            root / "dset" / relative
            for relative in LEGACY_AUTHORITY_PATHS
            if (root / "dset" / relative).exists()
        ]
        if conflicts:
            rendered = ", ".join(path.as_posix() for path in conflicts)
            raise ValueError(
                "layout conflict: legacy and layered DSET authorities coexist: "
                f"{rendered}"
            )
    elif legacy.is_file() and scopes.exists():
        raise ValueError(
            f"layout conflict: legacy manifest and layered DSET roots coexist: {scopes}"
        )
    return RepositoryLayout(root=root, schema_version=version, layered=is_layered)


def has_manifest(root: Path) -> bool:
    root = root.resolve()
    return (
        _manifest_candidate(root / "dset" / "dset.yaml").is_file()
        or (
            _manifest_candidate(root / "dset" / "scopes" / "meta" / "dset.yaml")
        ).is_file()
    )


def _schema_version(path: Path) -> str | None:
    try:
        data = load(path)
    except (OSError, ValueError, YamlSubsetError):
        return None
    raw = data.get("schema_version") if isinstance(data, dict) else None
    if isinstance(raw, str):
        return raw
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return f"{float(raw):.1f}"
    return None


def _canonical_relative(relative: str | Path) -> Path:
    raw = str(relative)
    if (
        not raw
        or raw.startswith("/")
        or "\\" in raw
        or (len(raw) >= 2 and raw[0].isalpha() and raw[1] == ":")
    ):
        raise ValueError(f"path is not canonical relative POSIX: {raw}")
    segments = raw.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise ValueError(f"path is not canonical relative POSIX: {raw}")
    return Path(*segments)


def _manifest_candidate(requested: Path) -> Path:
    return RepositoryLayout.structured_file(requested.parent, requested.name)


def _registered_snapshot_after_cutover(snapshot: Path) -> bool:
    """Refuse legacy read fallback once a registered repository has cut over."""

    resolved = snapshot.resolve()
    for root in (resolved.parent, *resolved.parents):
        registry_candidates = (
            root / "dset/scopes/gov/artifact-types.toml",
            root / "dset/scopes/gov/artifact-types.yaml",
            root / "dset/artifact-types.toml",
            root / "dset/artifact-types.yaml",
        )
        registry = next(
            (candidate for candidate in registry_candidates if candidate.is_file()),
            None,
        )
        if registry is None:
            continue
        cutover = (root / "dset/scopes/meta/dset.toml").is_file() or (
            root / "dset/dset.toml"
        ).is_file()
        if not cutover:
            return False
        try:
            data = load(registry)
        except (OSError, ValueError, YamlSubsetError):
            return False
        entries = data.get("legacy_structured") if isinstance(data, dict) else None
        if not isinstance(entries, list):
            return False
        for entry in entries:
            raw = entry.get("path") if isinstance(entry, dict) else None
            if isinstance(raw, str) and (root / raw).resolve() == resolved:
                return True
        return False
    return False
