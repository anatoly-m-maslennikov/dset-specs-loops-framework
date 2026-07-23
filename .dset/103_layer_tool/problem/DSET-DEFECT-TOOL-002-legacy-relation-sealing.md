+++
artifact_id = "DSET-ATOMIC-RECORD-038"
semantic_id = "DSET-DEFECT-TOOL-002"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
authority = "repository:self-host-review"
claim = "The atom sealing path accepts new legacy child_of metadata even though compatibility is restricted to historical carriers."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Recursive self-application exposed an admission-path gap that ordinary validation of sealed history could not reveal."

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-013"
+++

# Defect — Legacy relation metadata can enter new atoms

The atom sealing path accepts a newly authored top-level `child_of` field.
That contradicts the active typed-relation Decision, which permits the field
only as compatibility input for already sealed historical carriers.

## Completion condition

New atoms that contain top-level `child_of` cannot be sealed, canonical
`relations` remain sealable, and existing sealed legacy atoms remain valid.

## Rationale

Compatibility readers and admission writers have different obligations. The
runtime must continue to understand historical carriers without allowing new
legacy metadata to extend the compatibility surface.
