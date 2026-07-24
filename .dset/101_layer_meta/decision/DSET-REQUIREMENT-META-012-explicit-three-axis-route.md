+++
artifact_id = "DSET-ATOMIC-RECORD-281"
semantic_id = "DSET-REQUIREMENT-META-012"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every governed artifact explicitly declares one revision_mode, one content_role, and one governance_locus; other metadata remains outside this route."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Independent explicit axes prevent filenames, folders, workflow position, authority, or lifecycle from silently reclassifying an artifact."

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Explicit three-axis route

Routing values are declared metadata. Authority, provenance, priority,
lifecycle state, applicability, and scope path remain independent.
