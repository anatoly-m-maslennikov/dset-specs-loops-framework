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
