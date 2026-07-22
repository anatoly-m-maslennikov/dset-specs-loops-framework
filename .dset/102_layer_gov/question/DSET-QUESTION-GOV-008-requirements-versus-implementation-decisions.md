+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-181"
type = "question"
semantic_id = "DSET-QUESTION-GOV-008"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Should DSET classify observable required results as Requirements and reserve Decisions for selected implementation or governance choices, instead of treating Requirement as a Decision subtype with a broad general Decision fallback?"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The current parent-and-subtype model may hide the practical WHAT-versus-HOW distinction that authors need when converting operator intent into durable artifacts."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-007"

[[relations]]
type = "relates_to"
target = "DSET-DECISION-GOV-008"
+++

# Question — Requirements versus implementation Decisions

Should accepted authority use two plainly distinct concepts?

- **Requirement:** the observable result, behavior, quality, boundary, or limit
  the project must satisfy.
- **Decision:** the selected implementation, architecture, governance, or
  operating approach used to satisfy Requirements.

The unresolved point is whether DSET still needs a general Decision fallback
and a Decision parent family, or whether those structures add ambiguity without
adding useful meaning.
