+++
artifact_id = "DSET-ATOMIC-RECORD-261"
semantic_id = "DSET-REQUIREMENT-META-028"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET keeps authoritative claims, checking methods, implementations, observations, evidence, and verification judgments semantically distinct, and assurance cannot establish or override authority."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Evidence can be canonical for an observation without becoming the authority for desired behavior, implementation policy, or project scope."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Separate authority from assurance

DSET distinguishes:

- authoritative Definitions and Methods;
- maintained and generated Implementations;
- Test and Evaluation Methods;
- execution Observations and Evidence;
- Verification judgments about sufficiency and currentness.

Tests, Evaluations, Evidence, dashboards, and Verification may support,
challenge, or invalidate reliance on a claim. They cannot establish, edit,
replace, or override semantic authority. An assurance failure creates feedback
for the appropriate owner rather than silently changing the governing claim.
