---
name: dset
description: Route any DSET lifecycle request to the next governed repository-local workflow. Use for initialization, decomposition, landscape or decision work, proof and implementation planning, implementation, verification, work-item triage, release readiness, completion checks, or when the operator asks what to do next.
---

# DSET

This is the thin primary wrapper for `lifecycle-orchestration`; repository-local governing documents own all substantive behavior.

## Resolve and route

1. Walk upward from the target path for schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop if both authorities exist.
2. With no root, route only to the distribution-owned bootstrap transaction specified by `DSET-RULE-LIFECYCLE`. If the installed distribution exposes no executable bootstrap, report `initialize` as unavailable with an installation/materialization handoff and stop; never invent a command or bootstrap from memory. With an invalid root, run only `dset rules check`, report diagnostics, and stop.
3. Otherwise run `dset rules resolve lifecycle-orchestration --format json` or `python -m dset_toolchain rules resolve lifecycle-orchestration --format json`; stop on a nonzero result without fallback.
4. Report the workflow ID, profile/version, customization and wrapper identities, ordered rule IDs/paths, and conflicts; then read and apply those documents in returned order.
5. Re-read the resolved authority owners, compute applicable modes, and recommend exactly one mode with evidence. An explicit operator override is valid only when the resolved rules permit it.

## Chain and hand off

Start or resume the DSET session through the resolved `DSET-RULE-SKILL-RUNS` behavior, refresh authoritative state after every transition or resumed checkpoint, and return the session ID with the handoff.

Perform at most two workflow transitions. Stop on ambiguity, failure, the selected workflow's output boundary, or before any newly required authorization; never infer permission for writes, external effects, publication, or implementation.
