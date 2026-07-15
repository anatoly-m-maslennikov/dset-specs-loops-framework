---
name: dset-prototype
description: Run a bounded disposable experiment to answer a specific design, framework, library, protocol, performance, recovery, or integration question with comparable evidence. Use when uncertainty blocks a DSET Solution Landscape or Decision and production-quality implementation would be premature; never use the prototype as an unreviewed path into production.
---

# DSET Prototype

This is the thin wrapper for the registered `prototyping` workflow. Repository-local governing documents own every substantive experiment and evidence rule.

## Bootstrap and invocation

1. Locate the repository root by walking upward to `dset/scopes/meta/dset.yaml` for schema 1.2 or legacy `dset/dset.yaml` for schema 1.0/1.1; stop if both authorities exist.
2. Run `dset rules resolve prototyping --format json` or `python -m dset_toolchain rules resolve prototyping --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, agent memory, an installed template, or remote framework prose.
4. Join the matching explicit DSET session or start one as the resolved session rules require. When automatically chained, remain a child run in the current session.
5. Before governed work, report the workflow, profile/version, customization, ordered rule IDs and paths, wrapper identity, conflicts, and session ID.
6. Read and apply the resolved governing documents in order, without exceeding the current write authorization.

## Handoff

Return comparable disposable evidence to the resolved owning artifacts and checkpoint the governed handoff. Never treat prototype work as accepted design or production implementation; stop before adoption or promotion.
