---
artifact_type: implementation_decision
scope_path: []
priority: medium
artifact_id: "{{semantic_artifact_id}}"
llm_session_ids: []
---

# Decision — {{title}}

- **Decision ID:** `{{project_key}}-DECISION{{id_layer}}-001`
- **Status:** proposed
- **Decision date:** pending
- **Resolves Question:** pending
- **Replacement of:** none
- **Replaces claims:** none
- **Priority:** unknown
- **Selected option:** pending
- **LLM session IDs:** pending

## Context and scope

State the bounded consequential choice, affected Work Areas or repository scope,
fixed Contracts, assumptions, and the comparison frame used. A fixed external
Contract is not a candidate.

## Rationale (recommended, optional)

Link the Solution Landscape, eligible evidence, comparator/criteria, rejected,
tied, incomparable, inconclusive, or evidence-needed alternatives, and explain
why the selected option is justified for this context. Comparison results do not
select an option by themselves. Omission alone does not invalidate the Decision;
do not add placeholder prose when the reason is genuinely self-evident.

## Evidence basis

Link the evidence used for the selection and state its relevant limitations.

## Consequences and discharge

Record trade-offs, affected structure, integration and data-ownership
boundaries, implementation feasibility, upgrade/rollback policy, lock-in,
replacement seam, and the canonical Requirements, Contracts, Design, proof
plans, and operating rules updated by the Decision. Those owners carry
normative truth; this record retains rationale.

Name the evergreen projections compiled from this Decision. The accepted,
active Decision remains the atomic authority source; a projection that differs
from it is stale.

## Successor and archive policy

- **Expected confirmation evidence:** pending
- **Known counter-evidence:** none observed
- **Replacement trigger:** pending
- **Archive condition:** resolved, replaced, or withdrawn with no active
  structural dependant

This emitted Decision atom is immutable. Semantic change requires a successor.
A complete successor points backward with `replacement_of`; reverse
`replaced_by` links are derived, and the predecessor moves byte-for-byte to
`archive/`. Withdrawal archives the atom and routes future intent to a Version
Roadmap. Reopening is forbidden.
