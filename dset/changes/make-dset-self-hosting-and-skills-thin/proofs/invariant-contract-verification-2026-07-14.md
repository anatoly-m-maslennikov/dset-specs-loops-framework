# Invariant contract verification — 2026-07-14

## Scope

This evidence covers only the DSET 0.2 invariant-contract batch. It verifies stable ownership, requirement, scenario, test, and eval mappings and the integrity of the current repository. It does not claim that the planned governance resolver, materializer, thin wrappers, recursive self-hosting runner, TypeScript profile, or adopter pilots are implemented.

## Contract identity

- Roadmap invariants: `DSET-INVARIANT-TOOL-001..002`, `DSET-INVARIANT-GOV-001..004`, `DSET-INVARIANT-SKILL-001..002`, and `DSET-INVARIANT-META-001`
- Candidate change requirements: `DSET-REQUIREMENT-TOOL-006..007`, `DSET-REQUIREMENT-GOV-007..010`, `DSET-REQUIREMENT-SKILL-002..003`, and `DSET-REQUIREMENT-META-005`
- Candidate deterministic proof: `DSET-TEST-TOOL-009..011`, `DSET-TEST-GOV-009..011`, `DSET-TEST-SKILL-002..003`, and `DSET-TEST-META-004`
- Candidate qualitative proof: `DSET-EVAL-TOOL-001..002`, `DSET-EVAL-SKILL-002`, and `DSET-EVAL-GOV-009`
- Candidate accepted invariants: `METH-INV-013`–`METH-INV-021`
- Candidate accepted requirements: `METH-REQ-026`–`METH-REQ-034`
- Candidate accepted deterministic proof: `METH-TEST-027`–`METH-TEST-035`
- Candidate accepted qualitative proof: `METH-EVAL-015`–`METH-EVAL-018`

## Deterministic results

| Check | Result | Bounded evidence |
|---|---|---|
| Canonical structural validation | Pass | `python -m dset_toolchain check .` returned `DSET validation passed` throughout the edit sequence |
| Full current toolchain | Pass | `.venv/bin/dset verify .` with `UV_CACHE_DIR` set to a writable cache outside the repository reported 19 Python files formatted, clean Ruff, clean mypy, 18/18 unit tests passing, fresh traceability, and `DSET validation passed` |
| Diff hygiene | Pass | `git diff --check` returned no output |
| Accepted package ID counts | Pass | 34 requirements, 35 deterministic tests, and 18 qualitative evals are present and registered |
| Invariant counts | Pass | The accepted methodology has 21 invariants including the nine new IDs; the roadmap retains exactly nine DSET 0.2 invariants |
| Capability-claim audit | Pass | Every unimplemented 0.2 mechanical seam is labeled `Planned`; the active change is `in-progress`, its PR is `pending`, and its verification status says the mechanics are not implemented |

The first direct `uv run dset verify .` attempt could not use the sandbox-denied user cache. Running the same repository commands through the existing project environment with a writable cache produced the passing result above; `uv` emitted non-blocking project-lock warnings but every configured command completed successfully.

## Disposition

The invariant contract is internally consistent and ready to govern later 0.2 implementation batches. `DSET-TEST-TOOL-009..011`, `DSET-TEST-GOV-009..011`, `DSET-TEST-SKILL-002..003`, `DSET-TEST-META-004`, `DSET-EVAL-TOOL-001..002`, `DSET-EVAL-SKILL-002`, and `DSET-EVAL-GOV-009` remain planned proof obligations and must not be marked passing until their corresponding mechanics and fixtures exist.
