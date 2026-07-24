---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-006"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Requirement — Orthogonal profile selection

Each profile axis specializes only its declared concern. Combining profiles
does not let one profile redefine another axis or make a non-applicable
mechanism mandatory.

## Primary claim

Implementation-language, artifact-governance, runtime-risk, and durability-topology profiles are selected as independent concerns.

## Rationale

A documentation-only project, local Python tool, and deployable TypeScript service must not inherit unrelated mechanisms from one universal profile.
