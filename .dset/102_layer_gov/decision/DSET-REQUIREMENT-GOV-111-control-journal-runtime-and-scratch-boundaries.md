---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-111
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-043"
      - "DSET-REQUIREMENT-GOV-100"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-053"
---

# Requirement — Separate control, journal, runtime, and scratch state

Every DSET project uses four distinct storage boundaries:

| Boundary | Owned content | Revision behavior |
|---|---|---|
| `.dset/` | Governed artifacts, installed methodology, settings, tools, skill instructions, schemas, templates, and maintained views | Atomic or maintained by registered type |
| `.dset_journal/` | Canonical running logs, event streams, audit trails, and ordered record sequences | Append-only NDJSON |
| `.dset_runtime/` | Ignored reconstructible or resumable run state, checkpoints, caches, recovery material, and temporary materializations | Mutable and disposable between completed workflows |
| Host temporary root | Process scratch and test workspaces | Disposable; cleaned when the owning operation exits |

Nothing under `.dset_runtime` or the host temporary root may be the only copy
of governed truth, durable history, or canonical evidence. DSET scratch uses
the operating system's native temporary root and never an ambient path that
places scratch in the repository. Cleanup failure is reported as failure.

Every journal line is one complete UTF-8 JSON record followed by a newline.
Accepted records are never edited, reordered, or deleted. Rotation may create
or seal carriers without rewriting accepted records. A generated TOON or other
summary is a maintained view; the selected NDJSON frontier remains canonical
for its observations.

Short-lived same-directory swap state may exist only for atomic publication
and must be replaced or removed before the operation returns.

## Primary claim

DSET separates governed control state, canonical append-only journals,
reconstructible runtime state, and disposable host scratch into four explicit
boundaries.

## Rationale

The merged boundary removes the former conflict over whether runtime state is
resumable or scratch and protects append-only observations from both cleanup
paths.
