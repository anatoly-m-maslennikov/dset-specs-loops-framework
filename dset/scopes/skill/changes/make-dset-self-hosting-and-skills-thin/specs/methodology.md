# Requirement connections and delta — DSET 0.3

Already accepted behavior is not redefined in this Change. The table connects
the implementation scope to its current layer-owned Requirement owners.

| Capability | Current Requirement owners |
|---|---|
| Framework-first self-hosting and bounded recursion | `DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-TOOL-004` |
| Repository-owned rules, fail-closed ownership, customization, and one owner | `DSET-REQUIREMENT-GOV-014..017` |
| Separate test/eval proof | `DSET-REQUIREMENT-META-007` |
| Thin wrappers, local-rule following, lifecycle-mode entrypoints, runs, budget, and continuity | `DSET-REQUIREMENT-SKILL-002..009` |
| Release transaction, RC/final gate, and coordinated version identity | `DSET-REQUIREMENT-OPS-004..007` |
| Intake routing and stable layer-qualified IDs | `DSET-REQUIREMENT-GOV-018..019` |
| Neutral repository or Work Area scope | `DSET-REQUIREMENT-META-011` |
| Atomic authority, compiled projections, absorption, commit provenance, and session provenance | `DSET-REQUIREMENT-GOV-020..022` |
| Governance constitution, dependency/precedence separation, and authority/assurance boundary | `DSET-REQUIREMENT-GOV-023` |
| Generated project health and portable Markdown rendering | `DSET-REQUIREMENT-GOV-024`, `DSET-REQUIREMENT-TOOL-018` |
| Independent external review packet/report and explicit finding reconciliation | `DSET-REQUIREMENT-GOV-025` |
| One explicit or inherited priority for every governed artifact | `DSET-REQUIREMENT-GOV-026` |
| Workflow-independent Problem, Question, and Conflict semantics | `DSET-REQUIREMENT-GOV-027` |
| Role-aware handling for every governed conflict pairing, with priority selection only where permitted | `DSET-REQUIREMENT-TOOL-019` |

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
`DSET-REQUIREMENT-TOOL-018`,
`DSET-REQUIREMENT-TOOL-019`,
`DSET-REQUIREMENT-SKILL-002`, `DSET-REQUIREMENT-SKILL-003`,
`DSET-REQUIREMENT-SKILL-004`, `DSET-REQUIREMENT-SKILL-005`,
`DSET-REQUIREMENT-SKILL-006`, `DSET-REQUIREMENT-SKILL-007`,
`DSET-REQUIREMENT-SKILL-008`, `DSET-REQUIREMENT-SKILL-009`,
`DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-OPS-004`,
`DSET-REQUIREMENT-OPS-005`, `DSET-REQUIREMENT-OPS-006`, and
`DSET-REQUIREMENT-OPS-007`.

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
Decision they implement, or the authorizing Problem, Opportunity, Question, or
Change when no Decision is required. Newly emitted atomic artifacts and
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
