# Requirement connections and delta — DSET 0.3

Already accepted behavior is not redefined in this Change. The table connects
the implementation scope to its current layer-owned Requirement owners.

| Capability | Current Requirement owners |
|---|---|
| Framework-first self-hosting and bounded recursion | `DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-TOOL-004` |
| Repository-owned rules, fail-closed ownership, customization, and one owner | `DSET-REQUIREMENT-GOV-014..017` |
| Separate test/eval proof | `DSET-REQUIREMENT-META-007` |
| Thin wrappers, local-rule following, lifecycle-mode entrypoints, runs, budget, continuity, and outcome-first entry closure | `DSET-REQUIREMENT-SKILL-002..010` |
| Release transaction, RC/final gate, and coordinated version identity | `DSET-REQUIREMENT-OPS-004..007` |
| Intake routing and stable layer-qualified IDs | `DSET-REQUIREMENT-GOV-018..019` |
| Neutral repository or Work Area scope | `DSET-REQUIREMENT-META-011` |
| Atomic authority, compiled projections, absorption, commit provenance, and session provenance | `DSET-REQUIREMENT-GOV-020..022` |
| Governance constitution, dependency/precedence separation, and authority/assurance boundary | `DSET-REQUIREMENT-GOV-023` |
| Generated project health and portable Markdown rendering | `DSET-REQUIREMENT-GOV-024`, `DSET-REQUIREMENT-TOOL-018` |
| Independent external review packet/report and explicit finding reconciliation | `DSET-REQUIREMENT-GOV-025` |
| One explicit or inherited priority for every governed artifact | `DSET-REQUIREMENT-GOV-026` |
| Workflow-independent Problem, Question, and Conflict semantics | `DSET-REQUIREMENT-GOV-027` |
| Recommended optional rationale for Decisions and other atomic artifacts | `DSET-REQUIREMENT-GOV-028` |
| Independent MECE artifact classification and Analysis Report boundaries | `DSET-REQUIREMENT-GOV-029` |
| Type-first artifact names and independently selectable subtype-name capability | `DSET-REQUIREMENT-GOV-030` |
| One-level-down project/group/feature/layer architecture views | `DSET-REQUIREMENT-GOV-031` |
| Narrowest-common-scope ownership for project, group, feature, and layer truth | `DSET-REQUIREMENT-GOV-032` |
| Parent-to-child artifact inheritance, local implementation/cancellation, and direct fallback | `DSET-REQUIREMENT-GOV-033` |
| Many-to-many child-owned lineage and derived reverse/transitive traceability | `DSET-REQUIREMENT-GOV-034` |
| Six flat Delivery lifecycle subtypes | `DSET-REQUIREMENT-OPS-013` |
| Role-aware handling for every governed conflict pairing, with priority selection only where permitted | `DSET-REQUIREMENT-TOOL-019` |
| Evidence-derived TypeScript candidate profile and promotion boundary | `DSET-REQUIREMENT-TOOL-021` |
| Framework-reference versus project-applied TypeScript profile authority | `DSET-REQUIREMENT-TOOL-022` |

The canonical text lives in the accepted META, GOV, TOOL, SKILL, and OPS package
fragments under `dset/scopes/<layer>/specs/packages/methodology/`. This Change
owns implementation and proof for those accepted requirements, not duplicate
normative prose.

