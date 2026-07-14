# Methodology public contract

## Inputs

- Domain and product decisions accepted by DSET maintainers.
- Evidence from implementation, tests, evals, pilots, and defect repair.
- External sources used as provenance or candidates for adaptation.
- Language/ecosystem evidence used to create or revise applied gate profiles.

## Outputs

- A GitHub-portable public methodology under `methodology/`.
- A repository navigation map in `README.md`, stable area hubs, and methodology document 00.
- Artifact architecture, type, authoring, hub, maintenance, and rationale references under `documentation/`.
- Independently selected implementation-language and artifact-governance profiles, including the `documentation-v1` registry under `dset/artifacts.yaml`.
- Accepted package truth under `dset/specs/`.
- Bounded, PR-traceable changes under `dset/changes/`.
- Versioned schemas, templates, fixtures, migration guidance, provenance, and generated traceability under `dset/`.
- The `dset` CLI through `python -m dset_toolchain` and an installable console entry point.
- Three implemented specialist skill sources under `skills/`; the active DSET 0.2 change owns the unimplemented five-skill release target.
- A coordinated DSET product/CLI-package release contract, with project-configured delivery and independent schema/profile/template compatibility versions.
- Active authoritative-boundary Contract records with explicit ownership, direction, conformance, compatibility, and lifecycle.

## Skill release target

`dset` is the primary operator entrypoint for initialization, decomposition, landscape/decision/spec/proof/implementation planning, implementation, verification, work-item routing, and next-step advice through registered project-local workflows. `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` are explicit specialist triggers. Helper operations are modes or chained workflows, not additional public skill names. Until `skills/dset/` and `skills/dset-release/` are implemented and proven, only the three specialist skills listed in [the skills hub](../../../../skills/README.md) are released.

All five target skills are thin wrappers over the repository governance registry. The registered `DSET-RULE-LIFECYCLE`, `DSET-RULE-SKILL-RUNS`, `DSET-RULE-RELEASE`, `DSET-RULE-DELEGATION-BUDGET`, and `DSET-RULE-WORK-ITEMS` documents own substantive behavior. Versioned bounded local run records under `.dset/runs/` are operational evidence only and are excluded from committed project truth.

Subagents request the main session's model and reasoning effort by default and report effective attestation or uncertainty. Medium budget targets two and caps the whole tree at three unique subagents, depth one, and two rounds. Scope, proof, and safety are invariant; model overrides require dated task-relevant evidence and remain visible in run records.

Intake routing uses only problems, opportunities, and questions in `dset/intake.yaml`. Decision is the durable entity and artifact and uses the full `DECISION` type. Decisions and DSET Changes are artifacts, tasks live inside Changes, and GitHub Issues and Jira/support tickets are external representations. IDs use the `DSET` project prefix: project-wide IDs omit the optional layer, while layer-owned IDs insert `META`, `GOV`, `TOOL`, `SKILL`, or `OPS` between the full type and sequence. Optional accepted User Stories use the compact full `STORY` ID type, measurable intended effects use the full `OUTCOME` type, and authoritative boundaries use the full `CONTRACT` type.

## Specification boundary surface

A User Story is optional accepted truth, not an intake queue. When present, `DSET-STORY-<NNN>` or `DSET-STORY-<LAYER>-<NNN>` records an actor or stakeholder, desired capability or outcome, value or purpose, and links to normative Requirements and applicable Scenarios. Absence is valid where no meaningful User Story exists. A User Story never substitutes for a Requirement; `STORY` remains its compact ID token.

Requirements own observable verifiable delivered behavior, results, and constraints; Scenarios own observable examples and edge cases. Decisions own consequential choices among alternatives with rationale, tradeoffs, and consequences, not every implementation detail. Design owns internal logic, implementation plans own build sequence, and Contracts own boundaries the project cannot choose or rewrite.

An Outcome is a measurable change in user, business, operational, or system state, not a delivered output or feature. `DSET-OUTCOME-<NNN>` or `DSET-OUTCOME-<LAYER>-<NNN>` records baseline, target, observation method/source, evaluation window, originating Problem or Opportunity links, relevant User Story links when present, and applicable Eval links. Requirements and their deterministic evidence prove delivered behavior; Outcome evidence shows whether that behavior had the intended effect. This model-only change defines the type without asserting a concrete Outcome.

## Authoritative boundary contracts

A Contract is not implementation advice. It is an authoritative boundary that implementation must satisfy without rewriting. Every Contract record names its authority, source, exactly one version or digest, direction, producer, consumer, conformance rule, compatibility rule, and lifecycle state. Lifecycle is `declared -> active -> superseded` or `declared -> active -> retired`; only the named authority may issue a superseding version. Ambiguity creates a Question, incompatibility creates a Problem, and a Decision cannot override an active Contract.

