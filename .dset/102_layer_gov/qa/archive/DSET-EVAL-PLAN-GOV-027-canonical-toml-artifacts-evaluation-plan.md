---
artifact_type: "evaluation_plan"
artifact_id: "DSET-EVAL-PLAN-GOV-027"
scope_path:
  - "layer:gov"
priority: "medium"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-036"
---

# Evaluation Plan — Judge TOML artifact readability

Cold readers must identify scalar, list, table, and nested-record boundaries;
find every active `dset.toml` option, valid value, effect, and default; and
distinguish canonical TOML truth from generated or externally prescribed
JSON/YAML adapters without implementation knowledge.

At least 90% of representative artifact and settings questions must be
answered correctly, with no authority-source error and no reliance on
indentation to infer ownership.

This emitted Evaluation definition is immutable. Execution and evidence are
separate.

## Primary claim

Readers find canonical TOML artifacts and documented settings clearer without mistaking generated or host-mandated adapters for authority.
