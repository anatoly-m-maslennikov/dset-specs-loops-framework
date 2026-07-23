+++
artifact_id = "DSET-ATOMIC-RECORD-018"
semantic_id = "DSET-TEST-PLAN-TOOL-022"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
child_of = ["DSET-REQUIREMENT-TOOL-022"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test Plan — Enforce reference and applied profile roles

Deterministic proof must require an explicit `reference` or `applied` role,
require `derived_from` only for applied instances, expose the role in read-only
inspection, reject an adopter that attempts to execute a distributed reference,
accept the same adopter after a local applied instance exists, and preserve the
complete existing profile validation and target-drift matrix.

This emitted Test definition is immutable. Test code and execution results are
separate implementation and evidence artifacts.
