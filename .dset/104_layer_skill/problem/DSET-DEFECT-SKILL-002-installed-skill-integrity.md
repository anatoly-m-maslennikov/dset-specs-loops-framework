+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-064"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-SKILL-002"
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "Installed wrapper and shared-runtime verification accepts post-install content mutation because it reports observed digests without comparing them to a sealed installation identity."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A verifier that authenticates only shape can bless modified executable instructions and code as a valid DSET installation."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-SKILL-011"
+++

# Defect — Installed skill integrity is not authenticated

The installed wrapper verifier accepts a changed `SKILL.md`, and the runtime
verifier accepts changed installed runtime code. Receipts can therefore report
the modified digest as success instead of rejecting drift from the source-bound
installation manifest.

This emitted Problem atom is immutable. Resolution requires implementation,
proof, and an append-only lifecycle event.
