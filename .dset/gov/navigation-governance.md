# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.toml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- [Architecture and bootstrap](specification-architecture.md)
- [Build rules](../tool/specification-build-rules.md)
- [Domain and specification authoring](../meta/procedure-domain-spec-authoring.md)
- [Deterministic test planning](../meta/procedure-test-planning.md)
- [Qualitative and probabilistic eval planning](../meta/procedure-evaluation-planning.md)
- [Diagnosis](../skill/procedure-diagnosis.md)
- [Prototyping](../skill/procedure-prototyping.md)
- [Supportability](../ops/specification-supportability.md)
- [Artifact maintenance](specification-artifact-maintenance.md)
- [Artifact classification](specification-artifact-classification.md)
- [Lifecycle orchestration](../skill/procedure-lifecycle-orchestration.md)
- [Skill-run records](../skill/procedure-skill-runs.md)
- [Delegation budgets](../skill/procedure-delegation-budget.md)
- [Release transaction](../ops/procedure-release.md)
- [Problem, opportunity, and question intake](specification-work-items.md)

Use `dset rules check` to validate ownership, dependency order, and declared
precedence. Use `dset rules resolve <workflow-id>` to obtain the
dependency-ordered rule set plus precedence metadata. Use `dset rules refresh`
only after an intentional local edit, and review
`dset rules diff --source <framework-root>` before adopting later framework
changes.
