+++
artifact_id = "DSET-ATOMIC-RECORD-212"
semantic_id = "DSET-REQUIREMENT-GOV-064"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "Each DSET project explicitly enables or disables a project prefix in dset_settings.toml, and dset-init selects that setting while recommending no prefix for a single small project and a prefix where multiple project identities share a repository or artifact namespace."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A mandatory project token adds noise without disambiguating a small single-project repository, while an explicit setting preserves collision-free identities for monorepos and multi-project control planes."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-034"
+++

# Requirement — Make the project prefix optional

The project prefix is an explicit identity setting, not an invariant of every
DSET project.

`dset_settings.toml` records:

- whether the project prefix is enabled; and
- the prefix value when enabled.

`dset-init` selects both values. Its default recommendation is:

- disabled for one small project with one artifact namespace; and
- enabled for a monorepo, a repository containing multiple DSET projects, or
  any shared artifact namespace where otherwise-valid IDs could collide.

With the prefix disabled, an ID begins with its artifact kind, such as
`REQUIREMENT-001` or `PROBLEM-TOOL-001`. With the prefix enabled, the same IDs
begin with the configured prefix, such as `APP-REQUIREMENT-001`.

Changing the setting after governed IDs exist requires one complete identity
migration. It updates identities, filenames, relations, lifecycle targets,
evergreen references, implementation references, evidence, and commit
provenance together. It never creates a second accepted identity vocabulary.
