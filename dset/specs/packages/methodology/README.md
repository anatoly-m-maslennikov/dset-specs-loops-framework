# Methodology package

**Package ID:** `methodology`

This package owns the accepted behavioral truth for the public DSET methodology. Its implementation surface is the repository [README](../../../../README.md) plus the numbered documents under [`methodology/`](../../../../methodology/).

## Boundary

The package owns stage boundaries, terminology, applicability rules, proof separation, production supportability requirements, enforcement categories, portability rules, and external-grounding integration. It does not yet own executable schemas, validators, utilities, or skills; those become separate packages when implemented and independently meaningful.

## Current-truth files

| File | Ownership |
|---|---|
| [domain.md](domain.md) | Entities, vocabulary, and invariants |
| [spec.md](spec.md) | Accepted behavioral requirements and scenarios |
| [contracts.md](contracts.md) | Public inputs, outputs, document map, and compatibility surface |
| [test-plan.md](test-plan.md) | Deterministic proof obligations |
| [eval-plan.md](eval-plan.md) | Qualitative usability and ambiguity evaluation |

Changes to this package enter through `dset/changes/<change-id>/specs/methodology.md` and become current truth only through verified archival.
