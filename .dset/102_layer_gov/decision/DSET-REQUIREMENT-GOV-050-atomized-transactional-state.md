+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-121"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-050"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every active lifecycle event, Problem, Question, Decision-family directive, QA claim, analysis report, and promoted evidence record has its own atomic carrier rather than an aggregate ledger or intake queue."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]
+++

# Requirement — Atomize transactional state

Current status, active authority, intake, and traceability are derived by
scanning atomic carriers plus settings. `atoms.toml`, `intake.toml`, and
`lifecycle.toml` do not remain active aggregate authorities.

Migration creates one carrier per existing intake item and lifecycle event.
Historical aggregate ledgers may remain only below the explicit root legacy or
migration archive.

## Rationale

An append-only array inside one mutable file still couples unrelated claims and
creates merge, provenance, and ownership ambiguity. One event or claim per
carrier preserves atomicity directly.
