+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-003"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-032"
status = "accepted"
priority = "unknown"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Own cross-child truth at the narrowest common scope

When a project enables features, feature groups, or layers, every atomic claim
and compiled artifact must belong to the narrowest structural scope that fully
contains all affected owners and subjects. A claim is not project-level merely
because it is abstract or important.

The project-level artifact set owns only genuinely project-wide concerns:

- project outcomes, user journeys, and high-level requirements that span
  multiple immediate children;
- Contracts, dependency rules, and shared API/data/event semantics between
  children;
- end-to-end Tests and Evaluations whose subject crosses child boundaries;
- cross-cutting Invariants and Constraints such as security, privacy,
  compatibility, supportability, performance budgets, and licensing;
- system architecture, integration topology, version scope, release planning,
  readiness, and publication history for the whole project; and
- cross-owner Decisions, Questions, Problems, Conflicts, Risks, Opportunities,
  and Analysis Reports.

The same rule applies recursively: a concern spanning features inside one
feature group belongs to that group, while a concern spanning groups or layers
belongs to the project. Parent artifacts reference child-owned detail and must
not duplicate it.

## Rationale

The narrowest-common-scope rule keeps global truth complete without turning it
into a parallel copy of every child specification. It also gives cross-boundary
Contracts and end-to-end proof one unambiguous owner.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
