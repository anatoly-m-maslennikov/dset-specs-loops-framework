# Solution landscape — Make DSET self-hosting and skills thin

## Capability gaps

| Capability | Requirement/test/eval IDs | Hard constraints |
|---|---|---|
| Repository rule authority | `DSET-REQUIREMENT-GOV-014`, `DSET-REQUIREMENT-GOV-017`; `DSET-TEST-GOV-014`, `DSET-TEST-GOV-017`; `DSET-EVAL-GOV-007` | Local paths, one editable owner per rule ID, no remote live authority |
| Thin adaptive wrappers | `DSET-REQUIREMENT-SKILL-002`, `DSET-REQUIREMENT-SKILL-003`; `DSET-TEST-SKILL-002`, `DSET-TEST-SKILL-003`; `DSET-EVAL-SKILL-002`, `DSET-EVAL-GOV-009` | Same wrapper hash, no embedded normative fallback |
| Bounded self-hosting | `DSET-REQUIREMENT-OPS-003`, `DSET-REQUIREMENT-TOOL-004`; `DSET-TEST-OPS-003`, `DSET-TEST-TOOL-005` | Terminates, profile-aware, framework before external pilot |
| Honest failure/customization | `DSET-REQUIREMENT-GOV-015..016`; `DSET-TEST-GOV-015..016`; `DSET-EVAL-GOV-008..009` | Stable diagnostics, justified non-applicability, explicit custom identity |
| Separate proof | `DSET-REQUIREMENT-META-007`; `DSET-TEST-META-007`; all evals | Tests and evals remain different artifacts and evidence streams |
| Discoverable skill surface | `DSET-REQUIREMENT-SKILL-004`, `DSET-REQUIREMENT-SKILL-005`; `DSET-TEST-SKILL-004`, `DSET-TEST-SKILL-005`; `DSET-EVAL-SKILL-003` | One catch-all entrypoint, explicit lifecycle shortcuts, no duplicated substantive rules |
| Investigable next-step routing | `DSET-REQUIREMENT-SKILL-006`; `DSET-TEST-SKILL-006`; `DSET-EVAL-SKILL-005` | Bounded local evidence, redaction, no competing authority |
| Predictable pre-1.0 releases | `DSET-REQUIREMENT-OPS-004`, `DSET-REQUIREMENT-OPS-007`; `DSET-TEST-OPS-004`, `DSET-TEST-OPS-007`; `DSET-EVAL-OPS-002` | Integer version tuple, one bump per main PR, coordinated product/package identity |
| Guarded RC/final publication | `DSET-REQUIREMENT-OPS-005..006`; `DSET-TEST-OPS-005..006`; `DSET-EVAL-OPS-003` | PR-only main updates, fully working RC, evidence-gated 1.0 |
| Proportional delegation budget | `DSET-REQUIREMENT-SKILL-007..008`; `DSET-TEST-SKILL-007..008`; `DSET-EVAL-SKILL-005..006` | Main model/effort inheritance, useful medium fan-out, outcome cost rather than nominal price |
| Session continuity | `DSET-REQUIREMENT-SKILL-009`; `DSET-TEST-SKILL-009`; `DSET-EVAL-SKILL-008` | One public entrypoint, linked internal runs, bounded checkpoint recovery after compaction, and authoritative-state refresh |
| Unambiguous semantic routing | `DSET-REQUIREMENT-GOV-018..019`; `DSET-TEST-GOV-018..019`; `DSET-EVAL-GOV-010..011` | Exactly four Types; one direct subtype at most; User Story is a Decision subtype; tasks and Changes remain non-Type structures; legacy IDs retain stable lookup |

## Candidates

Comparison frame: each row names its comparator and criteria. Fixed constraints
are repository-local authority, fail-closed resolution, bounded recursion,
separate tests/evals, protected delivery, and no automatic 1.0 promotion.
Evidence is `sufficient` only for the cited claim and recorded revision;
otherwise it is `degraded` or `insufficient`.

