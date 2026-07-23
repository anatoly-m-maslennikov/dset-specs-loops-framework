# Test plan — Make DSET self-hosting and skills thin

Accepted deterministic claims remain owned by the layer plans below. This
Change executes and records their applicable proof; it does not redefine them.

| Owning plan | Applicable Test IDs |
|---|---|
| `plan-tests.md` | `DSET-TEST-PLAN-META-007`, `DSET-TEST-PLAN-META-010..011` |
| `plan-tests.md` | `DSET-TEST-PLAN-GOV-014..032`, `DSET-TEST-PLAN-GOV-035..036`, `DSET-TEST-PLAN-GOV-039`, `DSET-TEST-PLAN-GOV-042..044`, `DSET-TEST-PLAN-GOV-048..050` |
| `plan-tests.md` | `DSET-TEST-PLAN-TOOL-005`, `DSET-TEST-PLAN-TOOL-018..019`, `DSET-TEST-PLAN-TOOL-021..022` |
| `plan-tests.md` | `DSET-TEST-PLAN-SKILL-001..010`, `DSET-TEST-PLAN-SKILL-012..013` |
| `plan-tests.md` | `DSET-TEST-PLAN-OPS-003..007`, `DSET-TEST-PLAN-OPS-016` |

Connected accepted IDs are `DSET-TEST-PLAN-META-007`, `DSET-TEST-PLAN-META-010`,
`DSET-TEST-PLAN-META-011`, `DSET-TEST-PLAN-GOV-014`, `DSET-TEST-PLAN-GOV-015`,
`DSET-TEST-PLAN-GOV-016`, `DSET-TEST-PLAN-GOV-017`, `DSET-TEST-PLAN-GOV-018`,
`DSET-TEST-PLAN-GOV-019`, `DSET-TEST-PLAN-GOV-020`, `DSET-TEST-PLAN-GOV-021`,
`DSET-TEST-PLAN-GOV-022`, `DSET-TEST-PLAN-GOV-023`, `DSET-TEST-PLAN-TOOL-005`,
`DSET-TEST-PLAN-GOV-024`, `DSET-TEST-PLAN-GOV-025`, `DSET-TEST-PLAN-GOV-026`,
`DSET-TEST-PLAN-GOV-027`,
`DSET-TEST-PLAN-GOV-028`,
`DSET-TEST-PLAN-GOV-029`,
`DSET-TEST-PLAN-GOV-030`, `DSET-TEST-PLAN-GOV-031`, `DSET-TEST-PLAN-GOV-032`,
`DSET-TEST-PLAN-GOV-035`, `DSET-TEST-PLAN-GOV-036`,
`DSET-TEST-PLAN-GOV-039`, `DSET-TEST-PLAN-GOV-042`, `DSET-TEST-PLAN-GOV-043`,
`DSET-TEST-PLAN-TOOL-018`, `DSET-TEST-PLAN-TOOL-019`,
`DSET-TEST-PLAN-TOOL-021`,
`DSET-TEST-PLAN-TOOL-022`,
`DSET-TEST-PLAN-SKILL-001`, `DSET-TEST-PLAN-SKILL-002`, `DSET-TEST-PLAN-SKILL-003`,
`DSET-TEST-PLAN-SKILL-004`, `DSET-TEST-PLAN-SKILL-005`,
`DSET-TEST-PLAN-SKILL-006`, `DSET-TEST-PLAN-SKILL-007`, `DSET-TEST-PLAN-SKILL-008`,
`DSET-TEST-PLAN-SKILL-009`, `DSET-TEST-PLAN-SKILL-010`,
	`DSET-TEST-PLAN-SKILL-012`, `DSET-TEST-PLAN-SKILL-013`,
`DSET-TEST-PLAN-OPS-003`, `DSET-TEST-PLAN-OPS-004`,
`DSET-TEST-PLAN-OPS-005`, `DSET-TEST-PLAN-OPS-006`, `DSET-TEST-PLAN-OPS-007`, and
`DSET-TEST-PLAN-OPS-016`.

## Change-only deterministic proof

| Test ID | Contract/Requirement | Assertion |
|---|---|---|
| `DSET-TEST-PLAN-SKILL-011` | `DSET-CONTRACT-SKILL-001` | Install/link every declared host-native skill in a clean host fixture and prove discovery, load, invocation, local resolution, handoff, and stop behavior. |
| `DSET-TEST-PLAN-TOOL-016` | `DSET-CONTRACT-TOOL-001` | Exercise path, process, shell, encoding, temporary-file, write-safety, and exit behavior on every declared platform or prove honest narrower applicability before execution. |
| `DSET-TEST-PLAN-TOOL-017` | `DSET-CONTRACT-TOOL-002` | Enforce dependency registry/version/license/provenance, lockfile authority, allow/deny policy, and bounded unexpired exceptions. |
| `DSET-TEST-PLAN-OPS-014` | `DSET-CONTRACT-OPS-001` | Bind real GitHub workflow/run/check evidence to the actual implementing PR head and protected-target disposition. |
| `DSET-TEST-PLAN-OPS-015` | `DSET-REQUIREMENT-OPS-012`, `DSET-CONTRACT-OPS-002` | Require integration-branch default scaffolding, accept explicit worktree isolation, allow shared integration branches/PRs, preserve isolated-branch uniqueness, and require head/candidate equality only at verified or archive-ready states. |

Add a failing deterministic proof before repairing every reproducible defect.
