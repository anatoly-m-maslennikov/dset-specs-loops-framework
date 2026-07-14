# TODO — DSET 0.2: Self-Hosting and Repository-Governed Skills

**Status:** Proposed roadmap. Unchecked items are not implemented capability claims.

**Outcome:** Make DSET self-hosting before external adoption, make skills thin wrappers over repository-local governing documents, prove that unchanged skills follow changed local rules, and validate the design through the first owned TypeScript pilot in [obsidian-your-harness](https://github.com/anatoly-m-maslennikov/obsidian-your-harness).

**Release label:** `0.2.0` is the first coordinated DSET product and CLI-package release under the new policy. The unreleased independent package `1.0.0` candidate is superseded before merge. Schema, profile, and template-format versions remain independent compatibility identities rather than product-maturity claims.

## 0.2 invariants

- **DSET-02-INV-001 — Framework first:** The DSET framework repository is the first complete adopter of every released capability applicable to its selected profiles. A profile-specific capability that is not applicable to the repository must pass through a versioned in-repository adopter fixture before any external pilot may depend on it.
- **DSET-02-INV-002 — Bounded recursion:** Self-hosting is a terminating fixed point, not an unbounded directory recursion: the released validator checks the candidate change; the candidate checks this repository; the candidate creates and checks a temporary adopter.
- **DSET-02-INV-003 — Local rule authority:** An adopting repository's governing documents are the sole editable owners of its selected rules. Framework templates seed those documents but stop being authoritative after materialization.
- **DSET-02-INV-004 — Thin skills:** Skills own discovery and invocation only. They do not duplicate normative workflow, architecture, authoring, proof, threshold, or supportability rules.
- **DSET-02-INV-005 — Same wrapper, new rules:** A user may change repository-local governing rules and the same unchanged skill wrappers must apply the new rules.
- **DSET-02-INV-006 — Fail closed:** Missing, conflicting, cyclic, out-of-repository, or incompatible selected rule ownership stops the workflow with a stable diagnostic. Explicitly justified non-applicability remains valid and must not be converted into a failure.
- **DSET-02-INV-007 — Honest customization:** A locally changed ruleset remains valid project truth but is identified as a local/custom profile rather than silently claiming byte-equivalence to an unchanged framework profile.
- **DSET-02-INV-008 — Separate proof:** Deterministic resolver, structure, wrapper, and recursion checks remain tests; agent interpretation, rule-following, navigation, and diagnostic usefulness remain evals.
- **DSET-02-INV-009 — One owner per rule:** Every normative rule ID has exactly one editable governing document. Agent guidance, skills, templates, generated installations, and summaries link to that owner and never become parallel writable rule stores.
- **DSET-02-INV-010 — Small skill surface:** Core users see `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release`; helper lifecycle operations remain modes or chained workflows.
- **DSET-02-INV-011 — Primary orchestration:** `dset` selects bounded next actions from authoritative local state and registered local rules without embedding the lifecycle or authorizing effects silently.
- **DSET-02-INV-012 — Investigable runs:** Every skill emits a bounded redacted local run record under ignored `.dset/runs/`; records support heuristics but never replace repository, Git, hosted, or promoted-proof authorities.
- **DSET-02-INV-013 — One version transition per main PR:** After bootstrap `0.2.0`, every accepted `dev` to `main` PR declares exactly one normal, small, RC, or final product/package transition using integer components.
- **DSET-02-INV-014 — Protected release transaction:** Release artifacts are prepared before merge; tags and GitHub Releases derive from the protected merge commit without post-merge content changes.
- **DSET-02-INV-015 — Fully working 1.0 gate:** `1.0.0-rc.N` and `1.0.0` require complete scope, supportability, proof, pilots, distribution, and no known release blockers; arithmetic and schedules cannot promote them.
- **DSET-02-INV-016 — Main-session inheritance:** Subagents use the main session's model and reasoning effort by default; medium budget targets two or three useful agents and every deviation is explicit.
- **DSET-02-INV-017 — Outcome-cost budgets:** Low/medium/high budgets vary useful fan-out, roles, rounds, context, evidence, and stopping thresholds before model quality; nominal token price alone never determines the cheaper plan.

**Contract status:** Self-hosting and rule-ownership invariants are defined as `METH-INV-013`–`METH-INV-021` with requirements `METH-REQ-026`–`METH-REQ-034`. Skill topology, release-cycle, and budget invariants are defined as `METH-INV-022`–`METH-INV-029` with requirements `METH-REQ-035`–`METH-REQ-043`, each with separate deterministic and qualitative proof mappings. Roadmap §§0–§4 are implemented and pass local plus hosted deterministic proof on draft PR #9. The new skill/budget/release mechanics, qualitative evals, TypeScript profile, external pilots, distribution, and final release reconciliation remain open; DSET 0.2 is not yet an adoption-readiness claim.

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

- [x] **DSET-02-TASK-001:** Establish coordinated DSET product/CLI-package `0.2.0`, keep schema/profile/template versions independent, supersede the unreleased package `1.0.0` candidate before merge, and preserve archived v1 evidence unchanged.
- [x] **DSET-02-TASK-002:** Define the last-released-validator versus candidate-validator contract so a candidate is never its own only judge.
- [x] **DSET-02-TASK-003:** Define the minimum non-project bootstrap protocol that wrappers may contain: locate the repository root, locate `dset/dset.yaml`, resolve the governance registry, and fail closed.
- [x] **DSET-02-TASK-004:** Open one standard DSET change, `make-dset-self-hosting-and-skills-thin`, with separate requirements, test plan, eval plan, design, implementation batches, evidence, and PR identity.

## §1 | Add the repository-local governance registry

- [x] **DSET-02-TASK-005:** Define `dset/governance.yaml` as the machine-readable resolver surface; it points to governing documents but does not restate their rules.
- [x] **DSET-02-TASK-006:** Publish a JSON Schema covering registry version, workflow IDs, rule IDs, one owner per rule, ordered dependencies, applicability, local path, source profile/version, and customization status.
- [x] **DSET-02-TASK-007:** Require every normative path to remain inside the repository. External sources may supply provenance or rationale but cannot be a live writable project-rule owner.
- [x] **DSET-02-TASK-008:** Define deterministic precedence without implicit fallback: project-local accepted rule → explicitly selected local profile → failure. A wrapper must not silently fall back to embedded prose or a remote framework checkout.
- [x] **DSET-02-TASK-009:** Add `dset rules resolve <workflow-id>` to print the stable ordered governing-document set without writing.
- [x] **DSET-02-TASK-010:** Add `dset rules check` to validate identity, path containment, existence, ownership uniqueness, dependency ordering, cycles, applicability, and profile/customization metadata.
- [x] **DSET-02-TASK-011:** Emit stable diagnostics for missing registry, missing owner, duplicate owner, missing document, outside-root path, cycle, unknown workflow, and incompatible profile.
- [x] **DSET-02-TASK-012:** Make `dset check` and `dset verify` run the governance resolver whenever a project selects repository-governed skills.
- [x] **DSET-02-TASK-013:** Add a thin governance hub explaining purpose, boundaries, rule owners, workflow routes, customization, and migration without duplicating the registered rules.

### Proposed local shape

```text
dset/
├── governance.yaml
└── governance/
    ├── README.md
    ├── architecture.md
    ├── build-rules.md
    └── workflows/
        ├── domain-clarification.md
        ├── diagnosis.md
        └── prototyping.md
```

The registry, not this example path, is the compatibility surface. A repository may use different local document paths when the registry resolves them unambiguously.

## §2 | Move rules out of skills

- [x] **DSET-02-TASK-014:** Inventory every normative statement formerly embedded in `skills/dset-grill/SKILL.md` (renamed `dset-clarify`), `skills/dset-diagnose/SKILL.md`, and `skills/dset-prototype/SKILL.md`.
- [x] **DSET-02-TASK-015:** Assign each statement one governing owner: normative methodology/reference, behavioral specification, architecture, playbook/runbook, authorization contract, proof plan, or supportability rule.
- [x] **DSET-02-TASK-016:** Move domain-clarification rules into repository-governed documents covering vocabulary, entities/value objects/actors, per-owned-entity lifecycles, invariants, boundary cases, decision routing, and test/eval separation.
- [x] **DSET-02-TASK-017:** Move diagnosis rules into repository-governed documents covering reproduction, minimization, hypotheses, evidence, first-bad-change analysis, Back-to-Left provenance, regression proof, containment, authorization, and stop conditions.
- [x] **DSET-02-TASK-018:** Move prototype rules into repository-governed documents covering hypothesis, timebox, representative cases, provenance/license, proof-of-fit, disposal, adopt/adapt/build/defer, promotion, and stop conditions.
- [x] **DSET-02-TASK-019:** Reduce every skill to metadata/trigger, DSET-root discovery, workflow ID, resolver invocation, application instruction, output handoff, and fail-closed behavior.
- [x] **DSET-02-TASK-020:** Remove concrete thresholds, file inventories, workflow steps, domain rules, architecture rules, and copied safety/supportability prose from skill bodies.
- [x] **DSET-02-TASK-021:** Update the artifact-type contract: a skill invokes a governed workflow; it does not own that workflow's substantive rules.
- [x] **DSET-02-TASK-022:** Require wrapper output to identify the resolved workflow ID, rule IDs, document paths, profile/customization identity, and unresolved conflicts before acting.
- [x] **DSET-02-TASK-023:** Validate that installed/generated Claude, Codex, and other runtime copies match the canonical framework wrapper source and are never edited as rule owners.

## §3 | Materialize project-owned rules from templates

- [x] **DSET-02-TASK-024:** Add versioned governing-document templates for architecture, build rules, domain/spec authoring, deterministic proof, qualitative/probabilistic evals, diagnosis, prototyping, supportability, and artifact maintenance.
- [x] **DSET-02-TASK-025:** Add an explicit adoption/materialization command or documented transaction that copies selected defaults into the adopting repository, records source version/provenance, and refuses existing destinations.
- [x] **DSET-02-TASK-026:** State that materialized documents become project-owned truth immediately; later framework releases provide reviewed migrations/deltas, never invisible overwrites.
- [x] **DSET-02-TASK-027:** Record local customization status and origin without treating the original template as a second current owner.
- [x] **DSET-02-TASK-028:** Provide a migration map for existing `AGENTS.md`, `CLAUDE.md`, project rules, specs, test plans, eval plans, implementation plans, ADRs, runbooks, and evidence.
- [x] **DSET-02-TASK-029:** Require old rule surfaces to become concise hubs/pointers, read-only history, or removed artifacts after verified cutover; never leave both old and new locations writable.
- [x] **DSET-02-TASK-030:** Add update guidance that compares framework changes against local rules and produces an explicit proposed delta rather than replacing customized files.

## §4 | Prove bounded recursive self-hosting

- [x] **DSET-02-TASK-031:** Make the last released DSET version validate the active change that modifies the candidate toolchain and governing contracts.
- [x] **DSET-02-TASK-032:** Make the candidate validate this framework repository's methodology, documentation, governance registry, project truth, templates, skills, CLI, schemas, fixtures, traceability, and supportability.
- [x] **DSET-02-TASK-033:** Scaffold a complete temporary adopter from released templates during tests without using private paths or machine-global state.
- [x] **DSET-02-TASK-034:** Make the same candidate validate the generated adopter with the same public command and schemas.
- [x] **DSET-02-TASK-035:** Mutate one generated local rule while preserving the skill wrapper bytes; prove registry/check results change only because the local rule/profile identity changed.
- [x] **DSET-02-TASK-036:** Corrupt each bootstrap boundary—manifest, registry, rule owner, path, dependency, wrapper identity, template, and candidate command—and prove the earliest stable failure.
- [x] **DSET-02-TASK-037:** Define the recursion stop: the generated adopter may consume the candidate toolchain but does not regenerate the framework repository or recursively create another adopter.
- [x] **DSET-02-TASK-038:** Run the full fixed point in local verification and hosted CI before an external pilot may claim DSET 0.2 adoption readiness.

## §5 | Derive TypeScript v1 from Your Harness

- [ ] **DSET-02-TASK-039:** Inventory the actual Your Harness Node, TypeScript, ESLint, Jest, esbuild, package-lock, source/test scopes, generated outputs, warnings, and CI behavior at a pinned revision.
- [ ] **DSET-02-TASK-040:** Map the six language-neutral gate categories to observed TypeScript-native tools and commands; do not translate Python thresholds mechanically.
- [ ] **DSET-02-TASK-041:** Start from the real canonical sequence: typecheck, lint, unit/integration tests, production build, DSET structural/rule checks, trace freshness, and diff hygiene.
- [ ] **DSET-02-TASK-042:** Define dependency/layer checks for provider-neutral `core`, provider adapters, feature orchestration, shared UI, and style boundaries using syntax-aware TypeScript/ESLint evidence.
- [ ] **DSET-02-TASK-043:** Record current complexity/max-function warnings as a bounded baseline or advisory gate; new violations must not silently expand the baseline.
- [ ] **DSET-02-TASK-044:** Define schema/contracts, secret hygiene, generated-bundle, lockfile, and test-to-source mapping gates appropriate to the plugin.
- [ ] **DSET-02-TASK-045:** Publish `typescript-v1` only after the pilot passes; use an explicitly labeled candidate profile before acceptance.

## §6 | Adopt DSET in obsidian-your-harness

- [ ] **DSET-02-TASK-046:** Use the owned `anatoly-m-maslennikov/obsidian-your-harness` repository as the first external pilot; record its exact starting revision, branch, upstream Claudian revision, MIT license, and adaptation boundary.
- [ ] **DSET-02-TASK-047:** Inventory `your_harness_specs/`, root and scoped `CLAUDE.md` files, README/architecture surfaces, tests, package scripts, generated assets, local context, and active feature work before creating a second authority.
- [ ] **DSET-02-TASK-048:** Classify every existing spec/plan as accepted truth, active change, failed/incomplete work, or history before migration.
- [ ] **DSET-02-TASK-049:** Create the visible `dset/` control plane with project manifest, governance registry, artifact registry, provenance, one initial `harness` package, changes/archive roots, supportability, templates/migration record, and generated traceability.
- [ ] **DSET-02-TASK-050:** Move accepted feature behavior into stable-ID domain/spec/contracts and separate deterministic test and qualitative/probabilistic eval plans.
- [ ] **DSET-02-TASK-051:** Move the current autotest plan out of the legacy implementation-plan area and into the deterministic test-plan owner; retain implementation phases only as active or historical implementation artifacts.
- [ ] **DSET-02-TASK-052:** Convert root `CLAUDE.md` and `AGENTS.md` into concise agent-facing hubs/wrappers; move their substantive build, architecture, supportability, and workflow rules to registered governing documents.
- [ ] **DSET-02-TASK-053:** Register scoped architecture/rule documents under `src/` as owners or migrate their normative content; do not copy the same rule into global guidance.
- [ ] **DSET-02-TASK-054:** Add a production supportability contract covering plugin/build identity, provider and CLI boundaries, vault/session storage authorities, safe diagnostics, redaction, retention/access, failure containment, rollback, recovery, and incident-to-change/PR traceability.
- [ ] **DSET-02-TASK-055:** Make the repository README a valid root hub with purpose, boundaries, stable navigation, installation/operation, supportability, and project-control routes.
- [ ] **DSET-02-TASK-056:** Select the candidate TypeScript and documentation profiles independently; configure one canonical `dset verify` command to run both plus project tests/build.
- [ ] **DSET-02-TASK-057:** Install/generated-link the same canonical thin skills for supported agent runtimes without copying rules into those installations.
- [ ] **DSET-02-TASK-058:** Cut over atomically: old writable spec/rule roots become pointers, read-only history, or are removed only after the new DSET owners pass.
- [ ] **DSET-02-TASK-059:** Run a real feature/defect through proposal → requirements → test/eval plans → implementation → evidence → reconciliation → archive in one PR.
- [ ] **DSET-02-TASK-060:** Keep the pilot change active and the old owner intact if resolver, migration, TypeScript gates, skills, supportability, or recursive proof fails.

## §7 | Evaluate upstream Claudian after the owned pilot

- [ ] **DSET-02-TASK-061:** Treat upstream Claudian as a read-only clean-room fixture first; do not push DSET artifacts to an upstream-owned remote during evaluation.
- [ ] **DSET-02-TASK-062:** Re-run initialization, registry resolution, documentation classification, and candidate TypeScript gates against a pinned clean upstream revision.
- [ ] **DSET-02-TASK-063:** Compare which Your Harness governing rules are product-specific adaptations and which defaults generalize to an unmodified Claudian codebase.
- [ ] **DSET-02-TASK-064:** If durable Claudian adoption is desired, create or select an authorized personal fork/branch and open a separate DSET change with its own project truth and provenance.
- [ ] **DSET-02-TASK-065:** Prohibit cross-repository rule ownership: Claudian and Your Harness may share framework-template origin, but each repository owns its materialized rules independently.

## §8 | Deterministic test plan

- [ ] **DSET-02-TEST-001 — Registry shape:** Valid registries parse; missing versions, workflow IDs, rule IDs, owners, paths, dependencies, or customization metadata fail with stable diagnostics.
- [ ] **DSET-02-TEST-002 — Authority graph:** Duplicate owners, cycles, unknown dependencies, and outside-root paths fail deterministically.
- [ ] **DSET-02-TEST-003 — Stable resolution:** Repeated resolution produces byte-stable ordered output and performs no writes.
- [ ] **DSET-02-TEST-004 — Thin wrappers:** Released skills contain only the allowed bootstrap/wrapper fields and resolve every referenced workflow.
- [ ] **DSET-02-TEST-005 — Distribution identity:** Generated/installed wrapper files match the canonical source for every supported runtime.
- [ ] **DSET-02-TEST-006 — Local mutation:** Changing a materialized rule leaves wrapper hashes unchanged, changes profile/customization evidence, and keeps deterministic registry validation coherent.
- [ ] **DSET-02-TEST-007 — Recursive fixed point:** Released validator → candidate repository → generated adopter → candidate validation passes in the bounded sequence.
- [ ] **DSET-02-TEST-008 — Recursive failures:** Each corrupted bootstrap boundary fails at the expected stable diagnostic without falling back to embedded or remote rules.
- [ ] **DSET-02-TEST-009 — TypeScript profile:** Typecheck, lint, unit/integration tests, production build, layer rules, schemas/contracts, secret hygiene, lockfile, DSET checks, trace freshness, and diff hygiene run through one canonical command.
- [ ] **DSET-02-TEST-010 — Migration ownership:** The Your Harness migration leaves exactly one writable owner for every accepted rule, spec, test plan, eval plan, implementation change, and evidence concern.
- [ ] **DSET-02-TEST-011 — Provenance/supportability:** Exact upstream provenance/license and the required production supportability fields resolve and validate.
- [ ] **DSET-02-TEST-012 — Lifecycle:** The pilot completes a real PR-linked DSET change and guarded archive without predicting a future merge SHA.

## §9 | Qualitative eval plan

- [ ] **DSET-02-EVAL-001 — Rule propagation:** Give two repositories the same wrapper and different local rules; independent agents must follow the applicable local rule without skill edits or framework-repository access.
- [ ] **DSET-02-EVAL-002 — Cold resolution:** A cold agent locates the DSET root, registry, governing documents, accepted truth, active change, proof obligations, and canonical command without session memory.
- [ ] **DSET-02-EVAL-003 — No hidden fallback:** Remove or conflict a governing rule; the agent must stop and report the resolver failure rather than apply remembered or embedded methodology.
- [ ] **DSET-02-EVAL-004 — Rule ownership:** Reviewers distinguish framework template origin, project-local current rule, skill wrapper, agent hub, rationale, procedure, and historical evidence without creating duplicate authority.
- [ ] **DSET-02-EVAL-005 — Migration clarity:** A reviewer can classify and migrate the existing Your Harness specs, test plan, eval plans, implementation phases, and agent guidance without losing history or leaving two writable roots.
- [ ] **DSET-02-EVAL-006 — TypeScript applicability:** Reviewers apply only evidence-backed TypeScript gates and do not inherit Python tools or thresholds.
- [ ] **DSET-02-EVAL-007 — Production diagnosis:** An independent operator diagnoses and contains a synthetic provider/plugin/storage incident using bounded redacted evidence and the project supportability runbook.
- [ ] **DSET-02-EVAL-008 — Clean-room portability:** A cold upstream Claudian fixture can adopt the templates and resolver without Your Harness-only paths, rules, or private context leaking into it.

## §10 | Distribution and release

- [ ] **DSET-02-TASK-066:** Implement the thin primary `dset` orchestration wrapper and registered local orchestration rules; keep initialization, decomposition, landscape/ADR/spec/proof/implementation planning, implementation, verification, tickets, and next-step guidance as modes or chained workflows.
- [ ] **DSET-02-TASK-067:** Implement the thin `dset-release` wrapper and registered release rules; retain `dset-clarify`, `dset-diagnose`, and `dset-prototype` as the other specialist skills and reject helper-skill proliferation.
- [ ] **DSET-02-TASK-068:** Add bounded redacted append-only `.dset/runs/` records, ignored by Git, with schema/retention rules and authoritative-state reconciliation for next-step heuristics.
- [ ] **DSET-02-TASK-069:** Add the normal/small/RC/final transition matrix, exactly-one-class main-PR validation, coordinated product/package version surfaces, and independent schema/profile/template compatibility versions.
- [ ] **DSET-02-TASK-070:** Add pre-merge release preparation and post-merge tag/GitHub Release publication from the protected merge commit without a post-merge content write.
- [ ] **DSET-02-TASK-071:** Gate `1.0.0-rc.N` and `1.0.0` on fully working declared scope, self-hosting, documentation, supportability, migrations, deterministic tests, applicable evals, required pilots, distribution, and absence of known release blockers.
- [ ] **DSET-02-TASK-078:** Implement same-model/same-effort subagent inheritance, medium two-or-three-agent useful fan-out, explicit deviation reporting, and capacity-aware zero/fewer-agent behavior.
- [ ] **DSET-02-TASK-079:** Implement low/medium/high outcome-cost budget profiles, run-record plan/actual metrics, and task-relevant model-comparison evidence without price-only downgrade heuristics.
- [ ] **DSET-02-TASK-072:** Publish one pinned install/run path for the DSET CLI that adopters can use without copying validator code.
- [ ] **DSET-02-TASK-073:** Publish one canonical source for each thin skill plus generated installation mappings for supported runtimes.
- [ ] **DSET-02-TASK-074:** Add compatibility and migration notes for registry, template, schema, diagnostic, wrapper, and release-policy changes.
- [ ] **DSET-02-TASK-075:** Run the complete deterministic plan and at least two independent reviewers across the qualitative eval plan; preserve failures and corrective loops.
- [ ] **DSET-02-TASK-076:** Require green framework self-hosting and green Your Harness hosted verification before marking `typescript-v1`, thin skills, or DSET 0.2 ready.
- [ ] **DSET-02-TASK-077:** Reconcile accepted methodology and artifact contracts, archive through the implementing PR, and publish the final version mapping, release notes, pinned distribution identity, and migration guide.

## Definition of done

- [ ] The released validator checks the candidate change, and the candidate checks both this repository and one generated adopter.
- [ ] `dset/governance.yaml`, its schema, resolver commands, stable diagnostics, templates, and migrations are public and versioned.
- [ ] All first-wave skills are thin wrappers; no substantive governing rule exists only or independently inside a skill.
- [ ] The core distribution exposes exactly `dset`, `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release`; helper lifecycle actions remain modes or chained workflows.
- [ ] Bounded redacted local run records support investigation and next-step heuristics without becoming project truth.
- [ ] Every accepted `dev` to `main` PR carries exactly one valid version transition, and neither normal nor small progression can produce `1.0.0`.
- [ ] Product/package RC and final releases satisfy the fully working gate and publish from the protected merge commit.
- [ ] Subagents inherit the main model/effort by default; budget profiles vary useful fan-out/evidence first and record every model/effort deviation.
- [ ] Two different project-local rulesets produce different compliant agent behavior through byte-identical wrappers.
- [ ] Your Harness has one visible DSET root, one writable owner per concern, exact upstream provenance, a production supportability contract, and independent TypeScript/documentation profiles.
- [ ] A real Your Harness change completes the full DSET loop with deterministic tests, applicable evals, hosted checks, accepted-truth reconciliation, PR traceability, and guarded archive.
- [ ] The clean upstream Claudian evaluation proves that templates, resolver, skills, and TypeScript gates do not depend on Your Harness-only rules or private machine context.
- [ ] Version naming across methodology, CLI package, schemas, profiles, templates, skills, migrations, and release notes is explicit and non-contradictory.

## Stop conditions

Do not start the external pilot while the candidate is its own only validator, skills still own substantive rules, governing documents cannot be resolved locally, the CLI cannot be pinned, or TypeScript gates are guessed. Do not cut over Your Harness while its old rule/spec roots remain writable. Do not push adoption changes to upstream Claudian without an authorized repository/branch. Keep failed work active and preserve the previous authority until recovery proof passes.
