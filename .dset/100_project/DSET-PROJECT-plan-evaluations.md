# Eval plan — Make DSET self-hosting and skills thin

Accepted qualitative criteria remain owned by their layer plans. This Change
runs them independently from deterministic tests and records disagreements by
case and criterion.

| Owning plan | Applicable Eval IDs |
|---|---|
| `plan-evaluations.md` | `DSET-EVAL-PLAN-META-008..009` |
| `plan-evaluations.md` | `DSET-EVAL-PLAN-GOV-007..022`, `DSET-EVAL-PLAN-GOV-025`, `DSET-EVAL-PLAN-GOV-026`, `DSET-EVAL-PLAN-GOV-028..029`, `DSET-EVAL-PLAN-GOV-032..034` |
| `plan-evaluations.md` | `DSET-EVAL-PLAN-TOOL-003..004` |
| `plan-evaluations.md` | `DSET-EVAL-PLAN-SKILL-002..008`, `DSET-EVAL-PLAN-SKILL-010..011` |
| `plan-evaluations.md` | `DSET-EVAL-PLAN-OPS-002..003`, `DSET-EVAL-PLAN-OPS-010` |

Connected accepted IDs are `DSET-EVAL-PLAN-META-008`, `DSET-EVAL-PLAN-META-009`,
`DSET-EVAL-PLAN-GOV-007`, `DSET-EVAL-PLAN-GOV-008`, `DSET-EVAL-PLAN-GOV-009`,
`DSET-EVAL-PLAN-GOV-010`, `DSET-EVAL-PLAN-GOV-011`, `DSET-EVAL-PLAN-GOV-012`,
`DSET-EVAL-PLAN-GOV-013`,
`DSET-EVAL-PLAN-GOV-014`, `DSET-EVAL-PLAN-GOV-015`, `DSET-EVAL-PLAN-GOV-016`,
`DSET-EVAL-PLAN-GOV-017`,
`DSET-EVAL-PLAN-GOV-018`,
`DSET-EVAL-PLAN-GOV-019`,
`DSET-EVAL-PLAN-GOV-020`, `DSET-EVAL-PLAN-GOV-021`, `DSET-EVAL-PLAN-GOV-022`,
`DSET-EVAL-PLAN-GOV-025`, `DSET-EVAL-PLAN-GOV-026`,
`DSET-EVAL-PLAN-TOOL-003`,
`DSET-EVAL-PLAN-TOOL-004`,
`DSET-EVAL-PLAN-SKILL-002`,
`DSET-EVAL-PLAN-SKILL-003`, `DSET-EVAL-PLAN-SKILL-004`, `DSET-EVAL-PLAN-SKILL-005`,
`DSET-EVAL-PLAN-SKILL-006`, `DSET-EVAL-PLAN-SKILL-007`, `DSET-EVAL-PLAN-SKILL-008`,
	`DSET-EVAL-PLAN-SKILL-010`, `DSET-EVAL-PLAN-SKILL-011`,
`DSET-EVAL-PLAN-OPS-002`, `DSET-EVAL-PLAN-OPS-003`, and `DSET-EVAL-PLAN-OPS-010`.

## Change-only qualitative proof

| Eval ID | Scenario | Threshold |
|---|---|---|
| `DSET-EVAL-PLAN-SKILL-009` | Clean declared Claude, Codex, and other-host fixtures use the published installation path. | Every operator installs or links the real skill, confirms discovery, invokes its trigger, reaches local rules, and identifies the stop boundary. |
| `DSET-EVAL-PLAN-TOOL-005` | Operators run the utility workflow on every declared platform, including spaces, Unicode, failures, and interrupted writes. | Outcomes are equivalent and safe; any narrower applicability is visible before execution. |
| `DSET-EVAL-PLAN-TOOL-006` | Reviewers assess allowed, denied, unknown-registry, incompatible-license, provenance-drift, and expired-exception dependencies. | Every reviewer reaches the same accept/stop result from the authoritative rule and does not invent approval. |
| `DSET-EVAL-PLAN-OPS-008` | A cold operator investigates the implementing PR's live GitHub workflow/run/check and protected-target state. | Every operator binds evidence to the actual PR SHA and selects a safe merge, block, or retry action without bypassing protection. |
| `DSET-EVAL-PLAN-OPS-009` | Projects use shared integration branches and optional isolated worktrees across concurrent Changes and one protected PR. | Every reviewer identifies branch roles, actual workspace mode, and proof owner without requiring a worktree by default, merging Change identities, or creating permanent layer branches. |

Use at least two independent reviewers where interpretation matters. Correct the
earliest ambiguous owner and rerun the failed case; do not average a blocker
into a pass.
