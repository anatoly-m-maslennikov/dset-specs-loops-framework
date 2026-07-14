# DSET project root

## Purpose

This is the control-plane hub for the repository as an adopting DSET project. It routes to accepted truth, bounded changes, reusable contracts, generated traceability, migration guidance, and delivery supportability.

## Boundaries

This directory owns project configuration and DSET artifacts. It does not duplicate normative framework prose under `methodology/` or `documentation/`, the CLI implementation under `dset_toolchain/`, or live GitHub PR/check state.

## Start here

- [Accepted methodology package](specs/packages/methodology/README.md) — current truth and proof contracts.
- [Changes](changes/README.md) — active proposed work; `changes/archive/` preserves completed PR-linked evidence.
- [Templates](templates/README.md), [schemas](schemas/README.md), and [fixtures](fixtures/README.md) — reusable framework contracts and deterministic examples.
- [Traceability](traceability.yaml) — generated change-to-proof-to-PR discovery index.
- [Migrations](migrations/README.md) and the [delivery runbook](supportability/delivery-runbook.md) — adoption guidance and production supportability.

## Current structure

```text
dset/
├── dset.yaml
├── provenance.yaml
├── traceability.yaml
├── specs/
│   └── packages/
│       └── methodology/
├── changes/
│   ├── archive/
│   └── <change-id>/
├── templates/
├── schemas/
├── fixtures/
├── migrations/
├── history/
└── supportability/
```

The project currently has one package, `methodology`. A `specs/global/` layer is intentionally absent: it becomes justified only when a second package creates cross-package behavior, contracts, or release gates.

## Ownership

| Path | Owns |
|---|---|
| `dset.yaml` | Project identity, package registry, and selected profiles |
| `provenance.yaml` | Exact third-party sources, revisions, licenses, and use boundaries |
| `traceability.yaml` | Generated deterministic change-to-proof-to-PR relationship view |
| `specs/packages/methodology/` | Accepted current truth for the methodology package |
| `changes/<change-id>/` | Unaccepted proposal, deltas, proof plans, design, tasks, and verification for one bounded change |
| `changes/archive/` | Completed changes reconciled into current truth and archived through their implementing PR |
| `templates/` | Framework-owned reusable artifact templates |
| `schemas/` | Framework-owned machine-readable contracts and validators' schema inputs |
| `fixtures/` | Materialized base artifacts and deterministic pass/fail mutations |
| `migrations/` | One-writable-root adoption guidance and mapping template |
| `history/` | GitHub-authoritative PR metadata snapshot used as bounded evidence |
| `supportability/` | Production runbooks for this repository's hosted automation |

## Repository commands

| Command | Behavior |
|---|---|
| `python -m dset_toolchain check .` | Read-only validation with stable diagnostics and no third-party runtime dependency |
| `python -m dset_toolchain verify .` | Canonical aggregate: project-configured gates, unit/fixture tests, Markdown checks, diff hygiene, and trace freshness |
| `uv run dset new <change-id> --package <package-id> --profile <profile>` | Create a non-overwriting active change from released templates |
| `uv run dset trace .` | Print deterministic traceability; add `--write` to update or `--check` to compare |
| `uv run dset archive <change-id>` | Print an archive dry-run; add `--execute` only after readiness gates pass |

Inside this repository's locked development environment, `uv run dset verify .` invokes the same canonical aggregate through the installed console entry point.

`small`, `standard`, `large`, `defect`, and `adoption` profiles select proportional artifacts. Every profile preserves separate deterministic test and probabilistic/qualitative eval plans; an eval plan may explicitly state not applicable.

## Lifecycle

1. Create a kebab-case change under `changes/`.
2. Write requirements plus deterministic test proof and applicable eval proof before implementation.
3. Open a draft PR and record its repository-qualified identity in the change.
4. Implement and collect fresh verification evidence.
5. Reconcile accepted deltas into `specs/`, move the change under `archive/` as an explicitly labeled candidate, commit it, and push it to the still-draft PR so remote identity and archive-layout checks can inspect the real head.
6. Evaluate the pushed candidate, refresh `dset/traceability.yaml`, record final proof, run `uv run dset verify .`, and mark the candidate complete in an evidence-only commit.
7. Keep the PR draft until archive readiness passes; then mark it ready and merge.

An incomplete or failed change remains active and never modifies accepted truth. A dated candidate on a draft PR branch is not accepted archive history until its final evidence is recorded and the PR merges.
