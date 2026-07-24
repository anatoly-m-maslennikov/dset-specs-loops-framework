+++
artifact_id = "DSET-ATOMIC-RECORD-171"
semantic_id = "DSET-DECISION-IMPL-002"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Project-health digest implementation orders files by case-sensitive POSIX relative-path text before hashing paths and working-tree bytes."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The rule is a code-level cross-platform algorithm, so IMPL owns it while TOOL owns the observable health contract."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-OPS-009"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-TOOL-018"
+++

# Decision — Canonical project-health path ordering

Derived project-health source digests order included files by their
case-sensitive POSIX relative-path text before hashing that same path text and
the current working-tree bytes. The digest remains sensitive to uncommitted
content while producing one traversal order on Linux, macOS, native Windows,
and WSL.

This Decision completely replaces `DSET-DECISION-OPS-009`.
