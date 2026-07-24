+++
artifact_id = "DSET-ATOMIC-RECORD-056"
semantic_id = "DSET-DEFECT-TOOL-005"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:tool"]
status = "accepted"
priority = "high"
authority = "repository:fpf-review"
claim = "Project-health coverage can false-pass when an artifact ID is merely mentioned in prose instead of connected by a validated relation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Coverage is a claim-bound assurance relation, not a text-search result."
promotion = {}

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-024"
+++

# Defect — Health coverage trusts loose mentions

The health generator currently counts ID substrings and same-line
co-occurrence as compilation, check, and evidence coverage. A pending or
historical prose mention can therefore make an uncovered claim appear covered.

## Completion condition

Compilation, QA, implementation, and evidence coverage derive from validated
typed relations plus current lifecycle state. Prose links remain navigation
only, and false-positive fixtures stay uncovered.
