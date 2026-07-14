# Test plan — Add artifact governance profiles

Deterministic tests prove exact behavior. Probabilistic or qualitative proof belongs in [eval-plan.md](eval-plan.md).

| Test ID | Requirement | Deterministic proof |
|---|---|---|
| **ART-TEST-001** | ART-REQ-001 | Project and schema accept separate implementation-language and artifact-profile fields; neither field substitutes for the other |
| **ART-TEST-002** | ART-REQ-002/005 | The artifact registry accepts unique valid areas with existing hubs and rejects missing hubs, duplicate roots, missing parents, and parent cycles with stable diagnostics |
| **ART-TEST-003** | ART-REQ-002/006 | Root README links every registered top-level area hub and each hub contains the required purpose, boundaries, and navigation sections |
| **ART-TEST-004** | ART-REQ-003/004 | The released documentation-v1 profile declares the artifact-type catalog and universal plus specification-specific authoring rules |
| **ART-TEST-005** | ART-REQ-005 | JSON schemas parse; valid/invalid artifact-registry fixtures produce their expected results; `dset check` remains read-only |
| **ART-TEST-006** | All | `dset verify`, Markdown link/portability validation, Ruff, strict mypy, unit tests, trace freshness, and `git diff --check` pass |

## Regression rule

Every validator defect adds a failing unit case or fixture before correction. Do not convert qualitative prose judgments into deterministic checks without a stable structural signal.
