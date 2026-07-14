# Solution landscape — Make DSET self-hosting and skills thin

## Capability gaps

| Capability | Requirement/test/eval IDs | Hard constraints |
|---|---|---|
| Repository rule authority | `DSET-REQUIREMENT-GOV-007`, `DSET-REQUIREMENT-GOV-010`; `DSET-TEST-GOV-009`, `DSET-TEST-GOV-011`; `DSET-EVAL-TOOL-002` | Local paths, one editable owner per rule ID, no remote live authority |
| Thin adaptive wrappers | `DSET-REQUIREMENT-SKILL-002`, `DSET-REQUIREMENT-SKILL-003`; `DSET-TEST-SKILL-002`, `DSET-TEST-SKILL-003`; `DSET-EVAL-SKILL-002`, `DSET-EVAL-GOV-009` | Same wrapper hash, no embedded normative fallback |
| Bounded self-hosting | `DSET-REQUIREMENT-TOOL-006`, `DSET-REQUIREMENT-TOOL-007`; `DSET-TEST-TOOL-009`, `DSET-TEST-TOOL-010` | Terminates, profile-aware, framework before external pilot |
| Honest failure/customization | `DSET-REQUIREMENT-GOV-008`, `DSET-REQUIREMENT-GOV-009`; `DSET-TEST-TOOL-011`, `DSET-TEST-GOV-010`; `DSET-EVAL-SKILL-003` | Stable diagnostics, justified non-applicability, explicit custom identity |
| Separate proof | `DSET-REQUIREMENT-META-005`; `DSET-TEST-META-004`; all evals | Tests and evals remain different artifacts and evidence streams |
| Small skill surface | `DSET-REQUIREMENT-SKILL-004`, `DSET-REQUIREMENT-SKILL-005`; `DSET-TEST-SKILL-004`, `DSET-TEST-SKILL-005`; `DSET-EVAL-SKILL-004` | One obvious entrypoint, narrow specialists, no helper-skill explosion |
| Investigable next-step routing | `DSET-REQUIREMENT-SKILL-006`; `DSET-TEST-SKILL-006`; `DSET-EVAL-SKILL-005` | Bounded local evidence, redaction, no competing authority |
| Predictable pre-1.0 releases | `DSET-REQUIREMENT-OPS-008`, `DSET-REQUIREMENT-OPS-011`; `DSET-TEST-OPS-008`, `DSET-TEST-OPS-011`; `DSET-EVAL-SKILL-006` | Integer version tuple, one bump per main PR, coordinated product/package identity |
| Guarded RC/final publication | `DSET-REQUIREMENT-OPS-009`, `DSET-REQUIREMENT-OPS-010`; `DSET-TEST-OPS-009`, `DSET-TEST-OPS-010`; `DSET-EVAL-OPS-006` | PR-only main updates, fully working RC, evidence-gated 1.0 |
| Proportional delegation budget | `DSET-REQUIREMENT-SKILL-007`, `DSET-REQUIREMENT-SKILL-008`; `DSET-TEST-SKILL-007`, `DSET-TEST-SKILL-008`; `DSET-EVAL-SKILL-006`, `DSET-EVAL-SKILL-007` | Main model/effort inheritance, useful medium fan-out, outcome cost rather than nominal price |
| Unambiguous project intake | `DSET-REQUIREMENT-GOV-011`; `DSET-TEST-GOV-012`; `DSET-EVAL-GOV-010` | One registry; Problems include risks; Opportunities require no defect; Questions lead to Decisions; tasks stay in Changes; stable architectural layers own IDs |

## Candidates

| Candidate/version | Source and license | Evidence | Decision |
|---|---|---|---|
| Normative rules embedded in each skill | Existing skill pattern; repository-owned | Current skills require inventory | Reject: creates parallel owners and wrapper drift |
| Remote framework documents as live authority | Public repository; project license | Architectural comparison | Reject: breaks offline/local customization and project ownership |
| Generated local copies with silent framework fallback | Custom | Failure-mode analysis | Reject: makes authority depend on hidden precedence |
| Registry-resolved local governing documents plus thin wrappers | Custom, based on existing DSET schemas/CLI | Implemented governance, wrapper, materialization, and self-host tests | **Selected and implemented for §§0–§4** |
| One public skill per lifecycle step | Earlier DSET skill inventory; repository-owned | Trigger-overlap and operator-load review | Reject: too many commands and parallel workflow owners |
| One universal skill with embedded lifecycle rules | Custom | Thin-wrapper authority analysis | Reject: creates one oversized competing rule store |
| Primary orchestrator plus narrow clarify/diagnose/prototype/release specialists | Custom | Current thin-wrapper model plus requested operator workflow | **Selected for specification** |
| Decimal version arithmetic (`+0.1` / `+0.01`) | Informal convention | Transition edge-case analysis | Reject literal arithmetic: `0.9 + 0.1` would accidentally claim 1.0 |
| SemVer-compatible integer tuple with DSET normal/small classes | [Semantic Versioning 2.0.0](https://semver.org/) (CC BY 3.0; referenced, not copied) | `0.9.0` to `0.10.0`, prerelease precedence, package ecosystem compatibility | **Selected for specification** |
| Always delegate to the lowest token-price model | Generic cost heuristic | Contradicted by variable token use, retries, steps, and pass rates | Reject: input/output unit price is not completed-task cost |
| Same model/effort by default; vary useful fan-out and evidence first | Custom DSET policy; [DeepSWE v1.1](https://deepswe.datacurve.ai/) observed 2026-07-15 supports only the narrower cost claim | Its 113 single-agent tasks under a fixed mini-swe-agent harness show that token price alone does not determine trial cost or success; it does not evaluate native harnesses, inheritance, or multi-agent fan-out | **Selected for specification; fan-out requires DSET-specific eval evidence** |

## Decision

Use a YAML registry validated by published schemas, repository-relative owner paths, SHA-256 provenance/customization identity, explicit materialize/refresh/diff commands, and canonical wrapper digests. Use the pinned released validator plus the candidate CLI for the fixed-depth self-host sequence. Specify one primary `dset` orchestrator, three existing narrow specialists, and one explicit `dset-release` boundary. Use the complete SemVer transition table, initialize coordinated product/package `0.2.0`, and reserve RC/final publication for fully working gates. Request the main model/effort for subagents, use the tree-wide medium budget by default, and require task-relevant evidence for any model override. Route intake through problems, opportunities, and questions; put tasks inside changes. Governance and self-hosting are implemented for §§0–§4; the two new skills, run writer, budget/release automation, TypeScript adapters, pilots, and distribution remain later implementation work.
