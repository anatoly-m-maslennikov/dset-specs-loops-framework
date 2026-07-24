# Solution landscape — DSET v1 tooling

## Capability gaps

| Capability | Requirement/test IDs | Needed behavior |
|---|---|---|
| Project/change validation | `DSET-REQUIREMENT-TOOL-001`, `DSET-REQUIREMENT-TOOL-002`; `DSET-TEST-PLAN-TOOL-001`, `DSET-TEST-PLAN-TOOL-002` | Cross-platform, deterministic, actionable diagnostics |
| Scaffolding and archive safety | `DSET-REQUIREMENT-TOOL-001`, `DSET-REQUIREMENT-TOOL-004`; `DSET-TEST-PLAN-TOOL-003`, `DSET-TEST-PLAN-TOOL-005` | Explicit writes, no overwrite, lifecycle gates |
| Traceability generation | `DSET-REQUIREMENT-TOOL-003`; `DSET-TEST-PLAN-TOOL-004` | Stable output from committed metadata and PR identity |
| Agent workflows | `DSET-REQUIREMENT-SKILL-001`; `DSET-TEST-PLAN-SKILL-001`; `DSET-EVAL-PLAN-SKILL-001` | Three distinct, portable, concise skills |
| Delivery diagnostics | `DSET-REQUIREMENT-OPS-007`; `DSET-TEST-PLAN-OPS-007`; `DSET-EVAL-PLAN-OPS-005` | GitHub-hosted evidence and recovery routing |

## Candidates

| Candidate | Provenance | License | Fit | Decision |
|---|---|---|---|---|
| Repository-owned Python standard-library CLI | New DSET implementation | Apache-2.0 | Preserves `dset/`, runs without dependency installation, fully testable | **Build v1** |
| OpenSpec CLI | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) at `0a99f410457271aa773d8b106f03f637f7c6b3c0` | MIT | Useful conceptual precedent, but compatibility with the complete DSET artifact and proof contract is not yet demonstrated | **Defer code adoption** |
| JSON Schema plus third-party validator | JSON Schema ecosystem | Implementation-dependent | Strong external interoperability but adds runtime installation and does not validate Markdown semantics alone | **Publish schemas; do not require runtime dependency** |
| Ad hoc shell checks | Prior bootstrap proof commands | Repository-local | Proven for narrow checks, but not portable or composable enough for the public canonical command | **Replace** |

## Reuse decision

Build the minimum CLI independently in DSET terminology using only Python's standard library. Publish JSON Schemas for interoperability, but keep the canonical validator self-contained. Record OpenSpec and workflow-skill projects as conceptual influences in [third-party notices](../../../../../../THIRD_PARTY_NOTICES.md); do not copy code or prose. Re-evaluate external implementations only through a future proof-of-fit change with an exact version and license record.
