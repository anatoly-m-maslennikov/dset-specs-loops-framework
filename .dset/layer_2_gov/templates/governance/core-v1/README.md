# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.toml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- [Architecture and bootstrap](architecture.md)
- [Build rules](../../../../layer_3_tool/templates/governance/core-v1/build-rules.md)
- [Domain and specification authoring](../../../../layer_1_meta/templates/governance/core-v1/domain-spec-authoring.md)
- [Deterministic test planning](../../../../layer_1_meta/templates/governance/core-v1/test-planning.md)
- [Qualitative and probabilistic eval planning](../../../../layer_1_meta/templates/governance/core-v1/eval-planning.md)
- [Diagnosis](../../../../layer_4_skill/templates/governance/core-v1/diagnosis.md)
- [Prototyping](../../../../layer_4_skill/templates/governance/core-v1/prototyping.md)
- [Supportability](../../../../layer_5_ops/templates/governance/core-v1/supportability.md)
- [Artifact maintenance](artifact-maintenance.md)
- [Artifact classification](artifact-classification.md)
- [Lifecycle orchestration](../../../../layer_4_skill/templates/governance/core-v1/lifecycle-orchestration.md)
- [Skill-run records](../../../../layer_4_skill/templates/governance/core-v1/skill-runs.md)
- [Delegation budgets](../../../../layer_4_skill/templates/governance/core-v1/delegation-budget.md)
- [Release transaction](../../../../layer_5_ops/templates/governance/core-v1/release.md)
- [Problem, opportunity, and question intake](work-items.md)

Use `dset rules check` to validate ownership, dependency order, and declared
precedence. Use `dset rules resolve <workflow-id>` to obtain the
dependency-ordered rule set plus precedence metadata. Use `dset rules refresh`
only after an intentional local edit, and review
`dset rules diff --source <framework-root>` before adopting later framework
changes.
