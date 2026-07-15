# Hosted fixed-point proof — 2026-07-14

## Subject

- Draft PR: [#9](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9)
- Pushed `dev` head: `0fcf850cc4b4d8c1ae052b85ff3ebe2300be2f7f`
- Workflow: `DSET`
- Canonical command: `uv run dset verify .`

## Corrective loop

The first PR-head run, [29359397896](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29359397896), failed in `DSET / validate`. Formatting, lint, types, governance, and all non-self-host tests passed. The self-host tests failed at the released-validator boundary with:

```text
DSET-E140 ... released validator cannot be extracted:
fatal: not a tree object: a95bf7c576c8fcdfdf0565466aaca5ee1fe86157
```

The workflow used the checkout action's default depth of one commit, so the
pinned released validator was not present. The correction added a failing
regression test that requires the DSET workflow's checkout step to declare
`fetch-depth: 0`, then applied that setting. The self-hosting contract was not
weakened and the released baseline identity did not change.

## Passing rerun

| Evidence | Result |
|---|---|
| [Workflow run 29359618414](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29359618414) | Completed successfully |
| Job `87176049684`, `DSET / validate` | Completed successfully |
| Checked-out pushed head | `0fcf850cc4b4d8c1ae052b85ff3ebe2300be2f7f` |
| Canonical verification step | Success |
| Local post-fix suite | 36 tests passed |
| Local post-fix self-host command | Released validator, candidate repository, temporary adopter, customization, unchanged wrapper, and recursion-stop checks passed |

## Disposition

Roadmap §4 and `DSET-TASK-TOOL-025` pass for the current pushed head. This proof
does not satisfy the separate qualitative evals or later TypeScript, pilot,
distribution, reconciliation, archive, or DSET 0.2 release gates. PR #9 remains
draft.
