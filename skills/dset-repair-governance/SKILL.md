---
name: dset-repair-governance
description: Diagnose an existing but invalid repository-local DSET registry without resolving substantive rules from it. Use when DSET root discovery succeeds but schema, ownership, path, digest, applicability, or conflict validation fails; return stable diagnostics and a bounded repair handoff, then stop before any write.
---

# DSET Repair Governance

This is the diagnostic pre-resolution exception. Invalid local governance never falls back to installed templates, memory, or remote framework prose.

## Diagnose

1. Walk upward from the target and identify the candidate schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop on no root or competing roots.
2. Select exactly one available CLI entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module. Stop if neither exists. Never retry the alternate after a nonzero result.
3. Run the selected entrypoint with `rules check --root ROOT --format json`. Do not run `rules resolve` against governance that failed validation.
4. Report each stable schema, ownership, path, digest, applicability, and conflict diagnostic with its local file identity and proposed repair owner.
5. Preserve the invalid repository as evidence. Do not copy template content, select project policy, or mutate the registry under this invocation.

## Stop

Return diagnostics, proposed local paths, available session identity, and a separately authorizable repair handoff. Stop before any write or governed project workflow.
