+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-006"
child_of = ["DSET-REQUIREMENT-GOV-035"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Artifact-emission gate verification — 2026-07-20

## Proof identity

- **Claim:** DSET applies project-selected medium/high artifact-creation
  strictness, blocks material ambiguity with focused questions, and proposes
  eligible one-step broader-scope placement without emitting or promoting.
- **Intended use:** Support `DSET-REQUIREMENT-GOV-035`,
  `DSET-TEST-PLAN-GOV-035`, and `DSET-TASK-GOV-058`.
- **Producer/performed work:** Settings parser, deterministic read-only gate,
  CLI integration, skill-context propagation, governance compilation,
  bootstrap regeneration, and repository validation.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revision:** `5e4f2c0`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the evaluated implementation and this
  evidence-only reconciliation commit.
- **Reopen when:** settings schema, semantic Type catalog, structural scope
  hierarchy, emission fields, promotion rules, CLI contract, or governing
  artifact-maintenance rule changes.
- **Unsupported uses:** this proof does not claim the independent qualitative
  `DSET-EVAL-PLAN-GOV-025`, operator acceptance of any proposed promotion, or that a
  successful assessment itself authorizes a write.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Settings | Missing strictness defaults to `medium`; root/template explicitly select `medium`; only `medium` and `high` are accepted | Pass |
| Medium gate | Explicit authority, one claim, Type, scope, provenance, material links, and promotion assessment pass while non-material optional unknowns remain visible | Pass |
| High gate | Missing boundary, priority, lineage, acceptance, conflict state, or verification obligation blocks with one focused question per field | Pass |
| Material ambiguity | A material unknown blocks at either strictness and retains its focused question | Pass |
| Type integrity | Unknown Types/subtypes and empty-subtype QA stop before emission | Pass |
| Promotion | Only immediate feature-to-group/project, group-to-project, and layer-to-project candidates are considered; eligible promotion requires `keep_local` or `promote` operator disposition | Pass |
| No automatic write | Assessment always reports `writes_performed: false`; `promote` requires a newly assessed broader-scope candidate | Pass |
| Runtime handoff | Shared skill context returns the project-selected strictness to every governed wrapper | Pass |
| Canonical test gate | `python3 -m unittest discover -s tests` ran 177 tests | Pass |
| Static and structural gates | Ruff, strict mypy, DSET validation, fresh traceability, and diff hygiene | Pass |
