---
name: dset-implement
description: Deliver a bounded DSET implementation outcome from raw or prepared intent. Use when the operator wants code, documentation, methodology, tests, eval assets, or configuration changed; repository-local entry criteria decide and prepare missing prerequisites.
---

# DSET Implement

This is the thin wrapper for `implement`; resolved repository-local documents own substantive behavior.

## Resolve

1. Walk upward from the target for exactly one schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop on competing authorities. With no root, return a `$dset-init` handoff and stop.
2. Select exactly one available resolver entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module; stop if neither exists. Never retry the alternate after a nonzero result.
3. Run the selected entrypoint with `rules resolve implement --format json`; stop on a nonzero result without fallback to the wrapper, memory, installed templates, or remote framework prose.
4. Report workflow, profile/version, customization, wrapper and ordered rule identities, conflicts, and `conflict_resolution` coverage. Empty `conflicts` is unassured when coverage is absent or unavailable.
5. Read the returned rule documents in order. Stop on unresolved conflicts or when selected rules require unavailable conflict coverage.
6. Use the installed distribution runtime adapter only when exposed; otherwise return `persistence: unavailable` and obey the resolved stop behavior.

## Handoff

Follow the resolved entry-criteria closure: invoke `dset-decisions` first, then conditionally invoke proof and implementation planning before building. Re-read authority and require progress after every child run. Return changed assets, provenance, residual work, and session identity; stop on the resolved criteria and before claiming verification or release readiness.
