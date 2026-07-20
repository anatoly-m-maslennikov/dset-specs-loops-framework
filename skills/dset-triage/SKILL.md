---
name: dset-triage
description: Classify and route durable DSET Questions, including Conflicts and Opportunities, and Problems without defining type from workflow. Use when an artifact is unclassified, lacks priority/owner/Change linkage, or needs the next governed route; stop before diagnosis, decision, or implementation.
---

# DSET Triage

This is the thin wrapper for `work-triage`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-triage --target TARGET --objective OBJECTIVE --llm-session-id LLM_SESSION_ID`. Replace the placeholder with the current host session ID; stop when it or the launcher is unavailable or the command fails, and never select an alternate runtime.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.
4. Retain `run_id` and `repository_root`. Before every handoff or stop, invoke `dset runtime finish RUN_ID REPOSITORY_ROOT --status STATUS`; report failure and never claim terminal evidence without a terminal record.

## Handoff

Return semantic type, evidence, priority state, owner and Change/tracker links, next governed route, and available session identity. Route authorized writes through resolved owners; stop before solving the work.
