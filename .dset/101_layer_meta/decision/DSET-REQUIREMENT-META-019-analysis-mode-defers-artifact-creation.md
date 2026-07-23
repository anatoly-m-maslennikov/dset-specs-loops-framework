+++
artifact_id = "DSET-ATOMIC-RECORD-252"
semantic_id = "DSET-REQUIREMENT-META-019"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["project:dset-specs-loops-framework", "layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET Analysis Mode permits brainstorming, research, comparison, and read-only inspection without creating governed artifacts; only explicit operator acceptance ends the mode and authorizes the minimum durable artifacts for accepted conclusions."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Exploration produces overlapping and short-lived candidates. Deferring durable emission until explicit acceptance prevents artifact churn while preserving atomic immutability and clear operator authority."

[promotion]
affected_children = ["governance", "tool", "skill"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-018"
+++

# Requirement — Analysis Mode defers artifact creation

DSET enters Analysis Mode when the operator explicitly requests it or clearly
requests brainstorming, exploration, comparison, or discussion without asking
to record, apply, or implement a conclusion.

While Analysis Mode is active, DSET may:

- inspect the repository and external sources;
- reason, compare candidates, and create transient examples;
- use non-authoritative session state or `.dset_runtime` checkpoints to survive
  compaction or handoff.

It must not:

- create, update, archive, or refresh governed artifacts;
- create governance commits;
- treat intermediate agreement as operator acceptance.

Only an explicit operator instruction to accept, finalize, apply, or end the
analysis closes the mode. Closure separates:

- accepted conclusions, which may become the minimum necessary atomic records;
- rejected candidates, which are discarded;
- unresolved matters, which become durable Questions only when the operator
  accepts them for continued tracking.

Evergreen views may be refreshed only after the accepted atomic records exist.
