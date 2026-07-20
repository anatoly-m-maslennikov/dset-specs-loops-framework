---
name: dset-implement
description: Deliver a bounded DSET implementation outcome from raw or prepared intent. Use when the operator wants code, documentation, methodology, tests, eval assets, or configuration changed; repository-local entry criteria decide and prepare missing prerequisites.
---

# DSET Implement

This is the thin wrapper for `implement`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-implement --target TARGET --objective OBJECTIVE`. Stop if the launcher is unavailable or the command fails; never select an alternate runtime or fall back to this wrapper, memory, templates, another project, or remote prose.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.

## Handoff

Follow the returned local lifecycle contract. Return changed assets, provenance, residual work, and session identity; stop on the resolved criteria and before claiming verification or release readiness.
