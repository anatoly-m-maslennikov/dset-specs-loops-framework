+++
artifact_id = "DSET-ATOMIC-RECORD-216"
semantic_id = "DSET-REQUIREMENT-GOV-068"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "The canonical artifact catalog uses source_of_truth as the Boolean field that states whether an artifact is the canonical truth owner for its declared concern, and defines that field in the catalog's opening legend."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The field name authoritative is broader and less literal than the intended source-of-truth classification."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-067"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-049"
+++

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
