---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-055
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-039"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-GOV-098"
      - "DSET-REQUIREMENT-GOV-102"
      - "DSET-REQUIREMENT-GOV-112"
---

# Test Plan — Validate canonical project settings selections

## Controlled checks

1. Load `.dset/dset_settings.toml` with documented defaults.
2. Accept only enabled catalog types, subtypes, and Governance loci.
3. Accept only `medium` or `high` artifact creation strictness.
4. Accept only `silent` or `verbose` interaction reporting.
5. Reject unknown keys when the governing schema marks their table closed.
6. Confirm a second parse produces identical effective settings.

## Expected disposition

Every valid selection resolves deterministically and every invalid selection
fails closed with the exact key and allowed values.
