---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-007"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-REQUIREMENT-META-002"
---

# Requirement — Separate Test and Evaluation proof

Proof category follows the claim and acceptance method. Tests and Evaluations
remain separate even when both are automated.

## Primary claim

Exact resolver, ownership, path, identity, wrapper, and recursion behavior uses deterministic Test proof; interpretation, rule-following, navigation, and diagnostic usefulness uses separate Evaluation proof.

## Rationale

Automating a judgment does not turn it into a deterministic assertion, and using an agent does not turn an exact assertion into an Evaluation.
