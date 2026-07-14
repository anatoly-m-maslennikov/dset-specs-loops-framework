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
| Registry-resolved local governing documents plus thin wrappers | Custom, based on existing DSET schemas/CLI | Planned tests and evals in this change | Build in later batches |

## Decision

Build the deterministic local registry/resolver and adapt current skills into thin wrappers in later batches. This batch selects only invariant boundaries already directed by the roadmap; implementation choices such as registry schema fields, hashing, materialization format, and runtime adapters remain open and must pass their own solution/reuse gate.
