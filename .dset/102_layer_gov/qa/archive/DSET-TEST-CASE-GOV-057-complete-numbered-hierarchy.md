---
artifact_type: test_case
artifact_id: DSET-TEST-CASE-GOV-057
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-CASE-GOV-049"
      - "DSET-TEST-CASE-GOV-050"
  - type: check_of
    targets:
      - "DSET-IMPL-GOV-007"
      - "DSET-REQUIREMENT-META-023"
      - "DSET-REQUIREMENT-META-025"
---

# Test Case — Validate the complete numbered hierarchy

## Controlled checks

1. Assert the installed methodology has `00_project` then `01_meta` through
   `06_ops`.
2. Assert applied authority has `100_project`, `101_layer_meta` through
   `106_layer_ops`, and `150_versions`.
3. Assert reusable source has `10_project`, `11_layer_meta` through
   `16_layer_ops`, and `50_versions`.
4. Assert every methodology descendant has one sibling-unique zero-padded
   numeric prefix.
5. Reject any declared layer dependency from a later layer to an earlier layer.

## Expected disposition

The exact three hierarchies pass, missing or misordered layers fail, and every
backward dependency is reported with both endpoints.
