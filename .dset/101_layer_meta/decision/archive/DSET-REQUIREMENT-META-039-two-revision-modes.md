---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-039
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-017"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-020"
      - "DSET-REQUIREMENT-META-033"
      - "DSET-REQUIREMENT-META-035"
---

# Requirement — Use two Revision modes

DSET has exactly two Revision modes:

```toml
revision_mode = "atomic" # atomic | maintained
```

- `atomic` identifies an accepted immutable record. Changed meaning requires a
  new linked atom.
- `maintained` identifies a mutable current artifact whose applicable update
  procedure may revise or replace its content.

`evergreen` is not a Revision mode. It may describe a maintained artifact with
an explicit freshness obligation, current/stale lifecycle, and source
frontier. Whether a maintained artifact is authored directly, refreshed
semantically from atoms, synchronized, or generated is defined by its
registered artifact type and applicable procedure rather than another
universal Revision-mode value.

Generated code, dashboards, TOON log views, and other reproducible projections
are maintained artifacts with generation provenance. Hand-maintained code,
documents, and settings are maintained artifacts with their own edit
authority. A Git commit remains a separate atomic Implementation record; a
Merge Commit is relational and declares its parents explicitly.

## Primary claim

Revision mode distinguishes only immutable atomic records from mutable
maintained artifacts; evergreen freshness and artifact-specific update
mechanisms are separate concerns.

## Rationale

Evergreen and maintained overlap because both permit revision. Treating them as
peer values makes one artifact satisfy two supposedly exclusive modes.
Separating mutability from freshness and update mechanism keeps the axis MECE
while allowing each artifact type to use the procedure appropriate to its job.
