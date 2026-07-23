+++
artifact_id = "DSET-ATOMIC-RECORD-218"
semantic_id = "DSET-REQUIREMENT-GOV-070"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "The canonical artifact catalog uses commit_on_create for persisted artifacts, uses commit_on_update only for artifact entries whose governed content may be updated in place, and omits commit_on_update entirely for immutable Atomic Artifacts."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Atomic immutability is an invariant, not a configurable false value, and an inapplicable setting should be absent rather than encoded as an option."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-069"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-049"
+++

# Requirement — Omit update settings from Atomic Artifacts

The canonical artifact catalog starts with a concise commented legend before
the first group or Type definition. The legend defines every shared field,
including where the field applies.

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

Every persisted artifact entry uses:

```toml
commit_on_create = true
```

This means creating the artifact requires a Git commit that adds its carrier.

Only entries whose governed content may be updated in place declare:

```toml
commit_on_update = true
```

This means every persisted in-place update requires a Git commit.

Atomic Artifact entries do not contain `commit_on_update`. The field is not
applicable because atomic governed content cannot be updated in place. Changed
meaning requires a new successor artifact.

A governed identity, filename, path, or carrier-format migration does not
change the atomic claim and is handled as a separately authorized, fully
committed migration.

Any permitted removal is also a Git change. Atomic Artifacts are archived or
replaced through explicit relations and are not deleted as ordinary mutable
files.
