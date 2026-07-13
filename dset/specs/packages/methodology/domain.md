# Methodology domain

## Entities

| Entity | Definition |
|---|---|
| **Framework truth** | Released DSET methodology and framework-owned assets in this public repository |
| **Project truth** | Accepted requirements and proof contracts owned by one adopting project's `dset/specs/` |
| **Package** | A cohesive capability with one vocabulary, specification, public contract, deterministic test plan, and applicable eval plan |
| **Change** | One bounded unit of unaccepted intent and evidence under `dset/changes/<change-id>/` |
| **Requirement** | A stable-ID statement of accepted behavior with at least one scenario or acceptance check |
| **Test plan** | Deterministic proof for exact behavior, contracts, regressions, and machine gates |
| **Eval plan** | Probabilistic or qualitative proof using datasets/cases, criteria, rubrics, thresholds, and calibration |
| **Runtime risk profile** | Selection of recovery and operational semantics triggered by persistence, retry, concurrency, or external effects |
| **Durability topology** | Selection of authoritative files, a local database, or external backing services based on deployment, write volume, and concurrency |
| **Language profile** | Versioned mapping from the six neutral gate categories to language-native tools, scopes, thresholds, and exclusions |

## Invariants

- **METH-INV-001:** Framework truth and project truth never share a writable owner.
- **METH-INV-002:** Deterministic tests and probabilistic/qualitative evals remain separate artifacts and evidence streams.
- **METH-INV-003:** Runtime risk, durability topology, effect safety, and language enforcement are selected explicitly rather than inherited from one universal tool class.
- **METH-INV-004:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **METH-INV-005:** Public methodology renders and navigates on GitHub without Obsidian-only links or callouts.
- **METH-INV-006:** A change cannot alter accepted truth until its proof is fresh and the change is archived through its implementing PR.
