---
name: dset-clarify
description: Turn ambiguous product or domain intent into decision-ready DSET vocabulary, boundaries, invariants, requirements, scenarios, proof obligations, alternatives, and remaining unknowns. Use before specification acceptance when unresolved branches, overloaded terms, hidden actors or states, unclear ownership, conflicting edge cases, or premature solution choices block a decision; stop before selecting a consequential answer or implementing it.
---

# DSET Clarify

This is the thin wrapper for `domain-clarification`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-clarify --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Replace the host-session placeholder; reuse the explicit DSET `SESSION_ID` from a prior handoff and omit it only on initial DSET entry. Stop when the ID, launcher, or command is unavailable, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id`, `session_id`, and `repository_root`. For an active specialist transition, invoke `dset runtime handoff RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW`, return the same `session_id`, and require the next context call to pass it. Only a true session completion or stop invokes `dset runtime finish RUN_ID REPOSITORY_ROOT --status TERMINAL_STATUS`; report command failure.

## Handoff

Return decision-ready alternatives and remaining unknowns. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return the session identity when available, recommend the next handoff, and stop before consequential selection or implementation.
