# Deterministic verification — 2026-07-14

## Subject

- Repository: `anatoly-m-maslennikov/dset-specs-loops-framework`
- Branch: `dev`
- Verified pushed head: `c8e1e717215049b0bd119d5f529480be5c0668b8`
- Implementing PR: [#8](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/8)
- Selected implementation-language profile: `python-v1`
- Selected artifact-governance profile: `documentation-v1`
- Canonical command: `python -m dset_toolchain verify .`
- Locked repository entry point used: `uv run dset verify .`

## Fresh results

| Gate | Command | Exit | Bounded result |
|---|---|---:|---|
| Artifact schema syntax | `python -m json.tool dset/schemas/artifacts.schema.json` | 0 | JSON parsed |
| Formatting | `uv run ruff format --check dset_toolchain tests` | 0 | 19 files already formatted |
| Lint | `uv run ruff check dset_toolchain tests` | 0 | All checks passed |
| Strict typing | `uv run mypy dset_toolchain tests` | 0 | No issues in 19 source files |
| Unit and fixture suite | `python -m unittest discover -s tests -v` | 0 | 18 tests passed |
| Artifact-profile cases | `python -m unittest tests.test_artifact_profile -v` | 0 | Seven valid/invalid registry and hub cases passed |
| Contract validation | `python -m dset_toolchain check .` | 0 | DSET validation passed |
| Canonical aggregate | `uv run dset verify .` | 0 | Both selected profiles and trace freshness passed |
| Patch hygiene | `git diff --check` | 0 | No whitespace errors |

## Test-plan coverage

| Test ID | Evidence |
|---|---|
| ART-TEST-001 | `dset/dset.yaml` selects both profile axes; the project schema permits the optional artifact profile without replacing language enforcement |
| ART-TEST-002 | Artifact-profile unit cases reject missing hubs, duplicate roots, unresolved parents, and parent cycles with DSET-E121/E122 |
| ART-TEST-003 | Unit cases enforce required hub sections and root-to-top-level-area navigation with DSET-E123 |
| ART-TEST-004 | The documentation hub links the published architecture, type catalog, universal/type-specific authoring rules, hub rules, maintenance procedure, and rationale |
| ART-TEST-005 | The artifact registry and JSON Schema parse; `dset check` validates the active repository without writing |
| ART-TEST-006 | The complete Python-format/lint/type/test profile, documentation profile, Markdown portability checks, trace freshness, and diff hygiene passed together |

## Corrective loops

The first profile wording claimed deterministic rejection of machine-local paths, but the repository has legitimate historical evidence that records an evaluator environment. The applied profile was narrowed to the portable signals the validator actually owns: resolvable local links, GitHub alerts/details, and rejection of wiki links. Public authoring still avoids machine-specific dependencies; historical evidence may identify an environment without becoming a runtime dependency.

The first local `uv` run was blocked from its existing user cache by the restricted evaluator sandbox. The same locked command passed when granted access to the already-installed cache. Hosted CI remains the independent pushed-head execution environment.

## Data handling

This proof retains commands, public commit/PR identities, exit states, and bounded summaries only. It contains no tokens, environment values, or sensitive raw logs.
