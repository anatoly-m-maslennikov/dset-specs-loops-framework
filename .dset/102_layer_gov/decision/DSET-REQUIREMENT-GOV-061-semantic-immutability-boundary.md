---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-061"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-060"
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-062"
---

# Requirement — Semantic immutability boundary

The immutable part of an atomic artifact is its governed meaning:

- primary claim, question, problem statement, or proof intent;
- rationale and accepted authority or creation state;
- provenance facts and creation-session provenance;
- scope and applicability meaning;
- priority recorded at creation;
- relation types and the artifact identities they connect; and
- for QA, conditions, criteria, thresholds, and expected disposition.

An append-only event may derive later lifecycle state or effective priority. A
governed migration may recode an ID, classification-label spelling, filename,
path, heading label, carrier format, seal, or stored target spelling only when
the immutable meaning and connected artifact identities remain equal. Any
other change requires a successor atom.

## Primary claim

DSET atomic immutability protects governed meaning rather than a particular identifier spelling or carrier representation.

## Rationale

An atom must survive canonical naming and carrier migrations without permitting a migration to disguise a changed claim, provenance fact, scope, relation meaning, or QA criterion.
