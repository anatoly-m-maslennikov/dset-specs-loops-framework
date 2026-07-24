---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-047
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-001"
      - "DSET-REQUIREMENT-META-016"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-045"
      - "DSET-REQUIREMENT-META-046"
---

# Requirement — Use a streamlined content-role cycle

DSET has exactly six Content roles:

1. Inquiry;
2. Analysis;
3. Definition;
4. Method;
5. Implementation;
6. Observation.

They form the navigational feedback cycle:

```text
Inquiry → Analysis → Definition → Method → Implementation → Observation
    ↑                                                               │
    └───────────────────────────────────────────────────────────────┘
```

An Observation may create a new Inquiry and begin another cycle. A governed
artifact may enter at any justified role; the loop supports navigation and
entry gates but does not determine artifact identity, authority, Revision
mode, or Governance locus.

Rationale is no longer a separate Content role. Rationale is interpretive
content handled by Analysis.

## Rationale

Placing Analysis immediately after Inquiry makes the reasoning step explicit
before desired state is defined. The cycle then moves directly from definition
through realization to factual feedback.
