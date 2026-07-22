# TOOL scope

## Purpose

Own executable CLI, validation, fixture, traceability, and self-hosting contracts.

## Boundaries

TOOL governs executable behavior, deterministic diagnostics, and reusable
proof execution. Python/Test development sources remain in conventional
repository package roots and materialize into installed methodology without
symlinks. Applied QA definitions, evidence, and Verification remain with their
project or layer owners.

## Layer map

```mermaid
flowchart TB
    TOOL["TOOL"]
    CLI["CLI and runtime bridge"]
    VALIDATE["Validation and diagnostics"]
    LIFE["Change and release mechanics"]
    TRACE["Traceability and self-hosting"]
    PYTHON["Python runtime"]
    TESTS["Deterministic Tests"]
    EVALS["Qualitative Evaluations"]

    TOOL --> CLI
    TOOL --> VALIDATE
    TOOL --> LIFE
    TOOL --> TRACE
    TOOL --> PYTHON
    TOOL --> TESTS
    TOOL --> EVALS
```

## Start here

- `specification-build-rules.md`
- `navigation-methodology.md`
- Fixtures
- Schemas
- Templates
- Applied TOOL artifacts
- `000_dset-tool-python-hub.md`
- `000_dset-tool-tests-hub.md`
- `000_dset-tool-evaluations-hub.md`
- `changes`
