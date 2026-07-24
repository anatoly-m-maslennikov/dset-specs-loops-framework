+++
artifact_id = "DSET-ATOMIC-RECORD-090"
semantic_id = "DSET-DECISION-OPS-009"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Derived project-health source digests order included files by their case-sensitive POSIX relative-path text before hashing paths and working-tree bytes."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "POSIX relative-path text is already the digest's serialized path identity and provides one explicit order independent of the host Path implementation."
promotion = {}

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-OPS-003"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Canonically order project-health source paths

The project-health source digest first selects the governed non-generated
files. It then orders those entries by each file's case-sensitive POSIX
relative-path text and hashes that same path text followed by the current
working-tree bytes.

The rule keeps uncommitted source changes visible and keeps byte-level content
checks intact. It changes only traversal order, replacing host-native Path
comparison with one serialized ordering shared by Linux, macOS, native Windows,
and WSL.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
