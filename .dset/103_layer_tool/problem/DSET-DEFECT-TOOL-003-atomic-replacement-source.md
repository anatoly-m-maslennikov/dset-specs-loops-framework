+++
artifact_id = "DSET-ATOMIC-RECORD-045"
semantic_id = "DSET-DEFECT-TOOL-003"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
authority = "repository:self-host-review"
claim = "The relation validator rejects replacement_of from immutable QA atoms even though replacement is defined for every atomic successor."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The first QA successor authored under the typed-relation contract exposed a source restriction narrower than the governing definition."

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
