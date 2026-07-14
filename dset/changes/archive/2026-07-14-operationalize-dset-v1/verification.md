# Verification — DSET v1

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)
- **Status:** dated archive candidate created by the guarded CLI; final pushed-head evidence remains pending; PR remains draft
- **Canonical command:** `python -m dset_toolchain verify .`
- **Locked repository entry point:** `uv run dset verify .`

## Required evidence

| Gate | Status | Evidence |
|---|---|---|
| Schemas/templates/fixtures | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CLI and archive safety | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| Skill validation | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CI and Markdown portability | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) and [GitHub delivery evidence](proofs/github-delivery-evidence-2026-07-14.md) |
| Resumability and diagnostics evals | Pass | [qualitative evaluations](proofs/qualitative-evals-2026-07-14.md), including the corrected DSET-V1-EVAL-001 failure |
| Skill routing and migration evals | Pass | [qualitative evaluations](proofs/qualitative-evals-2026-07-14.md), including the corrected DSET-V1-EVAL-003 failure |
| Pushed-head archive readiness | Pending | final proof under `proofs/` |

## Accepted truth

Accepted-truth reconciliation: Pass

Requirements DSET-V1-REQ-001–006 and their proof contracts are reconciled as METH-REQ-014–019 in `dset/specs/packages/methodology/`. Project identity, profiles, supportability ownership, package registry, public navigation, and delivery policy are consistent with the implementation. External pilots, the JavaScript/TypeScript applied profile, Solution Landscape hardening, and Back-to-Left fixtures remain roadmap work and are not claimed by this change.

The directory move is an archive candidate on the still-draft PR, not accepted history. No completion claim is made while pushed-head archive readiness remains pending.
