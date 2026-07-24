+++
artifact_id = "DSET-ATOMIC-RECORD-215"
semantic_id = "DSET-REQUIREMENT-GOV-067"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "The canonical artifact catalog begins with an in-file legend that defines every shared field and explicitly distinguishes semantic authority from Git-managed carrier changes."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Without a local legend, Boolean fields such as authoritative and changed_through_git are easy to interpret as overlapping authority rules even though they govern different concerns."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-049"
+++

# Requirement — Explain catalog fields in the catalog

The canonical artifact catalog starts with a concise commented legend before
the first group or Type definition. The legend defines every field used by
more than one catalog entry, including its allowed values and its effect.

The two current Boolean fields are independent:

- `authoritative` describes semantic authority. `true` means an artifact of
  that catalog entry may directly establish canonical truth for the concern it
  owns. `false` means the artifact may support, implement, observe, summarize,
  or project authority, but cannot create or override normative project truth
  merely by existing.
- `changed_through_git` describes the mutation channel of the persisted
  carrier. `true` means every addition, replacement, migration, or removal of
  the repository-managed carrier is recorded in a Git commit. It does not make
  Git history the semantic authority and does not relax Atomic Artifact
  immutability: a changed atomic claim still requires a successor artifact.

The catalog must not rely on readers inferring these meanings from field names.
