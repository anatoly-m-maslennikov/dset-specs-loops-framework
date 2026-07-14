# Design — Make DSET self-hosting and skills thin

## Boundaries

This batch defines the DSET 0.2 release invariant contract. It owns stable requirement and proof IDs, not the resolver, wrappers, templates, or recursive runner. The roadmap owns sequencing; accepted methodology truth owns the eventual release contract; the active change owns unaccepted deltas and evidence.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Roadmap invariant wording | DSET 0.2 roadmap | Single repository writer | When planning changes | Diff review |
| Candidate invariant delta | This active change | Single PR branch | Every change revision | MDSHAST-TEST/EVAL IDs |
| Accepted invariant contract | `dset/specs/packages/methodology/` after merge | Protected `main` through `dev` PR | Release and adopter resolution | METH-TEST/EVAL IDs |
| Hosted PR/check state | GitHub | GitHub workflows/rulesets | Live query | Delivery runbook |

## Supportability

No application runtime is changed. Commit, PR, check, and ruleset evidence is covered by the existing [delivery runbook](../../supportability/delivery-runbook.md). A misleading contract is contained by keeping the change active and making every new requirement a DSET 0.2 release condition rather than a current capability claim.

## Decisions

- Use one accepted methodology invariant and requirement per roadmap invariant so traceability is mechanical.
- Define framework-first adoption by profile applicability; exercise non-applicable language profiles through versioned in-repository adopter fixtures.
- Define uniqueness per normative rule ID rather than the ambiguous word “concern.”
- Treat explicit justified non-applicability as valid; fail closed only for invalid or incompatible selected ownership.
- Keep exact behavior in tests and agent interpretation/usefulness in evals.
- No ADR is required for this contract-only batch because it refines already selected roadmap decisions without choosing an implementation architecture.
