# Methodology delta — DSET 0.3 invariants

## ADDED — DSET-REQUIREMENT-TOOL-006 Framework-first release applicability

A DSET version may release a capability only after this repository adopts it under every applicable selected profile. A profile-specific capability that is not applicable to this repository must pass through a versioned in-repository adopter fixture before an external pilot may depend on it.

**Scenario DSET-SCENARIO-TOOL-006:** A TypeScript-only gate is not applied to Python sources, but its versioned adopter fixture must pass before the gate can be presented to Your Harness as released DSET behavior.

## ADDED — DSET-REQUIREMENT-TOOL-007 Self-hosting terminates at a fixed point

The self-hosting release gate must have exactly three bounded levels: the last
released validator checks the candidate change, the candidate checks this
repository, and the candidate materializes and checks one temporary adopter.
During a declared bootstrap transition, an incompatible pre-transition
validator records its exact rejection as degraded assurance rather than a pass;
the other two levels still must pass. The temporary adopter must not recursively
create another adopter.

**Scenario DSET-SCENARIO-TOOL-007:** A candidate run records released-to-candidate, candidate-to-repository, and candidate-to-temporary-adopter results, then terminates without discovering or traversing unrelated nested `dset/` roots.

## ADDED — DSET-REQUIREMENT-GOV-007 Local governing documents own selected rules

Every selected normative rule must resolve to one editable governing document inside the adopting repository. Framework templates may seed that document, but the materialized local document becomes authoritative and the template remains provenance rather than a live fallback.

**Scenario DSET-SCENARIO-GOV-007:** After materialization, editing the framework template does not change the adopter's resolved rule set; editing the registered local governing document does.

## ADDED — DSET-REQUIREMENT-SKILL-002 Skills remain thin wrappers

A DSET skill may own trigger metadata, repository/root discovery, workflow identity, resolver invocation, rule-set reporting, output handoff, authorization boundaries, and stop behavior. It must not own substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.

**Scenario DSET-SCENARIO-SKILL-002:** Static inspection finds the `domain-clarification` workflow ID and resolver handoff in `dset-clarify` but no copied checklist, concrete threshold, or embedded fallback procedure.

## ADDED — DSET-REQUIREMENT-SKILL-003 Unchanged wrappers apply changed local rules

Wrapper behavior must depend on the resolved repository-local rule set rather than copied or cached normative prose. A local rule change must affect the next invocation without modifying the canonical wrapper.

**Scenario DSET-SCENARIO-SKILL-003:** Two otherwise identical adopters use the same wrapper hash but define different registered output conventions; each invocation follows its own local convention and reports the corresponding rule identity.

## ADDED — DSET-REQUIREMENT-GOV-008 Invalid selected ownership fails closed

Missing, duplicate, cyclic, outside-root, or profile-incompatible selected rule ownership must stop before governed work begins and emit a stable diagnostic. A rule or profile explicitly marked not applicable with a valid reason must remain a successful disposition rather than being converted into a failure.

**Scenario DSET-SCENARIO-GOV-008:** A selected rule pointing outside the repository stops with its stable code and path, while an unselected TypeScript profile in a documentation-only adopter passes as justified not applicable.

## ADDED — DSET-REQUIREMENT-GOV-009 Customization identity remains honest

A locally changed materialized rule set remains valid project truth but must identify itself as local/custom and retain its source profile/version provenance. It must not claim byte-equivalence to the unchanged framework profile.

**Scenario DSET-SCENARIO-GOV-009:** Changing one normative local rule changes the resolved ruleset identity to custom while preserving the originating framework profile and version as provenance.

## ADDED — DSET-REQUIREMENT-META-005 Proof categories remain separate

Exact resolver, ownership, path, identity, wrapper, and recursion behavior belongs to deterministic tests. Agent interpretation, rule-following, navigation, and diagnostic usefulness belong to qualitative or probabilistic evals. Automation does not move proof between categories.

**Scenario DSET-SCENARIO-META-006:** A scripted assertion that a cycle emits one code remains a test; an independent agent's ability to use that diagnostic to correct the governing document remains an eval even when the eval runner is automated.

## ADDED — DSET-REQUIREMENT-GOV-010 Every normative rule ID has one editable owner

