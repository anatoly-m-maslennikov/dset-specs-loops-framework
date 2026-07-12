# DSET Loops Framework

**A framework for production vibecoding.**

DSET expands to **Domain–Spec–Eval–Test**.

The framework treats natural language as a high-leverage programming interface while keeping durable software grounded in explicit domain models, accepted behavioral specifications, deterministic tests, qualitative or probabilistic evals, implementation plans, and machine-verifiable gates.

## Core loop

```text
Domain → Spec + Eval/Test Plan → Implement → Eval/Test → Review → Reconcile Spec → Next Loop
```

- **Domain** defines entities, language, states, invariants, and boundaries.
- **Spec** records accepted behavioral truth and change scope.
- **Evals** assess probabilistic, qualitative, or LLM-mediated behavior.
- **Tests** prove deterministic behavior.
- **Loops** deliver small vertical slices, use fresh evidence, and reconcile accepted results into current truth.

## Repository contents

- [`methodology/00_Tool Development Playbook.md`](methodology/00_Tool%20Development%20Playbook.md) — pipeline and document map.
- [`methodology/01_Spec Authoring Patterns — Service Spec Conventions.md`](methodology/01_Spec%20Authoring%20Patterns%20%E2%80%94%20Service%20Spec%20Conventions.md) — domain and specification conventions.
- [`methodology/02_Eval and Test Plan Patterns — Test Plan Authoring Conventions.md`](methodology/02_Eval%20and%20Test%20Plan%20Patterns%20%E2%80%94%20Test%20Plan%20Authoring%20Conventions.md) — proof designed before code.
- [`methodology/03_Implementation Plan Patterns — Service Build Conventions.md`](methodology/03_Implementation%20Plan%20Patterns%20%E2%80%94%20Service%20Build%20Conventions.md) — implementation and rollout planning.
- [`methodology/04_General Build Rules — Tool Code Conventions.md`](methodology/04_General%20Build%20Rules%20%E2%80%94%20Tool%20Code%20Conventions.md) — general code and runtime rules.
- [`methodology/05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md`](methodology/05_Layered%20Build%20Standard%20%E2%80%94%20DDD%2C%20TDD%2C%20Small%20Functions%2C%20Typed%20Gates.md) — executable architecture, TDD, typing, and conformance gates.
- [`methodology/06_External Grounding — LLM Power-User Practice.md`](methodology/06_External%20Grounding%20%E2%80%94%20LLM%20Power-User%20Practice.md) — provenance and external grounding.
- [`methodology/TODO — Operationalize OpenSpec and Composable Engineering Skills.md`](methodology/TODO%20%E2%80%94%20Operationalize%20OpenSpec%20and%20Composable%20Engineering%20Skills.md) — adoption roadmap for OpenSpec-derived change packages and selected Matt Pocock workflow patterns.

## Status

This is the initial repository extraction of the methodology. The TODO includes the explicit source-of-truth, migration, pilot, validation, and rollout decisions required before the repository becomes the canonical distribution.
