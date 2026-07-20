---
name: dset-init
description: Initialize repository-local DSET governance through an exact dry-run-first bootstrap transaction. Use when a target repository or monorepo Work Area has no valid DSET root and the operator wants to preview or authorize local manifest, registry, governing-document, and skill materialization; stop after preview or validation and never continue into project work.
---

# DSET Init

This is the bounded rootless initialization wrapper. It owns no project rules and cannot replace the new repository-local authority it creates.

## Preview and initialize

1. Invoke the installed shared runtime exactly once with `dset skills context --skill dset-init --target TARGET --objective OBJECTIVE`. Require `status: initialization-required`; stop if a project already owns the target, roots compete, the launcher is unavailable, or the command fails.
2. Collect explicit target, project key, project ID, name, license, profile, source, repository identity when known, package, and any Work Areas. Do not infer a different source or profile after preview.
3. Run `dset init TARGET --project-key KEY --project-id ID --name NAME --license LICENSE --profile PROFILE --source SOURCE --format json` without `--execute`. Report source identity, every planned path, refusal conditions, and that no write occurred.
4. Without explicit write authorization, return the exact preview and stop. With authorization, run the same invocation once with `--execute`; never overwrite or merge an existing destination.
5. Report materialized paths and validation result. Stop after any failure or successful validation; the next invocation must resolve the new local governance.

## Stop

Return initialization identity, preview or execution status, diagnostics, and the next `$dset` handoff. Never make a product Decision, create implementation work, or continue into another lifecycle mode.
