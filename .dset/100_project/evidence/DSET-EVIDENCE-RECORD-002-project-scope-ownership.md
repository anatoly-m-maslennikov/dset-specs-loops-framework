+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-002"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Project-scope ownership self-application — 2026-07-20

## Proof identity

- **Claim:** DSET defines and recursively applies narrowest-common-scope
  ownership so project-level truth owns cross-child concerns without copying
  child-owned detail.
- **Intended use:** Support `DSET-REQUIREMENT-GOV-032`,
  `DSET-INVARIANT-GOV-022`, `DSET-TEST-PLAN-GOV-032`, and
  `DSET-TASK-GOV-054`.
- **Producer/performed work:** Main-session Requirement emission, compile-down,
  DSET layer self-application, bootstrap refresh, and deterministic validation.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revision:** `2a85b0d`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the exact evaluated revision and this evidence-
  only reconciliation commit.
- **Reopen when:** the project/group/feature/layer ownership algorithm,
  structural metadata, architecture templates, cross-child artifact boundary,
  or applicable validator changes.
- **Unsupported uses:** this proof does not claim executable feature-group or
  feature allocation, qualitative reviewer agreement, hosted CI, or external-
  adopter evidence.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Atomic authority | Immutable `DSET-ATOMIC-RECORD-003` owns accepted `DSET-REQUIREMENT-GOV-032` with session provenance and rationale | Pass |
| Ownership algorithm | Canonical specs and architecture governance require the narrowest common structural ancestor; importance, abstraction, and reuse do not promote a claim | Pass |
| Global responsibilities | Cross-child outcomes/requirements, Contracts/shared semantics, end-to-end QA, cross-cutting policy, integration architecture, whole-project release/readiness, and cross-owner work have explicit ownership | Pass |
| Anti-duplication | Parent artifacts link child-owned details and may not restate them as parallel truth | Pass |
| Recursive DSET application | The root owns cross-layer concerns and the five layer hubs/spec fragments continue to own layer-local behavior | Pass |
| Distribution | The materialized governance template and generated bootstrap bundle carry the same rule | Pass |
| Canonical test gate | `TMPDIR=/tmp .venv/bin/python -m unittest discover -v` ran 158 tests in 94.121 seconds | Pass |
| Static and structural gates | Ruff format/lint, strict mypy, DSET/rule validation, trace freshness, and diff hygiene | Pass |

## Bounded limitation

The current repository exercises the project-to-layer case. Feature-group and
feature behavior is normatively specified and covered by reusable architecture
templates, but executable feature/group allocation fixtures remain pending
until those optional structural modes have runtime scaffolding. The qualitative
`DSET-EVAL-PLAN-GOV-022` reviewer-placement run also remains pending.
