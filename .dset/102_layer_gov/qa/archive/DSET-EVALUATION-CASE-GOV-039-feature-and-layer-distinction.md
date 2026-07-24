---
artifact_type: evaluation_case
artifact_id: DSET-EVALUATION-CASE-GOV-039
scope_path: ["layer:gov"]
priority: medium
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-EVALUATION-CASE-GOV-034"
  - type: check_of
    targets:
      - "DSET-REQUIREMENT-META-024"
      - "DSET-REQUIREMENT-META-025"
      - "DSET-REQUIREMENT-META-052"
---

# Evaluation Case — Assess feature and layer distinction

Give reviewers examples with horizontal peer contracts, forward-only ordered
authority, and unavoidable backward dependencies. Ask whether each structure
should use features, layers, nested scope paths, or conversion from layers to
features.

The evaluation passes when at least 90% classify horizontal ownership as
features, ordered downstream authority as layers, and irreducible backward
dependency as a reason to stop claiming a clean layer model.
