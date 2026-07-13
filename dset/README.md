# DSET project root

This repository is both the public source of DSET Spec Loops and an adopting DSET project. This directory contains this project's accepted truth and bounded changes; it does not duplicate the framework methodology under `methodology/`.

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
5. Reconcile accepted deltas into `specs/`, move the change under `archive/` as an explicitly labeled candidate, commit it, and push it to the still-draft PR so remote identity and archive-layout checks can inspect the real head.
6. Evaluate the pushed candidate, refresh the applicable traceability evidence, record final proof, and mark the candidate complete in an evidence-only commit. With executable enforcement configured, run its canonical command and regenerate its traceability index. Under an explicit pending enforcement profile, record a manual PR/link/archive audit and exact read-only checks without claiming that CI or generation ran.
7. Keep the PR draft until archive readiness passes; then mark it ready and merge.

An incomplete or failed change remains active and never modifies accepted truth. A dated candidate on a draft PR branch is not accepted archive history until its final evidence is recorded and the PR merges.