Each normative rule ID must resolve to exactly one editable governing document. Agent instructions, skills, templates, generated installations, indexes, summaries, and caches may point to or reproduce derived metadata about the owner but must never become additional writable rule authorities.

**Scenario DSET-SCENARIO-GOV-010:** The registry rejects two governing documents claiming the same rule ID and accepts multiple navigation or generated surfaces that link to the single owner without restating its normative text.

## ADDED — DSET-REQUIREMENT-SKILL-004 The core user-facing skill surface stays small

The release target must expose exactly five user-facing skills: `dset` for lifecycle orchestration and next-step routing; `dset-clarify` for unresolved domain/specification branches; `dset-diagnose` for evidence-first diagnosis; `dset-prototype` for bounded disposable experiments; and `dset-release` for the guarded release transaction. Initialization, decomposition, Solution Landscape work, Decision/spec/proof/implementation planning, implementation, verification, work-item handling, and next-step advice are governed `dset` modes or chained workflows rather than additional public skills. Project-owned lifecycle rules define pairwise triggers, outputs, precedence, and stops.

**Scenario DSET-SCENARIO-SKILL-004:** An operator asks what to do next for a large feature; `dset` resolves the local orchestration rules, identifies whether decomposition, clarification, landscape work, proof planning, implementation, verification, or release is next, and invokes a specialist only when its trigger applies.

## ADDED — DSET-REQUIREMENT-SKILL-005 The primary skill orchestrates without becoming a rule owner

After valid local resolution, `dset` uses the `lifecycle-orchestration` workflow and stable decomposition, diagnosis, clarification, landscape, prototype, decision, proof-plan, implementation-plan, implementation, verification, work-triage, release, and completion modes. `DSET-RULE-LIFECYCLE` owns precedence, exact specialist mappings, authority/freshness, the two-transition cap, and stops. Before resolution, distribution-owned `dset init` may only preview/authorize/materialize/validate/stop, while `dset rules check` may perform diagnostic-only governance repair guidance and stop.

**Scenario DSET-SCENARIO-SKILL-005:** The same `dset` wrapper routes two repositories differently because their registered local orchestration rules and current artifacts differ, while the wrapper bytes remain identical.

## ADDED — DSET-REQUIREMENT-SKILL-006 Skill runs leave bounded local operational evidence

The runtime must follow `DSET-RULE-SKILL-RUNS` and the versioned run-record schema: one atomically created immutable record per invocation, explicit terminal/interrupted lifecycle, finite age/count/byte retention, bounded allowlisted fields, and no secrets, prompts, source content, or raw logs. Pre-init, read-only, or persistence-failed runs emit the same bounded record with persistence unavailable; risk/profile rules may stop consequential work that requires durable audit evidence. Records are advisory only.

**Scenario DSET-SCENARIO-SKILL-006:** `dset` notices repeated implementation changes since the last proof run and recommends verification; it cites local run signals as advisory and confirms authoritative repository and Git state before acting.

## ADDED — DSET-REQUIREMENT-OPS-008 Every pull request to main declares one version transition

The DSET product and distributable CLI package use one canonical SemVer identity. `DSET-RULE-RELEASE` owns the complete table: unversioned bootstrap to `0.3.0`; pre-1.0 small patch/normal minor; passing pre-1.0 to `1.0.0-rc.1`; RC correction to `rc.N+1`; passing RC to `1.0.0`; and post-1.0 compatible small, capability normal, or incompatible breaking patch/minor/major transitions. Mixed scope takes the highest impact; ambiguity stops; a published RC never returns to a lower identity.

**Scenario DSET-SCENARIO-OPS-008:** From `0.2.4`, a normal PR targets `0.3.0` and a small PR targets `0.2.5`; from `0.9.0`, a normal PR targets `0.10.0`; none of these transitions may produce `1.0.0`.

## ADDED — DSET-REQUIREMENT-OPS-009 Release preparation and publication have separate authorities

The project configures integration/release branches, publisher, and tag pattern. Every integration-to-protected PR has one release-owning Change with one committed declaration of class/base/target/readiness; other participating Changes contain only owner references. Omission, multiple declarations, and dangling/cyclic references fail. All version, package, note, PR, tag, and publisher surfaces are mirrors. Interactive `dset-release` prepares/verifies idempotently from the protected base; only authorized post-merge automation publishes at the exact merge SHA. Retry completes missing objects, accepts exact matches, and stops on collision; published tags are immutable, and corrections use a higher version through a new PR.

