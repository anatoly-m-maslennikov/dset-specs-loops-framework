+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-068"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-SKILL-004"
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "Wrapper instructions call terminal runtime finish before every handoff, so a successful specialist transition can complete the shared session and force the next skill into a new session."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The command surface contradicts the accepted session-continuity requirement and loses chain identity across the exact handoff it is meant to preserve."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-SKILL-009"
+++

# Defect — Handoff terminalizes the shared session

The wrappers do not distinguish an active handoff from a terminal stop. The
default successful finish completes the session, and the next directly invoked
specialist resolves a different session ID.

This emitted Problem atom is immutable. Resolution requires implementation,
proof, and an append-only lifecycle event.
