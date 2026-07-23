+++
artifact_id = "DSET-ATOMIC-RECORD-254"
semantic_id = "DSET-REQUIREMENT-META-021"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET Exploration Mode permits brainstorming, discussion, research, analysis, comparison, terminology work, and structural modeling without creating governed artifacts; only explicit operator acceptance ends the mode and authorizes the minimum durable artifacts for accepted conclusions."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Exploration is broader and more provider-neutral than analysis, discussion, or brainstorming alone. It covers divergent and convergent work across every project scope and routing axis while clearly separating candidate thinking from accepted governance."

[promotion]
affected_children = ["governance", "tool", "skill"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-META-019"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-020"
+++

# Requirement — Exploration Mode defers artifact creation

DSET enters Exploration Mode when the operator explicitly requests it or
clearly requests brainstorming, discussion, research, analysis, comparison,
terminology work, scope design, axis design, structural modeling, or other
candidate exploration without asking to record, apply, or implement a
conclusion.

While Exploration Mode is active, DSET may:

- inspect the repository and external sources;
- reason, compare candidates, and create transient examples;
- explore any project scope, route, axis, value, relation, or name;
- use non-authoritative session state or `.dset_runtime` checkpoints to survive
  compaction or handoff.

It must not:

- create, update, archive, or refresh governed artifacts;
- create governance commits;
- treat intermediate agreement as operator acceptance.

Only an explicit operator instruction to accept, finalize, apply, or end the
exploration closes the mode. Closure separates:

- accepted conclusions, which may become the minimum necessary atomic records;
- rejected candidates, which are discarded;
- unresolved matters, which become durable Questions only when the operator
  accepts them for continued tracking.

Evergreen views may be refreshed only after the accepted atomic records exist.
