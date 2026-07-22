# Project-local DSET control plane

## Purpose

Own the target repository's settings, installed methodology, and applied DSET
artifacts. Skills search only this `.dset` control root and resolve unique
identities or carrier names; they do not read the reusable root source as local
authority.

## Boundaries

`000_dset_methodology` contains methodology only. `100_project` through
`150_versions` contain applied project artifacts only. `.dset_runtime` owns
ignored runtime state and is not part of this control plane.

## Start here

- `dset_settings.toml` — settings and identity registries.
- `000_dset-methodology-hub.md` — installed methodology.
- `DSET-PROJECT-HUB.md` — applied project-wide truth.
- `DSET-META-HUB.md`, `DSET-GOV-HUB.md`, `DSET-TOOL-HUB.md`,
  `DSET-SKILL-HUB.md`, and `DSET-OPS-HUB.md` — applied layer truth.
- `DSET-VERSIONS-HUB.md` — applied Version artifacts.

Reusable framework source lives outside this project-local authority surface.
