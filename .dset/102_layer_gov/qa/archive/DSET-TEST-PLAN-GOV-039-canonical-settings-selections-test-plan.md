---
artifact_type: "test_plan"
artifact_id: "DSET-TEST-PLAN-GOV-039"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-038"
      - "DSET-REQUIREMENT-GOV-039"
      - "DSET-REQUIREMENT-SKILL-013"
---

# Test Plan — Validate canonical settings selections

The deterministic suite must prove defaults, every accepted value, invalid
value rejection, and selected runtime behavior for
`artifacts.subtype_in_names`, `artifacts.creation_strictness`, and
`workflows.implement.mode` in root `dset_settings.toml`.

Bootstrap and adopter writers emit only the canonical filename and keys. A
legacy root `dset.toml` remains read compatibility only, dual roots fail, and
no writer extends the legacy surface.

This Test definition is immutable. Runs and evidence are separate.

## Primary claim

Deterministic tests prove that canonical settings keys select artifact naming, atom-creation strictness, and implementation preparation without legacy write paths.
