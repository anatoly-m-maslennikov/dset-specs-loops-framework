---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-099
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-GOV-097"
---

# Requirement — Store running logs as NDJSON

Every persisted DSET running log uses NDJSON as its canonical carrier. Each
appended line is one complete UTF-8 JSON record followed by a newline. Records
are appended to a stream under `.dset_runtime` and are never rewritten merely
to optimize presentation to a human or language model.

A malformed record stops governed consumption with an actionable diagnostic;
readers do not silently reinterpret a partial line as a valid observation.
Rotation, retention, and promotion may create new carriers without rewriting
records already accepted into an existing stream.

TOON may represent a selected log frontier as a generated current view. That
view is non-authoritative and replaceable: the NDJSON stream remains the
canonical runtime record, and a promoted governed observation becomes a
separate Evidence Record.

## Primary claim

NDJSON is the canonical append-only carrier for every persisted DSET running
log, while TOON is permitted only as a derived non-authoritative view.

## Rationale

Independent JSON records provide append safety, streaming interoperability,
and bounded recovery. TOON can reduce LLM context size without weakening the
canonical runtime history or turning an optimized presentation into a second
source of truth.
