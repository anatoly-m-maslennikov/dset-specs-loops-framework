---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-012"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-META-018"
---

# Requirement — Explicit three-axis route

Routing values are declared metadata. Authority, provenance, priority,
lifecycle state, applicability, and scope path remain independent.

## Primary claim

Every governed artifact explicitly declares one revision_mode, one content_role, and one governance_locus; other metadata remains outside this route.

## Rationale

Independent explicit axes prevent filenames, folders, workflow position, authority, or lifecycle from silently reclassifying an artifact.
