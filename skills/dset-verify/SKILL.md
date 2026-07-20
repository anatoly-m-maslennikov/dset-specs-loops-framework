---
name: dset-verify
description: Check current implementation and governance against accepted DSET truth, implementation plans, deterministic tests, and applicable eval plans. Use after relevant changes or when proof freshness is uncertain; report conformance and evidence, then stop before repairing failures or releasing.
---

# DSET Verify

This is the thin wrapper for `verify`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-verify --target TARGET --objective OBJECTIVE`. Stop if the launcher is unavailable or the command fails; never select an alternate runtime or fall back to this wrapper, memory, templates, another project, or remote prose.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.

## Handoff

Return proof inputs and freshness, deterministic test results, applicable eval evidence, conformance gaps, created Problems, and available session identity. Do not rewrite authority from evidence; stop before repair or release.
