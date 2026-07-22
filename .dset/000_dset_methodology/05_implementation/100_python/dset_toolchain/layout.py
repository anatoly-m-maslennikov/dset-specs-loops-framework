"""Provide DSET layout behavior."""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import Final

from .yaml_subset import YamlSubsetError, load

# LAYERS defines layers; this module owns the default.
LAYERS: Final[tuple[str, ...]] = (
    "meta",
    "gov",
    "tool",
    "skill",
    "implementation",
    "ops",
)
# LAYER_ID_TOKENS defines layer id tokens; this module owns the default.
LAYER_ID_TOKENS: Final[dict[str, str]] = {
    "meta": "META",
    "gov": "GOV",
    "tool": "TOOL",
    "skill": "SKILL",
    "implementation": "IMPL",
    "ops": "OPS",
}
# ID_TOKEN_LAYERS defines id token layers; this module owns the default.
ID_TOKEN_LAYERS: Final[dict[str, str]] = {
    token: layer for layer, token in LAYER_ID_TOKENS.items()
}
# LAYER_DIRECTORIES defines layer directories; this module owns the default.
LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "01_layer_meta",
    "gov": "02_layer_gov",
    "tool": "03_layer_tool",
    "skill": "04_layer_skill",
    "implementation": "05_layer_implementation",
    "ops": "06_layer_ops",
}
# RECURSIVE_LAYER_DIRECTORIES defines recursive layer directories; this module owns the default.
RECURSIVE_LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "01_layer_meta",
    "gov": "02_layer_gov",
    "tool": "03_layer_tool",
    "skill": "04_layer_skill",
    "implementation": "05_layer_implementation",
    "ops": "06_layer_ops",
}
# METHODOLOGY_LAYER_DIRECTORIES defines methodology layer directories; this module owns the default.
METHODOLOGY_LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "01_meta",
    "gov": "02_gov",
    "tool": "03_tool",
    "skill": "04_skill",
    "implementation": "05_implementation",
    "ops": "06_ops",
}
# APPLIED_LAYER_DIRECTORIES defines applied layer directories; this module owns the default.
APPLIED_LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "101_layer_meta",
    "gov": "102_layer_gov",
    "tool": "103_layer_tool",
    "skill": "104_layer_skill",
    "implementation": "105_layer_implementation",
    "ops": "106_layer_ops",
}
# PRODUCT_LAYER_DIRECTORIES defines product layer directories; this module owns the default.
PRODUCT_LAYER_DIRECTORIES: Final[dict[str, str]] = {
    "meta": "11_layer_meta",
    "gov": "12_layer_gov",
    "tool": "13_layer_tool",
    "skill": "14_layer_skill",
    "implementation": "15_layer_implementation",
    "ops": "16_layer_ops",
}
# LEGACY_SLIM_LAYOUT defines legacy slim layout; this module owns the default.
LEGACY_SLIM_LAYOUT: Final[str] = "slim-v1"
# NUMBERED_LAYER_LAYOUT defines numbered layer layout; this module owns the default.
NUMBERED_LAYER_LAYOUT: Final[str] = "numbered-layers-v1"
# RECURSIVE_FRAMEWORK_LAYOUT defines recursive framework layout; this module owns the default.
RECURSIVE_FRAMEWORK_LAYOUT: Final[str] = "recursive-framework-v1"
# SEPARATED_METHODOLOGY_LAYOUT defines separated methodology layout; this module owns the default.
SEPARATED_METHODOLOGY_LAYOUT: Final[str] = "separated-methodology-v1"
# LEGACY_SCHEMA_VERSIONS defines legacy schema versions; this module owns the default.
LEGACY_SCHEMA_VERSIONS: Final[frozenset[str]] = frozenset({"1.0", "1.1"})
# LAYERED_SCHEMA_VERSION defines layered schema version; this module owns the default.
LAYERED_SCHEMA_VERSION: Final[str] = "1.2"
# SLIM_SCHEMA_VERSION defines slim schema version; this module owns the default.
SLIM_SCHEMA_VERSION: Final[str] = "1.3"
# RECURSIVE_SCHEMA_VERSION defines recursive schema version; this module owns the default.
RECURSIVE_SCHEMA_VERSION: Final[str] = "1.4"
# SEPARATED_SCHEMA_VERSION defines separated schema version; this module owns the default.
SEPARATED_SCHEMA_VERSION: Final[str] = "1.5"
# CURRENT_DSET_ROOT defines current dset root; this module owns the default.
CURRENT_DSET_ROOT: Final[str] = ".dset"
# LEGAL_FILES_ROOT defines legal files root; this module owns the default.
LEGAL_FILES_ROOT: Final[str] = "LICENSES"
# METHODOLOGY_ROOT defines methodology root; this module owns the default.
METHODOLOGY_ROOT: Final[str] = "000_dset_methodology"
# APPLIED_PROJECT_ROOT defines applied project root; this module owns the default.
APPLIED_PROJECT_ROOT: Final[str] = "100_project"
# APPLIED_VERSIONS_ROOT defines applied versions root; this module owns the default.
APPLIED_VERSIONS_ROOT: Final[str] = "150_versions"
# LEGACY_DSET_ROOT defines legacy dset root; this module owns the default.
LEGACY_DSET_ROOT: Final[str] = "dset"
# LEGACY_AUTHORITY_PATHS defines legacy authority paths; this module owns the default.
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


