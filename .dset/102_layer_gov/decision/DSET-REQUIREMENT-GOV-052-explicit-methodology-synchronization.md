+++
artifact_id = "DSET-ATOMIC-RECORD-178"
semantic_id = "DSET-REQUIREMENT-GOV-052"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Reusable methodology is authored only in the repository-root source and is copied unidirectionally into the installed .dset methodology only after an explicit operator synchronization command."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Separating authoring from installation keeps ordinary edits bounded, preserves a reviewable installed snapshot, and prevents accidental bidirectional drift."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-022"
+++

# Requirement — Synchronize installed methodology only on command

Framework maintainers edit the reusable methodology only in its repository-root
source. An ordinary source edit never rewrites
`.dset/000_dset_methodology/` and no workflow copies installed files back into
the root source.

An explicit operator synchronization command performs the one-way
root-to-installed refresh. Until that command runs, the installed methodology
remains the last accepted snapshot and may intentionally differ from the
working source.
