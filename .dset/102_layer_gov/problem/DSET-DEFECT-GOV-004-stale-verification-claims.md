---
artifact_type: "problem"
artifact_subtype: "defect"
artifact_id: "DSET-DEFECT-GOV-004"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Defect — Verification retains invalidated pass claims

The active Verification still promotes earlier shared-runtime, entry-closure,
and artifact-gate proofs as passing after later runtime activity fired their
declared reopen conditions. The evidence files remain valid historical
observations, but their current Verification dispositions are stale.

## Rationale

This is a current governance defect because Verification is derived current
state and must change when its own evidence validity boundary is crossed.
