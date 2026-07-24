---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-004
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-013"
  - type: resolution_of
    targets:
      - "DSET-DEFECT-TOOL-002"
      - "DSET-DEFECT-TOOL-003"
---

# Implementation Decision — Use the canonical artifact relations

DSET uses exactly these general forward artifact relations:

| Relation | Exclusive meaning |
|---|---|
| `child_of` | Narrows, decomposes, or specializes an active parent claim while both remain active |
| `analysis_of` | Interprets named inputs without becoming their authority or evidence |
| `projection_of` | Binds a maintained view to one registered atomic type and exact scope through its latest included identity |
| `implementation_of` | Connects code, configuration, documentation, migration, or a commit to the authority it realizes |
| `check_of` | Connects a Test Plan or Evaluation Plan to the claim it checks |
| `evidence_for` | Connects a bounded observation to the check, result, or Verification it supports |
| `resolution_of` | Closes a Question or Problem other than a Conflict |
| `solution_for` | Supplies the accepted solution that closes a Conflict |
| `override_of` | Replaces inherited authority only inside a declared narrower scope |
| `replacement_of` | Completely replaces an older immutable atom |
| `recurrence_of` | Links a new Question or Problem to an archived predecessor of the same registered type |
| `relates_to` | Records an association only when no precise relation applies and supplies no authority or coverage |

Every authored edge is stored on its source and names one or more stable target
identities. One source-target pair has one primary relation. Reverse edges,
including `parent_to`, are derived and never authored.

`child_of`, `override_of`, `replacement_of`, and `recurrence_of` are mutually
exclusive for one pair. `solution_for` is reserved for Conflict; other closure
uses `resolution_of`. `relates_to` has no authority, assurance, dependency,
precedence, lifecycle, or coverage semantics.

Rule-registry `depends_on` and `precedence_over` fields remain separate
constitutional controls and are not general artifact relations.

## Primary claim

DSET uses twelve precise forward relations with derived inverses, exclusive
closure semantics, and type/scope `projection_of` frontiers.

## Rationale

The earlier ten-relation decision predated archive recurrence and explicit
Conflict-solution semantics. Keeping those meanings implicit would overload
resolution and historical linkage, while a small bounded extension preserves
the anti-explosion rule and makes each edge reviewable.
