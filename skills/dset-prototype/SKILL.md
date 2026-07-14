---
name: dset-prototype
description: Run a bounded disposable experiment to answer a specific design, framework, library, protocol, performance, recovery, or integration question with comparable evidence. Use when uncertainty blocks a DSET Solution Landscape or Decision and production-quality implementation would be premature; never use the prototype as an unreviewed path into production.
---

# DSET Prototype

This is the thin wrapper for the registered `prototyping` workflow. Repository-local governing documents own every substantive experiment, evidence, licensing, disposal, and promotion rule.

## Bootstrap and invocation

1. Locate the repository root by walking upward to `dset/dset.yaml`.
2. Run `dset rules resolve prototyping --format json` or `python -m dset_toolchain rules resolve prototyping --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, agent memory, an installed template, or remote framework prose.
4. Before governed work, report the resolved workflow ID, profile/version, customization identity, ordered rule IDs and paths, wrapper identity, and conflicts.
5. Read and apply the resolved governing documents in their returned order.

## Handoff

Apply only the authorization and output boundaries resolved from the repository. Return evidence and decisions to the resolved owning artifacts. Never treat disposable runtime work as accepted design or production implementation.
