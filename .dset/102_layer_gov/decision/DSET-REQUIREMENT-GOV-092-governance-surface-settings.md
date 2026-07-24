+++
artifact_id = "DSET-ATOMIC-RECORD-267"
semantic_id = "DSET-REQUIREMENT-GOV-092"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "dset_settings.toml owns an explicit boolean activation state for every registered optional governance surface, with every surface inactive by default and deactivation preserving carriers and history."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "One documented settings owner makes progressive activation deterministic while preserving the distinction between semantic revision mode and optional governance participation."

[promotion]
affected_children = ["tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-META-033"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-049"
+++

# Requirement — Store governance-surface activation

`.dset/dset_settings.toml` owns one documented `governance_surfaces` table.
Every registered surface has one explicit boolean:

- `evergreen_specification`;
- `test_plan`;
- `evaluation_plan`;
- `implementation_plan`;
- `project_overview`; and
- `architecture_view`.

All values default to `false`. Missing configuration reads as the same
atomic-first default. Unknown surface names fail closed.

Activation makes the selected surface applicable to currentness and downstream
gates. Deactivation removes those obligations without deleting or archiving an
existing carrier. Retained files become inactive references until a later
reactivation reconciles them against current atomic authority.
