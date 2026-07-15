# DSET project root

## Purpose

This is the control-plane hub for the repository as both the DSET framework source and its recursive adopter. Project truth is divided among five stable semantic owners without duplicating one logical package.

## Boundaries

`dset/scopes/` owns project control artifacts. Public framework prose remains under `methodology/` and `documentation/`; executable source remains under `dset_toolchain/`, `skills/`, and `.github/`. Those implementation surfaces trace back to accepted layer-owned contracts.

## Start here

- [META](scopes/meta/README.md) — identity, accepted behavior, specification semantics, and proof plans.
- [GOV](scopes/gov/README.md) — governance, intake, provenance, migrations, and generated views.
- [TOOL](scopes/tool/README.md) — executable CLI, validation, fixtures, traceability, and self-hosting.
- [SKILL](scopes/skill/README.md) — agent workflows, delegation, and local run evidence.
- [OPS](scopes/ops/README.md) — delivery, release, supportability, and hosted evidence.

## Current structure

```text
dset/
├── README.md
└── scopes/
    ├── meta/
    ├── gov/
    ├── tool/
    ├── skill/
    └── ops/
```

Each scope has a hub and may own governing rules, schemas, templates, a fragment of the logical `methodology` package, and Changes. The project manifest is [META-owned](scopes/meta/dset.yaml). The single governance and intake registries are [GOV-owned](scopes/gov/governance.yaml) and [GOV-owned](scopes/gov/intake.yaml). Generated [traceability](scopes/gov/generated/traceability.yaml) is a non-authoritative relationship view.

## Ownership

| Scope | Owns |
|---|---|
| META | Project/version identity; accepted domain, behavior, Contracts, and proof-plan semantics |
| GOV | Artifact and repository governance; Problems, Opportunities, Questions; provenance and derived indexes |
| TOOL | CLI behavior, diagnostics, fixtures, trace generation, validation, and self-hosting |
| SKILL | Thin wrappers, lifecycle recommendation, delegation budgets, and local run records |
| OPS | Release, hosted delivery, supportability, incident investigation, and recovery evidence |

The accepted methodology remains one logical package with five writable fragments. A Change lives only under its `primary_layer`; `affected_layers` and stable IDs connect cross-layer work.

The project manifest also declares neutral repository-relative Work Areas. A
Work Area may contain a deployable service, local tool, library, documentation,
methodology, data, tests, hosted automation, or mixed content. It is a scope
boundary, not a feature/module/service classification. Every schema 1.2 Change
targets either the whole repository or one or more declared Work Areas.

## Repository commands

| Command | Behavior |
|---|---|
| `python -m dset_toolchain check .` | Read-only validation with stable diagnostics |
| `python -m dset_toolchain verify .` | Project-configured gates plus trace freshness |
| `python -m dset_toolchain rules check .` | Validate repository-local rule ownership and identity |
| `python -m dset_toolchain rules resolve <workflow-id> . --format json` | Print the ordered local rules used by a thin wrapper |
| `python -m dset_toolchain self-host .` | Run the bounded released-to-candidate fixed point |
| `uv run dset new <slug> --package <package-id> --profile <profile> --layer <layer> [--work-area <id> ...] [--workspace branch-worktree]` | Allocate a stable layer-qualified Change ID; use the integration branch by default or opt into an isolated worktree |
| `uv run dset trace . --write` | Regenerate deterministic relationship evidence |
| `uv run dset archive <stable-change-id>` | Preview guarded archival; add `--execute` only after readiness passes |

## Lifecycle

1. Create one Change with one stable `DSET-CHANGE-<LAYER>-NNN` ID, readable slug, repository-or-Work-Area target, and explicit workspace mode.
2. Record affected layers, dependencies, exact consumed commits, Contracts, proof plans, and reopen triggers.
3. Implement against accepted truth; keep deterministic tests and qualitative/probabilistic evals separate.
4. Reconcile only the affected package fragments, refresh the smallest invalidated proof closure, and regenerate traceability.
5. Archive the Change under its primary layer through its implementing PR.
6. By default, work on local `dev`, push remote `dev`, and open the release PR from `dev` to protected `main`.
7. Select `branch-worktree` only when the Change needs isolation; review that branch into `dev` before the release PR.

Permanent layer branches are forbidden. One cross-layer Change stays atomic when splitting would create an invalid intermediate state; split only independently reviewable, verifiable, and mergeable work.
