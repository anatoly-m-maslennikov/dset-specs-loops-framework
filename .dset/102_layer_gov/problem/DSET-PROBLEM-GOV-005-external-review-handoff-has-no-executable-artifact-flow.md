+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-151"
type = "problem"
subtype = "none"
semantic_id = "DSET-PROBLEM-GOV-005"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET defines independent review as transactional evidence, but it lacks a review-packet template, report envelope/schema, stable finding IDs, and an import/reconciliation flow that routes Codex, Claude, or human findings without silently authorizing fixes."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]
+++

# Problem — External review handoff has no executable artifact flow

DSET defines independent review as transactional evidence, but it lacks a review-packet template, report envelope/schema, stable finding IDs, and an import/reconciliation flow that routes Codex, Claude, or human findings without silently authorizing fixes.

## Migrated context

- Original intake status: `open`
- Original owner Change: `DSET-CHANGE-SKILL-001`

This one-claim carrier replaces the former aggregate intake row. Current
status is derived from atomic lifecycle events.
