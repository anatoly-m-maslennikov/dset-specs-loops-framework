# TOOL scope

## Purpose

Own executable CLI, validation, fixture, traceability, and self-hosting contracts.

## Boundaries

TOOL governs executable behavior and deterministic diagnostics. Source code remains in conventional repository folders and links back to these accepted contracts.

## Layer map

```mermaid
flowchart TB
    TOOL["TOOL"]
    CLI["CLI and runtime bridge"]
    VALIDATE["Validation and diagnostics"]
    LIFE["Change and release mechanics"]
    TRACE["Traceability and self-hosting"]

    TOOL --> CLI
    TOOL --> VALIDATE
    TOOL --> LIFE
    TOOL --> TRACE
```

## Start here

- [Build rules](specification-build-rules.md)
- [Methodology package fragment](navigation-methodology.md)
- [Fixtures](fixtures/README.md)
- [Schemas](schemas/README.md)
- [Templates](templates/README.md)
- [Project-wide Changes](../versions/changes/)
