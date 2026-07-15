---
name: dset-diagnose
description: Diagnose software or production failures through reproducible evidence, minimization, hypotheses, instrumentation, first-bad-commit analysis, and DSET Back-to-Left provenance. Use when the user asks to investigate, explain, triage, or find the cause of a defect, regression, failed gate, incident, or inconsistent behavior; diagnosis and reporting are read-only unless the user separately authorizes artifact edits or a fix.
---

# DSET Diagnose

This is the thin wrapper for the registered `diagnosis` workflow. Repository-local governing documents own every substantive diagnostic, proof, safety, and supportability rule.

## Bootstrap and invocation

1. Locate the repository root by walking upward to `dset/dset.yaml`.
2. Run `dset rules resolve diagnosis --format json` or `python -m dset_toolchain rules resolve diagnosis --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, agent memory, an installed template, or remote framework prose.
4. Before governed work, report the resolved workflow ID, profile/version, customization identity, ordered rule IDs and paths, wrapper identity, and conflicts.
5. Read and apply the resolved governing documents in their returned order.

## Handoff

Apply only the authorization and output boundaries resolved from the repository. Diagnosis remains read-only unless artifact edits are explicitly authorized, and it never authorizes an implementation fix by itself. Return findings to the resolved owning artifacts or provide the same bounded report without writing.
