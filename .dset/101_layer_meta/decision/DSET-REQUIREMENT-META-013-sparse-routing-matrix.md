+++
artifact_id = "DSET-ATOMIC-RECORD-282"
semantic_id = "DSET-REQUIREMENT-META-013"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The routing matrix is sparse: an occupied route has zero or one registered name at each enabled governance locus, and empty routes require no placeholder artifacts."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Sparse interface vocabulary avoids ontology and artifact proliferation while preserving precise routing."

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Sparse routing matrix

Internal governance is mandatory. External and relation governance are enabled
independently. Enabling a locus does not require filling every route.
