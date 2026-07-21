+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-002"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-031"
status = "accepted"
priority = "unknown"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Maintain one architecture view per structural level

Every project hub must include a Mermaid view of its immediate enabled
structural children: feature groups when present, otherwise features and/or
layers. Every feature-group hub must show its features. Every feature or layer
hub must show the main functions, capabilities, or components immediately
under it. A level that is not enabled requires no placeholder artifact.

Each view must describe how its level works and how responsibility descends one
level, remain consistent with the linked canonical owners, and avoid claiming
that navigation is authority.

## Rationale

The same one-level-down rule gives operators a helicopter view at every scale
without producing unreadable whole-system diagrams or forcing artificial
feature groups into small projects.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
