# SKILL scope

## Purpose

Own agent-facing workflow orchestration, delegation, local run evidence,
session continuity, and thin-wrapper contracts.

## Boundaries

SKILL owns workflow rules and accepted skill behavior. Host-native source packages remain under `skills/` and cannot become a second rule store.

## Layer map

```mermaid
flowchart TB
    SKILL["SKILL"]
    WRAP["Thin host wrappers"]
    FLOW["Lifecycle orchestration"]
    SESSION["Session and run continuity"]
    DELEGATE["Delegation and budget policy"]

    SKILL --> WRAP
    SKILL --> FLOW
    SKILL --> SESSION
    SKILL --> DELEGATE
```

## Start here

- [Lifecycle orchestration](procedure-lifecycle-orchestration.md)
- [Run and session continuity](procedure-skill-runs.md)
- [Delegation budget](budget.toml)
- [Methodology package fragment](navigation-methodology.md)
- [Schemas](schemas/README.md)
- [Templates](templates/README.md)
- [Project-wide Changes](../versions/changes/)
