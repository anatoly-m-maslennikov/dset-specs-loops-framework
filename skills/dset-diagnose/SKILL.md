---
name: dset-diagnose
description: Investigate a defect, regression, failed gate, incident, or inconsistent behavior and return evidence, cause confidence, and repair options. Use for cause-finding when the cause is unknown; diagnosis stops before implementing a fix.
---

# DSET Diagnose

This is the thin wrapper for `diagnosis`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-diagnose --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Handoff

Diagnosis remains read-only unless recording findings is separately authorized. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return evidence, cause confidence, repair options, and available session identity; stop before implementing a fix without separate repair authority.
