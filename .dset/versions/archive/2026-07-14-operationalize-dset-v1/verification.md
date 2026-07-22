# Verification — DSET v1

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)
- **Status:** archive evidence complete and ready for protected merge; PR remains draft until the evidence-only head passes hosted checks
- **Canonical command:** `python -m dset_toolchain verify .`
- **Locked repository entry point:** `uv run dset verify .`

## Required evidence

| Gate | Status | Evidence |
|---|---|---|
| Schemas/templates/fixtures | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CLI and archive safety | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| Skill validation | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CI and Markdown portability | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) and [GitHub delivery evidence](proofs/github-delivery-evidence-2026-07-14.md) |
| Resumability and diagnostics evals | Pass | [qualitative evaluations](proofs/qualitative-evals-2026-07-14.md), including the corrected DSET-EVAL-GOV-005 failure |
| Skill routing and migration evals | Pass | [qualitative evaluations](proofs/qualitative-evals-2026-07-14.md), including the corrected DSET-EVAL-SKILL-001 failure |
| Pushed-head archive readiness | Pass | [archive readiness](proofs/archive-readiness-2026-07-14.md) |

## Accepted truth

Accepted-truth reconciliation: Pass

Requirements `DSET-REQUIREMENT-TOOL-001..004`, `DSET-REQUIREMENT-SKILL-001`, and `DSET-REQUIREMENT-OPS-007` and their proof contracts are reconciled as the historical METH requirement set in `dset/specs/packages/methodology/`. Project identity, profiles, supportability ownership, package registry, public navigation, and delivery policy are consistent with the implementation. External pilots, the JavaScript/TypeScript applied profile, Solution Landscape hardening, and Back-to-Left fixtures remain roadmap work and are not claimed by this change.

Disposition: accepted for protected merge. The dated directory remains a candidate on the still-draft PR until GitHub merges PR #7. GitHub owns the final head, checks, and merge result; any later implementation or accepted-specification edit invalidates this evidence.
