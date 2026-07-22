+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-112"
type = "qa"
subtype = "evaluation"
semantic_id = "DSET-EVALUATION-GOV-033"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "A cold reviewer can infer the intended architectural layer order from the directory names without mistaking numeric prefixes for semantic identity."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-044"
+++

# Evaluation — Interpret numbered layer order

Given only the repository tree, layer hubs, and one artifact from each layer,
independent reviewers should identify the order META → GOV → TOOL → SKILL → OPS,
route each artifact to its owning layer, and explain that `layer_1_` through
`layer_5_` order filesystem presentation while `META`, `GOV`, `TOOL`, `SKILL`,
and `OPS` remain the stable semantic names.

Record any confusion between layer order, authority precedence, feature
hierarchy, dependency order, or artifact identity. This Evaluation atom is
immutable; later correction requires a successor Evaluation and append-only
lifecycle event.
