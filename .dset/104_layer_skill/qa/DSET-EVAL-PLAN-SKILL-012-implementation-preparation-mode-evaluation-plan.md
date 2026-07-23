+++
artifact_id = "DSET-ATOMIC-RECORD-043"
semantic_id = "DSET-EVAL-PLAN-SKILL-012"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "Operators consistently understand lazy as self-preparing and strict as implementation-only without learning internal skill choreography."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-012"

[[relations]]
type = "replacement_of"
target = "DSET-EVAL-PLAN-SKILL-010"
+++

# Evaluation Plan — Judge implementation-mode clarity

Given partially prepared and fully prepared implementation requests,
independent operators must predict whether DSET will create missing artifacts
or implement only, select the intended project setting, and understand every
stop without knowing the internal specialist-skill graph.

No reviewer may interpret strict mode as weaker authority, provenance,
authorization, Verification, or release rules. No reviewer may interpret lazy
mode as permission to invent acceptance or silently resolve ambiguity.

This Evaluation completely replaces `DSET-EVAL-PLAN-SKILL-010`. Execution and
evidence are separate.
