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
| **Artifact governance profile** | Versioned mapping from artifact architecture and authoring rules to machine-checkable ownership, hierarchy, hub, navigation, and portability gates; it is selected independently from an implementation-language profile |
| **Governed artifact area** | A stable public knowledge boundary with one purpose, owner, root, hub, and structural parent |
| **Artifact type** | A document family defined by one primary owning question, such as navigation, normative rules, behavior, architecture, rationale, decision, procedure, proof plan, evidence, or agent workflow |
| **Hub** | A thin navigation surface that identifies an area's purpose, boundaries, and stable owning documents without becoming an exhaustive index or a second normative owner |
| **Production supportability contract** | Risk- and topology-scaled agreement for the evidence, correlation and deploy/change identity, safe diagnostics, data controls, runbook, recovery/escalation paths, and incident-to-fix traceability needed to investigate and repair production behavior |
| **DSET toolchain** | The dependency-light CLI, schemas, templates, fixtures, traceability generator, migration guidance, CI gate, and focused skills that execute the accepted methodology contract |
| **Governance registry** | Repository-local machine-readable mapping from workflow and normative rule IDs to their editable governing documents, dependencies, applicability, and profile/customization identity; it points to rules without restating them |
| **Governing document** | The single editable repository-local owner of one or more normative rule IDs selected by the governance registry |
| **Workflow wrapper** | A thin skill or runtime adapter that discovers the repository, invokes one registered workflow, reports the resolved ruleset, and hands off output without owning substantive rules |
| **Lifecycle orchestrator** | The primary `dset` workflow wrapper that inspects authoritative project/change state, selects a bounded next action, and chains registered workflows without owning their rules |
| **Skill-run record** | Bounded structured machine-local evidence of one invocation, stored under ignored `.dset/runs/` for investigation and heuristics without becoming project truth |
| **Problem** | An observed bug, gap, or debt item that requires triage without implying its solution |
| **Question** | An unresolved choice or uncertainty whose consequential resolution is recorded in an ADR |
| **Opportunity** | A bounded improvement with expected value when no current problem exists |
| **Product release** | One coordinated DSET framework and distributable CLI-package identity prepared through the configured integration-to-protected release PR and published from its protected merge commit |
| **Release candidate** | A fully working `1.0.0-rc.N` build whose declared scope and required proof are complete and whose remaining work is release-blocker correction or final validation only |
| **Delegation budget** | Project-owned policy for inherited model/effort, useful subagent fan-out, roles, rounds, context/evidence depth, tool/live-eval allowance, and stopping thresholds |
| **Expected outcome cost** | Predicted completed-task cost across token price/volume, retries, agent/tool steps, latency, failure probability, review burden, and rework rather than token price alone |
| **Ruleset identity** | Stable declaration of selected profile/version provenance and whether the materialized local rules remain equivalent or have become a valid custom project profile |
| **Self-hosting gate** | Bounded release proof in which the last released validator checks the candidate change, the candidate checks this repository, and the candidate materializes and checks one non-recursive temporary adopter |
| **Diagnostic** | A stable code, artifact path, and actionable message emitted by a deterministic DSET gate |
| **Traceability index** | A deterministic committed view from changes to packages, requirements, tests, evals, ADRs, evidence, and repository-qualified PRs; it is derived evidence rather than the owner of GitHub state or code diffs |
| **Hosted delivery automation** | GitHub workflows and rulesets that govern the repository's production publication path and use GitHub PR/check/run/commit identities as authoritative operational evidence |

## Invariants

