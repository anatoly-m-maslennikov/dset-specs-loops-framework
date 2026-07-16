---
name: dset-init
description: Initialize repository-local DSET governance through an exact dry-run-first bootstrap transaction. Use when a target repository or monorepo Work Area has no valid DSET root and the operator wants to preview or authorize local manifest, registry, governing-document, and skill materialization; stop after preview or validation and never continue into project work.
---

# DSET Init

This is the bounded rootless initialization wrapper. It owns no project rules and cannot replace the new repository-local authority it creates.

## Preview and initialize

1. Inspect the target and its parents for exactly one schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`. If one already governs the target, return a `$dset` handoff; stop on competing authorities.
2. Select exactly one available CLI entrypoint before invocation: the `dset` executable, otherwise the active Python interpreter with the installed `dset_toolchain` module. Stop if neither exists. Never retry the alternate after a nonzero result.
3. Collect explicit target, project key, project ID, name, license, profile, source, repository identity when known, package, and any Work Areas. Do not infer a different source or profile after preview.
4. Run `init TARGET --project-key KEY --project-id ID --name NAME --license LICENSE --profile PROFILE --source SOURCE --format json` through the selected entrypoint without `--execute`. Report source identity, every planned path, refusal conditions, and that no write occurred.
5. Without explicit write authorization, return the exact preview and stop. With authorization, run the same invocation once with `--execute`; never overwrite or merge an existing destination.
6. Report materialized paths and validation result. Stop after any failure or successful validation; the next invocation must resolve the new local governance.

## Stop

Return initialization identity, preview or execution status, diagnostics, and the next `$dset` handoff. Never make a product Decision, create implementation work, or continue into another lifecycle mode.
