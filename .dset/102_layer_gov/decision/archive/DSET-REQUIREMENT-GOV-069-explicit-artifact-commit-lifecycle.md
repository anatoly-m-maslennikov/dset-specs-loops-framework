---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-069"
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
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-068"
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-049"
---

# Requirement — Make artifact commit lifecycle explicit

The canonical artifact catalog starts with a concise commented legend before
the first group or Type definition. The legend defines every shared field,
including its allowed values and effect.

## Truth ownership

```toml
source_of_truth = true # or false
```

- `true`: an artifact of this catalog entry is the canonical source of truth
  for the concern it explicitly owns.
- `false`: the artifact is derived, supporting, executable, observational, or
  navigational for that concern and does not replace its declared source of
  truth.

## Commit lifecycle

```toml
commit_on_create = true
commit_on_update = false # or true
```

- `commit_on_create = true`: creating a persisted artifact requires a Git
  commit that adds its carrier.
- `commit_on_update = true`: the artifact may be updated in place, and every
  persisted update requires a Git commit.
- `commit_on_update = false`: the artifact's governed content is immutable.
  Changed meaning requires a new successor artifact; it must never be updated
  without a commit.

Every persisted catalog entry uses `commit_on_create = true`.

Atomic Artifacts use `commit_on_update = false`. A governed identity, filename,
path, or carrier-format migration does not change the atomic claim and is
handled as a separately authorized, fully committed migration.

Mutable evergreen artifacts, settings, implementation, and reusable assets use
`commit_on_update = true`.

Deletion does not need a separate catalog flag. Any permitted removal is a Git
change. Atomic Artifacts are archived or replaced through explicit relations
and are not deleted as ordinary mutable files.

## Primary claim

The canonical artifact catalog begins with a field legend, uses source_of_truth for truth ownership, and replaces changed_through_git with explicit commit_on_create and commit_on_update lifecycle flags.

## Rationale

Creation and in-place update are different lifecycle operations, while the former changed_through_git field obscures the difference between immutable and mutable artifacts.
