+++
artifact_id = "DSET-ATOMIC-RECORD-021"
semantic_id = "DSET-DEFECT-GOV-002"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Defect — Compilation proves occurrence, not consequence

The compilation gate treats any occurrence of an active authority ID in an
evergreen Markdown file as a valid projection. It can remain fresh when the
surrounding projection contradicts the authority, so it does not prove that
the authority's consequence was compiled into current truth.

## Rationale

This is a current governance defect because the gate claims stronger semantic
coverage than its executable check establishes.
