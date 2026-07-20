---
name: dset
description: Route a general, multi-stage, or uncertain request to one governed DSET mode through repository-local governance. Use when the operator does not know which specialist skill applies; return the mode, evidence, and authorized handoff without performing the specialist workflow.
---

# DSET

This is the thin primary wrapper for `lifecycle-orchestration`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID [--session-id SESSION_ID]`. Replace the host-session placeholder; reuse the explicit DSET `SESSION_ID` from a prior handoff and omit it only on initial DSET entry. Stop when the ID, launcher, or command is unavailable, and never select an alternate runtime.
2. Verify and report the returned target, repository/Work Area, manifest, governance registry, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. When the context is resolved, read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id`, `session_id`, and `repository_root`. For an active specialist transition, invoke `dset runtime handoff RUN_ID REPOSITORY_ROOT --next-signal WORKFLOW`, return the same `session_id`, and require the next context call to pass it. Only a true session completion or stop invokes `dset runtime finish RUN_ID REPOSITORY_ROOT --status TERMINAL_STATUS`; report command failure.

## Route and hand off

Follow only the returned local rules and session handoff. Return one mode, its
evidence, and the next authorized specialist handoff; do not perform that
specialist workflow. Preserve one session and route writes through resolved
owners; never edit an emitted atom. Stop exactly where the resolved lifecycle
contract stops.
