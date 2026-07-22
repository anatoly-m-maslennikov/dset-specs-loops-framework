+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-009"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Semantic Type migration verification — 2026-07-20

## Proof identity

- **Claim:** DSET executes one flat four-Type semantic model for native atoms
  and preserved legacy IDs without silently editing or retyping historical
  carriers.
- **Intended use:** Support `DSET-DECISION-GOV-008`,
  `DSET-REQUIREMENT-GOV-027`, `DSET-INVARIANT-GOV-004`,
  `DSET-INVARIANT-GOV-017`, `DSET-TEST-GOV-027`, and
  `DSET-TASK-GOV-049`.
- **Producer/performed work:** Canonical Type/subtype module, modern atom and
  artifact-gate reuse, legacy ID/carrier compatibility classifier, layered
  intake schema 1.2, validator diagnostic, expanded stable ID vocabulary,
  traceability and health projections, skill-context routing identity,
  bootstrap regeneration, and deterministic fixtures.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revision:** `115cb22f136c5609c49ae86b54195edc85b28a05`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the evaluated revision and this proof-only
  reconciliation commit.
- **Reopen when:** the four Types, subtype catalog, ID kinds, canonical carrier
  roles, intake schema, atom envelope, trace schema, health model, or skill
  context contract changes.
- **Unsupported uses:** compatibility classification does not convert a legacy
  carrier into a native immutable atom, grant authority, infer acceptance, or
  erase its original status and spelling.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Canonical vocabulary | One shared module owns exactly Decision, Question, Problem, and QA plus one flat direct-subtype catalog | Pass |
| Native atoms | Atom parsing, ID-kind enforcement, sealing, lifecycle, and artifact-gate assessment consume the shared catalog | Pass |
| Legacy compatibility | 233 legacy IDs map to one Type/direct subtype through agreeing stable ID kind and canonical carrier role; no carrier is rewritten | Pass |
| Complete current population | Health reports 242 current semantic claims: 93 Decision-family, 18 Question-family, 15 Problem-family, and 116 QA-family records | Pass |
| Legacy vocabulary | `EVAL` maps to QA/Evaluation; standalone Opportunity maps to Question/Opportunity; all original IDs remain lookup keys | Pass |
| Fail closed | `DSET-E166` rejects ID-kind/carrier mismatch; nested, invalid, and QA-without-subtype native atoms remain rejected | Pass |
| Intake cutover | Schema 1.1 remains readable; schema 1.2 records Question/Problem plus direct subtype and accepts Decision-family resolution links | Pass |
| Trace and health | Traceability publishes normalized classification, carriers, compatibility flag, and lifecycle IDs; health publishes Type/subtype/native/compatibility counts | Pass |
| Skill routing | Resolved local skill context exposes the four-Type identity and current repository counts while retaining project-local governance as owner | Pass |
| Focused gate | 91 semantic, atom, emission, trace, health, runtime, intake, governance, and bootstrap tests passed with Ruff, strict mypy, fresh compilation/health, DSET validation, and diff hygiene | Pass |

Qualitative recognition judgment for newly authored ambiguous claims remains an
Evaluation concern; this proof covers deterministic envelopes, compatibility,
and routing consistency.
