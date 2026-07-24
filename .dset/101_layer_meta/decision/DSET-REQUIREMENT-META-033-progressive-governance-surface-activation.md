+++
artifact_id = "DSET-ATOMIC-RECORD-266"
semantic_id = "DSET-REQUIREMENT-META-033"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET starts atomic-first without requiring evergreen or maintained governance surfaces, and named optional surfaces may be activated or deactivated later without changing atomic authority."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Small projects should receive immutable authority and traceability without maintaining views or plans whose coordination value has not yet exceeded their cost."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-020"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-029"
+++

# Requirement — Activate governance surfaces progressively

A DSET project begins with atomic authority. Requirements are sufficient for
clear accepted obligations; Questions and Problems remain available whenever
uncertainty or observed discrepancy exists.

No evergreen specification, maintained plan, architecture view, or generated
overview is mandatory merely because DSET is initialized. The operator may
activate a named governance surface when its coordination value becomes useful
and deactivate it later without deleting its carrier or Git history.

Activation adds that surface's currentness and gate obligations. Deactivation
removes those obligations but cannot edit, replace, or weaken atomic authority.
A later reactivation reconciles the retained surface against current atoms
before calling it current.

Revision modes remain semantic classifications; activation applies to named
governance surfaces, not to every artifact sharing a revision mode.
