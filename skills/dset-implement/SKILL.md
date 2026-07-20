---
name: dset-implement
description: Deliver a bounded DSET implementation outcome from raw or prepared intent. Use when the operator wants code, documentation, methodology, tests, eval assets, or configuration changed; repository-local entry criteria decide and prepare missing prerequisites.
---

# DSET Implement

This is the thin wrapper for `implement`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-implement --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, implementation preparation mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Handoff

Follow the returned local lifecycle contract. Return changed assets, provenance, residual work, and session identity; stop on the resolved criteria and before claiming verification or release readiness.
