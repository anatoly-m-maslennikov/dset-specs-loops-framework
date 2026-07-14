# Repository governance

## Purpose

Route governed agent workflows to the repository-local documents that own their selected rules.

## Boundaries

This hub owns navigation only. `governance.yaml` owns machine-readable resolution metadata, and each linked document owns its registered normative rule IDs. Source templates are provenance after materialization, not live rule authorities.

## Start here

- [Architecture and bootstrap](architecture.md)
- [Build rules](build-rules.md)
- [Domain and specification authoring](domain-spec-authoring.md)
- [Deterministic test planning](test-planning.md)
- [Qualitative and probabilistic eval planning](eval-planning.md)
- [Diagnosis](diagnosis.md)
- [Prototyping](prototyping.md)
- [Supportability](supportability.md)
- [Artifact maintenance](artifact-maintenance.md)
- [Lifecycle orchestration](lifecycle-orchestration.md)
- [Skill-run records](skill-runs.md)
- [Delegation budgets](delegation-budget.md)
- [Release transaction](release.md)
- [Problem, opportunity, and question intake](work-items.md)

Use `dset rules check` to validate ownership and `dset rules resolve <workflow-id>` to obtain the ordered rule set. Use `dset rules refresh` only after an intentional local edit, and review `dset rules diff --source <framework-root>` before adopting later framework changes.
