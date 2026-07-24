+++
artifact_id = "DSET-ATOMIC-RECORD-279"
semantic_id = "DSET-REQUIREMENT-META-010"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "An intended measurable state belongs in a Definition or assessment Method, while an observed result is an Observation; Outcome is not a routing axis or mandatory registered name."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Separating intended and observed state prevents shipped output from being mistaken for evidence that the intended effect occurred."

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-001"
+++

# Requirement — Outcome framing

Required effects belong to Definitions. Assessment criteria belong to Methods.
Measured results belong to Observations.
