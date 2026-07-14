# Design — Executable DSET v1

## Public surfaces

```text
dset/                         committed project truth and released assets
├── dset.yaml                 project configuration
├── traceability.yaml         generated committed index
├── schemas/                  JSON Schemas
├── templates/                change and package templates
├── fixtures/                 pass/fail contract examples
├── migrations/               one-root migration guidance
├── specs/                    accepted project truth
└── changes/                  active and archived changes

dset_toolchain/               dependency-light Python package
skills/                       repository-native Codex skill sources
tests/                        CLI and contract regression tests
```

## CLI boundaries

- `new` is the only scaffolding writer and refuses an existing destination.
- `check` is read-only and reports stable diagnostic codes.
- `verify` runs repository validation, tests configured by this repository, link/portability checks, and trace freshness without changing source artifacts.
- `trace` prints the proposed deterministic index by default; `--write` updates it and `--check` compares without writing.
- `archive` validates first, prints a plan by default, and requires `--execute` for the atomic directory move. It never contacts GitHub or predicts a merge SHA.

## Parsing and portability

The canonical implementation uses Python's standard library. The YAML reader supports the documented DSET subset: indentation-based mappings, scalar lists, inline empty lists/maps, booleans, nulls, numbers, and strings. Published JSON Schemas describe the same semantic contract for external validators. Paths use `pathlib`; subprocess calls use argument lists; outputs use UTF-8 and stable ordering.

## Authority boundaries

| Concern | Authority |
|---|---|
| Accepted behavior | `dset/specs/` |
| Active intent and evidence | `dset/changes/<change-id>/` |
| PR state, checks, diffs, merge result | GitHub |
| Generated relationship view | `dset/traceability.yaml` |
| Local caches | optional `.dset/`; never committed truth |

Traceability stores repository-qualified PR evidence but does not replace GitHub. The GitHub-hosted delivery workflow is a production automation surface, so its supportability contract uses PR/check/run/ruleset identities rather than a local WAL.

## Package boundary

The toolchain remains an implementation surface of the `methodology` package for v1. A separate package becomes justified after external adoption creates an independently versioned API or release cadence.
