---
artifact_type: implementation_decision
scope_path: []
priority: medium
artifact_id: "{{semantic_artifact_id}}"
llm_session_ids: []
---

# Adoption Implementation Decision — {{title}}

- **Implementation Decision ID:** `{{project_key}}-IMPL{{id_layer}}-001`
- **Status:** proposed
- **Decision date:** pending
- **Resolves Question:** pending
- **Replacement of:** none
- **Replaces claims:** none
- **Priority:** unknown
- **Selected candidate/version:** pending

## Rationale (recommended, optional)

Explain why this candidate is selected in this context. Omission alone does
not invalidate the Implementation Decision; do not add placeholder prose when the reason is
genuinely self-evident.

## Evidence and consequences

Record the consequential choice among valid alternatives, the decision basis,
trade-offs, consequences, linked requirements/proof,
license/provenance, rejected or currently incomparable alternatives, affected
structure, integration boundary, data ownership, implementation feasibility,
upgrade/rollback policy, lock-in, replacement seam, confirmation/violation
evidence, reopen condition, and exit test. Require a candidate comparison only
when a genuine consequential choice exists; do not manufacture alternatives for
an externally fixed Contract or ordinary implementation detail. Keep observable
edge cases in Requirements/Scenarios and internal detail in Design.

Reflect the Implementation Decision's normative consequences in maintained specs, Design, and
proof plans; link those views and the resolved Question here. The
accepted active Implementation Decision remains the atomic authority source and wins if a
view is stale.

The emitted Implementation Decision is immutable. Semantic change requires a successor. A
complete successor points backward with `replacement_of`; reverse
`replaced_by` links are derived, and the predecessor moves byte-for-byte to
`archive/`. Withdrawal archives the atom and routes future intent to a Version
Roadmap. Reopening is forbidden. This adoption specialization uses the same
atom-state rules as the neutral atomic template; it adds candidate version, license,
lock-in, replacement, and upgrade concerns.
