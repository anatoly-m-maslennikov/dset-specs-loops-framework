---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-118
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-061"
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-117"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-GOV-070"
      - "DSET-REQUIREMENT-GOV-102"
---

# Requirement — Register canonical role-locus types and QA Cases

The GOV artifact catalog must register the following canonical semantic names
for the accepted Content-role and Governance-locus model:

| Content role | Internal | External | Relation |
|---|---|---|---|
| Problem | Problem | External Problem | Conflict |
| Analysis | Analysis Report | External Analysis Report | Conflict Analysis |
| Definition | Requirement | Constraint | Contract |
| Method | Technical Decision | Implementation Methodology | Integration Decision |
| Assurance | QA Case | Assurance Standard | Review Protocol |
| Implementation | Git Commit | External Git Commit | Pull Request |
| Observation | Evidence Record | External Evidence Record | Verification Record |

Each registered name resolves through exactly one full route consisting of
Revision mode, Content role, and Governance locus. The route does not infer
authority, provenance, priority, lifecycle state, or `scope_path`.

## QA Case boundary

`qa_case` is the atomic, internal Assurance type. It always has exactly one
direct subtype:

- `test_case`, displayed as **Test Case**, defines one deterministic check with
  exact conditions and a reproducible pass/fail disposition; or
- `eval_case`, displayed as **Eval Case**, defines one qualitative,
  probabilistic, statistical, or model-judged assessment with explicit
  criteria and a disposition rule.

A naked QA Case is invalid. Subtype-derived identities use `TEST-CASE` and
`EVAL-CASE`. Test Plans and Eval Plans remain maintained collections of
applicable QA Cases; a plan, case, executable check, and resulting observation
are distinct artifacts.

## Method and implementation boundaries

A Technical Decision selects an internal way to realize accepted Definitions.
An Integration Decision selects how explicit components, features, layers,
services, or repositories realize their relational obligations. A Contract
defines those obligations and therefore remains a relational Definition.

A Pull Request is a maintained relational Implementation carrier connecting
declared source and target endpoints. It is not a Method. Its patch,
description, reviews, checks, and comments retain their own meanings. Material
rationale in a Pull Request must be governed separately rather than becoming
canonical merely because it appears in the carrier. A successful merge yields
a separate Git Commit or External Git Commit identity.

## Relational boundary

Conflict, Conflict Analysis, Contract, Integration Decision, Review Protocol,
Pull Request, and Verification Record declare explicit endpoints appropriate
to their meaning. Relation artifacts never derive endpoint ownership from
their folder or filename.

## Rationale

The names distinguish desired behavior, selected technical realization,
assurance definitions, implementation carriers, and observations without
classifying containers by incidental text. Making Test Case and Eval Case
subtypes of QA Case also preserves one atomic Assurance type for the route.
