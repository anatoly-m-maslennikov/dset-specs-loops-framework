# Methodology package

**Package ID:** `methodology`

This package owns the accepted behavioral truth for the public DSET methodology. Its implementation surface is the repository [README](../../../../README.md) plus the numbered documents under [`methodology/`](../../../../methodology/).

## Boundary

The package owns stage boundaries, terminology, applicability rules, proof separation, production supportability requirements, enforcement categories, portability rules, external-grounding integration, and the v1 executable contract. Schemas, templates, the CLI, fixtures, migration guidance, and focused skills are implementation surfaces of this package until external adoption gives one of them an independently versioned public boundary.

## Current-truth files

| File | Ownership |
|---|---|
| [domain.md](domain.md) | Entities, vocabulary, and invariants |
| [spec.md](spec.md) | Accepted behavioral requirements and scenarios |
| [contracts.md](contracts.md) | Public inputs, outputs, document map, and compatibility surface |
| [test-plan.md](test-plan.md) | Deterministic proof obligations |
| [eval-plan.md](eval-plan.md) | Qualitative usability and ambiguity evaluation |
| [package.yaml](package.yaml) | Machine-readable package and proof-ID registry |

Changes to this package enter through `dset/changes/<change-id>/specs/methodology.md` and become current truth only through verified archival.
