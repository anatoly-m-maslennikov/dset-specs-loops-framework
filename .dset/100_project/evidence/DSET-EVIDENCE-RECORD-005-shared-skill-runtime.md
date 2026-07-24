+++
artifact_type = "evidence_record"
artifact_subtype = "run_record"
artifact_id = "DSET-EVIDENCE-RECORD-005"
child_of = ["DSET-REQUIREMENT-SKILL-011"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Shared skill runtime verification — 2026-07-20

## Proof identity

- **Claim:** One copied, versioned host package supplies deterministic shared
  mechanics for all 16 thin DSET skills and resolves the repository-local
  context belonging to an explicit target.
- **Intended use:** Support `DSET-REQUIREMENT-SKILL-011`,
  `DSET-TEST-PLAN-SKILL-013`, and `DSET-TASK-SKILL-057`.
- **Producer/performed work:** Shared-context implementation, all-wrapper
  migration, runtime-package installation, copied-package execution, and
  deterministic validation.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated revisions:** `47c491b`, `1839602`, and `943b48d`.
- **Observed:** 2026-07-20.
- **Currentness:** current for those implementation revisions and this
  evidence-only reconciliation commit.
- **Reopen when:** the public skill catalog, shared-context schema, host package
  layout, launcher contract, root/Work Area discovery, governance resolver, or
  installation transaction changes.
- **Unsupported uses:** this proof does not claim a real authenticated
  Codex/Claude inference, qualitative `DSET-EVAL-PLAN-SKILL-011`, or successful
  hosted Linux/macOS/native-Windows/WSL execution.

## Deterministic results

| Boundary | Observation | Result |
|---|---|---|
| Shared package | Codex and Claude roots receive one copied `packages/dset` runtime with a versioned manifest and Python, POSIX, and Windows launch adapters | Pass |
| Thin wrappers | All 16 wrappers invoke the same `dset skills context` boundary and contain no shared scripts or project rules | Pass |
| Installed execution | An isolated copied runtime executes `--version` and resolves `dset-implement` from a nested explicit target in a generated adopter | Pass |
| Catalog identity | Every registered skill/workflow pair is accepted; mismatches and unknown entries stop before run creation | Pass |
| Authority discovery | Nested targets resolve one repository/Work Area; competing roots stop; rootless initialization returns a non-writing handoff | Pass |
| Cross-project isolation | Byte-identical wrappers resolve distinct local rule content and rule digests in two generated projects | Pass |
| Installation safety | Preview is non-writing; differing skill or runtime destinations stop; combined installation preflights conflicts before writes | Pass |
| Portability contract | Paths use portable APIs; copied packages contain no symlinks or machine paths; Python, POSIX, and Windows launch surfaces are present | Pass |
| Canonical test gate | `python3 -m unittest discover -s tests` ran 171 tests | Pass |
| Static and structural gates | Ruff, strict mypy, DSET validation, fresh traceability, and diff hygiene | Pass |

Real host discovery/load/invocation receipts and hosted operating-system proof
remain separately owned by `DSET-TASK-SKILL-020` and
`DSET-TASK-TOOL-036`; they are not inferred from these deterministic fixtures.
