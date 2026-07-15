---
name: dset-clarify
description: Turn ambiguous product or domain intent into decision-ready DSET vocabulary, boundaries, invariants, requirements, scenarios, proof obligations, alternatives, and remaining unknowns. Use before specification acceptance when unresolved branches, overloaded terms, hidden actors or states, unclear ownership, conflicting edge cases, or premature solution choices block a decision; stop before selecting a consequential answer or implementing it.
---

# DSET Clarify

This is the thin wrapper for the registered `domain-clarification` workflow. Repository-local governing documents own every substantive rule.

## Resolve and clarify

1. Locate the repository root by walking upward to `dset/scopes/meta/dset.yaml` for schema 1.2 or legacy `dset/dset.yaml` for schema 1.0/1.1; stop if both authorities exist.
2. Run `dset rules resolve domain-clarification --format json` or `python -m dset_toolchain rules resolve domain-clarification --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, agent memory, an installed template, or remote framework prose.
4. Before governed work, report the resolved workflow ID, profile/version, customization identity, ordered rule IDs and paths, wrapper identity, and conflicts.
5. Through the repository-registered `DSET-RULE-SKILL-RUNS`, join a compatible explicit session or start a bounded one, record this invocation, and report its session ID; follow its stop behavior when continuity is unavailable.
6. Read and apply the resolved governing documents in their returned order.

## Handoff

Return decision-ready alternatives and remaining unknowns under this wrapper's registered specialist boundary. Write conclusions only to resolved owning artifacts when authorized; otherwise return a proposed update. Update session continuity, recommend the next handoff, and stop before consequential selection or implementation.
