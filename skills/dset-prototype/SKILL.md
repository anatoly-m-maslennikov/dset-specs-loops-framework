---
name: dset-prototype
description: Run a bounded disposable experiment to answer a specific design, framework, library, protocol, performance, recovery, or integration question with comparable evidence. Use when uncertainty blocks a DSET Solution Landscape or Decision and production-quality implementation would be premature; never use the prototype as an unreviewed path into production.
---

# DSET Prototype

This is the thin wrapper for `prototyping`; resolved repository-local documents own substantive behavior.

## Resolve

1. Walk upward from the target for exactly one schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop on competing authorities. With no root, return a `$dset` `initialize` handoff and stop.
2. Select exactly one available resolver entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module; stop if neither exists. Never retry the alternate after a nonzero result.
3. Run the selected entrypoint with `rules resolve prototyping --format json`; stop on a nonzero result without fallback to the wrapper, memory, installed templates, or remote framework prose.
4. Report workflow, profile/version, customization, wrapper and ordered rule identities, conflicts, and `conflict_resolution` coverage. Empty `conflicts` is unassured when coverage is absent or unavailable.
5. Read the returned rule documents in order before using session/runtime behavior. Stop on unresolved conflicts or when selected rules require unavailable conflict coverage.
6. Use the installed distribution runtime adapter only when exposed; otherwise return `persistence: unavailable` and obey the resolved stop behavior.

## Handoff

Return comparable disposable evidence. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return available session identity and the next handoff; never treat prototype work as accepted design or production implementation, and stop before adoption or promotion.
