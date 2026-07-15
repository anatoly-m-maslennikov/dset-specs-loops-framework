from __future__ import annotations

import re
from dataclasses import dataclass

_SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-rc\.(0|[1-9][0-9]*))?$"
)
RELEASE_CLASSES = {"bootstrap", "small", "normal", "rc", "final", "breaking"}


@dataclass(frozen=True, order=True)
class ProductVersion:
    major: int
    minor: int
    patch: int
    rc: int | None = None

    @classmethod
    def parse(cls, raw: str) -> ProductVersion:
        match = _SEMVER.fullmatch(raw)
        if match is None:
            raise ValueError(f"invalid DSET product version: {raw}")
        major, minor, patch, rc = match.groups()
        return cls(int(major), int(minor), int(patch), int(rc) if rc else None)

    @property
    def semver(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-rc.{self.rc}" if self.rc is not None else base

    @property
    def python(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}rc{self.rc}" if self.rc is not None else base


def expected_target(
    base: str | None,
    release_class: str,
    *,
    bootstrap_target: str | None = None,
    readiness_passed: bool = False,
) -> ProductVersion:
    if release_class not in RELEASE_CLASSES:
        raise ValueError(f"unknown release class: {release_class}")
    if release_class == "bootstrap":
        if base not in {None, "unversioned"}:
            raise ValueError("bootstrap requires an unversioned base")
        if bootstrap_target is None:
            raise ValueError("bootstrap requires an explicit target")
        target = ProductVersion.parse(bootstrap_target)
        if target.major != 0 or target.rc is not None:
            raise ValueError("bootstrap target must be a stable pre-1.0 version")
        return target
    if base in {None, "unversioned"}:
        raise ValueError(f"{release_class} requires a versioned base")

    current = ProductVersion.parse(base)
    if release_class == "rc":
        if current.rc is not None:
            return ProductVersion(1, 0, 0, current.rc + 1)
        if current.major != 0 or not readiness_passed:
            raise ValueError("the first 1.0 RC requires a passing pre-1.0 base")
        return ProductVersion(1, 0, 0, 1)
    if release_class == "final":
        if current != ProductVersion(1, 0, 0, current.rc) or current.rc is None:
            raise ValueError("final requires a 1.0.0 RC base")
        if not readiness_passed:
            raise ValueError("final requires passing readiness")
        return ProductVersion(1, 0, 0)
    if current.rc is not None:
        raise ValueError("published RCs advance only to a higher RC or final")
    if release_class == "small":
        return ProductVersion(current.major, current.minor, current.patch + 1)
    if release_class == "normal":
        return ProductVersion(current.major, current.minor + 1, 0)
    if release_class == "breaking" and current.major >= 1:
        return ProductVersion(current.major + 1, 0, 0)
    raise ValueError("breaking releases require a stable post-1.0 base")


def validate_coordinated_identity(product: str, python_package: str) -> None:
    version = ProductVersion.parse(product)
    if python_package != version.python:
        raise ValueError(
            "Python package version must be the exact PEP 440 serialization "
            f"of {version.semver}: {version.python}"
        )
