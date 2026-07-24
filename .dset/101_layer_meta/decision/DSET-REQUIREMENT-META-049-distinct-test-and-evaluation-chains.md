---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-049
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-002"
      - "DSET-REQUIREMENT-META-007"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-028"
      - "DSET-REQUIREMENT-META-047"
      - "DSET-REQUIREMENT-META-048"
---

# Requirement — Keep Test and Evaluation chains distinct

Tests and Evaluations are separate assurance chains.

A Test Plan defines one deterministic check with controlled conditions and an
exact expected disposition. An Evaluation Plan defines one qualitative,
probabilistic, statistical, rubric-based, or model-judged assessment with
explicit criteria and an interpretation rule.

Each chain keeps its plan, executable implementation, factual Observation,
evidence, and Verification judgment distinguishable. A shared runner or report
does not merge their meanings or coverage.

Exact resolver, ownership, path, identity, wrapper, and recursion behavior uses
Test proof. Interpretation, rule-following, navigation, diagnostic usefulness,
and variable output quality uses Evaluation proof.

## Rationale

Combining the former distinction and proof-routing requirements gives one
complete boundary from assurance definition through factual result without
collapsing deterministic correctness into judgment.
