# GOV scope

## Purpose

Own repository governance, artifact architecture, intake, provenance, migrations, and derived relationship views.

## Boundaries

GOV owns the single intake and governance registries. Generated views are navigational evidence, not parallel truth, and other scopes retain their own semantic artifacts.

## Layer map

```mermaid
flowchart TB
    GOV["GOV"]
    RULES["Governance and artifact registries"]
    INTAKE["Problems, Questions, provenance"]
    ASSETS["Schemas, templates, migrations"]
    VIEWS["Traceability and derived views"]

    GOV --> RULES
    GOV --> INTAKE
    GOV --> ASSETS
    GOV --> VIEWS
```

## Start here

- `dset_settings.toml`
- `navigation-governance.md`
- Applied GOV artifacts
- `navigation-methodology.md`
- Schemas
- Templates
- `changes`
- `generated`
