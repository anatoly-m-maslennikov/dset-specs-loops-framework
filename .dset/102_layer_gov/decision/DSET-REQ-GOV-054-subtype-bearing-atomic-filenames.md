+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-187"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQ-GOV-054"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "This project enables subtype-bearing names for newly emitted atomic artifacts so the REQ, CONSTR, CONTR, or IMPDEC kind is visible in the file list, while immutable existing names remain unchanged."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The compact subtype tokens make atomic project authority distinguishable during filesystem browsing without requiring the reader to open every carrier."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-030"
+++

# Requirement — Subtype-bearing atomic filenames

For newly emitted atomic artifacts in this repository, the semantic ID and
filename use the selected direct Decision subtype token: `REQ`, `CONSTR`,
`CONTR`, or `IMPDEC`. An empty-subtype Decision continues to use `DECISION`.

The project setting enables this naming form. It never renames or mutates an
existing atom, and readers continue to resolve long-form historical kinds as
compatibility input.
