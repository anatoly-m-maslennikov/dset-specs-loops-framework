# Qualitative evaluations — 2026-07-14

## Evaluation method

Three independent agent reviewers received bounded, read-only cases. They used committed repository files without session context and were told not to edit the repository or contact GitHub. One reviewer evaluated file-only resumability, one evaluated failure diagnosis and delivery recovery, and one evaluated skill routing plus one-root migration. Initial failures were corrected in normal commits and assigned back to the same reviewer for re-evaluation.

| Eval ID | Initial result | Corrective loop | Final result |
|---|---|---|---|
| DSET-EVAL-GOV-005 | Fail at `114fc3c`: active verification still called the canonical command pending and conflicted with current configuration | `4fe015d` made the canonical command explicit, distinguished the locked entry point, completed the traceability task, and refreshed gate status | Pass at `4fe015d` |
| DSET-EVAL-OPS-005 | Pass at `114fc3c` | No blocking correction | Pass |
| DSET-EVAL-SKILL-001 | Fail at `114fc3c`: diagnosis declared a read-only boundary but later steps implied unconditional regression-proof and DSET-artifact writes | `c14826b` separated read-only reporting, authorized diagnostic-artifact writes, and separately authorized implementation fixes | Pass at `4fe015d` |
| DSET-EVAL-GOV-006 | Pass with a template-clarity improvement requested at `114fc3c` | `4fe015d` added owner, consumers, status, target artifacts, retention, and read-only cutover fields to the migration map | Pass at `4fe015d` |

## DSET-EVAL-GOV-005 — File-only resumability

The evaluator found the current `in-progress` state and PR identity in `change.yaml`, the sole remaining task in `tasks.md`, deterministic and qualitative proof obligations in the two proof plans, current gate state in `verification.md`, and the canonical command in `dset.yaml`, `dset/README.md`, and `verification.md`. Cold navigation took approximately two minutes. The initial contradictory handoff was a threshold failure; after correction, the evaluator reported no material contradiction.

## DSET-EVAL-OPS-005 — Diagnostics and delivery recovery

For a failed `dset verify`, the evaluator located structural validation, ordered configured gates, stable diagnostic rendering, exact failed-command reporting through `DSET-E201`, and stale-trace reporting through `DSET-E111`. The safe recovery was to inspect read-only diagnostics, correct the bounded source failure, explicitly regenerate traceability only after review, and rerun the exact gate plus the aggregate.

For blocked `dev → main` delivery, the evaluator correctly routed live authority to the GitHub PR, exact head, named check runs, ruleset, and eventual merge commit through the [delivery runbook](../../../../../ops/supportability/delivery-runbook.md). The safe recovery preserves the draft PR evidence, fixes repository inputs on `dev`, reruns only demonstrably transient hosted failures, and never bypasses protected `main`.

Non-blocking observation: `DSET-E201` reports the exact child command and exit status but does not embed child stdout/stderr as structured JSON. Raw output remains deliberately transient; a concise operator-facing diagnostic-code catalogue is a possible later usability improvement.

## DSET-EVAL-SKILL-001 — Skill routing and authorization

All three prompts selected distinct skills after correction:

| Prompt class | Route | Verified stop boundary |
|---|---|---|
| Ambiguous actors, states, ownership, and acceptance rules | `dset-grill` | Without write authorization, return proposed artifact changes; stop before solution/code while a material domain branch remains |
| Explain a retry-related duplicate without fixing it | `dset-diagnose` | Diagnosis/reporting remain read-only; DSET-artifact writes and implementation fixes require separate explicit authorization |
| Run a disposable comparison to answer one recovery question | `dset-prototype` | Evidence remains in the active proof surface; production code/current truth are excluded; promotion returns through a Decision/design and normal proof |

Non-blocking observation: `dset-prototype` treats an explicit request to run the disposable experiment as authorization for bounded proof-directory writes. This is consistent with its trigger but differs from the explicit write-confirmation wording in the other two skills.

## DSET-EVAL-GOV-006 — One-root migration

The evaluator produced one writable `dset/` target while mapping accepted domain/spec truth, deterministic test plans, qualitative/probabilistic eval plans, active implementation work, and completed history to distinct owners. Old roots become read-only only after verified archival and ownership cutover. Test/eval separation survived the mapping.

The corrected [migration map template](../../../../../gov/migrations/migration-map.template.yaml) now carries owner, writer, consumers, current status, target artifacts, disposition, retention, and read-only state. A mixed legacy root must use multiple source entries when active and completed artifacts need different dispositions; this is an authoring decision, not a second writable authority.

## Disposition

All four thresholds pass after the recorded corrective loops. These evaluations prove file-only usability and routing against committed artifacts. They do not replace deterministic tests, validate external GitHub state, or claim that the archive/merge transaction has completed.
