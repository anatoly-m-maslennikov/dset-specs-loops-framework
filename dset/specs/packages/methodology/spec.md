# Methodology specification

## METH-REQ-001 — One governed pipeline

The methodology must define one five-stage pipeline: spec; test plan plus eval plan; implementation plan; code under general rules; and executable enforcement.

**Scenario METH-SCN-001:** Given a contributor deciding where a rule belongs, the document map identifies exactly one owning stage document and treats cross-links as pointers rather than duplicate ownership.

## METH-REQ-002 — Tests and evals remain distinct

The methodology must keep deterministic tests in `test-plan.md` and probabilistic or qualitative evaluation in `eval-plan.md`.

**Scenario METH-SCN-002:** Given behavior with one exact expected output, it is routed to the test plan even when the check is automated. Given multiple acceptable outputs judged by criteria or a rubric, it is routed to the eval plan.

## METH-REQ-003 — Runtime rules are selected by independent concerns

The methodology must select recovery semantics by runtime risk and durable backing by topology, write volume, and concurrency. Event sourcing, reconciliation, durable execution, and observed-progress liveness apply only when their specific semantics are required.

**Scenario METH-SCN-003:** A stateless CRUD service keeps durable state in its database without adding an application file WAL or event store unless audit/replay requirements independently demand one.

**Scenario METH-SCN-004:** A modest-write local resumable tool keeps accepted state in declared files with one writer and atomic/durable writes; a higher-volume or concurrent local tool selects a database instead of two writable authorities.

## METH-REQ-004 — Delivery semantics are bounded

The methodology must describe retries as at-least-once delivery plus receiving-side deduplication or idempotency. It may claim effectively-once effects only inside the declared key, retention, and atomicity boundary.

**Scenario METH-SCN-005:** A retryable receiver documents its deduplication key, retention window, owner, and atomic check/write operation without claiming universal exactly-once execution.

## METH-REQ-005 — Enforcement is language-neutral and profile-applied

The methodology must define six neutral gate categories and keep concrete tools, source scopes, thresholds, exclusions, and ratchets in versioned applied profiles.

**Scenario METH-SCN-006:** A Python project selects Python v1; a JavaScript/TypeScript project does not inherit Python line limits or tools.

## METH-REQ-006 — Change history is PR-traceable without a future SHA

The methodology must use a repository-qualified PR identity as the stable implementation link and keep the PR draft throughout archival. After fresh baseline verification and current-truth reconciliation, the change may move to a dated, explicitly incomplete archive candidate and be pushed so remote checks can inspect the real PR head. An evidence-only commit finalizes the archive after those checks pass. Missing PR identity keeps a change active; any later implementation or specification change invalidates prior readiness.

**Scenario METH-SCN-007:** The archived change links to the PR that owns the code diff and eventual merge result without attempting to store a merge SHA before it exists.

**Scenario METH-SCN-012:** A change with a pending PR identity cannot become an archive candidate. A pushed candidate remains unaccepted until final evidence is recorded, and a later implementation or specification edit requires verification and archive readiness to be refreshed.

## METH-REQ-007 — Public Markdown is portable

Public methodology must use ordinary Markdown links and GitHub-native alerts or collapsed details sections.

**Scenario METH-SCN-008:** A GitHub reader can navigate every local link and expand every collapsed section without an Obsidian renderer.

## METH-REQ-008 — Project truth uses a visible root

Committed project truth must live under the visible `dset/` root. Hidden `.dset/` is reserved for generated, local, cached, or other machine-owned state.

**Scenario METH-SCN-009:** `dset/README.md` exposes accepted truth, active changes, archive history, templates, and schemas, while no committed project truth is owned by `.dset/`.

## METH-REQ-009 — Package structure is proportional

The project manifest must register each package exactly once and must omit or null the global-truth root until cross-package ownership exists.

**Scenario METH-SCN-010:** A one-package project resolves `methodology` to `specs/packages/methodology` and reports `global_truth_root: null`.

## METH-REQ-010 — Standard changes expose complete proof structure

