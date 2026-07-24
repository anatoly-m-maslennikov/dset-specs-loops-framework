+++
artifact_id = "DSET-ATOMIC-RECORD-271"
semantic_id = "DSET-REQUIREMENT-META-002"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET keeps deterministic Tests and qualitative, probabilistic, statistical, or model-judged Evaluations in separate plans, implementations, and observation streams."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Automation does not erase the semantic difference between an exact assertion and a judgment against criteria or a rubric."

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-001"
+++

# Requirement — Tests and Evaluations remain distinct

Behavior with one exact expected result belongs to deterministic Test planning.
Behavior with multiple acceptable results judged by criteria belongs to
Evaluation planning. Their execution results remain distinct Observations.
