---
artifact_type: "question"
artifact_id: "DSET-QUESTION-GOV-010"
scope_path:
  - "layer:gov"
priority: "medium"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "ops"
  applies_unchanged: false
  local_context_required: true
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "relates_to"
    targets:
      - "DSET-QUESTION-GOV-005"
---

# Question — Should lifecycle-event artifacts be removed?

Current lifecycle events record later state without rewriting immutable Atomic
Artifacts. The implemented event vocabulary covers acceptance, answer,
confirmation, resolution, absorption, reopening, rejection, retirement,
withdrawal, and priority changes.

The current project contains 110 lifecycle-event carriers:

- 67 `absorbed`;
- 37 `resolved`;
- 5 `withdrawn`; and
- 1 `reopened`.

Of those, 48 absorption events already duplicate `replacement_of` relations
and 6 resolution events already duplicate `resolution_of` relations. The
remaining 56 events require an explicit one-time migration before the event
model can be removed.

The candidate replacement is:

- `replacement_of` determines supersession and absorption;
- `resolution_of` determines Question, Conflict, and Problem resolution;
- a new successor Question or Problem represents reopening;
- future work lives in a Version Roadmap rather than a withdrawn current atom;
- archive placement marks inactive historical carriers;
- the successor atom stores rationale and session provenance; and
- Git records when the persisted transition was introduced.

Open migration questions are whether any current event lacks a truthful typed
successor and where mutable execution priority should live after lifecycle
events are removed.

## Primary claim

Should DSET remove lifecycle_event as a standalone artifact type and derive atomic current state from typed successor relations, archive placement, atomic provenance, and Git history instead?

## Rationale

Lifecycle-event files preserve changes to immutable atoms, but the current repository contains 110 additional carriers and many duplicate information already expressed by typed relations.
