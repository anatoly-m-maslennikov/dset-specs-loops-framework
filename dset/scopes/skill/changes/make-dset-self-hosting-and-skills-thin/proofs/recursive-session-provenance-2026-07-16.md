# Recursive session-provenance self-application — 2026-07-16

## Proof identity

- **Claim:** DSET recursively applies its explicit LLM-session provenance rule
  to the framework repository and to the bounded generated adopter without
  making provenance authoritative or recursing indefinitely.
- **Intended use:** Support `DSET-REQUIREMENT-GOV-022`,
  `DSET-TEST-GOV-022`, and `DSET-TASK-GOV-041`; not certify hosted delivery,
  external pilots, or the pending runtime implementation.
- **Producer/performed work:** Main-thread repository audit, schema/template/
  validator implementation, retroactive material-review backfill, deterministic
  verification, and bounded self-host execution.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Method/setup:** Resolve the current repository-owned lifecycle rules; audit
  every supported atomic-artifact surface; enforce explicit provenance through
  schemas, templates, and `DSET-E155`; run canonical verification; then run the
  candidate validator on this repository and one generated adopter.
- **Evaluated DSET commit:**
  `df49da0111d86408e1dd919570bfc2f42a9867ec`.
- **Observed:** 2026-07-16.
- **Evidence polarity:** supporting with a declared released-validator
  bootstrap limitation.
- **Currentness:** current for the exact evaluated commit and the evidence-only
  record/verification update that contains this proof.
- **Reopen when:** Change/intake/Decision/proof/run/checkpoint provenance shape,
  the YAML subset, `DSET-E155`, the canonical verification commands, or bounded
  self-host behavior changes.
- **Unsupported uses:** this proof does not show that the released validator
  understands schema 1.2, that current hosted GitHub checks pass, that external
  pilots adopted DSET, or that the planned skill-run/checkpoint runtime exists.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Evergreen compile-down | Accepted GOV and SKILL specs, proof plans, governing rules, implementation plan, and task ledger describe the explicit provenance shape | Pass |
| Transactional self-application | Five Change manifests, 25 intake items, three Decisions, and 26 pre-existing promoted proofs carry the material-review session ID | Pass |
| Planned runtime records | Skill-run schema 1.2 and checkpoint schema 1.1 require bounded unique host-prefixed `llm_session_ids`; human-only work uses an explicit empty list | Pass |
| Failure contract | Missing or malformed Change/intake provenance and missing Decision/proof fields produce stable `DSET-E155`; Markdown `none` is accepted only as an explicit human-only disposition | Pass |
| YAML transport | Host-prefixed IDs and HTTPS URLs round-trip as list scalars rather than inline mappings | Pass |
| Canonical gate | Formatting, Ruff, mypy, 83 tests, DSET validation, trace freshness, and diff hygiene pass | Pass |
| Commit provenance | The evaluated commit body contains `Implements: DSET-DECISION-GOV-001` and the contributing Codex session | Pass |
| Recursive candidate | Candidate repository and temporary adopter pass; wrapper remains unchanged; local customization is detected; recursion stops after the adopter | Pass |

## Bounded limitation

The released validator remains a declared `bootstrap-transition` because it
predates the current schema 1.2 repository layout. That is the existing
`DSET-PROBLEM-TOOL-001`, not a failure of the candidate or adopter checks.
Hosted exact-head evidence and external-pilot adoption also remain open under
their existing Problems; this local proof does not upgrade those claims.
