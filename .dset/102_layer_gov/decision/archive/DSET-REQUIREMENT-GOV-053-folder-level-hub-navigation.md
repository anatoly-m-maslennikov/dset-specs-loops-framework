---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-053"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-DECISION-GOV-009"
      - "DSET-REQUIREMENT-GOV-043"
---

# Requirement — Keep hub navigation stable and folder-level

A hub may directly list:

- stable child areas and their hubs;
- folders that contain atomic artifacts;
- evergreen specifications and plans;
- settings and other long-lived non-atomic files.

A hub never enumerates individual Decision, Question, Problem, QA, or other
atomic carriers. Adding an atom therefore does not require a hub edit. The hub
also never lists or links any file or directory below `.dset_runtime/`; runtime
state is transient and outside durable navigation.

## Primary claim

Hubs represent atomic artifacts only through their containing folders, list evergreen settings and other long-lived non-atomic carriers, and never list or link a .dset_runtime descendant.

## Rationale

Folder-level navigation stays stable as immutable atoms accumulate, while long-lived owners remain directly discoverable and transient runtime state never leaks into the durable navigation surface.
