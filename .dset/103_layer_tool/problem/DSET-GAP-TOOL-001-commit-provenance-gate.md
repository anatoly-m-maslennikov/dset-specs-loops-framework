+++
artifact_id = "DSET-ATOMIC-RECORD-027"
semantic_id = "DSET-GAP-TOOL-001"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:tool"]
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Gap — Commit provenance is derived but not enforced

Traceability can parse commit trailers into derived edges, but no gate rejects
an evergreen or implementation commit that omits a governing Decision ID.
Arbitrary uppercase IDs can also satisfy the current parser, so the repository
cannot enforce its commit-provenance rule.

## Rationale

This is a missing tool capability because a derived view cannot replace the
required delivery gate.
