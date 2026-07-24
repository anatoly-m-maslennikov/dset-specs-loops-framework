---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-068"
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
      - "DSET-REQUIREMENT-GOV-067"
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-049"
---

# Requirement — Name the catalog truth-owner field literally

The canonical artifact catalog uses:

```toml
source_of_truth = true
```

or:

```toml
source_of_truth = false
```

The opening legend defines the values:

- `true`: an artifact of this catalog entry is the canonical source of truth
  for the concern it explicitly owns;
- `false`: the artifact is derived, supporting, executable, observational, or
  navigational for that concern and does not replace its declared source of
  truth.

Source-of-truth ownership is concern-specific. An artifact does not become the
source of truth for unrelated concerns merely because this field is `true`.

`changed_through_git` remains a separate carrier-governance field. It describes
how a persisted file changes, not whether the file owns semantic truth.

## Primary claim

The canonical artifact catalog uses source_of_truth as the Boolean field that states whether an artifact is the canonical truth owner for its declared concern, and defines that field in the catalog's opening legend.

## Rationale

The field name authoritative is broader and less literal than the intended source-of-truth classification.
