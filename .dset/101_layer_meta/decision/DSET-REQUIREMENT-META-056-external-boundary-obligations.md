---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-056
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-044"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-038"
      - "DSET-REQUIREMENT-META-051"
---

# Requirement — Preserve external boundary obligations

An operator-accepted DDL, file schema, API, protocol, host format,
supported-platform interface, CI interface, dependency boundary, or comparable
participant obligation is an immutable relational Definition with explicit
participants.

Implementation must conform to that obligation and cannot rewrite it. A
complete change requires a new accepted atomic Definition that replaces the
older one within a declared scope, followed by archive relocation of the
predecessor.

META defines this boundary meaning without assigning its concrete artifact type
or subtype name. GOV owns the canonical name, carrier, identity, and catalog
registration.

## Rationale

This preserves non-negotiable interfaces while removing concrete GOV taxonomy
from the META layer.
