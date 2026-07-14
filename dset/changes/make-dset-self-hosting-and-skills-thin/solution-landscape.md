# Solution landscape — Make DSET self-hosting and skills thin

## Capability gaps

| Capability | Requirement/test/eval IDs | Hard constraints |
|---|---|---|
| Repository rule authority | MDSHAST-REQ/TEST-003, 009; EVAL-002 | Local paths, one editable owner per rule ID, no remote live authority |
| Thin adaptive wrappers | MDSHAST-REQ/TEST-004, 005; EVAL-001, 004 | Same wrapper hash, no embedded normative fallback |
| Bounded self-hosting | MDSHAST-REQ/TEST-001, 002 | Terminates, profile-aware, framework before external pilot |
| Honest failure/customization | MDSHAST-REQ/TEST-006, 007; EVAL-003 | Stable diagnostics, justified non-applicability, explicit custom identity |
| Separate proof | MDSHAST-REQ/TEST-008; all evals | Tests and evals remain different artifacts and evidence streams |

## Candidates

| Candidate/version | Source and license | Evidence | Decision |
|---|---|---|---|
| Normative rules embedded in each skill | Existing skill pattern; repository-owned | Current skills require inventory | Reject: creates parallel owners and wrapper drift |
| Remote framework documents as live authority | Public repository; project license | Architectural comparison | Reject: breaks offline/local customization and project ownership |
| Generated local copies with silent framework fallback | Custom | Failure-mode analysis | Reject: makes authority depend on hidden precedence |
| Registry-resolved local governing documents plus thin wrappers | Custom, based on existing DSET schemas/CLI | Implemented governance, wrapper, materialization, and self-host tests | **Selected and implemented for §§0–§4** |

## Decision

Use a YAML registry validated by a published JSON Schema, repository-relative owner paths, SHA-256 provenance/customization identity, explicit materialize/refresh/diff commands, and canonical wrapper digests. Use the pinned released validator plus the candidate CLI for the fixed-depth self-host sequence. These choices are implemented for §§0–§4; TypeScript adapters, external pilot integration, and distribution remain separate later decisions.
