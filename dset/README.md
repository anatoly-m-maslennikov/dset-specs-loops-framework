# DSET project root

This repository is both the public source of the DSET Loops Framework and an adopting DSET project. This directory contains this project's accepted truth and bounded changes; it does not duplicate the framework methodology under `methodology/`.

## Current structure

```text
dset/
├── dset.yaml
├── specs/
│   └── packages/
│       └── methodology/
├── changes/
│   ├── archive/
│   └── <change-id>/
├── templates/
└── schemas/
```

The project currently has one package, `methodology`. A `specs/global/` layer is intentionally absent: it becomes justified only when a second package creates cross-package behavior, contracts, or release gates.

## Ownership

| Path | Owns |
|---|---|
| `dset.yaml` | Project identity, package registry, and selected profiles |
| `specs/packages/methodology/` | Accepted current truth for the methodology package |
| `changes/<change-id>/` | Unaccepted proposal, deltas, proof plans, design, tasks, and verification for one bounded change |
| `changes/archive/` | Completed changes reconciled into current truth and archived through their implementing PR |
| `templates/` | Framework-owned reusable artifact templates |
| `schemas/` | Framework-owned machine-readable contracts and validators' schema inputs |

## Lifecycle

1. Create a kebab-case change under `changes/`.
2. Write requirements plus deterministic test proof and applicable eval proof before implementation.
3. Open a draft PR and record its repository-qualified identity in the change.
4. Implement and collect fresh verification evidence.
5. Reconcile accepted deltas into `specs/`, move the change under `archive/`, regenerate traceability, and rerun checks inside the same PR.
6. Keep the PR draft until archive-readiness checks pass; then mark it ready and merge.

An incomplete or failed change remains active and never modifies accepted truth.
