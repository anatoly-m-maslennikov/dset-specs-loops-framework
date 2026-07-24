---
artifact_type: test_plan
artifact_id: DSET-TEST-PLAN-GOV-058
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-TEST-PLAN-GOV-051"
      - "DSET-TEST-PLAN-GOV-052"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-GOV-108"
---

# Test Plan — Validate semantic immutability and lossless recoding

## Controlled checks

1. Snapshot every protected semantic field and relation endpoint.
2. Perform a complete identifier, filename, heading, carrier, and target
   spelling migration.
3. Prove the semantic snapshot and graph connectivity are equal after recoding.
4. Move an inactive atom unchanged into its type-local archive.
5. Attempt to change one protected claim, rationale, provenance, scope,
   priority, relation meaning, or assurance criterion and require rejection.

## Expected disposition

Lossless graph-wide recoding and unchanged archive relocation pass; every
semantic mutation fails and requires a successor identity.
