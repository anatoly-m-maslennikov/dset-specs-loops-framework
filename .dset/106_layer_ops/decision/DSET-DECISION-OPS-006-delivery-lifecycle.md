+++
artifact_id = "DSET-ATOMIC-RECORD-034"
semantic_id = "DSET-DECISION-OPS-006"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The release lifecycle uses six flat Delivery subtypes while preserving explicit reference and gate boundaries."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[promotion]
affected_children = ["meta", "gov", "tool", "skill", "ops"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"
+++

# Decision — Run releases through six flat Delivery roles

The release lifecycle uses six flat peer roles classified as direct subtypes of
the primary `delivery` artifact type:

- Roadmap orders the mutable route toward one next-minor Version Scope and owns
  milestone entries;
- Version Scope defines one version line's promises, exclusions, and exit
  criteria;
- Change groups accepted work and evidence for one bounded delivery;
- Release Plan selects one exact transition and its participating Changes;
- Readiness Record owns gate applicability, evidence, blockers, and the
  ready-or-blocked disposition for one exact candidate; and
- Release Record immutably owns the delivered summary, migration notes,
  protected merge SHA, tag, packages, and publisher identity.

No role contains or subclasses another. Applicable roles use explicit stable
references. Version Scope remains the scope anchor, not a root type. Roadmap
references one next-minor Version Scope; Release Plan references one Version
Scope and exact candidate; Readiness Record references its Release Plan,
Version Scope, and candidate commit; Release Record references the accepted
Readiness Record, Release Plan, Version Scope, and protected merge commit.

Version Scope is evergreen while its line is planned and its published snapshot
becomes immutable evidence. Roadmap remains mutable route planning. Release
Plan and Readiness Record may be refreshed during preparation under candidate
rules. Release Record is emitted only after publication and is immutable.
Verification supplies assurance but never substitutes for the Readiness
Record's disposition. Forge notes and changelogs are mirrors or Derived Views
of the Release Record.

Patch releases normally reuse their minor Version Scope. A changed public scope
or compatibility promise requires a new Decision and recompilation. DSET keeps
the declared `0.3` foundation, `0.4` self-hosted core, `0.5` adopter-ready, and
`1.0` fully working stable Version Scopes; future changes require a new
Decision.

This Decision absorbs `DSET-DECISION-OPS-005` in full and, transitively, its
absorbed OPS predecessors. It preserves all lifecycle, reference, milestone,
release-record, gate, and Version Scope consequences while removing the invalid
lineage edge that treated absorption as parentage. It remains aligned with the
active Delivery catalog Decision.

## Rationale

Change connects accepted work to a release candidate and therefore belongs in
the same carrier family as planning, gate, and publication records. Flat roles
preserve their separate authority; one Delivery family makes the complete
lifecycle readable.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
