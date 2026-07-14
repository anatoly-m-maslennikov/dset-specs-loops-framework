# Diagnosis

**Rule ID:** `DSET-RULE-DIAGNOSIS`

## Workflow

1. Read accepted requirements, separate proof plans, active change, supportability contract, runbook, decisions, and current worktree/deploy identity.
2. Reproduce the symptom at the smallest public seam with exact input, observed output, expected requirement, and environment/build identity.
3. Minimize without changing the failure; separate product defects from sandbox, dependency, network, credential, and operator-environment failures.
4. Form competing falsifiable hypotheses and gather the cheapest discriminating safe evidence. Bound and redact logs, access, retention, volume, and cardinality.
5. Locate the first bad change when feasible. Treat blame and intuition as leads, not proof.
6. Trace backward through commit, PR, DSET change, decision/design, requirement, test/eval, and verification. Classify the earliest defective or missing artifact.
7. Specify an exact regression test or a variable failing baseline and threshold before proposing the fix boundary.
8. Record findings only when writes are authorized. Diagnosis does not authorize implementation changes.

## Stop conditions

Stop when evidence cannot distinguish remaining hypotheses, diagnostics exceed authorization, or reproduction risks production data/effects. Request the missing evidence or authority and mark inference as inference.