A standard change must contain exactly eight top-level document artifacts—proposal, test plan, eval plan, solution landscape, design, implementation plan, tasks, and verification—plus separate `specs/` and `proofs/` directories.

**Scenario METH-SCN-011:** Structural inspection counts the eight documents separately from the requirement-delta and evidence directories.

## METH-REQ-011 — Enforcement status is honest

Public metadata must name the selected enforcement profile and canonical command and must use explicit pending values until the corresponding executable assets exist.

**Scenario METH-SCN-013:** `documentation-v1-pending` and `canonical_command: pending` cannot be presented as an active executable gate.

## METH-REQ-012 — Public identity is stable

The public framework identity must use the display name **DSET Spec Loops**, the title **DSET Spec Loops: A Production Vibecoding Framework**, the expansion **Domain–Supportability–Evals–Tests**, and the repository slug `dset-specs-loops-framework`.

**Scenario METH-SCN-014:** README, project metadata, repository slug, and active methodology truth use the same identity; historical archive evidence may retain prior URLs when redirects preserve the recorded provenance.

## METH-REQ-013 — Production supportability is explicit and risk-scaled

Every production-bound tool must define a supportability contract appropriate to its runtime risk profile and deployment topology. The contract covers incident triggers or objectives; operator-usable evidence; end-to-end correlation and deploy/change identity; safe read-only diagnostics and permissions; retention, redaction, access, deletion, volume, cardinality, and sampling bounds; runbook, escalation, rollback or kill-switch paths; and traceability from an incident to governing requirements, changes, PRs, and fixes. Telemetry is diagnostic evidence, not a competing business-state authority. A non-production tool may mark the contract not applicable only with a reason.

**Scenario METH-SCN-015:** A production-bound local tool uses bounded structured local diagnostic records and run/build identity appropriate to its risk without being forced to deploy a tracing backend; a non-production one-shot tool records a justified not-applicable disposition.

**Scenario METH-SCN-016:** A distributed, stateful, retryable, or high-risk service propagates correlation and deploy/change identity across relevant effect boundaries, provides safe bounded diagnostics and incident runbooks, and adds tracing, audited access, rollback, or stronger redaction when its topology and profile require them.

## METH-REQ-014 — The canonical workflow is executable

The framework must provide one cross-platform CLI with `new`, `check`, `verify`, `trace`, and guarded `archive` commands. `check` is dependency-light and read-only; every write is explicit and refuses an existing destination.

**Scenario METH-SCN-017:** A contributor can run `python -m dset_toolchain check .` without installing OpenSpec or a second methodology and receives stable diagnostic codes for malformed artifacts.

## METH-REQ-015 — Contracts ship with proof fixtures

Versioned schemas, profile-aware templates, and valid/invalid fixtures must cover the project manifest, package truth, active and archived changes, separate test/eval artifacts, provenance, and traceability.

**Scenario METH-SCN-018:** The fixture runner accepts small, standard, failed-active, and archived cases and rejects missing-test, merged-test/eval, and missing-PR archive cases with their expected codes.

## METH-REQ-016 — Traceability is generated from durable identities

`dset/traceability.yaml` must be generated in stable order from committed change manifests and repository-qualified PR references. It may cache evidence relationships but must not replace GitHub as owner of PR state, checks, diffs, or merge results.

**Scenario METH-SCN-019:** Regeneration without source changes produces no diff, and every archived change resolves to the PR that owns its implementation history.

## METH-REQ-017 — Archive writes are guarded

Archive execution must require complete profile artifacts, fresh verification, accepted-truth reconciliation, an archive-ready status, a real PR identity, and a free dated destination. Dry-run is the default.

**Scenario METH-SCN-020:** A proposed, failed, incomplete, PR-less, or colliding change remains active and no archive path is overwritten.

## METH-REQ-018 — Workflow skills remain focused

The framework must publish distinct portable skills for pre-spec domain clarification, evidence-first diagnosis, and disposable prototyping. Each owns one trigger/output/verification/stop boundary and writes durable conclusions back to the active DSET change.