def layer_id_token(layer: str) -> str:
    """Return the compact ID segment for a canonical layer key."""

    normalized = layer.lower()
    try:
        return LAYER_ID_TOKENS[normalized]
    except KeyError as error:
        raise ValueError(f"unknown DSET layer: {layer}") from error


def layer_key_from_id_token(token: str) -> str:
    """Return the canonical layer key for a compact ID segment."""

    normalized = token.upper()
    try:
        return ID_TOKEN_LAYERS[normalized]
    except KeyError as error:
        raise ValueError(f"unknown DSET layer token: {token}") from error


def normalize_layer_id_token(layer: str) -> str:
    """Normalize either a canonical layer key or an ID segment to its token."""

    token = layer.upper()
    if token in ID_TOKEN_LAYERS:
        return token
    return layer_id_token(layer)


@dataclass(frozen=True)
class RepositoryLayout:
    """Canonical path authority for one DSET repository.

    Schema 1.0 and 1.1 use the central ``dset/`` layout. Schema 1.2 uses
    layer-owned roots below ``dset/``. Schema 1.3 uses the hidden ``.dset/``
    control root. Schema 1.4 separates the portable framework below ``.dset``
    from recursively governed project artifacts at the repository root.
    Schema 1.5 separates installed methodology from applied project artifacts
    inside ``.dset`` while leaving the governed product outside it.
    """

    root: Path
    schema_version: str | None
    layered: bool
    structure_layout: str | None = None

    @property
    def slim(self) -> bool:
        return self.schema_version in {
            SLIM_SCHEMA_VERSION,
            RECURSIVE_SCHEMA_VERSION,
            SEPARATED_SCHEMA_VERSION,
        }

    @property
    def recursive(self) -> bool:
        return self.schema_version == RECURSIVE_SCHEMA_VERSION

    @property
    def separated(self) -> bool:
        return self.schema_version == SEPARATED_SCHEMA_VERSION

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
    def legal_files_root(self) -> Path:
        """Return the external repository distribution surface for legal files."""

        return self.root / LEGAL_FILES_ROOT

    @property
    def project_root(self) -> Path:
        if self.separated:
            return self.dset_root / APPLIED_PROJECT_ROOT
        return (
            self.root / "00_project" if self.recursive else self.dset_root / "project"
        )

    @property
    def versions_root(self) -> Path:
        if self.separated:
            return self.dset_root / APPLIED_VERSIONS_ROOT
        return (
            self.root / "10_versions" if self.recursive else self.dset_root / "versions"
        )

    @property
    def scopes_root(self) -> Path:
        if self.separated:
            return self.dset_root
        if self.recursive:
            return self.root
        return self.dset_root if self.slim else self.dset_root / "scopes"

    def layer_root(self, layer: str) -> Path:
        normalized = layer.lower()
        if normalized not in LAYERS:
            raise ValueError(f"unknown DSET layer: {layer}")
        if self.separated:
            directory = APPLIED_LAYER_DIRECTORIES[normalized]
        elif self.recursive:
            directory = RECURSIVE_LAYER_DIRECTORIES[normalized]
        elif self.slim and self.structure_layout == NUMBERED_LAYER_LAYOUT:
            directory = LAYER_DIRECTORIES[normalized]
        else:
            directory = normalized
        return self.scopes_root / directory

    def framework_layer_root(self, layer: str) -> Path:
        normalized = layer.lower()
        if normalized not in LAYERS:
            raise ValueError(f"unknown DSET layer: {layer}")
        if self.separated:
            return (
                self.dset_root
                / METHODOLOGY_ROOT
                / METHODOLOGY_LAYER_DIRECTORIES[normalized]
            )
        if self.recursive:
            return self.dset_root / RECURSIVE_LAYER_DIRECTORIES[normalized]
        return self.layer_root(normalized)

    @property
    def framework_project_root(self) -> Path:
        if self.separated:
            return self.dset_root / METHODOLOGY_ROOT / "00_project"
        if self.recursive:
            return self.dset_root / "00_project"
        return self.project_root

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
        if self.recursive or self.separated:
            return self.settings_path
        if self.slim:
            return self.structured_file(self.project_root, "governance.toml")
        return self._owned_file("gov", self._preferred_name("governance"))

    @property
    def governance_root(self) -> Path:
        if self.recursive or self.separated:
            return self.framework_layer_root("gov")
        if self.slim:
            return self.layer_root("gov")
        return self._owned_directory("gov", "governance")

    @property
    def project_state_root(self) -> Path:
        """Own project-wide ledgers independently from compiled GOV rules."""

        return self.project_root if self.slim else self.governance_root

    @property
    def artifact_registry_path(self) -> Path:
        if self.recursive or self.separated:
            return self.settings_path
        if self.slim:
            return self.structured_file(self.project_root, "artifacts.toml")
        return self._owned_file("gov", self._preferred_name("artifacts"))

    @property
    def artifact_type_registry_path(self) -> Path:
        if self.recursive or self.separated:
            return self.settings_path
        if self.slim:
            return self.structured_file(self.project_root, "artifact-types.toml")
        return self._owned_file("gov", self._preferred_name("artifact-types"))

    @property
    def intake_path(self) -> Path:
        if self.recursive or self.separated:
            return self.project_root
        if self.slim:
            return self.structured_file(self.project_root, "intake.toml")
        return self._owned_file("gov", self._preferred_name("intake"))

    @property
    def provenance_path(self) -> Path:
        if self.recursive or self.separated:
            return self.settings_path
        if self.slim:
            return self.structured_file(self.project_root, "provenance.toml")
        return self._owned_file("gov", self._preferred_name("provenance"))

    @property
    def traceability_path(self) -> Path:
        if self.recursive or self.separated:
            return self.root / ".dset_runtime/generated/traceability.toml"
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
        if self.recursive or self.separated:
            return self.project_root / "migrations"
        if self.slim:
            return self.project_root / "migrations"
        return self._owned_directory("gov", "migrations")

    @property
    def version_path(self) -> Path:
        if self.recursive or self.separated:
            return self.settings_path
        if self.slim:
            return self.structured_file(self.versions_root, "version.toml")
        return self._owned_file("meta", self._preferred_name("version"))

    @property
    def budget_path(self) -> Path:
        if self.recursive or self.separated:
            return self._numbered_file(
                self.framework_layer_root("skill"), "budget.toml"
            )
        return self._owned_file("skill", self._preferred_name("budget"))

    @property
    def history_root(self) -> Path:
        if self.recursive:
            return self.versions_root / "history"
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
        base = (
            self.framework_layer_root("ops")
            if self.recursive or self.separated
            else self.layer_root("ops")
        )
        return self._numbered_directory(base, "supportability")

    @property
    def fixtures_root(self) -> Path:
        base = (
            self.framework_layer_root("tool")
            if self.recursive or self.separated
            else self.layer_root("tool")
        )
        return self._numbered_directory(base, "fixtures")

    @property
    def schema_roots(self) -> tuple[Path, ...]:
        if self.recursive or self.separated:
            return tuple(
                self._numbered_directory(self.framework_layer_root(layer), "schemas")
                for layer in LAYERS
            )
        if self.layered:
            return tuple(self.layer_root(layer) / "schemas" for layer in LAYERS)
        return (self.dset_root / "schemas",)

    @property
    def template_roots(self) -> tuple[Path, ...]:
        if self.recursive or self.separated:
            return tuple(
                self._numbered_directory(self.framework_layer_root(layer), "templates")
                for layer in LAYERS
            )
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
        if self.recursive or self.separated:
            return ()
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
        if self.recursive or self.separated:
            return self._find_numbered_unique(self.template_roots, relative, "template")
        return self._find_unique(self.template_roots, relative, "template")

    def package_fragments(self) -> tuple[Path, ...]:
        if self.recursive or self.separated:
            return ()
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
    def _numbered_directory(parent: Path, logical_name: str) -> Path:
        exact = parent / logical_name
        if exact.is_dir():
            return exact
        matches = (
            sorted(
                path
                for path in parent.iterdir()
                if path.is_dir() and _strip_numeric_prefix(path.name) == logical_name
            )
            if parent.is_dir()
            else []
        )
        if not matches:
            return exact
        if len(matches) > 1:
            rendered = ", ".join(path.as_posix() for path in matches)
            raise ValueError(
                f"methodology directory is not unique: {logical_name} ({rendered})"
            )
        return matches[0]

    @staticmethod
    def _numbered_file(parent: Path, logical_name: str) -> Path:
        exact = parent / logical_name
        if exact.is_file():
            return exact
        requested = Path(logical_name)
        suffix = "".join(requested.suffixes)
        stem = requested.name[: -len(suffix)] if suffix else requested.name
        pattern = f"*-{stem}{suffix}"
        matches = sorted(parent.glob(pattern)) if parent.is_dir() else []
        if not matches:
            return exact
        if len(matches) > 1:
            rendered = ", ".join(path.as_posix() for path in matches)
            raise ValueError(
                f"methodology file is not unique: {logical_name} ({rendered})"
            )
        return matches[0]

    @staticmethod
    def _find_numbered_unique(
        roots: tuple[Path, ...], relative: str | Path, kind: str
    ) -> Path:
        normalized = _canonical_relative(relative)
        suffixes = [normalized]
        if normalized.suffix.lower() in {".toml", ".yaml", ".yml"}:
            stem = normalized.with_suffix("")
            suffixes = [
                stem.with_suffix(suffix) for suffix in (".toml", ".yaml", ".yml")
            ]
        candidates: list[Path] = []
        for root in roots:
            for candidate in suffixes:
                ending = "-".join(
                    _methodology_component(part) for part in candidate.parts
                )
                candidates.extend(root.rglob(f"*-{ending}"))
        matches = sorted({path for path in candidates if path.is_file()})
        if not matches:
            raise FileNotFoundError(f"{kind} is missing: {relative}")
        if len(matches) > 1:
            rendered = ", ".join(path.as_posix() for path in matches)
            raise ValueError(f"{kind} is not unique: {relative} ({rendered})")
        return matches[0]

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


