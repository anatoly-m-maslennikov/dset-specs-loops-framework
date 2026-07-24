---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-062"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-DECISION-GOV-018"
---

# Requirement — Semantic immutability survives representation changes

Every registered current carrier must either match its original seal or be the
target of one complete validated transition chain from that seal. Each link
preserves normalized semantic content and records declared loss; normal DSET
artifact migrations permit no loss.

Lifecycle changes remain append-only events or successor atoms. An unregistered
byte change, missing source return address, broken chain, semantic mismatch, or
direct replacement of the original seal is invalid.

This Invariant atom is immutable. Later correction requires a successor and
append-only lifecycle event.

## Primary claim

An atomic artifact's semantic ID, payload, provenance, and relations never change; carrier encoding or path changes only through a lossless append-only transition with a source return address.

## Rationale

Separating semantic immutability from carrier bytes permits readable canonical formats without allowing silent historical revision.
