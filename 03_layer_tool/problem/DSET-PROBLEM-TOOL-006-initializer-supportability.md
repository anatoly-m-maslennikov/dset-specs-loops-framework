+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-016"
type = "problem"
semantic_id = "DSET-PROBLEM-TOOL-006"
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Problem — Initializer contradicts active automation

When a target repository already has active GitHub workflows, `dset init
--execute` emits `supportability.status: not-applicable`. The post-write DSET
validator then rejects hosted production automation without applicable
supportability and rolls the initialization back. The initializer therefore
cannot initialize an otherwise valid automated repository using its own
default output.

## Rationale

This is a TOOL-layer Problem because the defect is in bootstrap target
classification. Project-level promotion is inappropriate: the correct value
depends on target repository state, and the accepted validation rule should
remain unchanged.
