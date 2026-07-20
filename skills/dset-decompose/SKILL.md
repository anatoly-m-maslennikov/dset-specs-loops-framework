---
name: dset-decompose
description: Decompose a large repository, monorepo, product area, feature, service, documentation set, or deployable unit into governed DSET Work Areas and bounded Changes. Use when ownership, package, dependency, deployment, or proof boundaries are materially unclear; stop before specifying or implementing a selected unit.
---

# DSET Decompose

This is the thin wrapper for `decompose`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-decompose --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Handoff

Return the bounded Work Area/Change decomposition, ownership and dependency seams, unresolved boundaries, and available session identity. Route authorized writes through resolved owners; stop before specification or implementation.
