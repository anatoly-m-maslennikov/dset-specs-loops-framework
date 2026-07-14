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

## Decision

Use a YAML registry validated by a published JSON Schema, repository-relative owner paths, SHA-256 provenance/customization identity, explicit materialize/refresh/diff commands, and canonical wrapper digests. Use the pinned released validator plus the candidate CLI for the fixed-depth self-host sequence. Specify one primary `dset` orchestrator, three existing narrow specialists, and one explicit `dset-release` boundary. Use SemVer-compatible integer components, initialize the coordinated product/package release at `0.2.0`, and reserve RC/final publication for fully working evidence gates. The governance and self-host choices are implemented for §§0–§4; orchestration, run records, release automation, TypeScript adapters, external pilot integration, and distribution remain later implementation decisions.
