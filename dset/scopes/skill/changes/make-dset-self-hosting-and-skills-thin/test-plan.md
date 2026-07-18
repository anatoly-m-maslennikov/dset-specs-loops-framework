# Test plan — Make DSET self-hosting and skills thin

Accepted deterministic claims remain owned by the layer plans below. This
Change executes and records their applicable proof; it does not redefine them.

| Owning plan | Applicable Test IDs |
|---|---|
| [META](../../../meta/specs/packages/methodology/test-plan.md) | `DSET-TEST-META-007`, `DSET-TEST-META-010..011` |
| [GOV](../../../gov/specs/packages/methodology/test-plan.md) | `DSET-TEST-GOV-014..028` |
| [TOOL](../../../tool/specs/packages/methodology/test-plan.md) | `DSET-TEST-TOOL-005`, `DSET-TEST-TOOL-018..019` |
| [SKILL](../../specs/packages/methodology/test-plan.md) | `DSET-TEST-SKILL-001..010` |
| [OPS](../../../ops/specs/packages/methodology/test-plan.md) | `DSET-TEST-OPS-003..007` |

Connected accepted IDs are `DSET-TEST-META-007`, `DSET-TEST-META-010`,
`DSET-TEST-META-011`, `DSET-TEST-GOV-014`, `DSET-TEST-GOV-015`,
`DSET-TEST-GOV-016`, `DSET-TEST-GOV-017`, `DSET-TEST-GOV-018`,
`DSET-TEST-GOV-019`, `DSET-TEST-GOV-020`, `DSET-TEST-GOV-021`,
`DSET-TEST-GOV-022`, `DSET-TEST-GOV-023`, `DSET-TEST-TOOL-005`,
`DSET-TEST-GOV-024`, `DSET-TEST-GOV-025`, `DSET-TEST-GOV-026`,
`DSET-TEST-GOV-027`,
`DSET-TEST-GOV-028`,
`DSET-TEST-TOOL-018`, `DSET-TEST-TOOL-019`,
`DSET-TEST-SKILL-001`, `DSET-TEST-SKILL-002`, `DSET-TEST-SKILL-003`,
`DSET-TEST-SKILL-004`, `DSET-TEST-SKILL-005`,
`DSET-TEST-SKILL-006`, `DSET-TEST-SKILL-007`, `DSET-TEST-SKILL-008`,
`DSET-TEST-SKILL-009`, `DSET-TEST-SKILL-010`,
`DSET-TEST-OPS-003`, `DSET-TEST-OPS-004`,
`DSET-TEST-OPS-005`, `DSET-TEST-OPS-006`, and `DSET-TEST-OPS-007`.

## Change-only deterministic proof

| Test ID | Contract/Requirement | Assertion |
|---|---|---|
| `DSET-TEST-SKILL-011` | `DSET-CONTRACT-SKILL-001` | Install/link every declared host-native skill in a clean host fixture and prove discovery, load, invocation, local resolution, handoff, and stop behavior. |
| `DSET-TEST-TOOL-016` | `DSET-CONTRACT-TOOL-001` | Exercise path, process, shell, encoding, temporary-file, write-safety, and exit behavior on every declared platform or prove honest narrower applicability before execution. |
| `DSET-TEST-TOOL-017` | `DSET-CONTRACT-TOOL-002` | Enforce dependency registry/version/license/provenance, lockfile authority, allow/deny policy, and bounded unexpired exceptions. |
| `DSET-TEST-OPS-014` | `DSET-CONTRACT-OPS-001` | Bind real GitHub workflow/run/check evidence to the actual implementing PR head and protected-target disposition. |
| `DSET-TEST-OPS-015` | `DSET-REQUIREMENT-OPS-012`, `DSET-CONTRACT-OPS-002` | Require integration-branch default scaffolding, accept explicit worktree isolation, allow shared integration branches/PRs, preserve isolated-branch uniqueness, and require head/candidate equality only at verified or archive-ready states. |

Add a failing deterministic proof before repairing every reproducible defect.
