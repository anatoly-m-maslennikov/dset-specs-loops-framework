---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-005
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-002"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-022"
      - "DSET-REQUIREMENT-META-027"
---

# Implementation Decision — Use one governance constitution

META owns the layer constitution and governance invariants. GOV is its only
direct governance implementation owner and defines the project-local carrier,
catalog, settings, admission, precedence, maintenance, and assurance rules.
No sibling registry, rule family, or proof source may become an independent
constitutional root.

Accepted authority and its assurance remain distinct. Evidence and
Verification can establish confidence in an applicable rule, but cannot create
or erase the rule. Conflicting authority is resolved through the governed
conflict policy and successor artifacts; registry order and file order never
create precedence.

## Primary claim

DSET has one META constitution and one direct GOV implementation owner, while
assurance remains evidence about authority rather than a competing source of
authority.

## Rationale

The successor retains the useful single-root and authority-versus-assurance
boundaries while removing the retired rule graph, compile-down, and lifecycle
event mechanisms from the former Decision.