### DSET-CONTRACT-SKILL-001 — Released skills are host-native

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | Official skill/package formats for every declared target host, each pinned by version or digest in release evidence |
| Version or digest | `1.0` |
| Direction | DSET release artifacts to declared host skill loaders |
| Producer | DSET skill release workflow |
| Consumer | Each declared target host, including Claude and Codex when claimed |
| Conformance | Every released DSET skill is a real installable host-native skill, not descriptive Markdown alone; each target has artifact, install, load, and representative invoke proof |
| Compatibility | The release declares a host matrix and passes every claimed target against its pinned format; unsupported targets are omitted rather than implied |
| Lifecycle | `active` |

### DSET-CONTRACT-TOOL-001 — Released utilities match declared platforms

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | Declared host/platform matrix and pinned runtime or host-format references |
| Version or digest | `1.0` |
| Direction | Released skill scripts and utilities to supported operating environments |
| Producer | DSET tool and skill release workflows |
| Consumer | Users on macOS, native Windows, WSL, and Linux |
| Conformance | Each released utility installs and runs on every declared platform with path/shell portability proof, or declares narrower applicability before release with an honest reason |
| Compatibility | Every matrix cell has executed proof or explicit honest `N/A`; generic Markdown validation is insufficient |
| Lifecycle | `active` |

### DSET-CONTRACT-TOOL-002 — Dependencies follow exact policy

| Field | Value |
|---|---|
| Authority | DSET maintainers; exception authority must also be named in the applicable policy |
| Source | Versioned dependency policy and pinned ecosystem, package, registry, license, and provenance sources |
| Version or digest | `1.0` |
| Direction | Dependency policy to implementation dependency selection and release proof |
| Producer | DSET dependency-policy owner and release workflow |
| Consumer | DSET implementations, contributors, package tooling, and release gates |
| Conformance | Policy records exact ecosystem/package/registry/license/version allowlists and denylists, sources, rationale, enforcement command, and exception authority/expiry; proof covers lockfiles, dependency resolution, licenses, and provenance |
| Compatibility | Every selected dependency is allowed and source-constrained; denied or expired-exception dependencies fail release |
| Lifecycle | `active` |

A mandated library is a Contract constraint, not a Decision. A consequential selection among alternatives that the Contract permits may be recorded as a Decision.

### DSET-CONTRACT-OPS-001 — CI is hosted GitHub Actions evidence

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | GitHub Actions workflow syntax/event/permission contracts and repository protected-branch configuration, pinned by version or digest in release evidence |
| Version or digest | `1.0` |
| Direction | Repository workflow artifacts and PR-head commits to GitHub-hosted checks and protected integration |
| Producer | `.github/workflows/` and GitHub Actions on the actual pull-request head |
| Consumer | Contributors, reviewers, required-check rules, and protected-branch integration |
| Conformance | Real workflow artifacts under `.github/workflows/` define valid syntax, events, least-required permissions, stable check names, artifact/log retention, exact-SHA correlation, failure visibility, and execution on the actual PR head |
| Compatibility | Required hosted checks integrate with protected-branch policy and retain stable GitHub check/run evidence; local scripts and specification prose are inputs, not hosted-CI proof |
| Lifecycle | `active` |

## Release compatibility surface

DSET versions use integer SemVer components. The complete transition table includes bootstrap, pre-1.0 normal/small, first/subsequent RC, final, and post-1.0 small/normal/breaking releases. Product/package identity is canonical SemVer with defined ecosystem serialization; tag and publisher release derive idempotently from the configured protected merge commit. Schema, profile, and template-format versions remain independent compatibility surfaces.

## CLI compatibility surface

| Command | Contract |
|---|---|
| `dset new` | Create a profile-aware active change without overwrite |
| `dset check` | Read-only structural, artifact-area/hub, ID, portability, provenance, and lifecycle validation |
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

The cross-cutting [documentation architecture](../../../../documentation/README.md) owns artifact types, authoring rules, hubs, maintenance, rationale, and applied artifact profiles. It is independent from the numbered implementation pipeline and is not a sixth stage or an implementation language.

Numbered responsibilities are stable compatibility surfaces. A rename may improve the title, but moving responsibility between documents requires a delta spec, updated links, and explicit migration notes.

## Non-contractual surfaces

Examples, diagrams, and cited candidates may evolve without compatibility guarantees when they do not change a requirement, invariant, artifact shape, or ownership boundary.
