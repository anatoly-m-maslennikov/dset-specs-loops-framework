---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-054
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-033"
      - "DSET-REQUIREMENT-META-042"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-041"
---

# Requirement — Make maintained semantic views optional and thin

DSET starts atomic-first. Named maintained semantic views are optional
governance surfaces that may be activated or deactivated independently without
changing atomic authority.

When active, a maintained semantic view is a thin, reasoned current model rather
than a concatenation or mechanical compilation of atoms. It may contain domain
flows, dependency-ordered entity definitions, lifecycle models, and direct
links from each represented claim to its active atomic sources.

An inactive surface creates no currentness gate. An active surface becomes
stale when its applicable atomic frontier changes and becomes current only
after a reasoned refresh. Deactivation preserves its carrier and Git history.

## Rationale

One rule now owns both optional activation and the semantic shape of the view,
eliminating the former split between surface lifecycle and view construction.
