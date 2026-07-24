+++
artifact_id = "DSET-ATOMIC-RECORD-255"
semantic_id = "DSET-REQUIREMENT-META-022"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "META owns only invariants that remain valid across downstream technologies, govern multiple layers or a layer boundary, and can be stated without importing downstream implementation vocabulary."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A stable constitutional layer must govern later layers without accumulating volatile Git, language, CLI, host, provider, or deployment mechanisms."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false
+++

# Requirement — Apply the META eligibility rule

A rule belongs in META only when all three conditions hold:

1. it remains true when downstream languages, tools, hosts, providers, and
   repository layouts change;
2. it governs multiple layers or defines a boundary between layers; and
3. it can be stated without importing downstream implementation concepts.

If any condition fails, place the rule in the earliest downstream layer that
can own it completely. META owns the invariant; that layer owns the mechanism.

For example, META may require durable changes to be traceable. GOV or TOOL owns
the Git carrier and executable enforcement. META must not absorb those
mechanisms merely because several later layers use them.
