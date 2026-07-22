# Independent bootstrap-eval baseline — 2026-07-14

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

This report records the pre-reconciliation, pre-archive baseline. It is historical evidence, not the current completion status. The archive-layout rerun is recorded separately after reconciliation and the dated move.

## Protocol

Four isolated, read-only reviewers each evaluated one bootstrap criterion from the repository root. They received no conversation history, expected path, or private routing instruction. Each reviewer recorded its actual discovery path, repository evidence, ambiguities, and a strict pass/fail result. No reviewer edited the repository.

## Results

| Eval ID | Result | Independent finding |
|---|---|---|
| **DSET-EVAL-GOV-001** | Pass | All five contributor cases resolved to the correct repository-owned path without private context. |
| **DSET-EVAL-GOV-002** | Pass | The reviewer kept framework publication, accepted project truth, active deltas, and archived evidence under distinct owners. |
| **DSET-EVAL-GOV-003** | Pass | The one-package tree covers all current accepted behavior; no present cross-package contract justifies an empty global layer. |
| **DSET-EVAL-GOV-004** | Pass | The reviewer reconstructed completed tasks, PR identity, remaining gates, and the next task from repository files alone. |

## DSET-EVAL-GOV-001 — Findability

The reviewer started at `README.md`, followed its `dset/README.md` entrypoint, then used the manifest, package README, changes README, and active bootstrap documents.

| Case | Located destination |
|---|---|
| Accepted methodology requirements | `dset/specs/packages/methodology/spec.md`, identified by `dset/specs/packages/methodology/README.md` as accepted behavioral truth |
| Start a bounded methodology change | `dset/changes/<change-id>/` with requirement deltas at `specs/methodology.md` |
| Separate truth from deltas | `dset/specs/packages/methodology/` for accepted truth; `dset/changes/<change-id>/` for unaccepted intent and evidence |
| Decide whether global truth is needed | `dset/README.md` plus `dset/dset.yaml`; one package and `global_truth_root: null` mean no global layer yet |
| Resume the bootstrap | Root README link to the bootstrap, then `proposal.md`, `tasks.md`, `verification.md`, and `implementation-plan.md` |

The only friction was that no copy-ready change template exists yet and resumption state spans several intentionally separate artifacts. Neither issue caused a misroute. Result: **Pass, 5/5 cases**.

## DSET-EVAL-GOV-002 — Ownership

The reviewer found the ownership boundary consistently in `README.md`, `dset/README.md`, `dset/dset.yaml`, the methodology package README, and the changes READMEs:

- Root `methodology/` is the public framework implementation/publication surface.
- `dset/specs/packages/methodology/` owns accepted project truth for that surface.
- `dset/changes/<change-id>/` owns unaccepted proposals, deltas, plans, and evidence.
- `dset/changes/archive/` owns immutable evidence only after reconciliation and fresh verification.

The shared word “methodology” and normative language inside the active delta were tested as likely confusion points. Explicit boundary statements and active-change status resolved both. Result: **Pass, no ownership confusion observed**.

## DSET-EVAL-GOV-003 — Proportionality

The manifest registers exactly one active package, `methodology`; its current-truth directory contains a domain, specification, public contract, deterministic test plan, and qualitative eval plan. No second independently meaningful capability, cross-package dependency, shared journey, or aggregate release gate exists.

The reviewer also checked the future `schemas/` and `templates/` roots. Their READMEs identify placeholders rather than implemented packages or global truth. The design and solution landscape provide a concrete trigger for later expansion: add a global layer only when multiple packages create shared contracts or release gates. Result: **Pass, no global layer required**.

## DSET-EVAL-GOV-004 — Resumability

The reviewer reconstructed this state without chat history:

- DSET-TASK-GOV-001 through DSET-TASK-OPS-001 were complete.
- The implementing PR was `anatoly-m-maslennikov/dset-loops-framework#2`.
- DSET-TASK-GOV-004 was the next task.
- Fresh proof, reconciliation, archival, readiness review, and merge remained after the eval.

The reviewer found two stale pre-rebase commit IDs in `implementation-plan.md`. It also noted that “PR pending” in the verification disposition could mean review/readiness/merge because PR creation was already complete. These are correctable readiness findings, not blockers to reconstructing the next action. Result: **Pass with two handoff corrections required before archive**.

## Disagreements and disposition

No reviewer disagreed with the expected folder ownership or proportional one-package design. The minor findability friction and two stale handoff references are retained as findings rather than averaged away. Archive readiness requires correcting the stale commit IDs and making the remaining PR state explicit.
