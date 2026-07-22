# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.toml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- [Architecture and bootstrap](specification-architecture.md)
- [Build rules](../03_layer_tool/specification-build-rules.md)
- [Domain and specification authoring](../01_layer_meta/procedure-domain-spec-authoring.md)
- [Deterministic test planning](../01_layer_meta/procedure-test-planning.md)
- [Qualitative and probabilistic eval planning](../01_layer_meta/procedure-evaluation-planning.md)
- [Diagnosis](../04_layer_skill/procedure-diagnosis.md)
- [Prototyping](../04_layer_skill/procedure-prototyping.md)
- [Supportability](../05_layer_ops/specification-supportability.md)
- [Artifact maintenance](specification-artifact-maintenance.md)
- [Artifact classification](specification-artifact-classification.md)
- [Lifecycle orchestration](../04_layer_skill/procedure-lifecycle-orchestration.md)
- [Skill-run records](../04_layer_skill/procedure-skill-runs.md)
- [Delegation budgets](../04_layer_skill/procedure-delegation-budget.md)
- [Release transaction](../05_layer_ops/procedure-release.md)
- [Problem, opportunity, and question intake](specification-work-items.md)

Use `dset rules check` to validate ownership, dependency order, and declared
precedence. Use `dset rules resolve <workflow-id>` to obtain the
dependency-ordered rule set plus precedence metadata. Use `dset rules refresh`
only after an intentional local edit, and review
`dset rules diff --source <framework-root>` before adopting later framework
changes.