Connected accepted IDs are `DSET-REQUIREMENT-META-007`,
`DSET-REQUIREMENT-META-011`, `DSET-REQUIREMENT-TOOL-004`,
`DSET-REQUIREMENT-GOV-014`, `DSET-REQUIREMENT-GOV-015`,
`DSET-REQUIREMENT-GOV-016`, `DSET-REQUIREMENT-GOV-017`,
`DSET-REQUIREMENT-GOV-018`, `DSET-REQUIREMENT-GOV-019`,
`DSET-REQUIREMENT-GOV-020`, `DSET-REQUIREMENT-GOV-021`,
`DSET-REQUIREMENT-GOV-022`, `DSET-REQUIREMENT-GOV-023`,
`DSET-REQUIREMENT-GOV-024`, `DSET-REQUIREMENT-GOV-025`,
`DSET-REQUIREMENT-GOV-026`, `DSET-REQUIREMENT-GOV-027`,
`DSET-REQUIREMENT-GOV-028`,
`DSET-REQUIREMENT-GOV-029`,
`DSET-REQUIREMENT-GOV-030`, `DSET-REQUIREMENT-GOV-031`,
`DSET-REQUIREMENT-GOV-032`,
`DSET-REQUIREMENT-GOV-033`,
`DSET-REQUIREMENT-GOV-034`,
`DSET-REQUIREMENT-TOOL-018`,
`DSET-REQUIREMENT-TOOL-019`,
`DSET-REQUIREMENT-TOOL-021`,
`DSET-REQUIREMENT-TOOL-022`,
`DSET-REQUIREMENT-SKILL-002`, `DSET-REQUIREMENT-SKILL-003`,
`DSET-REQUIREMENT-SKILL-004`, `DSET-REQUIREMENT-SKILL-005`,
`DSET-REQUIREMENT-SKILL-006`, `DSET-REQUIREMENT-SKILL-007`,
`DSET-REQUIREMENT-SKILL-008`, `DSET-REQUIREMENT-SKILL-009`,
`DSET-REQUIREMENT-SKILL-010`,
`DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-OPS-004`,
`DSET-REQUIREMENT-OPS-005`, `DSET-REQUIREMENT-OPS-006`,
`DSET-REQUIREMENT-OPS-007`, and `DSET-REQUIREMENT-OPS-013`.

## ADDED — DSET-REQUIREMENT-SKILL-010 Outcome-first entry closure

Public skills accept a desired outcome rather than requiring the operator to
invoke every prerequisite skill manually. Repository-local lifecycle rules own
entry criteria, allowed prerequisite workflows, exit criteria, and stops. Each
transition must satisfy a missing criterion and re-read authority; no progress,
repeated state, cycles, ambiguity, failure, or a new authorization boundary
stops the finite closure.

`dset-implement` invokes `decisions` first, conditionally prepares separate
Test/Evaluation and implementation plans, and implements only after all entry
criteria are satisfied. Session history is candidate evidence rather than
authority, so reconciliation never invents acceptance or edits immutable atoms.

## ADDED — DSET-REQUIREMENT-GOV-029 MECE artifact classification

Every governed carrier must have one primary artifact type and at most one
allowed direct artifact subtype, independently from the four semantic Types.
The project-local artifact-type registry owns the eleven development roles,
their primary questions, direct subtypes, fallback behavior, and path rules.
Analysis Report is non-authoritative and permits Solution Landscape,
Root-Cause Analysis, Proposal, Technical Investigation, and External Audit
Analysis. Unknown, mismatched, nested, missing, or ambiguous classifications
fail closed.

Roadmap, Version Scope, Change, Release Plan, Readiness Record, and Release
Record are direct subtypes of Delivery and share the `DELIVERY` identity
sequence for newly emitted carriers.

**Scenario DSET-SCENARIO-GOV-030:** A Proposal recommends one candidate; a
separate Decision accepts it; Specification/Design compiles it; Evidence Record
captures a Test run; Verification assesses the evidence; and Readiness Record
makes the explicit release gate disposition without any workflow-derived
reclassification.

## ADDED — DSET-REQUIREMENT-GOV-032 Structural-scope ownership

Every claim and compiled artifact belongs to the narrowest common structural
scope containing all affected owners and subjects. Project-level truth owns
only genuinely cross-child or whole-project concerns—shared outcomes and
requirements, Contracts and semantics, end-to-end QA, cross-cutting policy,
integration architecture, release/readiness, and cross-owner unresolved work.
High-level wording does not promote a child-owned claim, and parents link rather
than duplicate child detail.

