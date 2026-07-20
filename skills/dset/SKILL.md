---
name: dset
description: Reach a general, multi-stage, or uncertain DSET outcome through repository-local governance. Use when the operator wants progress without choosing prerequisite skills manually; prefer a direct skill only when its desired outcome is already clear.
---

# DSET

This is the thin primary wrapper for `lifecycle-orchestration`; resolved repository-local documents own substantive behavior.

## Resolve

1. Walk upward from the target for exactly one schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop on competing authorities.
2. Select exactly one available resolver entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module; stop if neither exists. Never retry the alternate after a nonzero result.
3. With no root, use only an exposed distribution bootstrap transaction; otherwise return `initialize` as unavailable with an installation/materialization handoff and stop. With an invalid root, run only `rules check`, report diagnostics, and stop.
4. With a valid root, run the selected entrypoint with `rules resolve lifecycle-orchestration --format json`; stop on a nonzero result without fallback to the wrapper, memory, installed templates, or remote framework prose.
5. Report workflow, profile/version, customization, wrapper and ordered rule identities, conflicts, and `conflict_resolution` coverage. Empty `conflicts` is unassured when coverage is absent or unavailable.
6. Read the returned rule documents in order before using session/runtime behavior. Stop on unresolved conflicts or when selected rules require unavailable conflict coverage.

## Route and hand off

After reading the rules, use the installed distribution runtime adapter only when exposed; otherwise return `persistence: unavailable` and obey the resolved stop behavior. Follow the finite entry-criteria closure returned by local governance, re-read authority after each transition, and require observable progress. Preserve one session and route writes through resolved owners. Never edit an emitted atom; stop on repeated state, cycles, no progress, ambiguity, failure, an exit criterion, or newly required authority.
