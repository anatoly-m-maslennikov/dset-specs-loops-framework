# Methodology public contract

## Inputs

- Domain and product decisions accepted by DSET maintainers.
- Evidence from implementation, tests, evals, pilots, and defect repair.
- External sources used as provenance or candidates for adaptation.
- Language/ecosystem evidence used to create or revise applied gate profiles.

## Outputs

- A GitHub-portable public methodology under `methodology/`.
- A repository navigation map in `README.md` and methodology document 00.
- Accepted package truth under `dset/specs/`.
- Bounded, PR-traceable changes under `dset/changes/`.
- Versioned schemas, templates, fixtures, migration guidance, provenance, and generated traceability under `dset/`.
- The `dset` CLI through `python -m dset_toolchain` and an installable console entry point.
- Focused skill sources under `skills/dset-grill/`, `skills/dset-diagnose/`, and `skills/dset-prototype/`.

## CLI compatibility surface

| Command | Contract |
|---|---|
| `dset new` | Create a profile-aware active change without overwrite |
| `dset check` | Read-only structural, ID, portability, provenance, and lifecycle validation |
| `dset verify` | Run `check`, project-configured deterministic gates, and trace freshness |
| `dset trace` | Print by default; write or compare only with explicit flags |
| `dset archive` | Dry-run by default; execute only after archive readiness gates pass |

Stable diagnostic codes, command names, schema version 1.0, and trace ordering are public compatibility surfaces. Human-readable messages and non-contractual examples may improve compatibly.

## Stable document map

| Document | Public responsibility |
|---|---|
| `00` | Pipeline and routing map, including supportability ownership |
| `01` | Spec authoring, including the production supportability contract |
| `02` | Separate deterministic test-plan and qualitative/probabilistic eval-plan authoring, including supportability proof |
| `03` | Implementation planning, supportability milestones, and rollout |
| `04` | General code/runtime pattern catalog, risk-scaled supportability, and applicability |
| `05` | Six language-neutral enforcement categories, applied profiles, and supplemental risk-triggered gates |
| `06` | External grounding and provenance map |

Numbered responsibilities are stable compatibility surfaces. A rename may improve the title, but moving responsibility between documents requires a delta spec, updated links, and explicit migration notes.

## Non-contractual surfaces

Examples, diagrams, and cited candidates may evolve without compatibility guarantees when they do not change a requirement, invariant, artifact shape, or ownership boundary.
