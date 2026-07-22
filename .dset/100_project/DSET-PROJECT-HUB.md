# Applied project-wide DSET artifacts

## Purpose

This directory owns project-wide atomic artifacts, evergreen specifications
and plans, analysis, promoted evidence, migrations, and retained history for
the repository that develops DSET.

## Boundaries

Layer-specific truth belongs to the corresponding applied layer. Installed
methodology is referenced by unique identity and never duplicated here.

```mermaid
flowchart LR
    PROJECT["100 Project"]
    META["101 META"]
    GOV["102 GOV"]
    TOOL["103 TOOL"]
    SKILL["104 SKILL"]
    OPS["105 OPS"]
    VERSION["150 Versions"]

    PROJECT --> META --> GOV --> TOOL --> SKILL --> OPS
    PROJECT --> VERSION
```

## Start here

- `DSET-META-HUB.md`
- `DSET-GOV-HUB.md`
- `DSET-TOOL-HUB.md`
- `DSET-SKILL-HUB.md`
- `DSET-OPS-HUB.md`
- `DSET-VERSIONS-HUB.md`
- `000_dset-methodology-hub.md`
