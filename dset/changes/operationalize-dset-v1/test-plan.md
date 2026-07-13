# Test plan — DSET v1

Deterministic tests prove exact CLI behavior and artifact structure. Human usability and workflow selection remain in [eval-plan.md](eval-plan.md).

| Test ID | Requirement | Deterministic proof |
|---|---|---|
| **DSET-V1-TEST-001** | DSET-V1-REQ-001 | CLI help exposes the five commands; repository `check` and `verify` exit zero |
| **DSET-V1-TEST-002** | DSET-V1-REQ-002 | All valid fixtures pass and each invalid fixture fails with its expected diagnostic code |
| **DSET-V1-TEST-003** | DSET-V1-REQ-001/002 | `new` creates the selected profile without overwrite and the result passes structural validation |
| **DSET-V1-TEST-004** | DSET-V1-REQ-003 | Trace generation is stable; `trace --check` detects stale or missing output |
| **DSET-V1-TEST-005** | DSET-V1-REQ-004 | Archive dry-run reports the move; unsafe status, missing PR, incomplete proof, and destination collision fail without writes |
| **DSET-V1-TEST-006** | DSET-V1-REQ-005 | Skill folders pass the Codex skill validator and static portability audit |
| **DSET-V1-TEST-007** | DSET-V1-REQ-006 | CI workflow parses, invokes canonical verification, and exposes a stable required-check name |
| **DSET-V1-TEST-008** | All | Public Markdown links resolve, prohibited Obsidian constructs are absent, and `git diff --check` passes |

## Regression rule

Every validator defect adds a failing fixture or unit test before correction. Stable diagnostic codes are part of the CLI contract; explanatory text may improve without breaking automation.
