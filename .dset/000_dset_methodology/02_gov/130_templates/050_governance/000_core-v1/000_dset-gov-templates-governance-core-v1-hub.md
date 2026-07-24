---
artifact_type: navigation
artifact_subtype: hub
scope_path: []
priority: medium
---

# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.toml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- `architecture.md`
- `build-rules.md`
- `domain-spec-authoring.md`
- `test-planning.md`
- `eval-planning.md`
- `diagnosis.md`
- `prototyping.md`
- `supportability.md`
- `artifact-maintenance.md`
- `artifact-classification.md`
- `lifecycle-orchestration.md`
- `skill-runs.md`
- `delegation-budget.md`
- `release.md`
- `work-items.md`

Use `dset rules check` to validate ownership, dependency order, and declared
precedence. Use `dset rules resolve <workflow-id>` to obtain the
dependency-ordered rule set plus precedence metadata. Use `dset rules refresh`
only after an intentional local edit, and review
`dset rules diff --source <framework-root>` before adopting later framework
changes.
