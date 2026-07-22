+++
artifact_type = "evidence_record"
artifact_subtype = "evaluation_result"
artifact_id = "DSET-EVIDENCE-RECORD-015"
priority = "high"
child_of = ["DSET-EVALUATION-TOOL-003"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Evaluation result — Claudian clean-room comparison

**LLM session IDs:**
`codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

Clean upstream Claudian commit
`783df1ceb149ac9cd9a00a3444c3dadf83bbacf4`, OYOHA through
`badbd69b5e8b6e847fc096a21db1c8fab3fb194b`, and DSET implementation
`581714c`. This record satisfies the clean-upstream execution half of
`DSET-EVALUATION-TOOL-003`; it does not promote the candidate.

## Method and observations

1. Materialized an exact detached sparse Claudian worktree without changing
   or pushing the upstream checkout.
2. Ran `dset init` as a no-write preview, then executed it only in a disposable
   copy. The first executable attempt exposed `DSET-PROBLEM-TOOL-006`; after
   its regression-tested repair, initialization, `dset check`, `dset rules
   check`, `rules resolve implement`, and `skills context --skill
   dset-implement` passed with an independent local ruleset.
3. Ran the framework's OYOHA-pinned candidate inspection against exact
   Claudian. It executed no target command and returned only expected target
   revision and file-population drift: 340 source TypeScript files, 248 test
   TypeScript files, and 588 lint files.
4. Installed the exact lockfile into the disposable copy with lifecycle
   scripts disabled. Typecheck passed. Lint passed with zero errors and zero
   warnings. The isolated production build passed.
5. The full Jest run passed 5,744 of 5,754 Tests. One test required a forbidden
   home-directory temp write and nine required a forbidden local listening
   socket; those ten results are host-blocked rather than product failures.

The local host exposed Node 26.5.0 while both projects declare Node 24. This
limits the command results to comparative evidence. Initialization, registry,
classification, and read-only profile inspection do not depend on claiming
Node 24 conformance.

## Disposition

**Keep candidate.** Neutral gate categories, read-only inspection, exact
evidence binding, hard-error protection, shrink-only debt, isolated build, and
environment/result separation generalize. Exact evidence, commands, roots,
counts, warning thresholds, CI jobs, product architecture, Obsidian policy,
secret scanner, supportability, and blocker IDs remain project-local applied
fields. See
[`DSET-ANALYSIS-REPORT-001`](../DSET-ANALYSIS-REPORT-001-clean-upstream-typescript-boundary.md).

## Reopen conditions

Reopen when the candidate schema or applied-profile split changes, either
repository's compared revision changes, a Node 24/hosted clean-upstream result
exists, or the candidate is considered for promotion.
