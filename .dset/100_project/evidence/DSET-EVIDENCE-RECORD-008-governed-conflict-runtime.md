+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-008"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Governed conflict runtime verification — 2026-07-20

## Proof identity

- **Claim:** DSET classifies governed incompatibilities by role and lifecycle
  before priority, emits immutable Conflict atoms only for genuine authority
  conflicts, invalidates stored dispositions when their effective basis
  changes, and preserves retired atoms byte-for-byte with stable lookup.
- **Intended use:** Support `DSET-DECISION-GOV-003`,
  `DSET-DECISION-GOV-010`, `DSET-REQUIREMENT-GOV-020`,
  `DSET-REQUIREMENT-GOV-026`, `DSET-REQUIREMENT-TOOL-019`,
  `DSET-TEST-PLAN-GOV-026`, and `DSET-TEST-PLAN-TOOL-019`.
- **Producer/performed work:** Deterministic resolver, atom emission and
  sealing, append-only lifecycle integration, result freshness check,
  retirement archive move, traceability/health propagation, schemas, CLI,
  and focused tests.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revision:** `6b8aa6955fdf4c534c2f43d6e5071ccdbc2fd0f5`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the evaluated revision and this proof-only
  reconciliation commit.
- **Reopen when:** the governed role set, priority scale/inheritance,
  lifecycle vocabulary, atom schema, conflict eligibility, selection policy,
  trace schema, health model, or archive condition changes.
- **Unsupported uses:** this evidence does not prove that every future project
  supplies correct conflict context, that priority can satisfy incompatible
  immutable external obligations, or that an unresolved Conflict is safe to
  auto-resolve.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Role matrix | All 81 ordered pairs from the nine governed roles return a stable non-empty class and disposition | Pass |
| False Conflicts | Source/projection drift, assurance changes, implementation nonconformance/ownership, evidence adjudication, generated staleness, and inapplicable contexts do not emit Conflict atoms | Pass |
| Authority Conflicts | Comparable authority pairs use explicit precedence before higher effective priority; equal, unknown, incomparable, nonselectable, or mutually immutable cases stop | Pass |
| First-class carrier | Explicit `--emit` applies the project artifact gate, writes one `question/conflict` atom with both parties in `child_of`, and seals its ID/content digest | Pass |
| Resolution evidence | JSON results bind raw input and effective resolution-basis digests; `--check-result` rejects reprioritized or otherwise changed inputs | Pass |
| Lifecycle | Later state uses append-only events; no conflict path edits an emitted atom | Pass |
| Retirement archive | Only explicitly retired atoms without active child reliance move to adjacent `archive/`; bytes and semantic ID stay unchanged and canonical ledger lookup updates | Pass |
| Derived views | Traceability exposes type/subtype, lifecycle events, current/effective priority source, absorption, archive lookup, and implementation edges; health exposes open and resolved Conflict states | Pass |
| Focused gate | 60 conflict, atom, traceability, health, governance, and bootstrap tests passed with Ruff, strict mypy, compilation/health freshness, DSET validation, and diff hygiene | Pass |

This proof closes the deterministic implementation scope. Qualitative policy
usefulness remains owned by the existing Evaluation plan and its current
evidence boundary.
