---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-043
type: qa
subtype: evaluation
semantic_id: DSET-EVALUATION-SKILL-012
status: accepted
priority: medium
authority: "operator:anatoly-m-maslennikov"
claim: "Operators consistently understand lazy as self-preparing and strict as implementation-only without learning internal skill choreography."
scope:
  kind: project
  id: dset-specs-loops-framework
promotion:
  parent_scope: null
relations:
  - type: check_of
    target: DSET-REQUIREMENT-SKILL-012
  - type: replacement_of
    target: DSET-EVAL-SKILL-010
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Evaluation — Judge implementation-mode clarity

Given partially prepared and fully prepared implementation requests,
independent operators must predict whether DSET will create missing artifacts
or implement only, select the intended project setting, and understand every
stop without knowing the internal specialist-skill graph.

No reviewer may interpret strict mode as weaker authority, provenance,
authorization, Verification, or release rules. No reviewer may interpret lazy
mode as permission to invent acceptance or silently resolve ambiguity.

This Evaluation completely replaces `DSET-EVAL-SKILL-010`. Execution and
evidence are separate.
