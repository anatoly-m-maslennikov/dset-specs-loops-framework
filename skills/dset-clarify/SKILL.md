---
name: dset-clarify
description: Turn ambiguous product or domain intent into explicit DSET vocabulary, boundaries, invariants, requirements, scenarios, proof obligations, and decision records. Use before specification acceptance when a feature request has unresolved branches, overloaded terms, hidden actors or states, unclear ownership, conflicting edge cases, or premature solution choices.
---

# DSET Clarify

This is the thin wrapper for the registered `domain-clarification` workflow. Repository-local governing documents own every substantive rule.

## Bootstrap and invocation

1. Locate the repository root by walking upward to `dset/dset.yaml`.
2. Run `dset rules resolve domain-clarification --format json` or `python -m dset_toolchain rules resolve domain-clarification --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, agent memory, an installed template, or remote framework prose.
4. Before governed work, report the resolved workflow ID, profile/version, customization identity, ordered rule IDs and paths, wrapper identity, and conflicts.
5. Read and apply the resolved governing documents in their returned order.

## Handoff

Apply only the authorization and output boundaries resolved from the repository. Return durable conclusions to their owning project artifacts. Without write authorization, return a proposed update and leave the repository unchanged.
