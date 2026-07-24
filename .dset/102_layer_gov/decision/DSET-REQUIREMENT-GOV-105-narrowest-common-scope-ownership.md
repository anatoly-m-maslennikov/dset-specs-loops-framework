---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-105
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-032"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-052"
---

# Requirement — Own truth at the narrowest common scope

Every atomic or maintained artifact belongs to the narrowest enabled
structural scope that fully contains all affected owners and subjects. A claim
is not project-level merely because it is abstract, important, or widely
reused.

Project scope owns only genuinely project-wide obligations, cross-child
relations and interfaces, end-to-end assurance, cross-cutting constraints,
system architecture, version governance, and inquiries or observations whose
subject crosses immediate child boundaries.

The rule applies recursively. A concern spanning features inside one feature
group belongs to that group; a concern spanning groups or layers belongs to
their narrowest common ancestor. Parent artifacts may summarize or link
child-owned detail but do not duplicate its claim.

## Primary claim

Every governed artifact is owned by the narrowest common enabled scope that
contains its complete subject.

## Rationale

Scope-local ownership prevents global truth from becoming a second copy of
child authority while retaining one owner for cross-boundary behavior.