- **METH-INV-001:** Framework truth and project truth never share a writable owner.
- **METH-INV-002:** Deterministic tests and probabilistic/qualitative evals remain separate artifacts and evidence streams.
- **METH-INV-003:** Runtime risk, durability topology, effect safety, language enforcement, and artifact governance are selected explicitly rather than inherited from one universal tool class.
- **METH-INV-004:** Each durable concern has one authoritative owner; process memory and derived views are not independent truth.
- **METH-INV-005:** Public methodology renders and navigates on GitHub without Obsidian-only links or callouts.
- **METH-INV-006:** A change cannot alter accepted truth until its proof is fresh and the change is archived through its implementing PR.
- **METH-INV-007:** Every production-bound tool has an explicit supportability contract scaled to its risk profile and topology; a non-production tool may mark it not applicable only with a reason.
- **METH-INV-008:** The canonical validator is read-only; scaffolding, trace updates, and archival require explicit write commands and never overwrite existing project truth.
- **METH-INV-009:** Stable diagnostic codes and deterministic trace ordering are compatibility surfaces; explanatory prose may improve without changing their meaning.
- **METH-INV-010:** Repository skills have distinct triggers and stop conditions and cannot replace the owning DSET specification, diagnosis authorization boundary, or implementation plan.
- **METH-INV-011:** Each governed artifact has one primary type and owning question; links connect authorities without duplicating their rules.
- **METH-INV-012:** Hubs own navigation and boundaries, while atomic documents own rules, rationale, procedures, decisions, proof, and history.
- **METH-INV-013:** Before release, this repository adopts every new capability applicable to its selected profiles; a non-applicable profile-specific capability passes through a versioned in-repository adopter fixture before any external pilot depends on it.
- **METH-INV-014:** Self-hosting terminates after released-to-candidate, candidate-to-repository, and candidate-to-temporary-adopter proof; the temporary adopter never recursively creates another adopter.
- **METH-INV-015:** Every selected normative rule resolves to one editable governing document inside the adopting repository; a source template remains provenance rather than a live authority after materialization.
- **METH-INV-016:** Workflow wrappers own discovery, invocation, reporting, handoff, authorization, and stop behavior but no substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.
- **METH-INV-017:** Changing a registered local rule changes the next governed invocation without changing the canonical workflow wrapper.
- **METH-INV-018:** Invalid or incompatible selected rule ownership fails closed with a stable diagnostic, while explicitly justified non-applicability remains valid.
- **METH-INV-019:** A locally changed ruleset remains valid project truth only under an explicit custom identity that retains its source profile/version provenance.
- **METH-INV-020:** Exact governance and recursion behavior remains deterministic test proof; agent interpretation, rule-following, navigation, and diagnostic usefulness remain separate eval proof.
- **METH-INV-021:** Every normative rule ID has exactly one editable governing document; skills, agent guidance, templates, generated installations, indexes, summaries, and caches never become parallel writable rule stores.
- **METH-INV-022:** The release-target user-facing skill surface contains one primary `dset` orchestrator plus the narrow `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` specialists; helper lifecycle actions remain modes or chained workflows.
- **METH-INV-023:** Skill-run records are schema-bounded, redacted, immutable local operational evidence with finite retention; unavailable persistence is explicit, and records never override accepted artifacts, active changes, Git history, hosted state, or promoted proof.
- **METH-INV-024:** Every release PR has one committed bootstrap, normal, small, RC, final, or post-1.0 breaking transition selected by the complete state table; integer-component progression never promotes `0.y.z` to `1.0.0` automatically.
- **METH-INV-025:** Release artifacts are prepared and reviewed before merge; immutable tag and publisher-release identity derive from the configured protected merge commit without a post-merge content mutation.
- **METH-INV-026:** `1.0.0-rc.N` and `1.0.0` represent fully working, evidence-complete gates; schedules, accumulated version increments, or partial scope cannot substitute for readiness.
- **METH-INV-027:** Product, CLI package, release notes, tag, and publisher release share one canonical/equivalent release identity, while schemas, profiles, and template formats retain independent compatibility versions.
- **METH-INV-028:** Subagents request the main session's model and reasoning effort by default; capability and effective configuration are attested when possible, and every uncertainty or deviation is explicit.
- **METH-INV-029:** One tree-wide low/medium/high budget preserves requested scope, required proof, and safety while bounding unique agents, depth, and rounds; nominal token price alone never proves a cheaper plan.
- **METH-INV-030:** Intake routes only to problems, opportunities, or questions; ADRs/decisions and changes are artifacts, tasks live inside changes, and external tickets are representations rather than semantic types.
