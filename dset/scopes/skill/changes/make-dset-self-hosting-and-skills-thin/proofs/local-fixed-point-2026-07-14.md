# Local fixed-point proof — 2026-07-14

- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject

- Branch: `dev`
- Reconciled local head: `50a5008`
- Released validator baseline: `a95bf7c576c8fcdfdf0565466aaca5ee1fe86157`
- Candidate command: `python -m dset_toolchain check`
- Governance profile: `core-v1@0.2`, customization `unmodified`

## Deterministic results

| Gate | Command or seam | Exit/result |
|---|---|---|
| Formatting | `.venv/bin/ruff format --check dset_toolchain tests` | 0; 25 files formatted |
| Lint | `.venv/bin/ruff check dset_toolchain tests` | 0 |
| Types | `.venv/bin/mypy --strict dset_toolchain tests` | 0; 25 source files |
| Unit/fixture suite | `.venv/bin/python -m unittest discover -s tests -v` | 0; 35 tests |
| Released/candidate fixed point | `.venv/bin/python -m dset_toolchain self-host .` | 0 |
| Project contract | `.venv/bin/python -m dset_toolchain check .` | 0 |
| Canonical aggregate | `.venv/bin/dset verify .` | 0 |
| Diff hygiene | `git diff --check` | 0 |
| `dset-grill` package | Skill Creator `quick_validate.py skills/dset-grill` | 0 |
| `dset-diagnose` package | Skill Creator `quick_validate.py skills/dset-diagnose` | 0 |
| `dset-prototype` package | Skill Creator `quick_validate.py skills/dset-prototype` | 0 |

The shared Skill Creator environment emitted a warning that it could not
create its project-environment lock temporary file. All three validators still
completed with `Skill is valid!`; the warning did not change repository files
or bypass a failed check.

## Fixed-point result

```json
{
  "released_validator": "pass",
  "candidate_repository": "pass",
  "temporary_adopter": "pass",
  "customization": "custom",
  "wrapper_unchanged": true,
  "recursion_stopped": true,
  "released_ref": "a95bf7c576c8fcdfdf0565466aaca5ee1fe86157"
}
```

The released validator checked the candidate repository first. The candidate
then checked this repository, materialized and checked one complete temporary
adopter, detected and explicitly recorded one local rule customization, kept
the wrapper bytes unchanged, and stopped because the adopter has no framework
version contract from which to create another adopter.

## Boundary matrix

The governance and self-host suites prove stable first failures for the
manifest (`DSET-E001`), registry (`DSET-E130`), owner (`DSET-E131`/`E132`),
document (`DSET-E133`), path (`DSET-E134`), dependency (`DSET-E135`), workflow
(`DSET-E136`), applicability/profile (`DSET-E137`), wrapper (`DSET-E138`),
customization identity (`DSET-E139`), released/template boundary (`DSET-E140`),
and candidate command (`DSET-E141`). Justified unselected non-applicability
passes.

## Disposition

Roadmap §§0–§3 and the local portion of §4 pass. Hosted execution of the same
fixed point remains required before `DSET-TASK-TOOL-025` or external-adoption
readiness can pass. `DSET-EVAL-TOOL-001`–`004` remain separate pending evals and
are not implied by these deterministic results.
