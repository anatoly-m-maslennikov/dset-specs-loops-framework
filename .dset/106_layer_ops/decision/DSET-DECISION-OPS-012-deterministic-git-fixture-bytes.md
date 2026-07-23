+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-099"
type = "decision"
semantic_id = "DSET-DECISION-OPS-012"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Temporary Git repositories used by deterministic tests disable autocrlf and select LF explicitly, while byte-sensitive text fixtures write LF explicitly or capture their actual written bytes before asserting preservation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A deterministic fixture must own the same byte boundary it asserts instead of inheriting machine-global Git or text-I/O defaults."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-TOOL-010"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Make Git fixture byte policy explicit

All temporary repositories initialized by the deterministic suite set local
`core.autocrlf=false` and `core.eol=lf` before staging files. Tests whose
assertion depends on exact authored text write with an explicit LF newline
policy. Tests whose assertion is preservation of an already materialized file
capture the actual bytes after the write instead of predicting host text-I/O
translation.

The rule is fixture-local and does not alter an operator's global Git config.
The tracked repository `.gitattributes` remains authoritative for the real
project checkout.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
