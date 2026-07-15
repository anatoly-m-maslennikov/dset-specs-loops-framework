# Archive readiness — 2026-07-14

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Candidate identity

- Repository: `anatoly-m-maslennikov/dset-specs-loops-framework`
- Pull request: [#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)
- Route and author: `dev` → `main`, authored by `anatoly-m-maslennikov`
- Pushed archive-candidate head: `c7d04b1122942b93c758b1a337f6fdfd9e991b1a`
- GitHub state at capture: open, mergeable, and draft
- Archive path: `dset/changes/archive/2026-07-14-operationalize-dset-v1`

## Guarded transaction

1. `uv run dset archive operationalize-dset-v1 --date 2026-07-14` returned the exact active-to-archive plan without writing.
2. `uv run dset archive operationalize-dset-v1 --date 2026-07-14 --execute` moved the change, set `status: archived`, and wrote the dated archive metadata without overwriting an existing destination.
3. The first post-move aggregate correctly rejected six now-invalid relative links with `DSET-E113`. The links were adjusted for the additional `archive/` path level.
4. `uv run dset trace . --write` regenerated stable archived paths and evidence pointers.
5. `python -m dset_toolchain verify .` then exited 0: 18 Python files formatted and lint-clean, strict typing passed for 18 files, 11 unit/fixture tests passed, trace freshness passed, and DSET validation passed.
6. `git diff --check` exited 0 and the candidate was committed and pushed with a clean worktree.

The moved-link failure is retained as evidence that archive layout is validated after the real transaction, not inferred from the active layout.

## Hosted candidate-head checks

| Check | Result | GitHub evidence |
|---|---|---|
| `DSET / validate` on the `dev` push | Pass | [run 29295009593, job 86966474511](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29295009593/job/86966474511) |
| `DSET / validate` on the PR | Pass | [run 29295011987, job 86966481366](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29295011987/job/86966481366) |
| `PR policy` | Pass | [run 29295011333, job 86966479524](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29295011333/job/86966479524) |
| `Enable auto-merge` | Correctly skipped while draft | [run 29295011333, job 86966492794](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29295011333/job/86966492794) |

## Protected-main decision

[Ruleset 18897046](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18897046) was active at capture with no bypass actors. It requires a pull request, requires both `PR policy` and `DSET / validate`, permits only a merge commit, and blocks deletion and non-fast-forward updates to `main`.

## Evidence-only finalization rule

This proof and the corresponding verification/task updates form the final evidence-only commit after the tested candidate. They do not change implementation code or accepted package specifications. Hosted checks must pass again on that evidence-only head before PR #7 is marked ready. GitHub remains authoritative for the final head, auto-merge action, and merge commit; no artifact predicts a future merge SHA.

## Disposition

The dated archive candidate satisfies deterministic tests, qualitative evals, accepted-truth reconciliation, link portability, trace freshness, real PR identity, and protected-merge readiness. Any later implementation or accepted-specification edit invalidates this disposition and requires a new verification cycle.