| Candidate/version | Source/license | Compared with / criteria | Evidence address/currentness | Evidence eligibility | Comparison result | Costs and observed failures |
|---|---|---|---|---|---|---|
| Normative rules embedded in each skill/current pattern | Repository/project license | Registry-owned rules / ownership and maintenance | [Wrapper inventory](evidence/archive/wrapper-rule-inventory-2026-07-14.md); current for recorded skill sources | sufficient | Unfavorable: duplicates authority and increases drift | Duplicate maintenance; observed wrapper/rule drift risk |
| Remote framework documents as live authority/current public repo | Public repository/project license | Repository-owned rules / offline and customized operation | [Architecture rule](../02_layer_gov/specification-architecture.md); current for the authority Contract | sufficient | Unfavorable: fails local ownership and offline use | Network/runtime dependency; local customization cannot own truth |
| Generated local copies with silent framework fallback/custom | Project license | Explicit local registry / precedence and reproducibility | [Lifecycle failure behavior](../04_layer_skill/procedure-lifecycle-orchestration.md); current for fail-closed resolution | sufficient | Not eligible under the fixed no-hidden-fallback constraint | Hidden precedence and non-reproducible choices |
| Registry-resolved local governing documents plus thin wrappers/current implementation | Repository/project license | Embedded/remote/fallback models / authority, offline use, customization | [Local gate](evidence/archive/local-gate-2026-07-15.md); current locally; hosted proof is stale | degraded | Favorable locally for §§0–§4; hosted comparison remains pending | Registry/materialization maintenance; distribution remains open |
| One public skill per lifecycle mode/current target | Repository/project license | Five-skill topology / direct discoverability and trigger overlap | [Skill-surface specification](specification-methodology.md); selected by `DSET-DECISION-SKILL-002`; expanded runtime proof pending | degraded | Selected for implementation; host-native usability remains to be evaluated | Larger discovery surface; exact registry and generated checks constrain drift |
| One universal skill with embedded lifecycle rules/custom | Repository/project license | Thin orchestrator / single-owner authority | [Architecture rule](../02_layer_gov/specification-architecture.md); current for rule ownership | sufficient | Not eligible under the fixed repository-owned-rule constraint | One oversized competing rule store |
| Primary orchestrator plus four specialists/absorbed target | Repository/project license | One-skill and per-mode alternatives / discovery, ownership, stop boundaries | [Historical Decision](../04_layer_skill/decision/DSET-DECISION-SKILL-001-select-the-dset-0-3-operating-shape.md); five wrappers implemented at the recorded commit | sufficient for historical source claim | Replaced for the public-topology claim by `DSET-DECISION-SKILL-002` | Smaller discovery surface but indirect access to most modes |
| Decimal version arithmetic (`+0.1`/`+0.01`) | Informal convention/no imported code | Integer SemVer tuple / transition correctness | [Release transition table](../05_layer_ops/procedure-release.md#classification-and-transitions); current for specified edges | sufficient | Unfavorable: arithmetic can claim 1.0 without readiness | Low implementation cost; invalid `0.9 + 0.1` promotion |
| SemVer-compatible tuple with DSET normal/small classes/SemVer 2.0.0 | [SemVer 2.0.0](https://semver.org/), CC BY 3.0 reference | Decimal arithmetic / ecosystem mapping and RC ordering | [Release transition table](../05_layer_ops/procedure-release.md#classification-and-transitions); transition engine tested; coordinated writes and publication pending | degraded | Favorable for deterministic transitions; end-to-end release proof pending | Transition and mirror-validation cost |
| Always lowest token-price model/generic heuristic | No governed source | Same-model inheritance / completed-task cost | [Delegation evidence rule](../04_layer_skill/procedure-delegation-budget.md#model-selection-evidence); no task-relevant DSET comparator | insufficient | Evidence-needed; nominal price alone is not comparable completed-task cost | Retry/token expansion can cost more and fail more often |
| Same model/effort by default; vary useful fan-out and evidence/current policy | DSET policy; [DeepSWE v1.1](https://deepswe.datacurve.ai/), observed 2026-07-15 | Price-only downgrade / outcome quality and completed-task cost | [Delegation evidence rule](../04_layer_skill/procedure-delegation-budget.md#model-selection-evidence); benchmark supports only the token-price limitation | degraded | Provisionally favorable; DSET fan-out comparison remains pending | Inheritance may use expensive models; avoids unsupported downgrade risk |

## Decision

The original operating shape is recorded in
[`DSET-DECISION-SKILL-001`](../04_layer_skill/decision/DSET-DECISION-SKILL-001-select-the-dset-0-3-operating-shape.md). Its exact-five
topology claim is partially replaced by
[`DSET-DECISION-SKILL-002`](../04_layer_skill/decision/DSET-DECISION-SKILL-002-expose-every-dset-lifecycle-mode-as-a-public-skill.md); its other
claims remain active. Candidate rows above contain comparison results only;
they do not authorize adoption, implementation, release, or rejection.
