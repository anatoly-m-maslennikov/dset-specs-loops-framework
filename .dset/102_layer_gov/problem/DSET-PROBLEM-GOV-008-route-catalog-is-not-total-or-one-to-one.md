---
artifact_type: problem
artifact_id: DSET-PROBLEM-GOV-008
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-045"
      - "DSET-REQUIREMENT-META-046"
      - "DSET-REQUIREMENT-GOV-102"
---

# Problem — Route catalog is not total or one-to-one

The current GOV artifact catalog does not satisfy the accepted META routing
requirements.

Its 22 top-level names occupy only 14 of the 54 required semantic routes.
Forty routes are empty. Five occupied routes contain multiple top-level names:

- atomic / method / internal;
- atomic / observation / internal;
- atomic / rationale / internal;
- maintained / definition / internal;
- maintained / method / internal.

The `conflict` subtype also overrides its parent `question` route, although
direct subtypes must inherit the complete route of their canonical type.

Until a separate governed migration assigns exactly one canonical type to each
route and moves finer meanings to direct subtypes, the existing route table and
catalog template are pre-migration inventory rather than a conforming
executable taxonomy.