## ADDED — DSET-REQUIREMENT-GOV-033 Artifact inheritance

Artifact inheritance uses only canonical `child_of` and derived reverse
`parent_to`. If a target feature or layer has no child, it applies the inherited
parent directly. A local child Decision may select implementation, replace, or
cancel the parent only for its subtree, leaving the immutable parent and sibling
scopes unchanged. No additional inheritance relation is introduced.

## ADDED — DSET-REQUIREMENT-GOV-034 Artifact lineage

Every governed non-root child stores `child_of` as a non-empty list of one or
more canonical immediate-parent IDs. Multiple parents and children are valid;
`parent_to`, ancestry, and descendants are derived without editing parents.
The neutral relation traces APP-PLAN decomposition through authority, analysis,
compiled truth, implementation, QA, evidence, Verification, readiness, and
release. Missing parents, authored reverse links, scalar or empty lists,
duplicates, self-links, and cycles fail closed.

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

## ADDED — DSET-REQUIREMENT-GOV-020 Artifact roles

DSET must classify durable artifacts as atomic authority sources, evergreen
compiled projections, transactional context/evidence, or implementation-layer
artifacts so reviewers do not confuse rationale, evidence, code, or generated
views with accepted source truth.

**Scenario DSET-SCENARIO-GOV-021:** An accepted Decision owns its atomic choice,
the spec and proof plans compile the current consequences, and implementation
cites the Decision without becoming authority. If projection and Decision
differ, the Decision wins and the projection is stale.

## ADDED — DSET-REQUIREMENT-GOV-021 Atomic-source compilation

Accepted, active, applicable Requirements, Contracts, Decisions, and other
normative atoms must compile their current behavioral consequences into the
owning evergreen specs, plans, runbooks, or governing rules. Atomic artifacts
are immutable; later state is append-only. A new atom may explicitly and
acyclically absorb older ones while preserving or replacing every applicable
consequence. Only a fully retired atom may move byte-for-byte to `archive/`.

**Scenario DSET-SCENARIO-GOV-022:** A resolved Question produces a Decision, the
Decision compiles into the relevant projection, and review rejects a code-only
change that leaves the spec stale. A successor Decision explicitly absorbs its
immutable predecessor rather than winning because it is newer.

## ADDED — DSET-REQUIREMENT-GOV-022 Commit and session provenance

Commits that change evergreen truth or implementation artifacts must cite the
Decision or Decisions they implement. A Problem, Question, QA atom, or Change
may be cited as additional provenance but never substitutes for authorizing
Decision authority. Newly emitted atomic artifacts and
append-only lifecycle events expose explicit unique host-prefixed
`llm_session_ids` when an LLM helped produce them, or an explicit empty/`none`
disposition for human-only work. Review, correction, and status changes emit
linked records instead of revising atoms. Missing provenance is invalid. The
rule applies to Changes, intake items, Decisions, promoted proofs, skill-run
records, and session checkpoints.

**Scenario DSET-SCENARIO-GOV-023:** A commit body contains
`Implements: DSET-DECISION-GOV-001`, and the Decision artifact records the
Codex session IDs that produced or materially revised it.

## ADDED — DSET-REQUIREMENT-GOV-023 Governance constitution

`DSET-RULE-ARCHITECTURE` remains the sole dependency-free governance root.
Every rule declares separate acyclic dependency and conflict-precedence
relations. Rule authority comes from accepted active atomic sources compiled
into the applicable current local governing document; a mismatch selects the
source and makes the projection stale. Active Decisions explain and authorize
changes, provenance identifies origin, and tests/evals/reviews/evidence assess
assurance without becoming authority.

**Scenario DSET-SCENARIO-GOV-024:** A precedence cycle or missing precedence
owner fails closed. Stale evidence leaves the affected assurance claim stale
and blocks its relying gate without silently erasing the applicable rule.
