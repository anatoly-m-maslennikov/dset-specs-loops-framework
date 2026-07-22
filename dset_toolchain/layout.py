from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import Final

from .yaml_subset import YamlSubsetError, load

LAYERS: Final[tuple[str, ...]] = ("meta", "gov", "tool", "skill", "ops")
LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "layer_1_meta",
    "gov": "layer_2_gov",
    "tool": "layer_3_tool",
    "skill": "layer_4_skill",
    "ops": "layer_5_ops",
}
LEGACY_SLIM_LAYOUT: Final[str] = "slim-v1"
NUMBERED_LAYER_LAYOUT: Final[str] = "numbered-layers-v1"
LEGACY_SCHEMA_VERSIONS: Final[frozenset[str]] = frozenset({"1.0", "1.1"})
LAYERED_SCHEMA_VERSION: Final[str] = "1.2"
SLIM_SCHEMA_VERSION: Final[str] = "1.3"
CURRENT_DSET_ROOT: Final[str] = ".dset"
LEGACY_DSET_ROOT: Final[str] = "dset"
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
    layer-owned roots below ``dset/``. Schema 1.3 uses the hidden, distinctive
    ``.dset/`` control root, removes the redundant ``scopes`` segment, moves
    project-wide control artifacts below ``.dset/project/``, and uses one
    combined settings and project manifest at ``.dset/dset_settings.toml``.
    """

    root: Path
    schema_version: str | None
    layered: bool
    structure_layout: str | None = None

    @property
    def slim(self) -> bool:
        return self.schema_version == SLIM_SCHEMA_VERSION

    @property
    def dset_root(self) -> Path:
        directory = CURRENT_DSET_ROOT if self.slim else LEGACY_DSET_ROOT
        return self.root / directory

    @property
    def settings_path(self) -> Path:
        if self.slim:
            return self.dset_root / "dset_settings.toml"
        return self.root / "dset_settings.toml"

    @property
    def project_root(self) -> Path:
        return self.dset_root / "project"

    @property
    def versions_root(self) -> Path:
        return self.dset_root / "versions"

    @property
    def scopes_root(self) -> Path:
        return self.dset_root if self.slim else self.dset_root / "scopes"

    def layer_root(self, layer: str) -> Path:
        normalized = layer.lower()
        if normalized not in LAYERS:
            raise ValueError(f"unknown DSET layer: {layer}")
        directory = (
            LAYER_DIRECTORIES[normalized]
            if self.slim and self.structure_layout == NUMBERED_LAYER_LAYOUT
            else normalized
        )
        return self.scopes_root / directory

    @property
    def layer_roots(self) -> dict[str, Path]:
        return {layer: self.layer_root(layer) for layer in LAYERS}

    @property
    def manifest_path(self) -> Path:
        if self.slim:
            return self.settings_path
        if self.layered:
            return self.structured_file(self.layer_root("meta"), "dset.toml")
        return self.structured_file(self.dset_root, "dset.toml")

    @property
    def governance_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.project_root, "governance.toml")
        return self._owned_file("gov", self._preferred_name("governance"))

    @property
    def governance_root(self) -> Path:
        if self.slim:
            return self.layer_root("gov")
        return self._owned_directory("gov", "governance")

    @property
    def project_state_root(self) -> Path:
        """Own project-wide ledgers independently from compiled GOV rules."""

        return self.project_root if self.slim else self.governance_root

    @property
    def artifact_registry_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.project_root, "artifacts.toml")
        return self._owned_file("gov", self._preferred_name("artifacts"))

    @property
    def artifact_type_registry_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.project_root, "artifact-types.toml")
        return self._owned_file("gov", self._preferred_name("artifact-types"))

    @property
    def intake_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.project_root, "intake.toml")
        return self._owned_file("gov", self._preferred_name("intake"))

    @property
    def provenance_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.project_root, "provenance.toml")
        return self._owned_file("gov", self._preferred_name("provenance"))

    @property
    def traceability_path(self) -> Path:
        if self.slim:
            return self.structured_file(
                self.project_root / "generated",
                self._preferred_name("traceability"),
            )
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
        if self.slim:
            return self.project_root / "migrations"
        return self._owned_directory("gov", "migrations")

    @property
    def version_path(self) -> Path:
        if self.slim:
            return self.structured_file(self.versions_root, "version.toml")
        return self._owned_file("meta", self._preferred_name("version"))

    @property
    def budget_path(self) -> Path:
        return self._owned_file("skill", self._preferred_name("budget"))

    @property
    def history_root(self) -> Path:
        if self.slim:
            return self.versions_root / "history"
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
        if self.slim:
            return (self.versions_root / "changes",)
        if self.layered:
            return tuple(self.layer_root(layer) / "changes" for layer in LAYERS)
        return (self.dset_root / "changes",)

    @property
    def archive_change_roots(self) -> tuple[Path, ...]:
        if self.slim:
            return (self.versions_root / "archive",)
        return tuple(path / "archive" for path in self.active_change_roots)

    @property
    def package_roots(self) -> tuple[Path, ...]:
        if self.slim:
            return tuple(self.layer_root(layer) for layer in LAYERS)
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
        if self.slim:
            return tuple(
                path
                for path in (
                    self.structured_file(self.layer_root(layer), "package.toml")
                    for layer in LAYERS
                )
                if path.is_file()
            )
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
        if self.slim:
            return self.active_change_roots[0]
        if not self.layered:
            return self.active_change_roots[0]
        if layer is None:
            raise ValueError("schema 1.2 changes require an owning DSET layer")
        return self.layer_root(layer) / "changes"

    def archive_change_root(self, layer: str | None = None) -> Path:
        if self.slim:
            return self.archive_change_roots[0]
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
        if self.slim:
            manifest = self.structured_file(resolved, "change.toml")
            try:
                data = load(manifest)
            except (OSError, ValueError, YamlSubsetError) as error:
                raise ValueError(
                    f"cannot read Change layer: {manifest}: {error}"
                ) from error
            raw = data.get("primary_layer") if isinstance(data, dict) else None
            if not isinstance(raw, str) or raw.lower() not in LAYERS:
                raise ValueError(f"Change has no registered layer: {manifest}")
            return raw.lower()
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
    legacy_root = root / LEGACY_DSET_ROOT
    current_root = root / CURRENT_DSET_ROOT
    legacy = _manifest_candidate(legacy_root / "dset.yaml")
    layered = _manifest_candidate(legacy_root / "scopes" / "meta" / "dset.yaml")
    slim = current_root / "dset_settings.toml"
    manifests = [path for path in (legacy, layered, slim) if path.is_file()]
    if len(manifests) > 1:
        raise ValueError(
            "DSET project has competing manifests: "
            + ", ".join(path.as_posix() for path in manifests)
        )
    manifest = slim if slim.is_file() else layered if layered.is_file() else legacy
    is_slim = slim.is_file()
    is_layered = is_slim or layered.is_file()
    version = _schema_version(manifest) if manifest.is_file() else None
    structure_layout = _structure_layout(manifest) if is_slim else None
    if is_slim and version != SLIM_SCHEMA_VERSION:
        raise ValueError(f"slim DSET manifest must declare schema 1.3: {slim}")
    if is_slim and structure_layout not in {
        LEGACY_SLIM_LAYOUT,
        NUMBERED_LAYER_LAYOUT,
    }:
        raise ValueError(
            f"slim DSET manifest must select slim-v1 or numbered-layers-v1: {slim}"
        )
    if not is_slim and is_layered and version != LAYERED_SCHEMA_VERSION:
        raise ValueError(f"layered DSET manifest must declare schema 1.2: {layered}")
    if not is_layered and version is not None and version not in LEGACY_SCHEMA_VERSIONS:
        raise ValueError(
            f"central DSET manifest must declare schema 1.0 or 1.1: {legacy}"
        )
    scopes = legacy_root / "scopes"
    if is_slim:
        layer_directories = (
            tuple(LAYER_DIRECTORIES.values())
            if structure_layout == NUMBERED_LAYER_LAYOUT
            else LAYERS
        )
        missing_layers = [
            current_root / directory
            for directory in layer_directories
            if not (current_root / directory).is_dir()
        ]
        if missing_layers:
            raise ValueError(
                "slim DSET project is missing fixed layer roots: "
                + ", ".join(path.as_posix() for path in missing_layers)
            )
        competing_layers = [
            current_root / directory
            for directory in (
                tuple(LAYER_DIRECTORIES.values())
                if structure_layout == LEGACY_SLIM_LAYOUT
                else LAYERS
            )
            if (current_root / directory).exists()
        ]
        if competing_layers:
            raise ValueError(
                "slim DSET project has competing layer roots: "
                + ", ".join(path.as_posix() for path in competing_layers)
            )
        if scopes.exists():
            raise ValueError(
                f"layout conflict: schema 1.3 and legacy dset/scopes coexist: {scopes}"
            )
        if legacy_root.exists():
            raise ValueError(
                "layout conflict: schema 1.3 .dset root and legacy dset root "
                f"coexist: {legacy_root}"
            )
        old_settings = root / "dset_settings.toml"
        if old_settings.exists():
            raise ValueError(
                "layout conflict: schema 1.3 combined settings and retired root "
                f"settings coexist: {old_settings}"
            )
    elif is_layered:
        actual_layers = {path.name for path in scopes.iterdir() if path.is_dir()}
        if actual_layers != set(LAYERS):
            raise ValueError(
                "layered DSET project must contain exactly the fixed layer roots: "
                f"{', '.join(LAYERS)}"
            )
        conflicts = [
            legacy_root / relative
            for relative in LEGACY_AUTHORITY_PATHS
            if (legacy_root / relative).exists()
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
    return RepositoryLayout(
        root=root,
        schema_version=version,
        layered=is_layered,
        structure_layout=structure_layout,
    )


def has_manifest(root: Path) -> bool:
    root = root.resolve()
    return (
        (root / CURRENT_DSET_ROOT / "dset_settings.toml").is_file()
        or _manifest_candidate(root / LEGACY_DSET_ROOT / "dset.yaml").is_file()
        or (
            _manifest_candidate(
                root / LEGACY_DSET_ROOT / "scopes" / "meta" / "dset.yaml"
            )
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


def _structure_layout(path: Path) -> str | None:
    try:
        data = load(path)
    except (OSError, ValueError, YamlSubsetError):
        return None
    structure = data.get("structure") if isinstance(data, dict) else None
    raw = structure.get("layout") if isinstance(structure, dict) else None
    return raw if isinstance(raw, str) else None


def _canonical_relative(relative: str | PurePath) -> Path:
    raw = relative.as_posix() if isinstance(relative, PurePath) else str(relative)
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
            root / ".dset/project/artifact-types.toml",
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
        cutover = (
            (root / ".dset/dset_settings.toml").is_file()
            or (root / "dset/dset_settings.toml").is_file()
            or (root / "dset/scopes/meta/dset.toml").is_file()
            or (root / "dset/dset.toml").is_file()
        )
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