**Scenario DSET-SCENARIO-OPS-009:** A release PR fails when its declared target differs across the product manifest and package metadata. After a valid merge, automation tags that exact merge commit without modifying `main` content.

## ADDED — DSET-REQUIREMENT-OPS-010 Release candidates and 1.0 are fully working gates

`1.0.0-rc.N` may begin only after the declared 1.0 scope is feature-complete, self-hosted, documented, supportable, migration-ready, green under every deterministic test and applicable eval, verified in required adopters/pilots, and free of known release blockers. Exact-SHA `verification.md` owns gate dispositions, evidence, and blockers. Final promotion permits only release metadata/evidence updates; substantive changes require `rc.N+1` and fresh proof.

**Scenario DSET-SCENARIO-OPS-010:** A candidate with an unfinished TypeScript profile or required pilot remains on `0.y.z` even if every current test passes. A fully working `1.0.0-rc.2` with completed final evidence may promote to `1.0.0` without feature additions.

## ADDED — DSET-REQUIREMENT-OPS-011 Product/package releases are coordinated while compatibility schemas remain independent

The product, CLI package, notes, rendered configured tag, and publisher release must carry equivalent identity. Product SemVer is canonical; Python maps every `MAJOR.MINOR.PATCH-rc.N` only to PEP 440 `MAJOR.MINOR.PATCHrcN`. The current repository's configured tag pattern renders `v<product-semver>`; generic adopters may configure another schema-valid pattern. Schema, profile, and template-format versions remain independent compatibility surfaces.

**Scenario DSET-SCENARIO-OPS-011:** DSET `0.3.0` may continue to use project schema `1.0` and governance profile `core-v1@0.2`; package metadata and the product release still both report `0.3.0`.

## ADDED — DSET-REQUIREMENT-SKILL-007 Delegation inherits the main session by default

Every subagent must request the main session's model family/version and reasoning-effort level by default. The runtime discovers request/attestation support and records requested/effective values as confirmed, runtime-default-unverified, or unsupported. Known overrides are reported before spawn. Unsupported/unverified identity stops when exact configuration is a proof or safety precondition; otherwise uncertainty remains visible.

**Scenario DSET-SCENARIO-SKILL-007:** A main session using model M at extra-high effort requests independent review; the default plan uses two or three M/extra-high reviewers. If the runtime cannot supply that configuration, the orchestrator reports the constraint and asks for or follows an explicit project policy rather than substituting a cheaper model silently.

## ADDED — DSET-REQUIREMENT-SKILL-008 Budget policy optimizes expected outcome cost

One tree-wide project budget follows `DSET-RULE-DELEGATION-BUDGET`: low allows zero/one unique subagent, depth one, one round; default medium targets two and permits three, depth one, two rounds; high targets four and permits six, depth two, three rounds. Capacity reductions are recorded. Scope, required proof, and safety remain fixed; insufficiency stops. A model override requires dated task-relevant comparative quality/cost evidence with harness and limitations; missing/incomparable evidence preserves inherited model/effort, and single-agent benchmarks do not justify fan-out.

**Scenario DSET-SCENARIO-SKILL-008:** A lower-priced model consumes more tokens and retries and produces more failed work on a representative benchmark; DSET does not call it cheaper for that task. Low budget reduces optional breadth, not committed scope or required proof.

## ADDED — DSET-REQUIREMENT-SKILL-009 Sessions survive chaining and context compaction

The five public skills share one internal session-continuity capability; no sixth public session skill is added. `dset` starts, checkpoints, and resumes its workflow chain. Direct specialists start or join a compatible session, while automatically chained skills, governed model-only workflows, and delegated work remain child runs with session/root/parent identity. The runtime atomically updates a bounded ignored `.dset/sessions/<session-id>.json` checkpoint at workflow transitions, before observable handoff or compaction, and on terminal exit.

Checkpoint content is limited to a bounded objective, scope and artifact/run pointers, authorization state, authority snapshot, and next handoff. Full prompts, source content, arbitrary tool output, and secrets are forbidden. Resume prefers an explicit or host-provided ID, may infer only one compatible newest active checkpoint, and stops on ambiguity. It re-reads repository, Git, Change, proof, governance, and hosted owners before recomputing the next action; neither native session memory nor the checkpoint overrides them.

