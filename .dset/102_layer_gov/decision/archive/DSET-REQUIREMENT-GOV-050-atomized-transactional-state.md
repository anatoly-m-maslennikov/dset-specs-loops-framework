---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-050"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

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

## Primary claim

Every active lifecycle event, Problem, Question, Decision-family directive, QA claim, analysis report, and promoted evidence record has its own atomic carrier rather than an aggregate ledger or intake queue.
