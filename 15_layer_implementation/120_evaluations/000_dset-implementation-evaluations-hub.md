# Qualitative methodology Evaluations

## Purpose

Provide provider-neutral prompt implementations for independent qualitative
DSET Evaluation, explicit result reconciliation, and versioned case sets.

## Boundaries

These prompts implement Evaluation execution. Applied QA atoms and plans own
the criterion and threshold; an execution record owns observed output;
evidence and Verification remain with the applicable project scope.

## Start here

- `010_dset-implementation-evaluations-independent-review.md` — run one criterion with
  one isolated reviewer.
- `020_dset-implementation-evaluations-result-reconciliation.md` — reconcile independent
  results without averaging disagreement away.
- `030_dset-implementation-evaluations-skill-cases.toml` — minimum trigger,
  non-trigger, and ambiguous-routing definitions for every public DSET skill.

Apply `llm-evaluations-v1` to every created or updated definition, prompt,
harness, grader, case set, reconciliation procedure, and result carrier.
