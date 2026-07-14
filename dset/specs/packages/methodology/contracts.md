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

## Skill release target

`dset` is the primary operator entrypoint for initialization, decomposition, landscape/ADR/spec/proof/implementation planning, implementation, verification, work-item routing, and next-step advice through registered project-local workflows. `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` are explicit specialist triggers. Helper operations are modes or chained workflows, not additional public skill names. Until `skills/dset/` and `skills/dset-release/` are implemented and proven, only the three specialist skills listed in [the skills hub](../../../../skills/README.md) are released.

All five target skills are thin wrappers over the repository governance registry. The registered `DSET-RULE-LIFECYCLE`, `DSET-RULE-SKILL-RUNS`, `DSET-RULE-RELEASE`, `DSET-RULE-DELEGATION-BUDGET`, and `DSET-RULE-WORK-ITEMS` documents own substantive behavior. Versioned bounded local run records under `.dset/runs/` are operational evidence only and are excluded from committed project truth.

Subagents request the main session's model and reasoning effort by default and report effective attestation or uncertainty. Medium budget targets two and caps the whole tree at three unique subagents, depth one, and two rounds. Scope, proof, and safety are invariant; model overrides require dated task-relevant evidence and remain visible in run records.

Intake routing uses only problems, opportunities, and questions. ADRs/decisions and DSET changes are artifacts; tasks live inside changes; GitHub Issues and Jira/support tickets are external representations.

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
