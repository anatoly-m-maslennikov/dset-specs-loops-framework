---
name: dset-prototype
description: Run a bounded disposable experiment to answer a specific design, framework, library, protocol, performance, recovery, or integration question with comparable evidence. Use when uncertainty blocks a DSET Solution Landscape or Decision and production-quality implementation would be premature; never use the prototype as an unreviewed path into production.
---

# DSET Prototype

This is the thin wrapper for `prototyping`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-prototype --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Replace the host-session placeholder; reuse the explicit DSET `SESSION_ID` from a prior handoff and omit it only on initial DSET entry. Stop when the ID, launcher, or command is unavailable, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id`, `session_id`, and `repository_root`. For an active specialist transition, invoke `dset runtime handoff RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW`, return the same `session_id`, and require the next context call to pass it. Only a true session completion or stop invokes `dset runtime finish RUN_ID REPOSITORY_ROOT --status TERMINAL_STATUS`; report command failure.

## Handoff

Return comparable disposable evidence. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return available session identity and the next handoff; never treat prototype work as accepted design or production implementation, and stop before adoption or promotion.
