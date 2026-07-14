# Design — Make DSET self-hosting and skills thin

## Boundaries

This change implements the DSET 0.2 invariant contract through roadmap §4 and finalizes the skill/release contract for later implementation. The repository manifest selects one local governance profile; the registry owns resolution metadata; registered local documents own normative rules; wrappers own invocation only; templates remain provenance; the recursive runner stops after one temporary adopter; and release preparation cannot bypass protected delivery. The roadmap owns sequencing, accepted methodology owns the release contract, and this active change owns unaccepted mechanics and evidence.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Selected profile | `dset/dset.yaml` | Project change | Explicit reviewed edit | Schema and repository check |
| Rule routing/provenance | `dset/governance.yaml` | Explicit materialize/refresh transaction | Every governed invocation | Governance schema and stable diagnostics |
| Normative project rules | `dset/governance/*.md` | Owning project | Next resolution | Digest/customization and mutation proof |
| Framework defaults | `dset/templates/governance/core-v1/` | Framework change | Explicit adopter comparison only | Template/schema tests |
| Canonical wrappers | `skills/*/SKILL.md` plus registered digest | Framework change | Install/generation | Static thinness and generated-copy identity tests |
| Released baseline | Commit in `dset/version.yaml` | Release process | Candidate self-host run | Extracted released-validator check |
| Candidate and adopter | Current checkout and temporary directory | Candidate command | One bounded run | Self-host report and failure matrix |
| Hosted PR/check state | GitHub | GitHub workflows/rulesets | Live query | Delivery runbook |
| Product/package release identity | Change release declaration; `dset/version.yaml` and package metadata are mirrors | Reviewed integration-to-protected release PR | Exactly once per accepted PR | Version transition and surface-consistency tests |
| Local skill-run evidence | Ignored `.dset/runs/` records | Invoked skill/runtime | Every run; bounded retention | Schema/redaction tests and authoritative-state comparison |
| Immutable published release | Configured protected merge commit, tag, and publisher release | Post-merge automation | Successful release PR merge | Tag/commit/release identity check and recovery runbook |
| Delegation budget | Resolved project orchestration/budget rule plus current main-session configuration | Orchestrator; explicit operator override | Before each delegation batch | Plan/actual run records and task-relevant evals |

## Supportability

No adopter application runtime or production data is changed. The CLI reads repository files; only explicit materialize/refresh operations write, and the self-host adopter is temporary. Proposed local skill-run records are ignored, bounded, redacted operational evidence and never project truth. Failures identify the earliest stable boundary. Commit, PR, check, tag, release, and ruleset evidence is covered by the existing [delivery runbook](../../supportability/delivery-runbook.md). A misleading release claim is contained by keeping this change active and the PR draft until hosted proof, evals, pilots, and release work pass.

## Decisions

- Use one accepted methodology invariant and requirement per roadmap invariant so traceability is mechanical.
- Define framework-first adoption by profile applicability; exercise non-applicable language profiles through versioned in-repository adopter fixtures.
- Define uniqueness per normative rule ID rather than the ambiguous word “concern.”
- Treat explicit justified non-applicability as valid; fail closed only for invalid or incompatible selected ownership.
- Keep exact behavior in tests and agent interpretation/usefulness in evals.
- Replace the unreleased independent Python-package `1.0.0` candidate with the coordinated DSET/product package release `0.2.0`; retain schema/profile/template versions as independent compatibility identities and leave archived v1 evidence unchanged.
- Use the pre-0.2 commit recorded in `dset/version.yaml` as the released validator baseline.
- Use one registry with local paths and source digests; never read a template as live fallback.
- Treat explicit `rules refresh` as acknowledgement of intentional local customization.
- Use generated adopter copies to prove runtime-wrapper distribution identity without making installed copies rule owners.
- Target five core user-facing skills: primary `dset`, specialist `dset-clarify`, `dset-diagnose`, `dset-prototype`, and guarded `dset-release`; do not claim the two new wrappers are released before implementation proof.
- Store bounded skill-run evidence under ignored `.dset/runs/`; never let heuristics override accepted artifacts, Git history, or hosted state.
- Use the complete bootstrap/pre-1.0/RC/final/post-1.0 transition table and never derive 1.0 by decimal arithmetic.
- Treat the change release declaration as the single pre-merge owner; publish/retry immutable tag/release objects idempotently from the protected merge commit.
- Inherit the main model and reasoning effort for subagents by default; use a medium two-or-three-agent fan-out only when the task benefits and runtime capacity permits.
- Bound low/medium/high by tree-wide unique agents, depth, and rounds while preserving scope, proof, and safety. Permit model/effort changes only through explicit policy or task-relevant evidence and report every deviation.
- Keep incomparable cost/quality metrics separate; never equate lower token price with lower task cost or use a single-agent benchmark to justify fan-out.
- Route intake through problems, opportunities, and questions; put tasks inside changes and treat ADRs/changes as artifacts and hosted tickets as representations.

## Open questions

- [**MDSHAST-QUESTION-001 — First-class Action entity**](../../questions.md#mdshast-question-001--should-action-become-a-first-class-entity):
  Should a later DSET version promote Action into a first-class entity or intake
  queue, or are tasks inside a change sufficient? Until an ADR resolves this,
  Action is not part of the released ontology and executable work remains in
  `tasks.md`.
