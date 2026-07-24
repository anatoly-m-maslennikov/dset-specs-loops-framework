---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-003
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-034"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-GOV-071"
---

# Implementation Decision — Use route-derived identity kinds

Every governed atomic artifact declares one registered `artifact_type` and at
most one direct `artifact_subtype`. The registered pair derives its semantic
route without a second parent-Type hierarchy.

Artifact IDs and filenames use the registered visible identity kind:

| Artifact type | Identity kind |
|---|---|
| `requirement` | `REQUIREMENT` |
| `constraint` | `CONSTRAINT` |
| `contract` | `CONTRACT` |
| `implementation_decision` | `IMPL` |
| `test_plan` | `TEST-PLAN` |
| `evaluation_plan` | `EVAL-PLAN` |

Other registered types use their own unambiguous configured kind. Optional
subtype-bearing names use the subtype kind only when project settings enable
that naming policy. An identity vocabulary change is one complete governed
migration; superseded aliases are not accepted after cutover.

## Primary claim

Artifact identity kinds follow the registered direct artifact type or enabled
direct subtype, not a separate Decision, Question, Problem, or QA parent
hierarchy.

## Rationale

Direct identity kinds remain understandable in file lists and resolve the same
one-to-one semantic route used by validation, without maintaining a parallel
classification system.
