# Adoption Decision — {{title}}

- **Decision ID:** `{{project_key}}-DECISION{{id_layer}}-001`
- **Status:** proposed
- **Decision date:** pending
- **Resolves Question:** pending
- **Supersedes:** none
- **Superseded by:** none
- **Selected candidate/version:** pending

Record the consequential choice among valid alternatives, the decision basis,
rationale, trade-offs, consequences, linked requirements/proof,
license/provenance, rejected or currently incomparable alternatives, affected
structure, integration boundary, data ownership, implementation feasibility,
upgrade/rollback policy, lock-in, replacement seam, confirmation/violation
evidence, reopen condition, and exit test. Require a candidate comparison only
when a genuine consequential choice exists; do not manufacture alternatives for
an externally fixed Contract or ordinary implementation detail. Keep observable
edge cases in Requirements/Scenarios and internal detail in Design.

Before marking the Decision accepted, discharge its normative consequences into
the owning canonical specs, Contracts, Design, and proof plans; link those edits
and the resolved Question here. This artifact retains rationale rather than
becoming a parallel specification.

When counter-evidence invalidates the basis, mark the Decision reopened or
superseded, retain its earlier evidence and rationale, state the invalid
assumptions and withdrawn authority, update affected downstream owners, and link
the successor or explicit retirement with `no successor`. Never silently edit
history to make the old Decision appear current. This adoption specialization
uses the same lifecycle as the neutral [`decision.md`](decision.md) template; it
adds candidate version, license, lock-in, replacement, and upgrade concerns.
