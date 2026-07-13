---
name: dset-diagnose
description: Diagnose software or production failures through reproducible evidence, minimization, hypotheses, instrumentation, first-bad-commit analysis, and DSET Back-to-Left provenance. Use when the user asks to investigate, explain, triage, or find the cause of a defect, regression, failed gate, incident, or inconsistent behavior; diagnosis remains read-only unless the user separately authorizes a fix.
---

# DSET Diagnose

Find the earliest evidence-backed failure boundary and preserve a reproducible regression proof. Do not implement a fix merely because the likely cause is known.

## Workflow

1. Read the active change, accepted spec, test/eval plan, supportability contract, runbook, relevant ADRs, and current worktree state. Identify the authoritative state owner for each affected concern.
2. Reproduce the symptom at the smallest public seam. Record exact inputs, environment/build/deploy identity, observed output, expected requirement, and whether the result is deterministic or variable.
3. Minimize without changing the failure. Separate product defects from sandbox, dependency, network, credential, or operator-environment failures.
4. Form competing falsifiable hypotheses. Gather the cheapest discriminating evidence using safe read-only diagnostics first; redact secrets and bound logs, cardinality, volume, and retention.
5. Locate the first bad commit with `git bisect`, focused history, or equivalent evidence when feasible. Treat `git blame` and intuition as leads, not proof.
6. Trace backward through commit, PR, DSET change, ADR/design, requirement, test/eval, and verification. Classify the earliest defective or missing artifact and give every relevant upstream artifact a disposition: correct, amend, supersede, or reviewed-no-change with reason.
7. Add a regression test for exact behavior or a failing baseline plus threshold for probabilistic behavior. Demonstrate failure against the defective revision when reproducible.
8. Record findings in a defect change's `root-cause.md`, proof artifacts, test/eval plan, and verification. Run `dset check` before handoff.

## Diagnostic report

Report symptom, reproduction, evidence, ruled-out hypotheses, likely or proven cause, first bad commit confidence, affected artifacts, regression proof, containment options, and the smallest safe fix boundary. Mark inference as inference.

## Stop conditions

Stop when evidence cannot distinguish the remaining hypotheses, required diagnostics exceed authorization, or reproduction risks production data or effects. Request the missing evidence or authority. Do not edit implementation code unless the user explicitly asks for the fix; if authorized, return to the earliest defective artifact and replay the DSET loop forward.