**Scenario METH-SCN-021:** A diagnosis request cannot silently authorize a fix, and prototype evidence cannot enter production without an accepted ADR/design and normal implementation proof.

## METH-REQ-019 — Repository delivery is supportable

The GitHub-hosted delivery path must document incident triggers, authoritative PR/check/run/ruleset/commit evidence, safe diagnostics, data controls, containment, recovery, escalation, and change-to-fix traceability. Hosted state remains authoritative; local files do not add a competing delivery-state store.

**Scenario METH-SCN-022:** An operator can diagnose a blocked or incorrect `dev → main` delivery, contain it by preserving the draft/PR evidence, and recover without bypassing protected `main` or rewriting history.

## METH-REQ-020 — Profile axes remain orthogonal

DSET must select implementation-language enforcement and artifact-governance enforcement independently. Runtime risk selects recovery/supportability semantics; durability topology selects durable authority; a language profile selects code tools and thresholds; an artifact profile selects document architecture, ownership, navigation, and authoring gates.

**Scenario METH-SCN-023:** A Python repository selects `python-v1` and `documentation-v1` together; a documentation-only repository selects `documentation-v1` without inheriting Python tools; a future TypeScript repository combines its own language profile with the same artifact profile.

## METH-REQ-021 — Governed areas have explicit architecture

Every governed public artifact area must declare one purpose, owner, root, hub, and parent relationship. The repository root hub gives the helicopter view and routes to area hubs. Hubs are thin navigation surfaces, not owners of atomic rules or exhaustive manually duplicated indexes.

**Scenario METH-SCN-024:** A cold reader starts at `README.md`, reaches the documentation or methodology hub, and identifies the owning artifact without scanning unrelated files.

## METH-REQ-022 — Artifact types own different questions

DSET must define distinct types for navigation, normative rules, behavioral specification, architecture, rationale, decisions, procedures, proof plans, evidence/history, and agent workflows. Each artifact has one primary type and one owning question; secondary meaning is expressed through links rather than duplicated rule text.

**Scenario METH-SCN-025:** A design explanation moves to rationale, a repeatable sequence moves to a playbook, and the normative rule remains in one reference document linked by both.

## METH-REQ-023 — Authoring rules are type-specific

Universal rules must require answer-first writing, one primary question, explicit scope and authority, links instead of copied rules, and GitHub-portable Markdown. Specification rules must keep observable what separate from why, model domain entities and per-entity lifecycle state machines before code, and order definitions so every entity is defined only from earlier entities; a forward section reference is a connection, not a definition.

**Scenario METH-SCN-026:** A specification that uses an undefined downstream entity as part of an earlier entity's definition fails review even when it contains a forward link; the entity is reordered or the relationship is stated as a later connection.

## METH-REQ-024 — Documentation v1 is executable

The `documentation-v1` profile must provide a machine-readable governed-area registry and deterministic checks for profile identity, required hubs, unique area IDs/roots, valid owner/purpose/parent fields, reachable parent hierarchy, required hub sections, root-to-area navigation, and existing portable links. Qualitative authoring judgments remain evals rather than brittle keyword gates.

**Scenario METH-SCN-027:** Removing an area hub or pointing an area at a missing parent produces a stable diagnostic through `dset check`; debating whether rationale is sufficiently separated remains a rubric-based eval.

## METH-REQ-025 — The framework dogfoods artifact governance

This public repository must activate `documentation-v1`, expose documentation and methodology hubs, register its stable governed areas, and keep current governance separate from archived change evidence.

**Scenario METH-SCN-028:** The same canonical verification command validates Python v1 and documentation v1 without describing documentation as a programming language.

## METH-REQ-026 — DSET 0.2 release is framework-first

A DSET 0.2 capability must not be released until this repository adopts it under every applicable selected profile. When a profile-specific capability is not applicable to this repository, a versioned in-repository adopter fixture must pass before an external pilot may depend on it.

**Scenario METH-SCN-029:** A TypeScript-only gate is not applied to Python sources, but its versioned adopter fixture passes before the gate is presented to Your Harness as released DSET behavior.

