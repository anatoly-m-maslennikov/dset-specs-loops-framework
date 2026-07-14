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
| Product/package release identity | `dset/version.yaml` plus package metadata | Reviewed `dev` to `main` release PR | Exactly once per accepted PR | Version transition and surface-consistency tests |
| Local skill-run evidence | Ignored `.dset/runs/` records | Invoked skill/runtime | Every run; bounded retention | Schema/redaction tests and authoritative-state comparison |
| Immutable published release | Protected `main` merge commit, tag, and GitHub Release | Post-merge automation | Successful release PR merge | Tag/commit/release identity check and rollback runbook |

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
- Publish five core user-facing skills: primary `dset`, specialist `dset-clarify`, `dset-diagnose`, `dset-prototype`, and guarded `dset-release`; keep helper operations as registered modes or chained workflows.
- Store bounded skill-run evidence under ignored `.dset/runs/`; never let heuristics override accepted artifacts, Git history, or hosted state.
- Treat normal/small as pre-1.0 minor/patch transitions, reserve RC/final for the explicit `1.0.0` readiness gate, and never derive 1.0 by decimal arithmetic.
- Prepare synchronized release artifacts before merge and publish the immutable tag/release from the protected merge commit after merge.
- No ADR is required because these choices implement the already accepted DSET 0.2 invariants without introducing an external component or irreversible production architecture.
