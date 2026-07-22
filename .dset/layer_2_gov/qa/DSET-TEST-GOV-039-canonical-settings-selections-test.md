+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-054"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-GOV-039"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove that canonical settings keys select artifact naming, atom-creation strictness, and implementation preparation without legacy write paths."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-038"

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-039"

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-SKILL-013"
+++

# Test — Validate canonical settings selections

The deterministic suite must prove defaults, every accepted value, invalid
value rejection, and selected runtime behavior for
`artifacts.subtype_in_names`, `artifacts.creation_strictness`, and
`workflows.implement.mode` in root `dset_settings.toml`.

Bootstrap and adopter writers emit only the canonical filename and keys. A
legacy root `dset.toml` remains read compatibility only, dual roots fail, and
no writer extends the legacy surface.

This Test definition is immutable. Runs and evidence are separate.
