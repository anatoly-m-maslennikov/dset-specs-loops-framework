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
| **Production supportability contract** | Risk- and topology-scaled agreement for the evidence, correlation and deploy/change identity, safe diagnostics, data controls, runbook, recovery/escalation paths, and incident-to-fix traceability needed to investigate and repair production behavior |
| **DSET toolchain** | The dependency-light CLI, schemas, templates, fixtures, traceability generator, migration guidance, CI gate, and focused skills that execute the accepted methodology contract |
| **Diagnostic** | A stable code, artifact path, and actionable message emitted by a deterministic DSET gate |
| **Traceability index** | A deterministic committed view from changes to packages, requirements, tests, evals, ADRs, evidence, and repository-qualified PRs; it is derived evidence rather than the owner of GitHub state or code diffs |
| **Hosted delivery automation** | GitHub workflows and rulesets that govern the repository's production publication path and use GitHub PR/check/run/commit identities as authoritative operational evidence |

## Invariants

- **METH-INV-001:** Framework truth and project truth never share a writable owner.
- **METH-INV-002:** Deterministic tests and probabilistic/qualitative evals remain separate artifacts and evidence streams.
- **METH-INV-003:** Runtime risk, durability topology, effect safety, and language enforcement are selected explicitly rather than inherited from one universal tool class.
- **METH-INV-004:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **METH-INV-005:** Public methodology renders and navigates on GitHub without Obsidian-only links or callouts.
- **METH-INV-006:** A change cannot alter accepted truth until its proof is fresh and the change is archived through its implementing PR.
- **METH-INV-007:** Every production-bound tool has an explicit supportability contract scaled to its risk profile and topology; a non-production tool may mark it not applicable only with a reason.
- **METH-INV-008:** The canonical validator is read-only; scaffolding, trace updates, and archival require explicit write commands and never overwrite existing project truth.
- **METH-INV-009:** Stable diagnostic codes and deterministic trace ordering are compatibility surfaces; explanatory prose may improve without changing their meaning.
- **METH-INV-010:** Repository skills have distinct triggers and stop conditions and cannot replace the owning DSET specification, diagnosis authorization boundary, or implementation plan.
