+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-001"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Artifact-role lifecycle self-application — 2026-07-20

## Proof identity

- **Claim:** DSET implements and recursively applies the independent artifact-
  role axis, Analysis Report family, five flat Release lifecycle roles,
  type-only default names, and one-level-down architecture views without
  changing its four semantic Types or editing immutable atoms.
- **Intended use:** Support `DSET-DECISION-GOV-009`,
  `DSET-DECISION-OPS-004`, `DSET-REQUIREMENT-GOV-029..031`,
  `DSET-REQUIREMENT-OPS-013`, and `DSET-TASK-GOV-051..053`.
- **Producer/performed work:** Main-session implementation, repository-local
  self-application, generated-adopter template closure, and deterministic
  verification.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revisions:** `be9f54d9ed28d7079517ca81547862a81f18c125`,
  `1a9623e1e0c6f46988058366e4baa77829e19641`, and
  `bd1498f2aebab82827937ae323e8f797ddfd4ff5`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the cited implementation revisions and this
  evidence-only reconciliation commit.
- **Reopen when:** the artifact catalog, path rules, naming setting, Release
  roles, architecture-view obligation, bootstrap contents, or their validators
  change.
- **Unsupported uses:** this proof does not complete the four-semantic-Type
  runtime migration, qualitative Evaluations, project-health or external-
  review tooling, native-host/platform proof, hosted CI, or release publication.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Semantic separation | The four semantic Types remain unchanged; the 13 artifact roles are a separate `artifact_type` axis | Pass |
| Analysis Report | General Analysis Report plus Solution Landscape, Root-Cause Analysis, Proposal, Technical Investigation, and External Audit Analysis templates are registered | Pass |
| Template closure | Every distributed template has one effective direct or path-derived classification; unknown, mismatched, nested, duplicate, and multiply matching classifications fail closed | Pass |
| Release lifecycle | Version Scope, Roadmap, Release Plan, Readiness Record, and Release Record are five flat peers with typed references; DSET owns current Version Scope and Roadmap instances | Pass |
| Naming | Root `dset.toml` defaults new IDs/files to the primary type token; subtype-bearing names are an independent opt-in for new artifacts and never rename stable history | Pass |
| Architecture views | The project and all five enabled DSET layers show exactly their immediate structural children; templates cover project, feature-group, and feature-or-layer levels | Pass |
| Bootstrap | Initializer/adopter materialization includes the project settings, registry, Release templates, and architecture-view templates; the generated bundle digest is fresh | Pass |
| Canonical test gate | `TMPDIR=/tmp .venv/bin/python -m unittest discover -v` ran 157 tests in 92.034 seconds | Pass |
| Static and structural gates | Ruff format/lint, strict mypy, `python -m dset_toolchain check .`, governance rule checks, trace freshness, and `git diff --check` | Pass |

## Bounded observations

Two preliminary sandboxed suite runs redirected temporary work into the
checkout and encountered cleanup contention after otherwise passing test
bodies. The authoritative rerun used the real system temporary directory and
passed all 157 tests. This proof makes no claim that multiple complete suites
may safely share one checkout-local temporary root.

The qualitative `DSET-EVAL-PLAN-GOV-019..021` and `DSET-EVAL-PLAN-OPS-010` runs remain
pending. No placeholder Release Plan, Readiness Record, or Release Record was
created: those artifacts require a real exact release subject or publication
event. `DSET-TASK-GOV-049` remains open for the broader four-Type runtime and
compatibility migration.
