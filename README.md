# DSET Loops Framework

**A framework for production vibecoding.**

DSET expands to **Domain–Spec–Eval–Test**.

The framework treats natural language as a high-leverage programming interface while keeping durable software grounded in explicit domain models, accepted behavioral specifications, deterministic tests, qualitative or probabilistic evals, implementation plans, and machine-verifiable gates.

## Core loop

```text
Domain → Spec + Test Plan + Eval Plan → Implement → Test + Evaluate → Review → Reconcile Spec → Next Loop
```

- **Domain** defines entities, language, states, invariants, and boundaries.
- **Spec** records accepted behavioral truth and change scope.
- **Evals** assess probabilistic, qualitative, or LLM-mediated behavior.
- **Tests** prove deterministic behavior.
- **Loops** deliver small vertical slices, use fresh evidence, and reconcile accepted results into current truth.

## Repository contents

- [`methodology/00_Tool Development Playbook.md`](methodology/00_Tool%20Development%20Playbook.md) — pipeline and document map.
- [`methodology/01_Spec Authoring Patterns — Service Spec Conventions.md`](methodology/01_Spec%20Authoring%20Patterns%20%E2%80%94%20Service%20Spec%20Conventions.md) — domain and specification conventions.
- [`methodology/02_Test and Eval Plan Patterns — Proof Artifact Conventions.md`](methodology/02_Test%20and%20Eval%20Plan%20Patterns%20%E2%80%94%20Proof%20Artifact%20Conventions.md) — separate deterministic test-plan and probabilistic/qualitative eval-plan conventions.
- [`methodology/03_Implementation Plan Patterns — Service Build Conventions.md`](methodology/03_Implementation%20Plan%20Patterns%20%E2%80%94%20Service%20Build%20Conventions.md) — implementation and rollout planning.
- [`methodology/04_General Build Rules — Tool Code Conventions.md`](methodology/04_General%20Build%20Rules%20%E2%80%94%20Tool%20Code%20Conventions.md) — general code and runtime rules.
- [`methodology/05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md`](methodology/05_Layered%20Build%20Standard%20%E2%80%94%20DDD%2C%20TDD%2C%20Small%20Functions%2C%20Typed%20Gates.md) — six language-neutral gate categories plus applied language profiles; Python v1 is active and JavaScript/TypeScript is pending evidence.
- [`methodology/06_External Grounding — LLM Power-User Practice.md`](methodology/06_External%20Grounding%20%E2%80%94%20LLM%20Power-User%20Practice.md) — provenance and external grounding.
- [`methodology/TODO — Operationalize OpenSpec and Composable Engineering Skills.md`](methodology/TODO%20%E2%80%94%20Operationalize%20OpenSpec%20and%20Composable%20Engineering%20Skills.md) — implementation roadmap for DSET-owned change packages informed by OpenSpec and selected Matt Pocock workflow patterns.
- [`dset/README.md`](dset/README.md) — this repository's accepted project truth, active changes, archive lifecycle, templates, and schemas.

## Source-of-truth model

This public repository is the canonical source for DSET Loops and every released framework-owned methodology document, schema, template, validator, utility, skill, fixture, and migration guide. Installed or workspace-local copies are distributions of this repository, not independent editable sources.

Each project that adopts DSET owns its project truth separately under its own `dset/` root. In an adopting project, `dset/specs/` contains accepted current truth and `dset/changes/` contains bounded work in progress. Framework truth never replaces project truth, and project artifacts do not become framework rules unless they are deliberately contributed here.

## Status

The methodology is published and this repository now dogfoods the project contract under `dset/`. Reusable schemas, templates, validators, utilities, skills, fixtures, and migration guidance are still being operationalized through the TODO. The [bootstrap archive candidate](dset/changes/archive/2026-07-14-bootstrap-dset-project-structure/proposal.md) has passed its independent baseline eval and reconciled current truth; it remains incomplete until draft PR [anatoly-m-maslennikov/dset-loops-framework#2](https://github.com/anatoly-m-maslennikov/dset-loops-framework/pull/2) confirms the candidate head, fresh archive-layout evals pass, and final evidence is recorded.
