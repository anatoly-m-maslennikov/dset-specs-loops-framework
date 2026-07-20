---
name: dset-complete
description: Confirm that no earlier DSET lifecycle mode applies and report terminal Change or session state. Use when implementation and proof appear finished and the operator wants residual obligations, archive/release status, and next handoff checked; stop without inventing work or performing release actions.
---

# DSET Complete

This is the thin wrapper for `complete`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-complete --target TARGET --objective OBJECTIVE`. Stop if the launcher is unavailable or the command fails; never select an alternate runtime or fall back to this wrapper, memory, templates, another project, or remote prose.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.

## Handoff

Return terminal status, residual open obligations, release/archive applicability, recommended handoff, and available session identity. Stop without creating work merely to continue and without performing release or archive effects.
