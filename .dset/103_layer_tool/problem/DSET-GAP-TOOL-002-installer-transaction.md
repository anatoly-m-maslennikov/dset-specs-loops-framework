+++
artifact_id = "DSET-ATOMIC-RECORD-030"
semantic_id = "DSET-GAP-TOOL-002"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "medium"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Gap — Host installation lacks transaction-wide rollback

The installer replaces skill directories one at a time and installs the shared
runtime afterward. A mid-copy I/O failure after an earlier replacement can
leave a host with a mixed old/new distribution because no transaction-wide
rollback restores every prior destination.

## Rationale

This is a missing tool capability because per-directory atomic replacement is
not equivalent to an atomic multi-package installation transaction.
