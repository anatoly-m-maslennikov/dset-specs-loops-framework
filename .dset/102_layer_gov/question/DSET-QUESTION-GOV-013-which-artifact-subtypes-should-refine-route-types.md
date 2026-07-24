---
artifact_type: question
artifact_id: DSET-QUESTION-GOV-013
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-045"
      - "DSET-REQUIREMENT-META-046"
      - "DSET-PROBLEM-GOV-008"
      - "DSET-REQUIREMENT-GOV-102"
---

# Question — Which artifact subtypes should refine route types?

After every semantic route has one canonical artifact type, which direct
subtypes should express the finer meanings needed by DSET?

The answer must:

- evaluate the current semantic names as subtype candidates;
- assign each accepted subtype to exactly one canonical parent type;
- keep subtype depth at one;
- require every subtype to inherit its parent's complete route;
- avoid duplicate meanings across sibling or unrelated subtypes;
- preserve distinct identity and numbering only where the distinction is
  operationally useful.

This Question does not authorize subtype creation. The subtype taxonomy remains
undefined until the operator accepts a separate resolution.
