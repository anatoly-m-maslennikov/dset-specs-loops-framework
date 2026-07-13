# GitHub delivery evidence — 2026-07-14

## Authoritative delivery record

- Repository: `anatoly-m-maslennikov/dset-specs-loops-framework`
- Pull request: [#7 — Operationalize the executable DSET v1 toolchain](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)
- Author: `anatoly-m-maslennikov`
- Route: `dev` → `main`
- State at evidence capture: open, mergeable, and draft
- Pushed head: `114fc3c90d39e1273cbc8cafadd33c67057d5bad`

GitHub is authoritative for PR state, changed files, checks, and the eventual merge result. The committed [PR history snapshot](../../../history/pull-requests.yaml) and [traceability index](../../../traceability.yaml) are reproducible discovery aids, not competing runtime authorities.

## Pushed-head checks

| Check | Result | GitHub evidence |
|---|---|---|
| `DSET / validate` on the `dev` push | Pass | [run 29294314773, job 86964415352](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29294314773/job/86964415352) |
| `DSET / validate` on the PR | Pass | [run 29294316577, job 86964421112](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29294316577/job/86964421112) |
| `PR policy` | Pass | [run 29294315583, job 86964417548](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29294315583/job/86964417548) |
| `Enable auto-merge` | Correctly skipped while draft | [run 29294315583, job 86964428867](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/actions/runs/29294315583/job/86964428867) |

## Protected-main contract

[Ruleset 18897046](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/rules/18897046), `Main accepts owner dev PRs only`, was active at capture and had no bypass actors. It required a pull request, allowed only the merge method, blocked deletion and non-fast-forward updates, and required both `PR policy` and `DSET / validate`.

## Operational correlation and recovery

An operator starts from PR #7, confirms its head SHA, opens the named check or workflow run, and compares the protected-main ruleset. Safe recovery changes repository inputs on `dev` and reruns the gates; it does not alter `main`, rewrite GitHub evidence, or treat the committed snapshot as live PR state. The complete diagnostic and containment path is documented in [the delivery runbook](../../../supportability/delivery-runbook.md).
