# Eval plan — Make DSET self-hosting and skills thin

Accepted qualitative criteria remain owned by their layer plans. This Change
runs them independently from deterministic tests and records disagreements by
case and criterion.

| Owning plan | Applicable Eval IDs |
|---|---|
| [META](../../../meta/specs/packages/methodology/eval-plan.md) | `DSET-EVAL-META-008..009` |
| [GOV](../../../gov/specs/packages/methodology/eval-plan.md) | `DSET-EVAL-GOV-007..021` |
| [SKILL](../../specs/packages/methodology/eval-plan.md) | `DSET-EVAL-SKILL-002..008` |
| [OPS](../../../ops/specs/packages/methodology/eval-plan.md) | `DSET-EVAL-OPS-002..003`, `DSET-EVAL-OPS-010` |

Connected accepted IDs are `DSET-EVAL-META-008`, `DSET-EVAL-META-009`,
`DSET-EVAL-GOV-007`, `DSET-EVAL-GOV-008`, `DSET-EVAL-GOV-009`,
`DSET-EVAL-GOV-010`, `DSET-EVAL-GOV-011`, `DSET-EVAL-GOV-012`,
`DSET-EVAL-GOV-013`,
`DSET-EVAL-GOV-014`, `DSET-EVAL-GOV-015`, `DSET-EVAL-GOV-016`,
`DSET-EVAL-GOV-017`,
`DSET-EVAL-GOV-018`,
`DSET-EVAL-GOV-019`,
`DSET-EVAL-GOV-020`, `DSET-EVAL-GOV-021`,
`DSET-EVAL-SKILL-002`,
`DSET-EVAL-SKILL-003`, `DSET-EVAL-SKILL-004`, `DSET-EVAL-SKILL-005`,
`DSET-EVAL-SKILL-006`, `DSET-EVAL-SKILL-007`, `DSET-EVAL-SKILL-008`,
`DSET-EVAL-OPS-002`, `DSET-EVAL-OPS-003`, and `DSET-EVAL-OPS-010`.

## Change-only qualitative proof

| Eval ID | Scenario | Threshold |
|---|---|---|
| `DSET-EVAL-SKILL-009` | Clean declared Claude, Codex, and other-host fixtures use the published installation path. | Every operator installs or links the real skill, confirms discovery, invokes its trigger, reaches local rules, and identifies the stop boundary. |
| `DSET-EVAL-TOOL-005` | Operators run the utility workflow on every declared platform, including spaces, Unicode, failures, and interrupted writes. | Outcomes are equivalent and safe; any narrower applicability is visible before execution. |
| `DSET-EVAL-TOOL-006` | Reviewers assess allowed, denied, unknown-registry, incompatible-license, provenance-drift, and expired-exception dependencies. | Every reviewer reaches the same accept/stop result from the authoritative rule and does not invent approval. |
| `DSET-EVAL-OPS-008` | A cold operator investigates the implementing PR's live GitHub workflow/run/check and protected-target state. | Every operator binds evidence to the actual PR SHA and selects a safe merge, block, or retry action without bypassing protection. |
| `DSET-EVAL-OPS-009` | Projects use shared integration branches and optional isolated worktrees across concurrent Changes and one protected PR. | Every reviewer identifies branch roles, actual workspace mode, and proof owner without requiring a worktree by default, merging Change identities, or creating permanent layer branches. |

Use at least two independent reviewers where interpretation matters. Correct the
earliest ambiguous owner and rerun the failed case; do not average a blocker
into a pass.
