---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-002"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-META-001"
---

# Requirement — Tests and Evaluations remain distinct

Behavior with one exact expected result belongs to deterministic Test planning.
Behavior with multiple acceptable results judged by criteria belongs to
Evaluation planning. Their execution results remain distinct Observations.

## Primary claim

DSET keeps deterministic Tests and qualitative, probabilistic, statistical, or model-judged Evaluations in separate plans, implementations, and observation streams.

## Rationale

Automation does not erase the semantic difference between an exact assertion and a judgment against criteria or a rubric.
