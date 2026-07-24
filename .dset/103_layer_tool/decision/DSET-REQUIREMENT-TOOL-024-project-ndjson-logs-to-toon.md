---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-TOOL-024
scope_path: ["layer:tool"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-GOV-099"
---

# Requirement — Project NDJSON logs to TOON

DSET provides a programmatic tool that reads a bounded selection of canonical
NDJSON runtime records and generates a TOON current view without changing the
source stream.

Every projection declares:

- the source stream identity and digest;
- the selected byte, record, or time frontier;
- the number and ordering of included records;
- the pinned TOON specification and encoder versions; and
- enough provenance to reproduce the same semantic JSON data model.

The projection is deterministic for the same source frontier, settings, and
tool version. Conversion preserves every selected JSON value losslessly or
fails before publishing output. Malformed NDJSON, an incomplete final record,
an unsupported value, or a changed source frontier produces an actionable
diagnostic rather than partial success.

TOON output is regenerated rather than appended in place. It lives in the
runtime/generated boundary, never becomes canonical evidence by existing, and
must return consumers to the NDJSON source frontier it represents.

## Primary claim

DSET can deterministically and losslessly project a bounded NDJSON log frontier
into a reproducible, non-authoritative TOON current view.

## Rationale

This preserves NDJSON's streaming and recovery properties while giving LLM
workflows a compact representation optimized for context consumption. Explicit
frontier and encoder provenance prevents a compact view from hiding omitted,
stale, or differently encoded source records.
