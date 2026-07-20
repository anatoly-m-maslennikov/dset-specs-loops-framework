# Design — Make DSET self-hosting and skills thin

## Boundaries

This change implements the DSET 0.3 invariant contract through roadmap §4 and finalizes the skill/release contract for later implementation. The repository manifest selects one local governance profile; the registry owns resolution metadata; registered local documents own normative rules; wrappers own invocation only; templates remain provenance; the recursive runner stops after one temporary adopter; and release preparation cannot bypass protected delivery. The roadmap owns sequencing, accepted methodology owns the release contract, and this active Change owns unaccepted mechanics and evidence.

The concrete distribution/platform/dependency/hosted-delivery contracts are defined
in [contracts.md](specs/contracts.md). They state observable compatibility and
evidence boundaries; Decisions remain separate records of choices and rationale.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Selected profile | `dset/scopes/meta/dset.yaml` | Project change | Explicit reviewed edit | Schema and repository check |
| Rule routing/provenance | `dset/scopes/gov/governance.yaml` | Explicit materialize/refresh transaction | Every governed invocation | Governance schema and stable diagnostics |
| Normative project rules | `dset/scopes/<layer>/governance/*.md` | Owning project layer | Next resolution | Digest/customization and mutation proof |
| Framework defaults | `dset/scopes/<layer>/templates/governance/core-v1/` | Framework change | Explicit adopter comparison only | Template/schema tests |
| Canonical wrappers | `skills/*/SKILL.md` plus registered digest | Framework change | Install/generation | Static thinness and generated-copy identity tests |
| Shared skill runtime | Versioned framework distribution installed under the host package root; Codex uses `$CODEX_HOME/packages/dset/` | DSET package installer | Every skill invocation and distribution upgrade | Explicit-target context resolution, catalog identity, package manifest, and cross-platform fixtures |
| Host-native installations | Declared host package/install surface | Generated or linked from canonical wrapper source | Every supported-host release | Clean install, host discovery, invocation, handoff, and stop proof |
| Platform support | Published applicability plus platform-native entry points | Tool release | Every supported-platform release | Native macOS/Windows/WSL/Linux jobs or explicit pre-write rejection |
| Dependency set | Lockfile, allowlist/denylist, registry/license/provenance record, bounded exceptions | Reviewed dependency change | Resolution and publication | Lockfile/license/provenance enforcement and exception-expiry fixtures |
| Released baseline | Commit in `dset/scopes/meta/version.yaml` | Release process | Candidate self-host run | Extracted released-validator check |
| Candidate and adopter | Current checkout and temporary directory | Candidate command | One bounded run | Self-host report and failure matrix |
| Hosted PR/check state | GitHub | GitHub workflows/rulesets | Live query | Delivery runbook |
| Protected delivery proof | GitHub workflow artifact, run/check identity, actual PR SHA, target ruleset | GitHub and protected integration | Every release PR head | Hosted run/check and protected-branch acceptance or block evidence |
| Product/package release identity | Change release declaration; `dset/scopes/meta/version.yaml` and package metadata are mirrors | Reviewed integration-to-protected release PR | Exactly once per accepted PR | Version transition and surface-consistency tests |
| Local skill-run evidence | Ignored `.dset/runs/` records | Invoked skill/runtime | Every run; bounded retention | Schema/redaction tests and authoritative-state comparison |
| Immutable published release | Configured protected merge commit, tag, and publisher release | Post-merge automation | Successful release PR merge | Tag/commit/release identity check and recovery runbook |
| Delegation budget | Resolved project orchestration/budget rule plus current main-session configuration | Orchestrator; explicit operator override | Before each delegation batch | Plan/actual run records and task-relevant evals |

## Change and delivery topology

The repository configures `dev` as its integration branch and `main` as its
protected release branch. The default is local work on `dev`, a push to remote
`dev`, then the release PR from `dev` to `main`. A Change may select an isolated
branch/worktree and review it into `dev` first when parallelism or risk requires
that boundary. This active Change uses the default integration-branch mode for
PR #9. Neither mode creates permanent layer branches or combines unrelated
Change proof.

This Change crosses META, GOV, TOOL, SKILL, and OPS atomically because its
authority, trace, wrapper, and delivery invariants would be invalid if merged as
independent partial states. Later work should split only when each part is
independently reviewable, verifiable, and mergeable. Cross-Change handoffs must
name stable IDs, exact commits or versions, applicable Contracts, evidence
locations, currentness, and reopen triggers.

## Supportability

No adopter application runtime or production data is changed. The CLI reads repository files; only explicit materialize/refresh operations write, and the self-host adopter is temporary. Proposed local skill-run records are ignored, bounded, redacted operational evidence and never project truth. Failures identify the earliest stable boundary. Commit, PR, check, tag, release, and ruleset evidence is covered by the existing [delivery runbook](../../../ops/supportability/delivery-runbook.md). A misleading release claim is contained by keeping this change active and the PR draft until hosted proof, evals, pilots, and release work pass.

