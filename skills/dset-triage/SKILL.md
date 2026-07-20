---
name: dset-triage
description: Classify and route durable DSET Problems, Opportunities, Questions, and Conflicts without defining type from workflow. Use when an artifact is unclassified, lacks priority/owner/Change linkage, or needs the next governed route; stop before diagnosis, decision, or implementation.
---

# DSET Triage

This is the thin wrapper for `work-triage`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-triage --target TARGET --objective OBJECTIVE`. Stop if the launcher is unavailable or the command fails; never select an alternate runtime or fall back to this wrapper, memory, templates, another project, or remote prose.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.

## Handoff

Return semantic type, evidence, priority state, owner and Change/tracker links, next governed route, and available session identity. Route authorized writes through resolved owners; stop before solving the work.