**Scenario DSET-SCENARIO-SKILL-009:** After `dset` chains clarification and planning, the host compacts context. The next invocation reloads the session checkpoint, notices a newer Git change, discards the stale next hint, and recommends verification without asking the operator to reconstruct history or invoke another skill.

## ADDED — DSET-REQUIREMENT-GOV-011 Intake routing stays at three queues

`DSET-RULE-WORK-ITEMS` exposes only problems, opportunities, and questions through one project-owned `dset/scopes/gov/intake.yaml` registry. Problems cover bugs, gaps, debt, and risks; opportunities describe improvements when nothing is wrong; consequential questions close through Decisions. Decision is the entity and a Decision record is its canonical artifact. Accepted items and Decisions enter a DSET Change, and executable work lives in its `tasks.md`. Decisions and Changes are artifacts; hosted tickets are representations. Canonical IDs use `DSET-<TYPE>-<LAYER>-<NNN>`, where `TYPE` is `REQUIREMENT`, `SCENARIO`, `INVARIANT`, `CONTRACT`, `TEST`, `EVAL`, `TASK`, `PROBLEM`, `OPPORTUNITY`, `QUESTION`, `DECISION`, `STORY`, or `OUTCOME`, and `LAYER` is `META`, `GOV`, `TOOL`, `SKILL`, or `OPS`. Numbering is independent per full artifact type within each layer.

**Scenario DSET-SCENARIO-GOV-011:** A defect and delivery risk are problems, optional automation is an opportunity, and an unresolved product choice is a question; their implementation steps become tasks only inside an accepted change.

## ADDED ENTITY — Work Area

A Work Area is a declared repository-relative folder that bounds DSET scope
without implying code, deployability, or a particular architecture. It may
contain local tools, deployable services, libraries, documentation,
methodology, data, or mixed content.

## ADDED INVARIANT — DSET-INVARIANT-META-008

Every scope-dependent DSET artifact or run resolves against the
repository-level scope or one or more declared Work Areas. A Work Area
declaration owns that scope boundary; session continuity may reference it but
cannot define, modify, or replace it. Neither repository-level scope nor a Work
Area implies code, a deployment unit, a service, a feature, or a module.

## ADDED — DSET-REQUIREMENT-META-011 Work Areas bound repository scope without assuming implementation type

DSET must support either one repository-level scope or one or more declared Work
Areas. A Work Area is a repository-relative folder declaration used to scope
accepted truth, Changes, proof, runs, and operational handoffs. Its content may
be a local tool, deployable service, library, documentation, methodology, data,
or any mixture of these. Declaring a Work Area must not classify it as code,
deployable, a service, a feature, or a module, and DSET must not require those
properties to use the boundary.

The repository's accepted Work Area declaration is authoritative. A session or
session checkpoint may reference the repository-level scope or declared Work
Areas so chained work can resume in the intended scope, but session continuity
does not own, create, rename, or supersede a Work Area. Every resume must
re-resolve the current authoritative declaration.

**Scenario DSET-SCENARIO-META-012:** A monorepo declares a deployable API folder,
a shared library folder, a documentation-and-methodology folder, and a mixed
data/tooling folder as separate Work Areas. Another repository declares only
its root. DSET scopes both projects without inventing services, modules,
features, or deployment semantics, and a resumed session follows the current
declaration rather than a stale checkpoint hint.

## ADDED — DSET-REQUIREMENT-OPS-012 Integration delivery is the default

Every applicable DSET project must use its configured local integration branch,
remote integration branch, and integration-to-protected release PR as the base
delivery flow. A Change may opt into a separate branch-backed worktree when
parallelism, risk, or conflicting work needs stronger isolation. That branch
must integrate into the configured integration branch before release. Workspace
mode never changes Change identity, scope, authorization, or proof ownership.

**Scenario DSET-SCENARIO-OPS-013:** This repository works locally on `dev`,
pushes remote `dev`, and opens PR `dev` to `main`. A parallel high-risk Change
selects `branch-worktree`, reviews that branch into `dev`, and then participates
in the same protected release flow without creating a permanent layer branch.
