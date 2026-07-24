+++
artifact_id = "DSET-ATOMIC-RECORD-258"
semantic_id = "DSET-REQUIREMENT-META-025"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET layer dependencies form an acyclic graph in which authority and refinement flow forward, later layers consume earlier authority, and feedback cannot create backward governance."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Separating authority flow, dependency direction, specialization, and feedback protects stable layers from volatile downstream mechanisms."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-045"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-023"
+++

# Requirement — Keep layer dependencies acyclic

The ordered layer graph is a directed acyclic graph:

- authority and refinement flow `META → GOV → TOOL → SKILL → IMPL → OPS`;
- a later layer may consume authority from its own or any earlier layer;
- no layer may govern or redefine an earlier layer;
- dependency is distinct from scope specialization and `child_of`;
- peer features interact through explicit Contracts rather than layer
  precedence.

An Observation from a later layer may become input to Exploration Mode. After
explicit acceptance, the result enters the normal forward flow at its proper
owning layer. This feedback is not a backward authority edge.

If backward coupling cannot be deleted, re-homed, or expressed as feedback,
DSET proposes remodeling the coupled owners as horizontal features. The
operator must accept that structural change.