## METH-REQ-027 — DSET 0.2 self-hosting is bounded

The DSET 0.2 self-hosting gate must have exactly three bounded levels: the last released validator checks the candidate change, the candidate checks this repository, and the candidate materializes and checks one temporary adopter. The temporary adopter must not create another adopter or traverse unrelated nested DSET roots.

**Scenario METH-SCN-030:** One release run records released-to-candidate, candidate-to-repository, and candidate-to-temporary-adopter results, then terminates at the declared fixed point.

## METH-REQ-028 — DSET 0.2 rules are repository-owned

Every selected normative rule must resolve to one editable governing document inside the adopting repository. A framework template may seed the document, but after materialization the local document is authoritative and the template remains provenance rather than a live fallback.

**Scenario METH-SCN-031:** Editing the framework template after materialization does not change the adopter's resolved rules; editing its registered local governing document does.

## METH-REQ-029 — DSET 0.2 skills are thin wrappers

A DSET 0.2 skill may own trigger metadata, root discovery, workflow identity, resolver invocation, ruleset reporting, output handoff, authorization boundaries, and stop behavior. It must not own substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.

**Scenario METH-SCN-032:** Static inspection finds a workflow ID and resolver handoff in a skill but no copied checklist, concrete threshold, embedded fallback procedure, or substantive normative rule.

## METH-REQ-030 — DSET 0.2 wrappers follow local changes

A DSET 0.2 wrapper must consume the currently resolved repository-local rule set. Changing a registered local rule must affect the next invocation without changing the canonical wrapper.

**Scenario METH-SCN-033:** Two adopters use the same wrapper hash but different registered output conventions; each invocation follows and reports its adopter's local rule identity.

## METH-REQ-031 — DSET 0.2 fails closed on invalid selected ownership

Missing, duplicate, cyclic, outside-root, or profile-incompatible selected rule ownership must stop before governed work and emit a stable diagnostic. A rule or profile explicitly marked not applicable with a valid reason must remain a successful disposition.

**Scenario METH-SCN-034:** A selected rule outside the repository stops with its stable code and path, while an unselected TypeScript profile in a documentation-only adopter passes as justified not applicable.

## METH-REQ-032 — DSET 0.2 identifies customization honestly

A locally changed materialized ruleset remains valid project truth but must identify itself as local/custom and preserve source profile/version provenance. It must not claim equivalence to the unchanged framework profile.

**Scenario METH-SCN-035:** Changing one normative local rule changes the resolved ruleset identity to custom while retaining the originating profile and version as provenance.

## METH-REQ-033 — DSET 0.2 proof categories remain separate

Exact resolver, ownership, path, identity, wrapper, and recursion behavior must be proven by deterministic tests. Agent interpretation, rule-following, navigation, and diagnostic usefulness must be proven by separate qualitative or probabilistic evals. Automation does not change the proof category.

**Scenario METH-SCN-036:** A scripted assertion that a cycle emits one stable code remains a test; an automated agent run measuring whether the diagnostic enables a safe correction remains an eval.

## METH-REQ-034 — DSET 0.2 gives every rule one owner

Every normative rule ID must resolve to exactly one editable governing document. Agent guidance, skills, templates, generated installations, indexes, summaries, and caches may link to that owner or reproduce derived metadata but must not become additional writable rule authorities.

**Scenario METH-SCN-037:** The registry rejects two governing documents claiming the same rule ID and accepts multiple navigation or generated surfaces that point to the single owner without restating its normative text.

## METH-REQ-035 — DSET exposes five core user-facing skills

The core distribution must expose exactly five user-facing skills: `dset` for lifecycle orchestration and next-step routing; `dset-clarify` for unresolved domain/specification branches; `dset-diagnose` for evidence-first diagnosis; `dset-prototype` for bounded disposable experiments; and `dset-release` for the guarded release transaction. Initialization, decomposition, Solution Landscape work, ADR/spec/proof/implementation planning, implementation, verification, ticket handling, and next-step advice must remain governed `dset` modes or chained workflows rather than additional public skills.

