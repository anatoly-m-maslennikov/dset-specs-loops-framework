+++
artifact_id = "DSET-ATOMIC-RECORD-262"
semantic_id = "DSET-REQUIREMENT-META-029"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Profiles specialize downstream realization and applicability without weakening META invariants, redefining routing semantics, or requiring placeholder artifacts for non-applicable concerns."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Profiles must support diverse projects without turning local implementation choices into competing constitutional truth."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-022"
+++

# Requirement — Bound profiles and applicability

A profile may specialize downstream realization for a declared scope. It may
select applicable tools, thresholds, durability behavior, language rules,
artifact governance, proof, or operational mechanisms.

A profile must not:

- weaken or redefine a META invariant;
- change the meaning of a routing axis or layer;
- infer applicability from convenience alone; or
- require dummy artifacts for non-applicable concerns.

Non-applicability is explicit and reasoned. Project settings select allowed
profiles and routes but do not become a second source for their meanings.
