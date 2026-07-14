# Methodology hub

## Purpose

This is the helicopter-view entry point for the DSET Spec Loops methodology. It routes readers through the delivery stages and cross-cutting standards without making the repository root README an exhaustive methodology index.

## Boundaries

This area owns the reusable DSET delivery method. In current schema 1.2
projects, project-specific accepted truth belongs under
`dset/scopes/<layer>/specs/` and active implementation evidence belongs under
the Change's `dset/scopes/<primary-layer>/changes/` root. Central `dset/specs/`
and `dset/changes/` paths describe legacy schema 1.0/1.1 projects. Artifact
architecture and authoring rules belong in the [documentation
architecture](../documentation/README.md).

## Start here

1. [00 — Tool Development Playbook](00_Tool%20Development%20Playbook.md) — pipeline, stage routing, and document responsibilities.
2. [01 — Spec Authoring Patterns](01_Spec%20Authoring%20Patterns%20%E2%80%94%20Service%20Spec%20Conventions.md) — domain and behavioral specification.
3. [02 — Test and Eval Plan Patterns](02_Test%20and%20Eval%20Plan%20Patterns%20%E2%80%94%20Proof%20Artifact%20Conventions.md) — deterministic tests and qualitative/probabilistic evals as separate proof contracts.
4. [03 — Implementation Plan Patterns](03_Implementation%20Plan%20Patterns%20%E2%80%94%20Service%20Build%20Conventions.md) — dependency-ordered build and rollout planning.
5. [04 — General Build Rules](04_General%20Build%20Rules%20%E2%80%94%20Tool%20Code%20Conventions.md) — runtime risk, durability topology, safety, and supportability patterns.
6. [05 — Layered Build Standard](05_Layered%20Build%20Standard%20%E2%80%94%20DDD%2C%20TDD%2C%20Small%20Functions%2C%20Typed%20Gates.md) — language-neutral code gates and applied implementation-language profiles.
7. [06 — External Grounding](06_External%20Grounding%20%E2%80%94%20LLM%20Power-User%20Practice.md) — external provenance and candidate practices.

## Cross-cutting navigation

- [Documentation architecture](../documentation/README.md) — artifact profiles, types, authoring, hubs, and maintenance.
- [DSET 0.3 roadmap](TODO%20%E2%80%94%20DSET%200.3%20Self-Hosting%20and%20Repository-Governed%20Skills.md) — self-hosting, repository-local governing rules, thin skills, a TypeScript profile, and the Your Harness pilot.
- [Superseded operationalization roadmap](TODO%20%E2%80%94%20Operationalize%20OpenSpec%20and%20Composable%20Engineering%20Skills.md) — historical pointer only; current work lives in the DSET 0.3 roadmap and project intake.
- [Accepted methodology package fragments](../dset/README.md#start-here) — machine-traceable current project truth and proof contracts distributed across the five layer owners.

The numbered documents remain stable responsibility owners. The documentation architecture is cross-cutting and is not pipeline stage 7.
