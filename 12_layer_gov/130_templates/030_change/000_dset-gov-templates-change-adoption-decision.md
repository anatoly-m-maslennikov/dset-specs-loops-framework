# Adoption Decision — {{title}}

- **Decision ID:** `{{project_key}}-DECISION{{id_layer}}-001`
- **Status:** proposed
- **Decision date:** pending
- **Resolves Question:** pending
- **Absorbs:** none
- **Replaces claims:** none
- **Priority:** unknown
- **Selected candidate/version:** pending

## Rationale (recommended, optional)

Explain why this candidate is selected in this context. Omission alone does
not invalidate the Decision; do not add placeholder prose when the reason is
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

Compile the Decision's normative consequences into evergreen specs, Design,
and proof plans; link those projections and the resolved Question here. The
accepted active Decision remains the atomic authority source and wins if a
projection is stale.

The emitted Decision is immutable. Counter-evidence, acceptance, reopening,
withdrawal, and retirement are append-only lifecycle events. A successor points
backward with `Absorbs`; reverse links and current state are derived. A fully
retired Decision may move byte-for-byte to `archive/` with stable ID, digest,
and lookup. This adoption specialization uses the same lifecycle as the neutral
`decision.md` template; it adds candidate version, license,
lock-in, replacement, and upgrade concerns.
