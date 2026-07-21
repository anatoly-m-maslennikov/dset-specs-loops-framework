+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-088"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-GOV-045"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "A repository fixture proves that substantive and mixed commits form implementation relations while a generated-only refresh commit does not."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-020"
+++

# Test — Enforce the generated-only provenance boundary

Create a temporary Git repository with a substantive commit, a generated-only
refresh commit, and a mixed commit. Give every commit valid provenance
trailers. The relation builder must retain the substantive and mixed commit
edges and omit the generated-only edge.

Run traceability, health, commit-provenance, lineage, and complete DSET gates.

This emitted Test atom is immutable. Later correction requires a successor Test
and append-only lifecycle event.
