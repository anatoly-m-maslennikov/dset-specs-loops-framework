# Layered Work Area verification — 2026-07-15

## Proof contract

- Claim: DSET 0.3 defines Work Area as a whole-framework Contract and applies
  it consistently through governance, schemas, CLI behavior, traceability,
  session records, and deterministic tests.
- Intended use: support local review of the layered schema 1.2 migration and
  its monorepo/arbitrary-folder targeting behavior.
- Evaluated candidate: `c95b8b82e9d2cb57119025ab0d4a5f446032ce34`.
- Framework/product/package version: `0.3.0`; schema version: `1.2`.
- Currentness: current for the evaluated candidate and its unchanged inputs.
- Reopen when: the Work Area Contract, project/change/session/run schemas,
  repository layout, target resolution, trace generation, or relevant tests
  change.

## Contract boundary

Work Area is not session scope and is not restricted to a feature, module,
service, deployable, or source-code directory. It is a neutral,
repository-relative boundary usable for local tools, deployables, libraries,
documentation, methodologies, data, tests, automation, or mixed content.
DSET supports a repository-level target or one or more declared Work Areas.
Session continuity consumes the same boundary; it does not redefine or own it.

The repository self-host declaration covers these Work Areas:
`methodology`, `documentation`, `project-control`, `toolchain`, `skills`,
`tests`, and `delivery`.

## Deterministic results

| Gate | Command | Result |
|---|---|---|
| Formatting | `uv run ruff format --check dset_toolchain tests` | Pass; 29 files already formatted |
| Lint | `uv run ruff check dset_toolchain tests` | Pass |
| Types | `uv run mypy dset_toolchain tests` | Pass; 29 source files |
| Unit/fixture suite | `python -m unittest discover -s tests -v` | Pass; 75 tests |
| Project contract | `python -m dset_toolchain check .` | Pass |
| Fixed-point self-host | `python -m dset_toolchain self-host .` | Pass |
| Trace freshness | `python -m dset_toolchain trace . --check` | Pass |
| Diff hygiene | `git diff --check` | Pass |

The `uv` commands emitted a project-environment lock warning but completed
successfully. No check was skipped or converted into a pass.

## Fixed-point result

```json
{
  "released_validator": "pass",
  "candidate_repository": "pass",
  "temporary_adopter": "pass",
  "customization": "custom",
  "wrapper_unchanged": true,
  "recursion_stopped": true,
  "released_ref": "0a5e6c91e3628582d0aad8ba307554b91b1ae802"
}
```

The referenced commit is a clearly labeled schema 1.2 migration baseline, not
a claim that the older published validator supports schema 1.2.
`DSET-PROBLEM-TOOL-001` keeps released-to-candidate assurance degraded until a
compatible published validator checks a later candidate or an accepted
compatibility proof closes the gap.

## Limits and disposition

The deterministic checks prove the Work Area contract and its current tooling
implementation. They do not prove the pending qualitative eval, hosted
exact-SHA checks, native platform matrix, or end-to-end session resume after
context compaction. Session continuity currently has governance, schemas, and
tests; its runtime resume implementation remains pending. The active Change is
therefore not archive-ready or adoption-ready.
