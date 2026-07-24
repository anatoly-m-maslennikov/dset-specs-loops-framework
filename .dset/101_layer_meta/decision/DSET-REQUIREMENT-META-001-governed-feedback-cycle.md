+++
artifact_id = "DSET-ATOMIC-RECORD-270"
semantic_id = "DSET-REQUIREMENT-META-001"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET uses one six-role feedback cycle: Inquiry, Definition, Rationale, Method, Implementation, and Observation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "One role cycle keeps desired state, reasoning, realization, and observed feedback distinct without turning workflow position into artifact identity."

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Governed feedback cycle

Test plans, evaluation plans, and implementation plans are Methods. Code and
generated operative outputs are Implementations. Test and evaluation results
are Observations. Each governed artifact has one primary content role while
relations connect it to other roles.
