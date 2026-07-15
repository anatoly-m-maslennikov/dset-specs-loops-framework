# FPF principle re-audit — 2026-07-15

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Proof identity

- **Claim:** At corrective commit
  `66eedd2c914c812b16cae2a94faaf53d885a7115`, DSET applies the selected FPF
  reasoning shapes with bounded provenance, separates comparison from selection,
  and self-applies its Decision lifecycle without importing FPF ontology or
  substantial expressive material.
- **Intended use:** Replace the earlier FPF-fidelity Pass claim for the corrected
  governance surfaces; not claim full FPF conformance or release readiness.
- **Producer/performed work:** One independent high-effort subagent re-audit plus
  main-thread evidence review, correction, focused regression tests, rule
  refresh, repository validation, and trace regeneration.
- **Planned method:** Compare the mapped DSET surfaces with the exact cited FPF
  patterns and independently inspect active DSET artifacts for self-application.
- **Performed work/deviations:** The reviewer found that the active Solution
  Landscape still selected candidates and that no neutral Decision carrier was
  used. The corrective loop therefore expanded beyond a read-only recheck into
  authorized DSET-owned governance, template, active-Change, provenance, notice,
  and regression-test edits.
- **Context:** DSET schema 1.2 on local `dev`; FPF checkout and recorded source at
  `afa4936541774021c92adb97c3cbf787bf126062`; observed 2026-07-15.
- **Evidence polarity:** Supporting evidence plus preserved limitations and open
  Questions.
- **Currentness:** Current for the mapped governance, template, provenance,
  notice, and active-Change surfaces at the corrective commit. This proof-only
  record and trace refresh do not alter those inputs.
- **Reopen when:** The cited FPF revision, mapped DSET rule/template, Decision,
  comparison frame, proof contract, provenance schema, or third-party-use
  boundary changes.
- **Unsupported uses:** This proof does not grant an FPF license, accept the open
  evidence-context, Work Area-tag, typed-edge, or Decision-schema Questions,
  validate external adopters, or prove hosted/release readiness.

## Re-audit result

| Principle | Result | DSET disposition |
|---|---|---|
| Claim-bound evidence and defeaters | Pass | Core fields remain mandatory; producer/maintainer separation, planned-versus-performed work, and rival explanations are risk-triggered reliance extensions. |
| Comparison versus selection | Pass after correction | Candidate rows now name comparator/criteria, evidence eligibility, and partial comparison result; adopt/adapt/reject appears only in the Decision. |
| Decision lifecycle and discharge | Pass after correction | A neutral template records status/date/evidence/supersession/reopen/retained/withdrawn/successor fields; `DSET-DECISION-SKILL-001` self-applies it while normative truth remains with owning artifacts. |
| Risk-scaled review | Pass | Baseline gates remain; extra depth follows risk without importing FPF Pattern certification semantics. |
| Derived views | Pass | Reliance-bearing views disclose captured/omitted structure, permitted/prohibited use, canonical return path, and currentness. |
| Lightweight versus durable threshold | Pass | Reversible ordinary work may stay bounded; reliance-bearing work requires durable artifacts. |
| Work Area and evidence context | Intentionally open | Work Areas remain content-neutral; separate context and optional tags remain Questions. |
| Typed relations and schema-enforced Decisions | Intentionally open | No new ontology or schema behavior is accepted without a Decision. |

## Provenance and material boundary

Each FPF mapping now states the adapted/generalized shape and explicit excluded
semantics. Architecture-specific C.32.ADR and FPF-Pattern-specific E.19 are not
presented as semantic equivalents to general DSET Decisions or delivery gates.
The notice boundary states that no substantial expressive passage, template,
code, ontology, index, or Obsidian mechanic is copied; short attributed
technical terms and independently re-expressed concepts are not described by an
inaccurate absolute no-text claim.

## Corrective-loop verification

- `python -m dset_toolchain check .` — pass.
- `python -m dset_toolchain rules check .` — pass after source digest refresh.
- `python -m unittest tests.test_governance -v` — 29 tests pass, including new
  comparison/Decision and bounded-provenance regressions.
- `python -m dset_toolchain trace . --check` — pass after regeneration.
- `git diff --check` — pass.

The earlier [FPF principle audit](fpf-principles-audit-2026-07-15.md) remains
historical evidence of the first review and is not the current Pass authority.
