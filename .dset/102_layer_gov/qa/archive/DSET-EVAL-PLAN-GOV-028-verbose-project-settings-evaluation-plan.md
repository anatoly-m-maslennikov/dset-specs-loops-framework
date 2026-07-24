---
artifact_type: "evaluation_plan"
artifact_id: "DSET-EVAL-PLAN-GOV-028"
scope_path:
  - "layer:gov"
priority: "medium"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-037"
  - type: "replacement_of"
    targets:
      - "DSET-EVAL-PLAN-GOV-027"
---

# Evaluation Plan — Judge settings discoverability

Without implementation knowledge, cold readers must find every active setting,
accepted value, default, effect, and practical example in
`dset_settings.toml`. They must correctly predict where to change an operator
preference and where to inspect project identity, topology, contracts, release
targets, or verification commands.

At least 90% of representative questions must be answered correctly, with no
authority-source error, no assumption that omitted settings are unavailable,
and no treatment of legacy `dset.toml` compatibility as a writable second
source.

This emitted Evaluation definition is immutable. Execution and evidence are
separate.

## Primary claim

Cold readers can configure DSET from dset_settings.toml and correctly distinguish selectable behavior from project truth and governing definitions.
