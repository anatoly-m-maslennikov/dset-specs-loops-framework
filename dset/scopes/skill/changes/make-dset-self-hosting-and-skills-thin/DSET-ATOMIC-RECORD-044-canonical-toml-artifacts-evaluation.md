---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-044
type: qa
subtype: evaluation
semantic_id: DSET-EVALUATION-GOV-027
status: accepted
priority: medium
authority: "operator:anatoly-m-maslennikov"
claim: "Readers find canonical TOML artifacts and documented settings clearer without mistaking generated or host-mandated adapters for authority."
scope:
  kind: project
  id: dset-specs-loops-framework
promotion:
  parent_scope: null
relations:
  - type: check_of
    target: DSET-REQUIREMENT-GOV-036
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Evaluation — Judge TOML artifact readability

Cold readers must identify scalar, list, table, and nested-record boundaries;
find every active `dset.toml` option, valid value, effect, and default; and
distinguish canonical TOML truth from generated or externally prescribed
JSON/YAML adapters without implementation knowledge.

At least 90% of representative artifact and settings questions must be
answered correctly, with no authority-source error and no reliance on
indentation to infer ownership.

This emitted Evaluation definition is immutable. Execution and evidence are
separate.
