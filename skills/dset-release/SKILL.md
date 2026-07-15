---
name: dset-release
description: Prepare or verify a governed DSET release transaction and, only with separate explicit publication authority, publish it. Use for an explicit release request or a verified release-ready Change; stop on identity, gate, ownership, or authorization mismatches.
---

# DSET Release

This is the thin wrapper for `release`; resolved repository-local documents own substantive behavior, and the wrapper supplies no release engine or publisher.

## Resolve

1. Walk upward from the target for exactly one schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop on competing authorities. With no root, return a `$dset` `initialize` handoff and stop.
2. Select exactly one available resolver entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module; stop if neither exists. Never retry the alternate after a nonzero result.
3. Run the selected entrypoint with `rules resolve release --format json`; stop on a nonzero result without fallback to the wrapper, memory, installed templates, or remote framework prose.
4. Report workflow, profile/version, customization, wrapper and ordered rule identities, conflicts, and `conflict_resolution` coverage. Empty `conflicts` is unassured when coverage is absent or unavailable.
5. Read the returned rule documents in order before using session/runtime behavior. Stop on unresolved conflicts or when selected rules require unavailable conflict coverage.
6. Use the installed distribution runtime adapter only when exposed; otherwise return `persistence: unavailable` and obey the resolved stop behavior.

## Stop and hand off

Prepare or verify only already-authorized actions. Route any authorized write through the resolved artifact owner and maintenance disposition; never edit an emitted atomic artifact. Return diagnostics, prepared/verified state, and available session identity. Publication requires separate explicit authority; stop on any mismatch, missing gate, collision, ambiguity, or new authority, and never claim absent automation completed it.
