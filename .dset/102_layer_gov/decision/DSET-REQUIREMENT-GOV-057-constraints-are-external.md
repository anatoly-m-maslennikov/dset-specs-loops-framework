+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-193"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-057"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The Constraint subtype is reserved for externally imposed limitations that the project must obey; operator-selected or project-owned required results use the Requirement subtype."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Separating external limits from required project outcomes makes Requirement and Constraint mutually exclusive and prevents implementation preferences from being mislabeled as unavoidable boundaries."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-033"
+++

# Requirement — Constraints are externally imposed

Use `constraint` only when the limitation originates outside the project's
choice boundary, such as a law, existing DDL, mandated host format, platform
limit, or non-negotiable upstream interface.

Use `requirement` for results the operator or project requires, including
format choices, supported behavior, forbidden project behavior, and quality
targets. A selected implementation approach remains
`implementation_decision`; an interface obligation between internal features
remains `contract`.
