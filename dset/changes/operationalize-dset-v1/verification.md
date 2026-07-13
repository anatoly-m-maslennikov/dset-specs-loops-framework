# Verification — DSET v1

- **Implementing PR:** [anatoly-m-maslennikov/dset-specs-loops-framework#7](https://github.com/anatoly-m-maslennikov/dset-specs-loops-framework/pull/7)
- **Status:** verification and evaluator-driven correction in progress; PR remains draft
- **Canonical command:** `python -m dset_toolchain verify .`
- **Locked repository entry point:** `uv run dset verify .`

## Required evidence

| Gate | Status | Evidence |
|---|---|---|
| Schemas/templates/fixtures | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CLI and archive safety | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| Skill validation | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) |
| CI and Markdown portability | Pass | [deterministic verification](proofs/deterministic-verification-2026-07-14.md) and [GitHub delivery evidence](proofs/github-delivery-evidence-2026-07-14.md) |
| Resumability and diagnostics evals | Re-evaluation required | DSET-V1-EVAL-001 found stale handoff text; DSET-V1-EVAL-002 passed |
| Skill routing and migration evals | Re-evaluation required | DSET-V1-EVAL-003 found a write-boundary contradiction; DSET-V1-EVAL-004 passed with template clarification requested |
| Pushed-head archive readiness | Pending | final proof under `proofs/` |

No completion or archive claim is made while any gate is pending or requires re-evaluation.
