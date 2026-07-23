+++
artifact_id = "DSET-ATOMIC-RECORD-204"
semantic_id = "DSET-GAP-TOOL-004"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
authority = "agent:codex"
claim = "The current conflict runtime reads the legacy priority scale and does not yet enforce assignable priorities, scope/layer comparison bonuses, virtual highest, legacy normalization, or conflict_resolution.mode."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Publishing settings without executable consumption would make ask_always appear protective while the existing resolver can still select through its older priority-list behavior."

[promotion]
affected_children = ["tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-058"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-059"
+++

# Gap — Derived-priority conflict handling is not executable yet

The current Tool resolver compares the direct `priority.scale` ordering and
does not read the new assignment scale, legacy aliases, scope bonus, layer
bonus, virtual cap, or conflict-selection mode.

Resolution requires updating settings validation and the conflict resolver,
adding deterministic comparison traces, making `ask_always` return an operator
decision request without selecting a normative winner, and covering unique,
tied, same-level, incomparable, legacy, and unsatisfiable cases. Until then,
the settings and GOV rules are authoritative design, not executable proof.
