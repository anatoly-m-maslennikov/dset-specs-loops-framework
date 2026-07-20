---
name: dset
description: Reach a general, multi-stage, or uncertain DSET outcome through repository-local governance. Use when the operator wants progress without choosing prerequisite skills manually; prefer a direct skill only when its desired outcome is already clear.
---

# DSET

This is the thin primary wrapper for `lifecycle-orchestration`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned target, repository/Work Area, manifest, governance registry, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. When the context is resolved, read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Route and hand off

Follow only the returned local rules and session handoff. Preserve one session and route writes through resolved owners; never edit an emitted atom. Stop exactly where the resolved lifecycle contract stops.
