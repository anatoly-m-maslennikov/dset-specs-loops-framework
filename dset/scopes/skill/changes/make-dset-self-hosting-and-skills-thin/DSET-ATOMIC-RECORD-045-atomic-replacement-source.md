+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-045"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-TOOL-003"
status = "accepted"
priority = "high"
authority = "repository:self-host-review"
claim = "The relation validator rejects replacement_of from immutable QA atoms even though replacement is defined for every atomic successor."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The first QA successor authored under the typed-relation contract exposed a source restriction narrower than the governing definition."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-013"
+++

# Defect — Atomic replacement rejects QA successors

`replacement_of` is defined as complete replacement by a new immutable atomic
artifact, but source validation currently permits only Decision atoms. A Test
or Evaluation therefore cannot replace its earlier definition even with a
matching append-only absorption event.

## Completion condition

Every semantic atom may originate `replacement_of`; non-atomic documents
remain invalid; matching absorption, cycle, and structural-exclusivity gates
remain unchanged.

## Rationale

Replacement is a lifecycle relation, not an authority grant. Restricting it to
Decisions prevents immutable QA correction and contradicts the canonical
relation definition.
