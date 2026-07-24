---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-007
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-022"
      - "DSET-DECISION-GOV-026"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-023"
      - "DSET-REQUIREMENT-META-057"
---

# Implementation Decision — Use the complete numbered control-plane layout

The installed project-local methodology lives only under:

```text
.dset/000_dset_methodology/
├── 00_project/
├── 01_meta/
├── 02_gov/
├── 03_tool/
├── 04_skill/
├── 05_implementation/
└── 06_ops/
```

Applied project authority lives only under:

```text
.dset/
├── 100_project/
├── 101_layer_meta/
├── 102_layer_gov/
├── 103_layer_tool/
├── 104_layer_skill/
├── 105_layer_implementation/
├── 106_layer_ops/
└── 150_versions/
```

The reusable framework product source remains distinct at the repository root:

```text
10_project/
11_layer_meta/
12_layer_gov/
13_layer_tool/
14_layer_skill/
15_layer_implementation/
16_layer_ops/
50_versions/
```

Every committed descendant of `000_dset_methodology` uses a stable,
zero-padded numeric prefix unique among its siblings. Materialization derives
these names deterministically and does not persist a source-to-installed path
registry.

## Primary claim

Installed methodology, applied project authority, and reusable framework source
use the complete numbered layouts above and remain distinct owners.

## Rationale

One complete layout replaces two partial artifacts whose layer lists no longer
matched the accepted META→GOV→TOOL→SKILL→IMPL→OPS flow.
