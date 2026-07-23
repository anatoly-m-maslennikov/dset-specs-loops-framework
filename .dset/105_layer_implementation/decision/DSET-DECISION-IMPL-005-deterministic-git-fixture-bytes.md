+++
artifact_id = "DSET-ATOMIC-RECORD-174"
semantic_id = "DSET-DECISION-IMPL-005"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Test implementations isolate temporary Git newline settings and write or observe explicit fixture bytes before asserting byte preservation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Deterministic fixture construction governs Test implementation and belongs in IMPL rather than the post-implementation OPS layer."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-012"

[[relations]]
type = "child_of"
target = "DSET-DECISION-TOOL-001"
+++

# Decision — Deterministic temporary Git bytes

Temporary Git repositories used by deterministic Tests disable autocrlf and
select LF through repository-local configuration before staging.
Byte-sensitive fixtures write explicit LF or capture the bytes actually
materialized before asserting preservation; they never inherit ambient Git or
text-I/O policy.

This Decision completely replaces `DSET-DECISION-OPS-012`.
