# Archive readiness — 2026-07-14

## Candidate identity

- Repository: `anatoly-m-maslennikov/dset-specs-loops-framework`
- Pull request: [#8](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/8)
- Route and author: `dev` → `main`, authored by `anatoly-m-maslennikov`
- Pre-archive baseline: `fcffd76`
- Pushed archive-candidate head: `57f4f4d`
- GitHub state at capture: open, mergeable, and draft
- Archive path: `dset/changes/archive/2026-07-14-add-artifact-governance-profile`

## Guarded transaction

1. The change recorded real PR #8, complete deterministic and qualitative proof, hosted evidence, accepted-truth reconciliation, and `status: archive-ready`.
2. `uv run dset trace . --write` refreshed the derived proof index and `uv run dset verify .` passed the pre-archive baseline.
3. `uv run dset archive add-artifact-governance-profile --date 2026-07-14` produced the exact active-to-dated-archive plan without writing.
4. The same command with `--execute` moved the change, set `status: archived`, and wrote archive date/path metadata without overwriting a destination.
5. `python -m dset_toolchain check .` passed immediately after the real move; no relative-link correction was required.
6. Traceability was regenerated for the archived path. The full aggregate then passed: 19 Python files were formatted, lint and strict typing were clean, all 18 tests passed, trace freshness passed, and DSET validation passed.
7. `git diff --check` passed; the dated candidate was committed and pushed as `57f4f4d` with a clean worktree.

## Hosted candidate-head checks

| Check | Result | GitHub evidence |
|---|---|---|
| `DSET / validate` on the `dev` push | Pass in 10 seconds | [run 29300385691, job 86982711630](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300385691/job/86982711630) |
| `DSET / validate` on the PR merge ref | Pass in 11 seconds | [run 29300387226, job 86982716257](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300387226/job/86982716257) |
| `PR policy` | Pass in 4 seconds | [run 29300386520, job 86982713899](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300386520/job/86982713899) |
| `Enable auto-merge` | Correctly skipped while draft | [run 29300386520, job 86982726640](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300386520/job/86982726640) |

## Readiness decision

The archive candidate satisfies profile configuration, artifact architecture, hub/navigation structure, portable Markdown, accepted-truth reconciliation, deterministic proof, four independent qualitative evals, fresh traceability, hosted validation, and the owner-only `dev → main` PR policy. PR #8 may leave draft after this final evidence-only head passes the same hosted checks.

This evidence does not predict a future merge SHA. GitHub remains authoritative for the ready transition, auto-merge state, and eventual merge commit. Any later implementation, accepted-specification, registry, hub, or validator edit invalidates readiness and requires a new cycle.
