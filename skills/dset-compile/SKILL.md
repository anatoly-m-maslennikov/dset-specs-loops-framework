---
name: dset-compile
description: Semantically reconcile accepted atomic DSET artifacts into affected evergreen specifications and plans under the target repository's local governance. Use when the operator requests compilation, pending atoms must become current project truth, or implementation, verification, or release entry criteria require current evergreen artifacts; do not run merely because one new atom exists.
---

# DSET Compile

This is the thin wrapper for `compile`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-compile --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Replace the host-session placeholder; reuse the explicit DSET `SESSION_ID` from a prior handoff and omit it only on initial DSET entry. Stop when the ID, launcher, or command is unavailable, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id`, `session_id`, and `repository_root`. For an active specialist transition, invoke `dset runtime handoff RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW`, return the same `session_id`, and require the next context call to pass it. Only a true session completion or stop invokes `dset runtime finish RUN_ID REPOSITORY_ROOT --status TERMINAL_STATUS`; report command failure.

## Handoff

Follow the resolved compilation and artifact-maintenance rules. Return updated and unchanged evergreen owners, pending atoms, conflicts, frontier state, material unknowns, and session provenance; stop before implementation, testing, evaluation, or release.
