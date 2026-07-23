+++
artifact_id = "DSET-ATOMIC-RECORD-170"
semantic_id = "DSET-DECISION-TOOL-001"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Repository-controlled text has one portable LF byte policy owned by TOOL configuration rather than by post-implementation operations."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Worktree byte normalization is repository/tool configuration that protects all carriers before implementation or release; it is not an operational release rule."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-008"

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-031"
+++

# Decision — Own portable text bytes in TOOL

Git-controlled text worktree content uses LF through the root repository
policy `* text=auto eol=lf`. The checkout boundary therefore preserves the byte
identity of immutable carriers on Linux, macOS, native Windows, and WSL without
weakening carrier-digest validation. Binary content is not line-ending
normalized.

This Decision completely replaces `DSET-DECISION-OPS-008`. The earlier atom
remains immutable history.
