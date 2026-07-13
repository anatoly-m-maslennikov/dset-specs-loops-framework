# Independent supportability evals — 2026-07-14

> Baseline evidence carried into the dated archive candidate for [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3).

## Review protocol

Two independent subagents received the five cases and SUP-EVAL-001–005 without seeing each other's answers. They reviewed README, methodology 00–05, DSET metadata, accepted methodology truth, and the active change. Reviewers made no edits.

## Baseline result before fixtures

Both reviewers independently returned the same result: SUP-EVAL-003, SUP-EVAL-004, and SUP-EVAL-005 passed; SUP-EVAL-001 and SUP-EVAL-002 failed. The methodology routed cases coherently, but the eval plan supplied no instantiated diagnostic entrypoint, incident identifier, runtime evidence, deployed version, repository-qualified PR record, proof record, or fix record. The corrective artifact was [synthetic-incidents.md](synthetic-incidents.md), committed as `545be89`.

## Independent rerun

| Eval | Reviewer A | Reviewer B | Consolidated evidence |
|---|---|---|---|
| SUP-EVAL-001 findability | Pass | Pass | README and methodology route to the contract; the fixture index exposes a diagnostic entrypoint and each case supplies a safe action/runbook |
| SUP-EVAL-002 incident traceability | Pass | Pass | Every synthetic case reaches runtime/build identity, commit, repository-qualified synthetic PR, DSET change, requirement, applicable test/eval, and repair record |
| SUP-EVAL-003 proportionality | Pass | Pass | The async case preserves producer/broker/receiver correlation and deduplication evidence; the resumable local case uses a local bundle and no distributed tracing backend |
| SUP-EVAL-004 safety | Pass | Pass | Fixtures are fictional and redacted; no investigation requires credentials, tokens, raw identifiers, user content, or unrelated personal data |
| SUP-EVAL-005 proof separation | Pass | Pass | Both reviewers classified schemas, identity, propagation, permissions, redaction, retention, and bounds as tests, and unfamiliar-operator diagnosis/action quality as evals |

## Case traversal times

Times are manual reading estimates, not instrumented performance measurements.

| Case | Reviewer A | Reviewer B | Owning record |
|---|---:|---:|---|
| SYN-INC-001 | 20–30 seconds | ~15 seconds | `acme/support-demo#417` |
| SYN-INC-002 | 30–45 seconds | ~20 seconds | `acme/support-demo#422` |
| SYN-INC-003 | 20–30 seconds | ~15 seconds | `acme/local-demo#38` |
| SYN-INC-004 | 20–30 seconds | ~15 seconds | `acme/support-demo#429` |
| SYN-INC-005 | 30–45 seconds | ~20 seconds | `acme/llm-demo#91` |

## Disagreements and limitations

- No reviewer disagreed with the stated test/eval classification.
- Both noted that “simple local case” is imprecise because crash/resume triggers Profile B semantics; the local topology still correctly avoids distributed telemetry.
- Fictional commands, runbooks, commits, PR records, and fixes prove framework traversal clarity only. They are intentionally non-executable and non-resolvable and do not replace a real adopter's contract tests.
- The synthetic PR records are not an implementing PR for this DSET change. Their presence does not make the active change archive-eligible.

## Disposition

Pass: both independent reviewers met all five thresholds after the corrective fixture. The change remains active solely because the user requested a `dev` push without an implementing PR, and the archive contract requires that PR identity.

**Later lifecycle update:** The statement above records the eval-time condition. Draft implementing [PR #3](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/3) was created afterward; archive readiness is verified separately against its pushed candidate head.
