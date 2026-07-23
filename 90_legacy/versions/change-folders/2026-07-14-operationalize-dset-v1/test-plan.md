# Test plan — DSET v1

Deterministic tests prove exact CLI behavior and artifact structure. Human usability and workflow selection remain in [eval-plan.md](eval-plan.md).

| Test ID | Requirement | Deterministic proof |
|---|---|---|
| **DSET-TEST-PLAN-TOOL-001** | DSET-REQUIREMENT-TOOL-001 | CLI help exposes the five commands; repository `check` and `verify` exit zero |
| **DSET-TEST-PLAN-TOOL-002** | DSET-REQUIREMENT-TOOL-002 | All valid fixtures pass and each invalid fixture fails with its expected diagnostic code |
| **DSET-TEST-PLAN-TOOL-003** | `DSET-REQUIREMENT-TOOL-001`, `DSET-REQUIREMENT-TOOL-002` | `new` creates the selected profile without overwrite and the result passes structural validation |
| **DSET-TEST-PLAN-TOOL-004** | DSET-REQUIREMENT-TOOL-003 | Trace generation is stable; `trace --check` detects stale or missing output |
| **DSET-TEST-PLAN-TOOL-005** | DSET-REQUIREMENT-TOOL-004 | Archive dry-run reports the move; unsafe status, missing PR, incomplete proof, and destination collision fail without writes |
| **DSET-TEST-PLAN-SKILL-001** | DSET-REQUIREMENT-SKILL-001 | Skill folders pass the Codex skill validator and static portability audit |
| **DSET-TEST-PLAN-OPS-007** | DSET-REQUIREMENT-OPS-007 | CI workflow parses, invokes canonical verification, and exposes a stable required-check name |
| **DSET-TEST-PLAN-GOV-006** | All | Public Markdown links resolve, prohibited Obsidian constructs are absent, and `git diff --check` passes |

## Regression rule

Every validator defect adds a failing fixture or unit test before correction. Stable diagnostic codes are part of the CLI contract; explanatory text may improve without breaking automation.
