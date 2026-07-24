---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-053
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-032"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-021"
      - "DSET-REQUIREMENT-META-041"
---

# Requirement — Bound the durable control plane

The durable DSET control plane is secret-free and LLM-provider agnostic.

Its active set contains accepted current project authority, applicable
maintained artifacts, and operative governance. Type-local archives preserve
accepted historical atoms without making them active authority. Future
intentions remain in Version Roadmaps, and unaccepted exploration remains
outside governed state.

Passwords, API keys, tokens, and other secrets never enter DSET artifacts,
settings, journals, evidence, or runtime logs. Runtime code obtains them only
through external secret-bearing environment keys or an equivalent governed
host boundary.

## Rationale

The corrected boundary distinguishes current authority from preserved history
without excluding archives from the durable control plane or admitting secrets
and session speculation.