def _strip_numeric_prefix(name: str) -> str:
    return re.sub(r"^\d{3}_", "", name, count=1)


def _methodology_component(name: str) -> str:
    normalized = _strip_numeric_prefix(name)
    if normalized.lower() == "readme.md":
        return "hub.md"
    path = Path(normalized)
    suffix = "".join(path.suffixes)
    stem = normalized[: -len(suffix)] if suffix else normalized
    stem = stem.replace("—", "-").replace("–", "-")
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    return f"{stem}{suffix.lower()}"


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
    if is_slim and version not in {
        SLIM_SCHEMA_VERSION,
        RECURSIVE_SCHEMA_VERSION,
        SEPARATED_SCHEMA_VERSION,
    }:
        raise ValueError(
            f"hidden DSET manifest must declare schema 1.3, 1.4, or 1.5: {slim}"
        )
    allowed_hidden_layouts = {
        LEGACY_SLIM_LAYOUT,
        NUMBERED_LAYER_LAYOUT,
        RECURSIVE_FRAMEWORK_LAYOUT,
        SEPARATED_METHODOLOGY_LAYOUT,
    }
    if is_slim and structure_layout not in allowed_hidden_layouts:
        raise ValueError(
            "hidden DSET manifest must select slim-v1, numbered-layers-v1, "
            "recursive-framework-v1, or separated-methodology-v1: "
            f"{slim}"
        )
    if (
        version == RECURSIVE_SCHEMA_VERSION
        and structure_layout != RECURSIVE_FRAMEWORK_LAYOUT
    ):
        raise ValueError(f"schema 1.4 must select recursive-framework-v1: {slim}")
    if (
        version == SLIM_SCHEMA_VERSION
        and structure_layout == RECURSIVE_FRAMEWORK_LAYOUT
    ):
        raise ValueError(f"recursive-framework-v1 requires schema 1.4: {slim}")
    if (
        version == SEPARATED_SCHEMA_VERSION
        and structure_layout != SEPARATED_METHODOLOGY_LAYOUT
    ):
        raise ValueError(f"schema 1.5 must select separated-methodology-v1: {slim}")
    if (
        version != SEPARATED_SCHEMA_VERSION
        and structure_layout == SEPARATED_METHODOLOGY_LAYOUT
    ):
        raise ValueError(f"separated-methodology-v1 requires schema 1.5: {slim}")
    if not is_slim and is_layered and version != LAYERED_SCHEMA_VERSION:
        raise ValueError(f"layered DSET manifest must declare schema 1.2: {layered}")
    if not is_layered and version is not None and version not in LEGACY_SCHEMA_VERSIONS:
        raise ValueError(
            f"central DSET manifest must declare schema 1.0 or 1.1: {legacy}"
        )
    scopes = legacy_root / "scopes"
    if is_slim:
        if structure_layout == SEPARATED_METHODOLOGY_LAYOUT:
            applied_directories = (
                APPLIED_PROJECT_ROOT,
                *APPLIED_LAYER_DIRECTORIES.values(),
                APPLIED_VERSIONS_ROOT,
            )
            missing_layers = [
                path
                for path in (
                    current_root / METHODOLOGY_ROOT,
                    *(current_root / directory for directory in applied_directories),
                )
                if not path.is_dir()
            ]
            competing_names = (
                *LAYERS,
                *LAYER_DIRECTORIES.values(),
                *RECURSIVE_LAYER_DIRECTORIES.values(),
                "00_project",
                "10_versions",
                "project",
                "versions",
            )
        elif structure_layout == RECURSIVE_FRAMEWORK_LAYOUT:
            framework_directories = tuple(RECURSIVE_LAYER_DIRECTORIES.values())
            project_directories = (
                "00_project",
                *framework_directories,
                "10_versions",
            )
            missing_layers = [
                path
                for path in (
                    *(current_root / directory for directory in project_directories),
                    *(root / directory for directory in project_directories),
                )
                if not path.is_dir()
            ]
            competing_names = (
                *LAYERS,
                *LAYER_DIRECTORIES.values(),
                "project",
                "versions",
            )
        else:
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
            competing_names = (
                tuple(LAYER_DIRECTORIES.values())
                if structure_layout == LEGACY_SLIM_LAYOUT
                else LAYERS
            )
        if missing_layers:
            raise ValueError(
                "hidden DSET project is missing fixed roots: "
                + ", ".join(path.as_posix() for path in missing_layers)
            )
        competing_layers = [
            current_root / directory
            for directory in competing_names
            if (current_root / directory).exists()
        ]
        if competing_layers:
            raise ValueError(
                "hidden DSET project has competing roots: "
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
            root / "00_project/artifact-types.toml",
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
