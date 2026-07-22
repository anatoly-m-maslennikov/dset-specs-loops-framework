# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.toml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- `specification-architecture.md`
- `specification-build-rules.md`
- `procedure-domain-spec-authoring.md`
- `procedure-test-planning.md`
- `procedure-evaluation-planning.md`
- `procedure-diagnosis.md`
- `procedure-prototyping.md`
- `specification-supportability.md`
- `specification-artifact-maintenance.md`
- `specification-artifact-classification.md`
- `procedure-lifecycle-orchestration.md`
- `procedure-skill-runs.md`
- `procedure-delegation-budget.md`
- `procedure-release.md`
- `specification-work-items.md`

Use `dset rules check` to validate ownership, dependency order, and declared
precedence. Use `dset rules resolve <workflow-id>` to obtain the
dependency-ordered rule set plus precedence metadata. Use `dset rules refresh`
only after an intentional local edit, and review
`dset rules diff --source <framework-root>` before adopting later framework
changes.
