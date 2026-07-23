+++
artifact_id = "DSET-ATOMIC-RECORD-228"
semantic_id = "DSET-QUESTION-GOV-011"
revision_mode = "atomic"
content_role = "inquiry"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Should DSET replace semantic compilation into evergreen specifications and plans with governed atomic refactoring that creates corrected, consolidated, or extended successor atoms and archives only the fully replaced predecessors?"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Making the active atomic set the complete current specification could remove a competing truth layer, but it also changes how skills consume project truth and how long-form specifications, plans, and release snapshots are represented."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-048"

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-001"
+++

# Question — Should active atoms replace evergreen compilation?

The proposed model makes the active Atomic Artifact set the complete current
governing truth:

1. New meaning is recorded in new immutable atoms.
2. Redundant, incorrect, or outdated atoms are replaced by new atoms.
3. Fully replaced atoms move to the archive.
4. Typed successor relations preserve provenance and semantic history.
5. Generated indexes and dashboards may summarize the active set but never
   become a second normative truth layer.

The decision must settle whether DSET eliminates the evergreen artifact class
or retains non-authoritative specification and plan views for human and LLM
consumption.

Any accepted replacement model must preserve the one-primary-claim invariant.
Several old atoms may be consolidated only when their successor still owns one
independently reviewable claim. Otherwise, the refactoring emits several
linked successor atoms.
