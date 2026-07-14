# DSET Spec Loops: A Production Vibecoding Framework

**A framework for production vibecoding.**

DSET expands to **Domain–Supportability–Evals–Tests**.

“Spec” remains in the name because every iteration is a governed spec loop; it is not the `S` in DSET.

The framework treats natural language as a high-leverage programming interface while keeping durable software grounded in explicit domain models, accepted behavioral specifications, production supportability, deterministic tests, qualitative or probabilistic evals, implementation plans, and machine-verifiable gates.

## Purpose

This repository is the public source for the DSET framework, executable toolchain, reusable artifact contracts, and focused agent workflows. It also dogfoods DSET as an adopting project.

## Boundaries

Framework rules and release assets live here. Each adopting repository owns its own behavioral truth and changes under its local `dset/` root. Installed skills, cached tooling, private working notes, and external project artifacts are not independent framework authorities.

## Core loop

```text
Domain → Spec + Supportability + Test Plan + Eval Plan → Implement → Test + Evaluate → Review → Reconcile Spec → Next Loop
```

- **Domain** defines entities, language, states, invariants, and boundaries.
- **Supportability** defines the risk-scaled production evidence, identity, diagnostics, data-safety controls, and runbook needed to investigate and fix real incidents.
- **Spec** records accepted behavioral truth and change scope.
- **Evals** assess probabilistic, qualitative, or LLM-mediated behavior.
- **Tests** prove deterministic behavior.
- **Loops** deliver small vertical slices, use fresh evidence, and reconcile accepted results into current truth.

## Repository areas

| Area | Start here | Owns |
|---|---|---|
| Methodology | [Methodology hub](methodology/README.md) | Delivery stages, runtime/build rules, proof conventions, and external grounding |
| Artifact governance | [Documentation architecture hub](documentation/README.md) | Artifact types, authoring rules, hubs, maintenance, and `documentation-v1` |
| Project control plane | [DSET project hub](dset/README.md) | Accepted project truth, active/archive changes, schemas, templates, fixtures, traceability, migrations, and supportability |
| Executable CLI | [`dset_toolchain/`](dset_toolchain/) | Dependency-light lifecycle, governance resolution/materialization, validation, traceability, archive, and bounded self-hosting |
| Agent workflows | [Skills hub](skills/README.md) | Focused domain-grilling, diagnosis, and disposable-prototype workflows |
| Delivery and provenance | [Delivery policy](.github/DELIVERY.md) and [third-party notices](THIRD_PARTY_NOTICES.md) | Protected publication path and external-source/license boundaries |

## Run DSET

Read-only validation requires only Python 3.10 or newer:

```bash
python -m dset_toolchain check .
```

For this repository's complete locked Python profile:

```bash
uv sync --locked --dev
uv run dset verify .
```

The CLI also provides `rules check`, `rules resolve`, `rules materialize`, `rules refresh`, `rules diff`, `self-host`, `version`, `new`, `trace`, and guarded `archive` workflows. See the [project-root guide](dset/README.md) for lifecycle and command details.

## Source-of-truth model

This public repository is the canonical source for DSET Spec Loops and every released framework-owned methodology document, schema, template, validator, utility, skill, fixture, and migration guide. Installed or workspace-local copies are distributions of this repository, not independent editable sources.

Each project that adopts DSET owns its project truth separately under its own `dset/` root. In an adopting project, `dset/specs/` contains accepted current truth and `dset/changes/` contains bounded work in progress. Framework truth never replaces project truth, and project artifacts do not become framework rules unless they are deliberately contributed here.

## Status

The methodology is published, the repository dogfoods its own project contract, and the executable DSET v1 toolchain was implemented and verified through PR [#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7). The DSET 0.2 framework milestone is now an active candidate: repository-local governance, thin wrappers, project-owned materialization, and the local bounded self-hosting fixed point are implemented on the active change. Hosted fixed-point proof, independent qualitative evals, the evidence-derived JavaScript/TypeScript profile, external pilots, pinned distribution, and final release reconciliation remain open; 0.2 is not yet an adoption-readiness claim.
