# Requirement connections and delta — DSET 0.3

Already accepted behavior is not redefined in this Change. The table connects
the implementation scope to its current layer-owned Requirement owners.

| Capability | Current Requirement owners |
|---|---|
| Framework-first self-hosting and bounded recursion | `DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-TOOL-004` |
| Repository-owned rules, fail-closed ownership, customization, and one owner | `DSET-REQUIREMENT-GOV-014..017` |
| Separate test/eval proof | `DSET-REQUIREMENT-META-007` |
| Thin wrappers, local-rule following, five-skill orchestration, runs, budget, and continuity | `DSET-REQUIREMENT-SKILL-002..009` |
| Release transaction, RC/final gate, and coordinated version identity | `DSET-REQUIREMENT-OPS-004..007` |
| Intake routing and stable layer-qualified IDs | `DSET-REQUIREMENT-GOV-018..019` |
| Neutral repository or Work Area scope | `DSET-REQUIREMENT-META-011` |
| Artifact classes, compile-down, commit provenance, and session provenance | `DSET-REQUIREMENT-GOV-020..022` |

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
`DSET-REQUIREMENT-GOV-022`,
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

## ADDED — DSET-REQUIREMENT-GOV-020 Artifact authority classes

DSET must classify durable artifacts as evergreen current truth,
transactional atomic records, or implementation-layer artifacts so reviewers do
not confuse rationale, evidence, code, or generated views with accepted specs
and plans.

**Scenario DSET-SCENARIO-GOV-021:** A Decision records why a behavior changes,
the spec and proof plans own the current behavior, and the implementation cites
the Decision without becoming a specification.

## ADDED — DSET-REQUIREMENT-GOV-021 Transactional compile-down

Accepted Decisions, Problems, Opportunities, Questions, proofs, and other
transactional artifacts must compile their current behavioral consequences into
the owning evergreen specs, plans, contracts, runbooks, or governing rules
before implementation relies on them.

**Scenario DSET-SCENARIO-GOV-022:** A resolved Question produces a Decision, the
Decision updates the relevant current truth, and review rejects a code-only
change that leaves the spec stale.

## ADDED — DSET-REQUIREMENT-GOV-022 Commit and session provenance

Commits that change evergreen truth or implementation artifacts must cite the
Decision they implement, or the authorizing Problem, Opportunity, Question, or
Change when no Decision is required. Atomic artifacts record `llm_session_ids`
when an LLM helped create or materially revise them.

**Scenario DSET-SCENARIO-GOV-023:** A commit body contains
`Implements: DSET-DECISION-GOV-001`, and the Decision artifact records the
Codex session IDs that produced or materially revised it.
