---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-SKILL-018
scope_path: ["layer:skill"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-SKILL-017"
---

# Requirement — Use dset-a-update for mutable artifacts

DSET provides `dset-a-update` as the secondary skill that creates or updates
evergreen and maintained artifacts of every registered applicable type and
subtype.

The skill resolves the current `scope_path`, governing atomic sources, enabled
governance surfaces, and the artifact's revision semantics before changing its
carrier. It preserves one current owner and does not emit, edit, replace, or
archive atomic artifacts.

The initialized DSET session may call this skill automatically when accepted
atomic truth requires a current evergreen view or when an authorized maintained
artifact must change.

## Rationale

Separating mutable artifact maintenance from atomic emission prevents an update
workflow from weakening atomic immutability. The provisional name may later be
replaced by a successor Requirement without weakening this responsibility
boundary.
