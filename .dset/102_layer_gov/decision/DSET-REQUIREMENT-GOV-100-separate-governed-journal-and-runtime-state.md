---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-100
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-099"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-GOV-097"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-041"
---

# Requirement — Separate governed, journal, and runtime state

Every DSET project uses three distinct root directories:

| Root | Owned content | Revision behavior |
|---|---|---|
| `.dset/` | Governed artifacts, installed methodology, settings, tools, skill instructions, schemas, templates, and maintained views | Atomic or maintained according to registered artifact type |
| `.dset_journal/` | Canonical durable running logs, event streams, audit trails, and other ordered record sequences | Append-only |
| `.dset_runtime/` | Caches, scratch files, temporary materializations, process state, and other reconstructible working data | Disposable |

Every persisted DSET running log uses NDJSON under `.dset_journal/` as its
canonical carrier. Each appended line is one complete UTF-8 JSON record
followed by a newline. Accepted records are never edited, reordered, or
deleted. Rotation and retention may create or seal carriers without rewriting
accepted records.

Nothing under `.dset_runtime/` may be the only copy of governed truth, durable
history, or canonical evidence. The directory may be removed between runs
without changing project meaning or losing accepted journal records.

TOON may represent a selected journal frontier as a generated maintained view.
A disposable rendering may live under `.dset_runtime/`; a promoted governed
view lives under `.dset/`. In both cases, the NDJSON sequence remains canonical
for the recorded observations.

Git-tracking, retention, rotation, and optional external replication of
`.dset_journal/` are separate project policies. They do not change its
append-only semantics or make it disposable runtime state.

## Primary claim

DSET separates governed project state, canonical append-only history, and
disposable runtime state into `.dset/`, `.dset_journal/`, and
`.dset_runtime/`.

## Rationale

The boundary prevents canonical observations from being deleted with runtime
scratch data while keeping high-churn append-only history separate from
human-governed artifacts and executable methodology.
