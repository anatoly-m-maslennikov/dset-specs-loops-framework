---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-051"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-044"
---

# Requirement — Use recursive numbered root directories

The visible self-hosting project structure is:

```text
00_project/
01_layer_meta/
02_layer_gov/
03_layer_tool/
04_layer_skill/
05_layer_ops/
10_versions/
```

The distributable framework uses matching `01_layer_meta` through
`05_layer_ops` names below `.dset/`. The numeric prefixes keep project scope,
ordered layers, and version scope stable in filesystem ordering while logical
layer IDs remain `META`, `GOV`, `TOOL`, `SKILL`, and `OPS`.

## Rationale

The names expose order without repeating `layer_` in every path and keep global
project/version scope visually distinct from the five behavioral layers.

## Primary claim

Recursive DSET project scope uses 00_project, 01_layer_meta, 02_layer_gov, 03_layer_tool, 04_layer_skill, 05_layer_ops, and 10_versions, with the same numbered framework layer names below .dset.
