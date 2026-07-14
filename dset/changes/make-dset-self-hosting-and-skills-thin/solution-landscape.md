# Solution landscape — Make DSET self-hosting and skills thin

## Capability gaps

| Capability | Requirement/test/eval IDs | Hard constraints |
|---|---|---|
| Repository rule authority | MDSHAST-REQ/TEST-003, 009; EVAL-002 | Local paths, one editable owner per rule ID, no remote live authority |
| Thin adaptive wrappers | MDSHAST-REQ/TEST-004, 005; EVAL-001, 004 | Same wrapper hash, no embedded normative fallback |
| Bounded self-hosting | MDSHAST-REQ/TEST-001, 002 | Terminates, profile-aware, framework before external pilot |
| Honest failure/customization | MDSHAST-REQ/TEST-006, 007; EVAL-003 | Stable diagnostics, justified non-applicability, explicit custom identity |
| Separate proof | MDSHAST-REQ/TEST-008; all evals | Tests and evals remain different artifacts and evidence streams |
| Small skill surface | MDSHAST-REQ/TEST-010, 011; EVAL-005 | One obvious entrypoint, narrow specialists, no helper-skill explosion |
| Investigable next-step routing | MDSHAST-REQ/TEST-012; EVAL-006 | Bounded local evidence, redaction, no competing authority |
| Predictable pre-1.0 releases | MDSHAST-REQ/TEST-013, 016; EVAL-007 | Integer version tuple, one bump per main PR, coordinated product/package identity |
| Guarded RC/final publication | MDSHAST-REQ/TEST-014, 015; EVAL-008 | PR-only main updates, fully working RC, evidence-gated 1.0 |
| Proportional delegation budget | MDSHAST-REQ/TEST-017, 018; EVAL-009, 010 | Main model/effort inheritance, useful medium fan-out, outcome cost rather than nominal price |
| Unambiguous project intake | MDSHAST-REQ/TEST-019; EVAL-011 | Problems include risks; opportunities require no defect; questions lead to ADRs; tasks stay in changes |

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
