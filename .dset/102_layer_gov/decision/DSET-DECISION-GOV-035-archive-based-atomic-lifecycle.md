+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-220"
type = "decision"
semantic_id = "DSET-DECISION-GOV-035"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET removes lifecycle_event artifacts and models an Atomic Artifact as either active or archived; typed successor relations explain resolution and replacement, withdrawn future work moves into a Version Roadmap, and a closed matter can return only as a new atom related to its archived predecessor by recurrence_of."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Standalone lifecycle-event carriers duplicate typed relations and add a second atomic state model when active/archive placement, successor atoms, Version artifacts, provenance, and Git already preserve the required history."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-GOV-010"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-050"
+++

# Decision — Use an archive-based Atomic Artifact lifecycle

DSET has no `lifecycle_event` artifact type. An Atomic Artifact has only two
storage states:

- **active:** its carrier is in the active Type folder and participates in
  current authority, planning, assurance, or work views as applicable;
- **archived:** its carrier is in the Type-local `archive/` folder and remains
  discoverable by identity as immutable history.

Moving an unchanged carrier into `archive/` is a committed storage transition,
not a mutation of the Atomic Artifact.

## Closing active artifacts

- A successor carrying `replacement_of` replaces an older claim. After the
  successor is committed, the replaced atom moves to `archive/`.
- A resolver carrying `resolution_of` closes a Question, Conflict, or Problem.
  After the resolver is committed, the resolved atom moves to `archive/`.
- An atom removed from current work without current implementation is moved to
  `archive/`, and the intended future work is represented by an entry in the
  applicable Version Roadmap or App Plan. That Version entry references the
  archived atom's ID for provenance.
- An atom that no longer applies and has no future intent moves to `archive/`
  in a commit whose rationale identifies why no successor is required.

Terms such as `absorbed`, `resolved`, `retired`, and `withdrawn` may describe
the reason for archival in human-facing history, but they are not stored
lifecycle states or artifact types.

## Returning matters

Reopening an archived atom is forbidden. A recurring Question or Problem is a
new Atomic Artifact with its own identity, current claim, provenance, priority,
and acceptance.

The new artifact may point to the archived predecessor with:

```toml
[[relations]]
type = "recurrence_of"
target = "DSET-PROBLEM-GOV-001"
```

`recurrence_of` means the same bounded matter occurred again after the earlier
artifact left the active set. It does not reactivate, replace, resolve, or
invalidate the archived predecessor.

## History and derivation

The successor or resolver owns the typed relation, rationale, and session
provenance. Git records the committed introduction and archival transition.
Derived views infer the current set from active folders and infer historical
connections from typed relations. No separate event carrier duplicates that
information.
