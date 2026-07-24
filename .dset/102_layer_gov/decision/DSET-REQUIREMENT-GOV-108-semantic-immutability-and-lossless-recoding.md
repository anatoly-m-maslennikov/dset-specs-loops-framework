---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-108
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-060"
      - "DSET-REQUIREMENT-GOV-061"
---

# Requirement — Preserve semantic atoms through lossless recoding

An atomic artifact is one independently identified immutable semantic record.
Its protected content includes its primary claim or proof intent, rationale,
accepted provenance facts, creation-session provenance, scope and
applicability, recorded priority, relation meanings and endpoints, and
applicable assurance conditions, criteria, thresholds, and expected
disposition.

Correction, withdrawal, replacement, resolution, or recurrence creates another
atom when needed and moves an inactive predecessor unchanged into its
type-local archive.

A governed whole-graph migration may recode an artifact's identifier,
classification-label spelling, filename, path, heading label, carrier
encoding, seal, and stored target spelling only when it preserves the protected
meaning and connected identities. Archive relocation and such lossless
recoding are not semantic mutation. Any other change requires a successor.

## Primary claim

Atomic immutability protects one semantic record while permitting only
lossless, graph-wide identity or carrier recoding and unchanged archive
relocation.

## Rationale

The merged rule makes semantic and storage atoms identical without freezing
historical identifiers or carriers forever.
