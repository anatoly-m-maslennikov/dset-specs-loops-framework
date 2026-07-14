# GitHub delivery evidence — 2026-07-14

## Authoritative subject

- Repository: `anatoly-m-maslennikov/dset-specs-loops-framework`
- Pull request: [#8 — Add artifact governance profiles](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/8)
- Author: `anatoly-m-maslennikov`
- Route: `dev` → `main`
- State at capture: open, mergeable, and draft
- Verified pushed head: `f38a102`

GitHub owns live PR state, checks, runs, and the eventual merge result. The committed PR-history and traceability files are discovery evidence, not competing authorities.

## Hosted checks

| Check | Result | GitHub evidence |
|---|---|---|
| `DSET / validate` on the `dev` push | Pass in 10 seconds | [run 29300308699, job 86982479969](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300308699/job/86982479969) |
| `DSET / validate` on the PR merge ref | Pass in 9 seconds | [run 29300310403, job 86982484738](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300310403/job/86982484738) |
| `PR policy` | Pass in 3 seconds | [run 29300309698, job 86982482860](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300309698/job/86982482860) |
| `Enable auto-merge` | Correctly skipped while draft | [run 29300309698, job 86982494362](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29300309698/job/86982494362) |

## Corrective loop

At head `4934e3e`, both DSET runs passed formatting, lint, strict typing, and all 18 tests, then failed with `DSET-E111` because `dset/traceability.yaml` did not yet list the two newly committed proof files. The derived index was regenerated, reviewed, verified locally, and committed alone as `f38a102`. Both hosted DSET contexts then passed. No implementation or accepted specification changed during this correction.

## Recovery boundary

If a later head fails, keep PR #8 draft, inspect the exact check and head SHA, correct the bounded source or derived index on `dev`, and rerun the canonical gate. Do not bypass protected `main`, force-push evidence, or treat a local snapshot as live hosted state.

## Data handling

This record contains public PR, commit, workflow-run, and job identities plus bounded result summaries. Authentication tokens and raw runner logs are not retained.
