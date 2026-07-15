# Local candidate gate — 2026-07-15

## Proof identity

- **Claim:** Candidate `4c08e748ebfca7534e9de285512896e3efe5366d`
  passes the complete local deterministic gate for the implemented 0.3.1
  surface.
- **Intended use:** Support local candidate selection; not hosted, release, or
  adoption-readiness proof.
- **Method/setup:** Run formatting, lint, typing, 78 unit/fixture tests, DSET
  repository and rule validation, bounded self-hosting, generated-trace
  freshness, and Git diff hygiene from a clean `dev` worktree.
- **Context:** Python 3.13 local environment, schema 1.2, observed 2026-07-15.
- **Evidence polarity:** Supporting evidence with one declared degraded
  compatibility boundary.
- **Currentness:** Current for the evaluated implementation and governance
  inputs. This proof record, candidate pointer, and generated-trace refresh do
  not change those inputs.
- **Reopen when:** Runtime, tests, schemas, governing rules, active Change
  behavior, or generated trace inputs change.
- **Unsupported uses:** This does not prove current GitHub checks, published
  validator compatibility, external pilot adoption, runtime evals, archive
  readiness, or release readiness.

## Commands and results

| Gate | Result |
|---|---|
| `uv run ruff format --check dset_toolchain tests` | Pass; 29 files formatted |
| `uv run ruff check dset_toolchain tests` | Pass |
| `uv run mypy dset_toolchain tests` | Pass; 29 source files |
| `python -m unittest discover -s tests -v` | Pass; 78 tests |
| `python -m dset_toolchain check .` | Pass |
| `python -m dset_toolchain rules check .` | Pass |
| `python -m dset_toolchain self-host .` | Candidate repository and temporary adopter pass; recursion stops; released validator reports the registered bootstrap-transition incompatibility |
| `python -m dset_toolchain trace . --check` | Pass |
| `git diff --check` | Pass |

The `uv` invocations emitted a non-fatal project-environment lock warning but
completed successfully. `DSET-PROBLEM-TOOL-001` remains open for the released
validator boundary; `DSET-PROBLEM-OPS-001` remains open for exact-head hosted
proof.
