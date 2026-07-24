---
artifact_type: evaluation_case
artifact_id: DSET-EVALUATION-CASE-GOV-040
scope_path: ["layer:gov"]
priority: medium
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-EVALUATION-CASE-GOV-039"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-META-052"
      - "DSET-REQUIREMENT-META-067"
      - "DSET-REQUIREMENT-META-068"
---

# Evaluation Case — Assess current scope and layer distinction

Give reviewers examples with horizontal peer contracts, forward-only ordered
authority, nested scope paths, and unavoidable backward dependencies. Ask
whether each structure should use peer scopes or features, ordered layers,
nested scope paths, or conversion from layers to a horizontal structure.

The evaluation passes when at least 90%:

- classify horizontal ownership as peer scopes or features;
- classify ordered downstream authority as layers;
- preserve the current META → GOV → SPEC → PROFILES → IMPL → OPS direction;
  and
- treat irreducible backward dependency as a reason to stop claiming a clean
  layer model.

## Primary claim

Reviewers can distinguish horizontal scope ownership from ordered layer
authority under the current DSET topology.
