---
name: dset-diagnose
description: Investigate a defect, regression, failed gate, incident, or inconsistent behavior and return evidence, cause confidence, and repair options. Use for cause-finding when the cause is unknown; diagnosis stops before implementing a fix.
---

# DSET Diagnose

This thin wrapper invokes the registered `diagnosis` workflow. Repository-local governing documents own all substantive rules.

## Bootstrap and invocation

1. Locate the repository root by walking upward to `dset/scopes/meta/dset.yaml` for schema 1.2 or legacy `dset/dset.yaml` for schema 1.0/1.1; stop if both authorities exist.
2. Join or start bounded DSET session continuity through the runtime adapter and keep this invocation in that session.
3. Run `dset rules resolve diagnosis --format json` or `python -m dset_toolchain rules resolve diagnosis --format json`.
4. Stop on any nonzero result. Never fall back to this wrapper, memory, templates, or remote framework prose.
5. Report session/run/persistence identity plus the resolved workflow, profile/version, customization, ordered rule IDs and paths, wrapper identity, and conflicts.
6. Read and apply the resolved governing documents in their returned order.

## Handoff

Apply the resolved authorization and output boundaries. Diagnosis remains read-only unless recording findings is separately authorized. Return evidence, cause confidence, repair options, session ID, and the recommended handoff; stop before implementing a fix, which requires separate repair authorization.
