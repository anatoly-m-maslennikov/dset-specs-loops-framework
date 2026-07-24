---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-121
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-118"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-069"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-070"
      - "DSET-REQUIREMENT-GOV-070"
      - "DSET-REQUIREMENT-GOV-102"
      - "DSET-PROBLEM-GOV-009"
---

# Requirement — Register base role-locus Types and QA Cases

The GOV artifact catalog uses these canonical semantic names for the base
Content-role and Governance-locus surface:

| Content role | Internal | External | Relation |
|---|---|---|---|
| Problem | Problem | External Problem | Conflict |
| Analysis | Analysis Report | External Analysis Report | Conflict Analysis |
| Definition | Requirement | Constraint | Contract |
| Method | Technical Decision | Implementation Methodology | Integration Decision |
| Assurance | QA Case | Assurance Standard | Review Protocol |
| Implementation | Git Commit | External Git Commit | Pull Request |
| Observation | Evidence Record | External Evidence Record | Verification Record |

Each name resolves through exactly one full route consisting of Revision mode,
Content role, and Governance locus. The matrix fixes 21 understandable base
names; it does not claim to fill the other 42 Revision-mode variants required
by the total route catalog.

Authority, provenance, priority, lifecycle, and `scope_path` remain separate
metadata.

## QA Case boundary

`qa_case` is the atomic, internal Assurance Type. It always has exactly one
direct subtype:

- `test_case`, displayed as **Test Case**, defines one deterministic check with
  exact conditions and a reproducible pass/fail disposition; or
- `eval_case`, displayed as **Eval Case**, defines one qualitative,
  probabilistic, statistical, or model-judged assessment with explicit
  criteria and a disposition rule.

A naked QA Case is invalid. Test Plans and Eval Plans remain maintained
collections of applicable QA Cases; a plan, case, executable check, and
resulting Observation are distinct artifacts.

## Method and Implementation boundaries

A Technical Decision selects an internal way to realize accepted Definitions.
An Integration Decision selects how explicit components, features, layers,
services, or repositories realize relational obligations. A Contract defines
those obligations and therefore remains a relational Definition.

A Pull Request is a maintained relational Implementation carrier connecting
declared source and target endpoints. It is not a Method. Its patch,
description, reviews, checks, and comments retain their own meanings. Material
rationale in a Pull Request is governed separately. A successful merge yields
a separate Git Commit or External Git Commit identity.

## Relational boundary

Conflict, Conflict Analysis, Contract, Integration Decision, Review Protocol,
Pull Request, and Verification Record declare explicit endpoints appropriate
to their meaning.

## Primary claim

GOV assigns 21 canonical base Type names to the seven-role and three-locus
surface, including QA Case with mandatory Test Case or Eval Case subtype,
without claiming that the total 63-route catalog is complete.

## Rationale

The predecessor correctly fixed the base names and boundaries but depended on
an archived META atom and implied a complete catalog. This successor binds the
same names to current META authority and makes the remaining route gap
explicit.
