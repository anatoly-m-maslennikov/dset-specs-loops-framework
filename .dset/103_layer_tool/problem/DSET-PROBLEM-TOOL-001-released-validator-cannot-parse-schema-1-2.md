+++
artifact_id = "DSET-ATOMIC-RECORD-124"
semantic_id = "DSET-PROBLEM-TOOL-001"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:tool"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "The previous released validator predates layered schema 1.2, so the current fixed point uses the exact migration commit as a clearly labeled non-release transition baseline. Release assurance remains degraded until a published compatible validator checks a later candidate or an accepted compatibility proof closes the gap."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}
+++

# Problem — Released validator cannot parse schema 1.2

The previous released validator predates layered schema 1.2, so the current fixed point uses the exact migration commit as a clearly labeled non-release transition baseline. Release assurance remains degraded until a published compatible validator checks a later candidate or an accepted compatibility proof closes the gap.

## Migrated context

- Original intake status: `open`
- Original owner Change: `DSET-CHANGE-SKILL-001`
- External references: https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/9

This one-claim carrier replaces the former aggregate intake row. Current
status is derived from atomic lifecycle events.