## Decisions

- Use one accepted methodology invariant and requirement per roadmap invariant so traceability is mechanical.
- Define framework-first adoption by profile applicability; exercise non-applicable language profiles through versioned in-repository adopter fixtures.
- Define uniqueness per normative rule ID rather than the ambiguous word “concern.”
- Treat explicit justified non-applicability as valid; fail closed only for invalid or incompatible selected ownership.
- Keep exact behavior in tests and agent interpretation/usefulness in evals.
- Replace the unpublished `0.3.0` draft, incomplete `0.2.0` development target, and unreleased independent Python-package `1.0.0` candidate with corrected coordinated DSET/product package bootstrap `0.3.1`; retain schema/profile/template versions as independent compatibility identities and leave archived evidence unchanged.
- Use the exact schema 1.2 migration commit recorded in `dset/scopes/meta/version.yaml` as a temporary fixed-point baseline. It is explicitly not a released-validator substitute: `DSET-PROBLEM-TOOL-001` remains open until a published compatible validator checks a later candidate or an accepted compatibility proof closes the gap.
- Use one registry with local paths and source digests; never read a template as live fallback.
- Treat explicit `rules refresh` as acknowledgement of intentional local customization.
- Use generated adopter copies to prove runtime-wrapper distribution identity without making installed copies rule owners.
- Install shared skill mechanics once per host, use `$CODEX_HOME/packages/dset/`
  for Codex, render its exact package-local launcher into each installed
  wrapper, and keep skill folders limited to thin outcome wrappers.
- Keep `dset` as the catch-all entrypoint and expose one thin direct wrapper for every stable lifecycle mode; do not claim the expanded source, distribution, or host surface before its separate implementation proof.
- Store bounded skill-run evidence under ignored `.dset/runs/`; never let heuristics override accepted artifacts, Git history, or hosted state.
- Use the complete bootstrap/pre-1.0/RC/final/post-1.0 transition table and never derive 1.0 by decimal arithmetic.
- Treat the change release declaration as the single pre-merge owner; publish/retry immutable tag/release objects idempotently from the protected merge commit.
- Inherit the main model and reasoning effort for subagents by default; use a medium two-or-three-agent fan-out only when the task benefits and runtime capacity permits.
- Bound low/medium/high by tree-wide unique agents, depth, and rounds while preserving scope, proof, and safety. Permit model/effort changes only through explicit policy or task-relevant evidence and report every deviation.
- Keep incomparable cost/quality metrics separate; never equate lower token price with lower task cost or use a single-agent benchmark to justify fan-out.
- Route semantic atoms through the flat Decision, Question, Problem, and QA
  model with at most one direct subtype; never nest User Story under
  Requirement, treat Conflict/Risk/Opportunity as Question subtypes and
  Defect/Gap/Debt as Problem subtypes, keep tasks and hosted tickets as
  non-Type workflow representations, and make Change an optional container.
- Treat each atom as one smallest independently reviewable primary claim.
  Split multi-head claims into linked siblings and use the empty subtype on
  irreducible ambiguity. Keep Decision directive content separate from the
  operator acceptance act and carrier; keep QA definitions separate from
  execution, results, evidence, gates, and Verification.
- Define Outcome as a measured state change with baseline, target, source/method, window, and related links or explicit dispositions; never use it as a synonym for a feature, output, milestone, or completed task.
- Defer Journey, Actor/Persona, Hypothesis/Experiment, prioritization, feedback/analytics, and generated roadmap/release views as Questions only; do not create new semantic Types or intake queues before Decisions standardize them.
- Expose the direct subtype kind in an atom ID when a subtype exists and the Type kind when it does not; never encode a nested subtype path. Preserve every emitted legacy ID and its lookup. Implement the successor Type/subtype envelope, recognition boundaries, and compatibility resolver under `DSET-TASK-GOV-049` rather than silently retyping history.

## Open questions

- **DSET-QUESTION-GOV-001 — First-class Action entity** in [`dset/scopes/gov/intake.yaml`](../../../gov/intake.yaml):
  Should a later DSET version promote Action into a first-class entity or intake
  queue, or are tasks inside a change sufficient? Until a Decision resolves this,
  Action is not part of the released ontology and executable work remains in
  `tasks.md`. This is a project question, not accepted methodology.
- Six additional open Questions in [`dset/scopes/gov/intake.yaml`](../../../gov/intake.yaml) defer
  Journey, Actor/Persona, Hypothesis/Experiment, prioritization,
  feedback/analytics, and generated roadmap/release views. They create no new
  ontology or queue until a later Decision accepts one.
