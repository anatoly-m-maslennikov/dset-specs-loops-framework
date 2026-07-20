---
name: dset-release
description: Prepare or verify a governed DSET release transaction and, only with separate explicit publication authority, publish it. Use for an explicit release request or a verified release-ready Change; stop on identity, gate, ownership, or authorization mismatches.
---

# DSET Release

This is the thin wrapper for `release`; resolved repository-local documents own substantive behavior, and the wrapper supplies no release engine or publisher.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-release --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Replace the host-session placeholder; reuse the explicit DSET `SESSION_ID` from a prior handoff and omit it only on initial DSET entry. Stop when the ID, launcher, or command is unavailable, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id`, `session_id`, and `repository_root`. For an active specialist transition, invoke `dset runtime handoff RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW`, return the same `session_id`, and require the next context call to pass it. Only a true session completion or stop invokes `dset runtime finish RUN_ID REPOSITORY_ROOT --status TERMINAL_STATUS`; report command failure.

## Stop and hand off

Prepare or verify only already-authorized actions. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return diagnostics, prepared/verified state, and available session identity. Publication requires separate explicit authority; stop on any mismatch, missing gate, collision, ambiguity, or new authority, and never claim absent automation completed it.
