# TODO — DSET 0.3: Self-Hosting and Repository-Governed Skills

**Status:** Proposed roadmap. Unchecked items are not implemented capability claims.

**Outcome:** Make DSET self-hosting before external adoption, make skills thin wrappers over repository-local governing documents, prove that unchanged skills follow changed local rules, and validate the design through the first owned TypeScript pilot in [obsidian-your-harness](https://github.com/anatoly-m-maslennikov/obsidian-your-harness).

**Release label:** `0.3.1` is the corrected first coordinated DSET product and CLI-package release under the new policy. The unpublished `0.3.0` draft, earlier incomplete `0.2.0` target, and unreleased independent package `1.0.0` candidate are superseded before merge. Schema, profile, and template-format versions remain independent compatibility identities rather than product-maturity claims.

## DSET 0.3 invariants

- **DSET-INVARIANT-TOOL-001 — Framework first:** The DSET framework repository is the first complete adopter of every released capability applicable to its selected profiles. A profile-specific capability that is not applicable to the repository must pass through a versioned in-repository adopter fixture before any external pilot may depend on it.
- **DSET-INVARIANT-TOOL-002 — Bounded recursion:** Self-hosting is a terminating fixed point, not an unbounded directory recursion: the released validator checks the candidate change; the candidate checks this repository; the candidate creates and checks a temporary adopter.
- **DSET-INVARIANT-GOV-001 — Local rule authority:** An adopting repository's governing documents are the sole editable owners of its selected rules. Framework templates seed those documents but stop being authoritative after materialization.
- **DSET-INVARIANT-SKILL-001 — Thin skills:** Skills own discovery and invocation only. They do not duplicate normative workflow, architecture, authoring, proof, threshold, or supportability rules.
- **DSET-INVARIANT-SKILL-002 — Same wrapper, new rules:** A user may change repository-local governing rules and the same unchanged skill wrappers must apply the new rules.
- **DSET-INVARIANT-GOV-002 — Fail closed:** Missing, conflicting, cyclic, out-of-repository, or incompatible selected rule ownership stops the workflow with a stable diagnostic. Explicitly justified non-applicability remains valid and must not be converted into a failure.
- **DSET-INVARIANT-GOV-003 — Honest customization:** A locally changed ruleset remains valid project truth but is identified as a local/custom profile rather than silently claiming byte-equivalence to an unchanged framework profile.
- **DSET-INVARIANT-META-001 — Separate proof:** Deterministic resolver, structure, wrapper, and recursion checks remain tests; agent interpretation, rule-following, navigation, and diagnostic usefulness remain evals.
- **DSET-INVARIANT-GOV-004 — One owner per rule:** Every normative rule ID has exactly one editable governing document. Agent guidance, skills, templates, generated installations, and summaries link to that owner and never become parallel writable rule stores.
- **DSET-INVARIANT-SKILL-003 — Small skill surface:** Core users see `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release`; helper lifecycle operations remain modes or chained workflows.
- **DSET-INVARIANT-SKILL-004 — Primary orchestration:** `dset` selects bounded next actions from authoritative local state and registered local rules without embedding the lifecycle or authorizing effects silently.
- **DSET-INVARIANT-SKILL-005 — Investigable runs:** Every skill emits a bounded redacted local run record under ignored `.dset/runs/`; records support heuristics but never replace repository, Git, hosted, or promoted-proof authorities.
- **DSET-INVARIANT-OPS-001 — One version transition per main PR:** After the explicit first pre-1.0 bootstrap target is published, every accepted `dev` to `main` PR declares exactly one normal, small, RC, or final product/package transition using integer components.
- **DSET-INVARIANT-OPS-002 — Protected release transaction:** Release artifacts are prepared before merge; tags and GitHub Releases derive from the protected merge commit without post-merge content changes.
- **DSET-INVARIANT-OPS-003 — Fully working 1.0 gate:** `1.0.0-rc.N` and `1.0.0` require complete scope, supportability, proof, pilots, distribution, and no known release blockers; arithmetic and schedules cannot promote them.
- **DSET-INVARIANT-SKILL-006 — Main-session inheritance:** Subagents use the main session's model and reasoning effort by default; medium budget targets two or three useful agents and every deviation is explicit.
- **DSET-INVARIANT-SKILL-007 — Outcome-cost budgets:** Low/medium/high budgets vary useful fan-out, roles, rounds, context, evidence, and stopping thresholds before model quality; nominal token price alone never determines the cheaper plan.

**Contract status:** Current accepted invariants are owned by
`DSET-INVARIANT-OPS-002..006`, `DSET-INVARIANT-TOOL-003`,
`DSET-INVARIANT-GOV-006..011`, `DSET-INVARIANT-META-004..008`, and
`DSET-INVARIANT-SKILL-002..008`; their layer-owned Requirement, Test, and Eval
plans are the authoritative mappings. Candidate-to-repository and
candidate-to-adopter deterministic proof passes locally, while the pinned
pre-transition validator is an explicit degraded bootstrap result and the
current branch lacks exact-head hosted proof. Qualitative evals, the TypeScript
profile and pilots, native-host proof, hosted proof, and final release
reconciliation remain open; DSET 0.3 is not yet an adoption-readiness claim.
The local runtime, skill distribution, budget, release-transaction, migration,
project-health, and external-review mechanics are implemented and must not
remain mislabeled as roadmap-only work.

**Measured outcome:** [`DSET-OUTCOME-META-001`](../dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/specs/outcomes.md) defines adoption readiness as a baseline-to-target state change proven by test, eval, hosted, pilot, and blocker evidence. Completing features or roadmap tasks alone does not satisfy it.

**Deferred product-practice questions:** `DSET-QUESTION-META-001..003`, `DSET-QUESTION-GOV-002..003`, and `DSET-QUESTION-OPS-001` in [`dset/scopes/gov/intake.yaml`](../dset/scopes/gov/intake.yaml) defer Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views. DSET 0.3 creates no corresponding artifact type or intake queue.

## Scope

- Repository-local governance registry and deterministic resolver.
- Thin versions of `dset-clarify`, `dset-diagnose`, and `dset-prototype`.
- Framework-owned governing-document templates and explicit materialization/migration behavior.
- Released/candidate recursive self-hosting gates.
- Evidence-derived TypeScript profile using the real Your Harness toolchain.
- First owned adoption in `obsidian-your-harness`.
- Later clean-room/read-only evaluation against upstream [Claudian](https://github.com/YishenTu/claudian).
- Pinned CLI and skill distribution with one canonical source.

## Non-goals

- Automatically inheriting future framework rule changes into a project that customized its local rules.
- Treating remote URLs, installed skills, agent memory, or generated caches as live project-rule authorities.
- Guessing general JavaScript/TypeScript thresholds before the Your Harness evidence pass.
- Migrating both Your Harness and upstream Claudian simultaneously.
- Rewriting every existing methodology document merely to change folder layout.
- Building a general documentation CMS, remote policy service, or unbounded plugin marketplace.

## §0 | Resolve version and bootstrap semantics

- [x] **DSET-TASK-OPS-016:** Establish corrected coordinated DSET product/CLI-package `0.3.1`, keep schema/profile/template versions independent, supersede the unpublished `0.3.0` draft, incomplete `0.2.0` target, and unreleased package `1.0.0` candidate before merge, and preserve archived evidence unchanged.
- [x] **DSET-TASK-TOOL-011:** Define the last-released-validator versus candidate-validator contract so a candidate is never its own only judge.
- [x] **DSET-TASK-SKILL-004:** Define the minimum non-project bootstrap protocol that wrappers may contain: locate the repository root, locate schema 1.2 `dset/scopes/meta/dset.yaml` or a legacy central manifest, resolve the layout-owned governance registry, and fail closed on duplicate authority.
- [x] **DSET-TASK-GOV-014:** Open one standard DSET change, `make-dset-self-hosting-and-skills-thin`, with separate requirements, test plan, eval plan, design, implementation batches, evidence, and PR identity.

## §1 | Add the repository-local governance registry

- [x] **DSET-TASK-GOV-015:** Define schema 1.2 `dset/scopes/gov/governance.yaml` as the machine-readable resolver surface while retaining legacy `dset/governance.yaml` compatibility; it points to governing documents but does not restate their rules.
- [x] **DSET-TASK-TOOL-012:** Publish a JSON Schema covering registry version, workflow IDs, rule IDs, one owner per rule, ordered dependencies, applicability, local path, source profile/version, and customization status.
- [x] **DSET-TASK-GOV-016:** Require every normative path to remain inside the repository. External sources may supply provenance or rationale but cannot be a live writable project-rule owner.
- [x] **DSET-TASK-GOV-017:** Define deterministic precedence without implicit fallback: project-local accepted rule → explicitly selected local profile → failure. A wrapper must not silently fall back to embedded prose or a remote framework checkout.
- [x] **DSET-TASK-TOOL-013:** Add `dset rules resolve <workflow-id>` to print the stable ordered governing-document set without writing.
- [x] **DSET-TASK-TOOL-014:** Add `dset rules check` to validate identity, path containment, existence, ownership uniqueness, dependency ordering, cycles, applicability, and profile/customization metadata.
- [x] **DSET-TASK-TOOL-015:** Emit stable diagnostics for missing registry, missing owner, duplicate owner, missing document, outside-root path, cycle, unknown workflow, and incompatible profile.
- [x] **DSET-TASK-TOOL-016:** Make `dset check` and `dset verify` run the governance resolver whenever a project selects repository-governed skills.
- [x] **DSET-TASK-GOV-018:** Add a thin governance hub explaining purpose, boundaries, rule owners, workflow routes, customization, and migration without duplicating the registered rules.

### Current self-hosted shape

```text
dset/
└── scopes/
    ├── meta/
    │   ├── dset.yaml
    │   └── governance/
    ├── gov/
    │   ├── governance.yaml
    │   └── governance/
    ├── tool/governance/
    ├── skill/governance/
    └── ops/governance/
```

The discovered layout and registry are the compatibility surfaces. Schema 1.0
and 1.1 repositories retain the central manifest, registry, and governance
paths; schema 1.2 assigns each governing document to its semantic layer.

## §2 | Move rules out of skills

- [x] **DSET-TASK-SKILL-005:** Inventory every normative statement formerly embedded in `skills/dset-grill/SKILL.md` (renamed `dset-clarify`), `skills/dset-diagnose/SKILL.md`, and `skills/dset-prototype/SKILL.md`.
- [x] **DSET-TASK-GOV-019:** Assign each statement one governing owner: normative methodology/reference, behavioral specification, architecture, playbook/runbook, authorization contract, proof plan, or supportability rule.
- [x] **DSET-TASK-SKILL-006:** Move domain-clarification rules into repository-governed documents covering vocabulary, entities/value objects/actors, per-owned-entity lifecycles, invariants, boundary cases, decision routing, and test/eval separation.
- [x] **DSET-TASK-SKILL-007:** Move diagnosis rules into repository-governed documents covering reproduction, minimization, hypotheses, evidence, first-bad-change analysis, Back-to-Left provenance, regression proof, containment, authorization, and stop conditions.
- [x] **DSET-TASK-SKILL-008:** Move prototype rules into repository-governed documents covering hypothesis, timebox, representative cases, provenance/license, proof-of-fit, disposal, adopt/adapt/build/defer, promotion, and stop conditions.
- [x] **DSET-TASK-SKILL-009:** Reduce every skill to metadata/trigger, DSET-root discovery, workflow ID, resolver invocation, application instruction, output handoff, and fail-closed behavior.
- [x] **DSET-TASK-SKILL-010:** Remove concrete thresholds, file inventories, workflow steps, domain rules, architecture rules, and copied safety/supportability prose from skill bodies.
- [x] **DSET-TASK-META-011:** Update the artifact-type contract: a skill invokes a governed workflow; it does not own that workflow's substantive rules.
- [x] **DSET-TASK-SKILL-011:** Require wrapper output to identify the resolved workflow ID, rule IDs, document paths, profile/customization identity, and unresolved conflicts before acting.
- [x] **DSET-TASK-SKILL-012:** Validate that installed/generated Claude, Codex, and other runtime copies match the canonical framework wrapper source and are never edited as rule owners.

## §3 | Materialize project-owned rules from templates

- [x] **DSET-TASK-GOV-020:** Add versioned governing-document templates for architecture, build rules, domain/spec authoring, deterministic proof, qualitative/probabilistic evals, diagnosis, prototyping, supportability, and artifact maintenance.
- [x] **DSET-TASK-TOOL-017:** Add an explicit adoption/materialization command or documented transaction that copies selected defaults into the adopting repository, records source version/provenance, and refuses existing destinations.
- [x] **DSET-TASK-GOV-021:** State that materialized documents become project-owned truth immediately; later framework releases provide reviewed migrations/deltas, never invisible overwrites.
- [x] **DSET-TASK-GOV-022:** Record local customization status and origin without treating the original template as a second current owner.
- [x] **DSET-TASK-GOV-023:** Provide a migration map for existing `AGENTS.md`, `CLAUDE.md`, project rules, specs, test plans, eval plans, implementation plans, Decision records, runbooks, and evidence.
- [x] **DSET-TASK-GOV-024:** Require old rule surfaces to become concise hubs/pointers, read-only history, or removed artifacts after verified cutover; never leave both old and new locations writable.
- [x] **DSET-TASK-GOV-025:** Add update guidance that compares framework changes against local rules and produces an explicit proposed delta rather than replacing customized files.

## §4 | Prove bounded recursive self-hosting

- [ ] **DSET-TASK-TOOL-018:** Close the degraded bootstrap transition by making a published schema-1.2-compatible DSET validator validate a later candidate; until then preserve the exact pre-transition rejection and never call it a pass.
- [x] **DSET-TASK-TOOL-019:** Make the candidate validate this framework repository's methodology, documentation, governance registry, project truth, templates, skills, CLI, schemas, fixtures, traceability, and supportability.
- [x] **DSET-TASK-TOOL-020:** Scaffold a complete temporary adopter from released templates during tests without using private paths or machine-global state.
- [x] **DSET-TASK-TOOL-021:** Make the same candidate validate the generated adopter with the same public command and schemas.
- [x] **DSET-TASK-TOOL-022:** Mutate one generated local rule while preserving the skill wrapper bytes; prove registry/check results change only because the local rule/profile identity changed.
- [x] **DSET-TASK-TOOL-023:** Corrupt each bootstrap boundary—manifest, registry, rule owner, path, dependency, wrapper identity, template, and candidate command—and prove the earliest stable failure.
- [x] **DSET-TASK-TOOL-024:** Define the recursion stop: the generated adopter may consume the candidate toolchain but does not regenerate the framework repository or recursively create another adopter.
- [ ] **DSET-TASK-TOOL-025:** Rerun the bounded candidate/repository/adopter proof on the exact pushed PR head in hosted CI; the recorded older head is not current release evidence.

## §5 | Derive TypeScript v1 from Your Harness

- [x] **DSET-TASK-TOOL-026:** Inventory the actual Your Harness Node, TypeScript, ESLint, Jest, esbuild, package-lock, source/test scopes, generated outputs, warnings, and CI behavior at a pinned revision.
- [x] **DSET-TASK-TOOL-027:** Map the six language-neutral gate categories to observed TypeScript-native tools and commands; do not translate Python thresholds mechanically.
- [x] **DSET-TASK-TOOL-028:** Start from the real canonical sequence: typecheck, lint, unit/integration tests, production build, DSET structural/rule checks, trace freshness, and diff hygiene.
- [x] **DSET-TASK-TOOL-029:** Define dependency/layer checks for provider-neutral `core`, provider adapters, feature orchestration, shared UI, and style boundaries using syntax-aware TypeScript/ESLint evidence.
- [x] **DSET-TASK-TOOL-030:** Record current complexity/max-function warnings as a bounded baseline or advisory gate; new violations must not silently expand the baseline.
- [ ] **DSET-TASK-TOOL-031:** Define schema/contracts, secret hygiene, generated-bundle, lockfile, and test-to-source mapping gates appropriate to the plugin.
- [ ] **DSET-TASK-TOOL-032:** Publish `typescript-v1` only after the pilot passes; use an explicitly labeled candidate profile before acceptance.

## §6 | Adopt DSET in obsidian-your-harness

- [x] **DSET-TASK-GOV-026:** Use the owned `anatoly-m-maslennikov/obsidian-your-harness` repository as the first external pilot; record its exact starting revision, branch, upstream Claudian revision, MIT license, and adaptation boundary.
- [x] **DSET-TASK-GOV-027:** Inventory `your_harness_specs/`, root and scoped `CLAUDE.md` files, README/architecture surfaces, tests, package scripts, generated assets, local context, and active feature work before creating a second authority.
- [x] **DSET-TASK-GOV-028:** Classify every existing spec/plan as accepted truth, active change, failed/incomplete work, or history before migration.
- [x] **DSET-TASK-GOV-029:** Create the visible schema 1.2 `dset/scopes/` control plane with META manifest, GOV governance/artifact/intake/provenance registries, one layer-fragmented `harness` package, layer-owned changes/archive roots, OPS supportability, distributed templates/migration record, and GOV-generated traceability.
- [ ] **DSET-TASK-META-012:** Move accepted feature behavior into stable-ID domain/spec/contracts and separate deterministic test and qualitative/probabilistic eval plans.
- [ ] **DSET-TASK-META-013:** Move the current autotest plan out of the legacy implementation-plan area and into the deterministic test-plan owner; retain implementation phases only as active or historical implementation artifacts.
- [x] **DSET-TASK-GOV-030:** Convert root `CLAUDE.md` and `AGENTS.md` into concise agent-facing hubs/wrappers; move their substantive build, architecture, supportability, and workflow rules to registered governing documents.
- [x] **DSET-TASK-GOV-031:** Register scoped architecture/rule documents under `src/` as owners or migrate their normative content; do not copy the same rule into global guidance.
- [x] **DSET-TASK-OPS-017:** Add a production supportability contract covering plugin/build identity, provider and CLI boundaries, vault/session storage authorities, safe diagnostics, redaction, retention/access, failure containment, rollback, recovery, and incident-to-change/PR traceability. OYOHA now owns the contract and a deterministically tested clipboard-only support report; installed-host recovery/rollback and a real incident path remain separate readiness proof.
- [x] **DSET-TASK-GOV-032:** Make the repository README a valid root hub with purpose, boundaries, stable navigation, installation/operation, supportability, and project-control routes.
- [ ] **DSET-TASK-TOOL-033:** Select the candidate TypeScript and documentation profiles independently; configure one canonical `dset verify` command to run both plus project tests/build.
- [ ] **DSET-TASK-SKILL-013:** Install/generated-link the same canonical thin skills for supported agent runtimes without copying rules into those installations.
- [ ] **DSET-TASK-GOV-033:** Cut over atomically: old writable spec/rule roots become pointers, read-only history, or are removed only after the new DSET owners pass.
- [ ] **DSET-TASK-OPS-018:** Run a real feature/defect through proposal → requirements → test/eval plans → implementation → evidence → reconciliation → archive in one PR.
- [x] **DSET-TASK-GOV-034:** Keep the pilot change active and the old owner intact if resolver, migration, TypeScript gates, skills, supportability, or recursive proof fails.

## §7 | Evaluate upstream Claudian after the owned pilot

- [x] **DSET-TASK-GOV-035:** Treat upstream Claudian as a read-only clean-room fixture first; do not push DSET artifacts to an upstream-owned remote during evaluation.
- [x] **DSET-TASK-TOOL-034:** Re-run initialization, registry resolution, documentation classification, and candidate TypeScript gates against a pinned clean upstream revision.
- [x] **DSET-TASK-META-014:** Compare which Your Harness governing rules are product-specific adaptations and which defaults generalize to an unmodified Claudian codebase.
- [ ] **DSET-TASK-GOV-036:** If durable Claudian adoption is desired, create or select an authorized personal fork/branch and open a separate DSET change with its own project truth and provenance.
- [x] **DSET-TASK-GOV-037:** Prohibit cross-repository rule ownership: Claudian and Your Harness may share framework-template origin, but each repository owns its materialized rules independently.

## §8 | Deterministic test plan

Accepted deterministic claims and their current automation are owned by the
layer plans under `dset/scopes/*/specs/packages/methodology/test-plan.md`. This
roadmap does not redeclare their IDs or assertions. The active Change selects
and executes its applicable set in its separate
[test plan](../dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/test-plan.md).

The implemented §0–§4 subset has current local proof. Remaining platform,
release, hosted, TypeScript, migration, pilot, and distribution tests stay open
through `DSET-TASK-TOOL-008..009`, `DSET-TASK-SKILL-020`,
`DSET-TASK-TOOL-036..037`, and `DSET-TASK-OPS-025` in the active Change; an
unchecked roadmap item never becomes a competing Test definition.

## §9 | Qualitative eval plan

Accepted qualitative criteria are owned by the layer plans under
`dset/scopes/*/specs/packages/methodology/eval-plan.md`. The active Change owns
only execution and evidence for its selected set in its separate
[eval plan](../dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/eval-plan.md).

Independent rule-following, navigation, diagnostic, platform, release,
TypeScript, migration, supportability, pilot, and clean-room reviews remain
pending where the active verification matrix says so. They are eval work, not
duplicate roadmap-owned Eval entities and not deterministic test substitutes.

## §10 | Distribution and release

- [x] **DSET-TASK-SKILL-014:** Implement the thin primary `dset` orchestration wrapper and registered local orchestration rules; keep initialization, decomposition, landscape/Decision/spec/proof/implementation planning, implementation, verification, tickets, and next-step guidance as modes or chained workflows.
- [x] **DSET-TASK-SKILL-015:** Implement the thin `dset-release` wrapper and registered release rules; preserve `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` as the primary operator surface while exposing the additional governed lifecycle wrappers accepted by `DSET-DECISION-SKILL-002` as direct shortcuts.
- [x] **DSET-TASK-SKILL-016:** Add bounded redacted append-only `.dset/runs/` records, ignored by Git, with schema/retention rules and authoritative-state reconciliation for next-step heuristics.
- [x] **DSET-TASK-OPS-019:** Add the normal/small/RC/final transition matrix, exactly-one-class main-PR validation, coordinated product/package version surfaces, and independent schema/profile/template compatibility versions.
- [x] **DSET-TASK-OPS-020:** Add pre-merge release preparation and post-merge tag/GitHub Release publication from the protected merge commit without a post-merge content write.
- [x] **DSET-TASK-OPS-021:** Gate `1.0.0-rc.N` and `1.0.0` on fully working declared scope, self-hosting, documentation, supportability, migrations, deterministic tests, applicable evals, required pilots, distribution, and absence of known release blockers.
- [x] **DSET-TASK-SKILL-018:** Implement same-model/same-effort subagent inheritance, medium two-or-three-agent useful fan-out, explicit deviation reporting, and capacity-aware zero/fewer-agent behavior.
- [x] **DSET-TASK-SKILL-019:** Implement low/medium/high outcome-cost budget profiles, run-record plan/actual metrics, and task-relevant model-comparison evidence without price-only downgrade heuristics.
- [x] **DSET-TASK-TOOL-035:** Publish one pinned install/run path for the DSET CLI that adopters can use without copying validator code.
- [x] **DSET-TASK-SKILL-017:** Publish one canonical source for each thin skill plus generated installation mappings for supported runtimes.
- [x] **DSET-TASK-GOV-038:** Add compatibility and migration notes for registry, template, schema, diagnostic, wrapper, and release-policy changes.
- [ ] **DSET-TASK-OPS-022:** Run the complete deterministic plan and at least two independent reviewers across the qualitative eval plan; preserve failures and corrective loops.
- [ ] **DSET-TASK-OPS-023:** Require green framework self-hosting and green Your Harness hosted verification before marking `typescript-v1`, thin skills, or DSET 0.3 ready.
- [ ] **DSET-TASK-OPS-024:** Reconcile accepted methodology and artifact contracts, archive through the implementing PR, and publish the final version mapping, release notes, pinned distribution identity, and migration guide.

## Definition of done

- [ ] The released validator checks the candidate change, and the candidate checks both this repository and one generated adopter.
- [x] `dset/scopes/gov/governance.yaml`, its GOV-owned schema, resolver commands, stable diagnostics, distributed templates, and migrations are public and versioned; legacy central paths remain validated compatibility surfaces.
- [x] All first-wave skills are thin wrappers; no substantive governing rule exists only or independently inside a skill.
- [x] The primary operator surface is `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release`; the complete distribution exposes the exact 16 accepted thin lifecycle wrappers, with non-primary wrappers acting only as direct shortcuts to the same governed modes.
- [x] Bounded redacted local run records support investigation and next-step heuristics without becoming project truth.
- [ ] Every accepted `dev` to `main` PR carries exactly one valid version transition, and neither normal nor small progression can produce `1.0.0`.
- [ ] Product/package RC and final releases satisfy the fully working gate and publish from the protected merge commit.
- [x] Subagents inherit the main model/effort by default; budget profiles vary useful fan-out/evidence first and record every model/effort deviation.
- [x] Two different project-local rulesets produce different compliant agent behavior through byte-identical wrappers.
- [ ] Your Harness has one visible DSET root, one writable owner per concern, exact upstream provenance, a production supportability contract, and independent TypeScript/documentation profiles.
- [ ] A real Your Harness change completes the full DSET loop with deterministic tests, applicable evals, hosted checks, accepted-truth reconciliation, PR traceability, and guarded archive.
- [ ] The clean upstream Claudian evaluation proves that templates, resolver, skills, and TypeScript gates do not depend on Your Harness-only rules or private machine context.
- [ ] Version naming across methodology, CLI package, schemas, profiles, templates, skills, migrations, and release notes is explicit and non-contradictory.

## Stop conditions

Do not start the external pilot while the candidate is its own only validator, skills still own substantive rules, governing documents cannot be resolved locally, the CLI cannot be pinned, or TypeScript gates are guessed. Do not cut over Your Harness while its old rule/spec roots remain writable. Do not push adoption changes to upstream Claudian without an authorized repository/branch. Keep failed work active and preserve the previous authority until recovery proof passes.
