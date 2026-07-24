---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-052
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-015"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-011"
      - "DSET-REQUIREMENT-META-035"
---

# Requirement — Keep Scope path structural

Scope path is a project-relative, ordered, and extensible structural coordinate.
It may address layers, features, feature groups, declared Work Areas, or their
configured compositions.

The current project is ambient and never repeated in `scope_path`. Project
scope therefore uses an empty path. Scope may govern ownership, applicability,
inheritance, and identity, but it never changes Revision mode, Content role, or
Governance locus.

## Rationale

Separating structural placement from semantic routing allows the same meaning
to apply at different project scales without multiplying semantic types.
