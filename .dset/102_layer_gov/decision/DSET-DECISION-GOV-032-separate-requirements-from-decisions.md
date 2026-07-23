+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-183"
type = "decision"
semantic_id = "DSET-DECISION-GOV-032"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET uses peer Requirement and Decision Types: Requirements state required results or obligations, while Decisions record material selected implementation, architecture, governance, or operating approaches."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The previous Decision-parent model obscures the practical WHAT-versus-selected-HOW boundary. Peer Types preserve both required truth and the rationale for consequential choices without classifying routine code as authority."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-008"

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-GOV-008"
+++

# Decision — Separate Requirements from Decisions

DSET has five peer semantic Types:

- **Requirement** — required observable results, behavior, capabilities,
  qualities, limits, and obligations;
- **Decision** — a material selected implementation, architecture, governance,
  or operating approach, normally with rationale and alternatives;
- **Question** — unresolved knowledge, interpretation, or choice;
- **Problem** — a currently true insufficiency;
- **QA** — a Test or Evaluation definition.

Constraint, Contract, User Story, Outcome, Scenario, and Invariant are direct
Requirement subtypes. Decision has no subtype. Question, Problem, and QA retain
their current direct subtype sets. No subtype contains another subtype.

Origin does not determine classification. A mandated approach is a Requirement
when the project has no discretion. A project-selected approach is a Decision.
Routine implementation detail remains implementation and does not require an
atom merely because code contains a choice.

This Decision completely replaces `DSET-DECISION-GOV-008`. The predecessor
remains immutable history and is removed from the active authority set through
its append-only absorption event.
