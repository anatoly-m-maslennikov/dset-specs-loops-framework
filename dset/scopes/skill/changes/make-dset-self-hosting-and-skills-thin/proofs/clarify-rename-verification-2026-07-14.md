# Clarify workflow rename verification — 2026-07-14

## Subject

- Canonical skill: `skills/dset-clarify/`
- Canonical workflow: `domain-clarification`
- Deprecated identities: `dset-grill`, `domain-grilling`
- Candidate profile: `core-v1@0.2`

The rename changes the unreleased 0.2 candidate surface without changing the
domain-clarification behavior or its repository-owned rule set. Archived v1
evidence and literal upstream provenance retain their historical names.

## Deterministic results

| Check | Result |
|---|---|
| Red test before registry/package rename | `domain-clarification` failed with `DSET-E136` as expected |
| `dset rules resolve domain-clarification --format json` | Pass; resolves `dset-clarify` and the ordered local rule set |
| Deprecated `domain-grilling` workflow | Fails closed with `DSET-E136` |
| Wrapper identity | Registered SHA-256 matches `skills/dset-clarify/SKILL.md` |
| Skill refactor audit | 20-line skill, two files, no scripts or local state |
| Skill Creator validation | `Skill is valid!` |
| Bounded self-hosting | Released validator, candidate, framework, adopter, mutation, wrapper, and recursion checks pass |
| Canonical verification | 37 tests plus Ruff, strict mypy, repository checks, trace freshness, and diff hygiene pass |

The shared validation environment emitted its known temporary-lock warning;
all commands completed successfully.

## Migration disposition

Adopters of the unreleased candidate replace the wrapper directory and registry
workflow/path together, then run `dset rules check`. No compatibility alias is
installed because a hidden fallback would violate fail-closed resolution. The
migration guide records this transaction.
