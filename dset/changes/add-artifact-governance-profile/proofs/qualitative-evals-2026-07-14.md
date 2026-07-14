# Qualitative evaluations — 2026-07-14

## Method

Three independent agent reviewers received bounded, read-only cases and used only committed public repository files. They did not edit files or contact GitHub. One reviewer evaluated cold navigation and profile independence, one evaluated artifact classification and authority, and one evaluated specification dependency ordering. Reviewer observations were corrected in commit `174c10b` and the affected cases were assigned back to the same reviewers.

| Eval ID | Initial result | Corrective loop | Final result |
|---|---|---|---|
| ART-EVAL-001 | Pass at `5e5b24f` in approximately 2 minutes 20 seconds; the project-control hub required minor filesystem navigation | `174c10b` made accepted truth, changes, contracts, traceability, migration, and supportability routes clickable | Pass at `174c10b` in under two minutes |
| ART-EVAL-002 | Pass at `9fa34ab`; rationale and maintenance were unambiguous but lacked direct authority links | `174c10b` linked rationale and procedure to the artifact-type catalog, hub rules, and specification authoring rules | Pass at `174c10b` with one normative owner per rule |
| ART-EVAL-003 | Pass at `5e5b24f`; reviewer requested clearer handling of value objects/external actors and a connection heuristic | `174c10b` scoped lifecycles to owned entities and added the remove-forward-sentence review test | Pass at `174c10b` without weakening definition-before-use |
| ART-EVAL-004 | Pass at `5e5b24f` | No blocking correction; profile surfaces were unchanged by `174c10b` | Pass remains valid at `174c10b` |

## ART-EVAL-001 — Cold-start helicopter navigation

The final route was root README → documentation and methodology hubs → framework purpose, methodology stages, artifact-type owner, authoring rules, rationale, and maintenance playbook. The reviewer completed it in under two minutes without repository search. The DSET project hub separately exposed clickable routes for accepted truth, changes, contracts, traceability, migration, and supportability.

Non-blocking observation: `changes/README.md` describes the lifecycle but does not manually list each active change. This is consistent with the rule that hubs route stable owners rather than duplicate volatile leaf inventories.

## ART-EVAL-002 — Artifact classification

Six representative requests produced one primary type each:

| Request | Primary type | Authority boundary |
|---|---|---|
| Stable security-area front door with purpose, boundaries, and start routes | Hub | Implements navigation; does not own the hub rule |
| Reusable rule for creating a hub only for stable, repeatedly visited areas | Normative reference | Single reusable rule owner |
| Explanation of why exhaustive indexes become stale | Rationale | Explains the rule without owning it |
| Repository decision to adopt `documentation-v1`, including alternatives and consequences | ADR | Records one contextual decision |
| Ordered split/move procedure with checks and stop conditions | Playbook/runbook | Applies governing rules procedurally |
| Validation/reviewer results for one revision | Evidence | Records an observation; cannot become current policy |

The re-evaluation confirmed direct authority links and no duplicate normative owner.

## ART-EVAL-003 — Specification dependency order

The reviewer used a synthetic Customer → Order → Shipment/Return → Refund domain. A defective version defined Refund, Shipment, Order, and Return before entities required by their definitions. The rules identified each undefined downstream dependency and rejected the forward section links as substitutes for meaning.

The corrected order was Customer, Order, Shipment, Return, Refund, then relationships. Each owned entity declared a lifecycle; value/reference/external concepts were classified separately. Forward sentences remained only where removing one would leave the current entity's identity and invariants comprehensible. A later relationships section expressed bidirectional connections after all definitions existed.

## ART-EVAL-004 — Orthogonal profiles

| Scenario | Selection |
|---|---|
| Python code | `python-v1`; add `documentation-v1` independently for governed artifacts |
| Future TypeScript code | Evidence-backed future `typescript-v1`; do not inherit Python defaults; combine `documentation-v1` independently |
| Documentation-only repository | No implementation-language profile; select `documentation-v1` |
| Mixed code and governed documentation | Select applicable code profile plus `documentation-v1` |

The reviewer confirmed that documentation is not described as a programming language and no Python threshold applies to documents. Polyglot code-profile multiplicity remains a future design question, not a claim of this profile.

## Disposition

All four thresholds pass at the corrected pushed head. Structural link, hierarchy, schema, and diagnostic behavior remain deterministic tests; these evals cover navigation usefulness, semantic classification, definition order, and profile-selection judgment only.

## Data handling

The evidence retains public revision identities, bounded synthetic cases, routes, timings, results, and corrections. It contains no secrets, private source paths, raw reviewer logs, or external-system state.
