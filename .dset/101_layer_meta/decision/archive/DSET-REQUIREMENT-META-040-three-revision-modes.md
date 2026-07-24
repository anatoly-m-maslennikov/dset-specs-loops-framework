---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-040
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-039"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-020"
      - "DSET-REQUIREMENT-META-033"
      - "DSET-REQUIREMENT-META-035"
---

# Requirement — Use three Revision modes

DSET has exactly three Revision modes:

```toml
revision_mode = "atomic" # atomic | append_only | maintained
```

- `atomic` identifies one independently governed immutable semantic unit.
  Changed meaning requires a new linked atom.
- `append_only` identifies a growing sequence whose accepted records remain
  immutable. Only complete new records may be appended; existing records
  cannot be edited, reordered, or removed.
- `maintained` identifies a mutable current artifact whose applicable update
  procedure may revise or replace existing content.

Revision mode applies to the governed artifact carrier. An NDJSON running log
is `append_only`; an individual record inside it is immutable but does not
become a separately governed Atomic Artifact unless promoted into one. A
current catalog generated from catalog events is `maintained`, while its event
ledger is `append_only`.

`evergreen` is not a Revision mode. It may describe a maintained artifact with
a freshness obligation, current/stale lifecycle, and source frontier.
Authoring, semantic refresh, synchronization, and generation remain
artifact-specific update mechanisms rather than additional Revision modes.

## Primary claim

Revision mode classifies governed artifacts as independently immutable atoms,
append-only record sequences, or mutable maintained artifacts.

## Rationale

The three values expose the only permitted change patterns needed by DSET:
never change an accepted unit, add records without rewriting history, or
maintain current content through an owned update procedure. `append_only`
states the invariant directly without narrowing it to logs, journals, ledgers,
or streams.
