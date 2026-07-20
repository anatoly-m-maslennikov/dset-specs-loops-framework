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

- [Governance registry](governance.toml)
- [Artifact-type registry](artifact-types.toml)
- [Governing rules](governance/README.md)
- [Intake](intake.toml)
- [Methodology package fragment](specs/packages/methodology/README.md)
- [Schemas](schemas/README.md)
- [Templates](templates/README.md)
- [Changes](changes/README.md)
- [Generated project health](generated/DSET-DERIVED-VIEW-001-project-health.md)
- [Generated authority compilation](generated/compilation.toml)
- [Generated traceability](generated/traceability.toml)
