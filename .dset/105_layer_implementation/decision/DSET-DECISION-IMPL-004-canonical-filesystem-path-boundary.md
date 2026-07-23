+++
artifact_id = "DSET-ATOMIC-RECORD-173"
semantic_id = "DSET-DECISION-IMPL-004"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Implementation compares filesystem paths by resolved identity and serializes repository-relative paths with canonical POSIX separators."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Filesystem identity and serialization are code-level portability rules used to implement TOOL contracts across operating systems."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-011"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Canonical filesystem path boundaries

Repository roots and filesystem paths are compared by resolved identity, so
macOS aliases and Windows short or long names cannot split one repository into
different identities. Relative `Path` inputs are serialized with POSIX
separators before canonical repository-relative validation; serialized string
inputs must already use canonical POSIX separators.

This Decision completely replaces `DSET-DECISION-OPS-011`.
