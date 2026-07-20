---
name: dset-release
description: Prepare or verify a governed DSET release transaction and, only with separate explicit publication authority, publish it. Use for an explicit release request or a verified release-ready Change; stop on identity, gate, ownership, or authorization mismatches.
---

# DSET Release

This is the thin wrapper for `release`; resolved repository-local documents own substantive behavior, and the wrapper supplies no release engine or publisher.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-release --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Stop and hand off

Prepare or verify only already-authorized actions. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return diagnostics, prepared/verified state, and available session identity. Publication requires separate explicit authority; stop on any mismatch, missing gate, collision, ambiguity, or new authority, and never claim absent automation completed it.
