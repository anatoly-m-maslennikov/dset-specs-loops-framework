---
name: dset-decisions
description: Reconcile available operator/session intent and repository evidence into missing accepted atomic DSET records and current compiled handoffs. Use when a desired outcome may rely on directives not yet captured; expose unclear acceptance and stop before implementation.
---

# DSET Decisions

This is the thin wrapper for `decisions`; resolved repository-local documents own substantive behavior.

## Resolve

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-decisions --target TARGET --objective OBJECTIVE`. Stop if the launcher is unavailable or the command fails; never select an alternate runtime or fall back to this wrapper, memory, templates, another project, or remote prose.
2. Verify and report the returned repository/Work Area, skill/workflow/mode, wrapper, ordered rule identities and digests, ruleset identity, conflict coverage, and run/session identity.
3. Read the returned project-owned rule documents in order. Stop on an identity mismatch, unresolved conflict, required unavailable conflict coverage, or any returned stop status.

## Handoff

Follow the resolved entry and exit criteria to reconcile only available current evidence. Return emitted atomic IDs, compiled-owner updates, material unknowns, and session provenance. Never invent acceptance, edit an emitted atom, or continue into implementation.