**Scenario METH-SCN-038:** A large feature request enters through `dset`; the local orchestration rules select decomposition or clarification first and invoke a specialist only when its distinct trigger applies.

## METH-REQ-036 — The primary skill orchestrates local rules

`dset` must discover current repository, project, package, feature, change, proof, and Git state; resolve the registered orchestration workflow; report its ruleset identity; select one bounded next action; and chain only registered workflows. It must not embed the substantive lifecycle or silently authorize writes, publication, external messages, or other consequential effects.

**Scenario METH-SCN-039:** Byte-identical `dset` wrappers route two repositories differently because their project-owned rules and current artifacts differ, while both report the resolved local identities before acting.

## METH-REQ-037 — Skill runs record bounded local evidence

Every skill invocation must append one structured record under ignored machine-local `.dset/runs/`. The record must contain run identity, time, repository/change/package/feature scope, skill and workflow IDs, resolved ruleset identity, main parameters, named output artifacts, result, and next-step signals. It must exclude secrets, full prompts, private source content, and unnecessary raw logs. A run record may inform `dset` heuristics or incident investigation but cannot replace accepted specs, active changes, Git history, authoritative PR/check state, or proof promoted into the owning change.

**Scenario METH-SCN-040:** A local log suggests verification is current, but Git shows later code changes; `dset` treats Git/change state as authoritative and recommends refreshed proof.

## METH-REQ-038 — Every main PR has one pre-1.0 release transition

The DSET product and distributable CLI package must share one SemVer-compatible `MAJOR.MINOR.PATCH[-PRERELEASE]` identity. The first policy-bearing release initializes `0.2.0`. Every later accepted `dev` to `main` PR must declare exactly one class: `normal` increments the pre-1.0 minor component and resets patch; `small` increments patch; `rc` advances `1.0.0-rc.N`; and `final` promotes the passing RC to `1.0.0`. Components are integers, not decimal fractions, and no normal or small transition may produce `1.0.0`.

**Scenario METH-SCN-041:** `0.2.4` becomes `0.3.0` for a normal PR or `0.2.5` for a small PR; `0.9.0` becomes `0.10.0`, never `1.0.0`.

## METH-REQ-039 — Release preparation precedes protected publication

`dset-release` must resolve repository-local release, proof, artifact-maintenance, and supportability rules. The `dev` branch and implementing PR must own release class, target version, synchronized version surfaces, migration/release notes, and readiness evidence before merge. The protected `main` merge commit owns the immutable release identity; post-merge automation may create the matching tag and GitHub Release but must not add an unreviewed content commit or bypass the pull-request path.

**Scenario METH-SCN-042:** A PR with mismatched product/package targets fails before merge; a passing merge is tagged at its exact merge commit without modifying `main` files afterward.

## METH-REQ-040 — RC and final releases are fully working gates

`1.0.0-rc.N` may begin only when the declared 1.0 scope is feature-complete, self-hosted, documented, supportable, migration-ready, green under every deterministic test and applicable eval, verified in required adopters or pilots, and free of known release-blocking defects. RC changes are limited to blocker corrections and validation evidence. `1.0.0` may publish only from a passing RC after final observation and distribution gates pass; time or accumulated pre-1.0 increments cannot replace proof.

**Scenario METH-SCN-043:** A green candidate with one required pilot unfinished remains `0.y.z`; a fully working `1.0.0-rc.2` may promote to `1.0.0` only after final evidence passes and without adding features.

## METH-REQ-041 — Product/package identity is coordinated

The framework product version, CLI package version, release notes, Git tag, and GitHub Release must carry the same release identity. Schema, governance-profile, language-profile, artifact-profile, and template-format versions remain independent compatibility surfaces and change only when their own contracts change. Independent compatibility versions must never be presented as product maturity or 1.0 readiness.

**Scenario METH-SCN-044:** Product/package `0.3.0` may validly use schema `1.0` and governance profile `core-v1@0.2`; neither compatibility version implies DSET 1.0 readiness.
