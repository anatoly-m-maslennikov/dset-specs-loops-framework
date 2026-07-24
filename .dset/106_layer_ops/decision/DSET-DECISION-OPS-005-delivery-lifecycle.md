+++
artifact_id = "DSET-ATOMIC-RECORD-032"
semantic_id = "DSET-DECISION-OPS-005"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The release lifecycle uses six flat Delivery subtypes while preserving explicit reference and gate boundaries."
child_of = ["DSET-DECISION-OPS-004", "DSET-DECISION-GOV-011"]
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

- Roadmap orders the mutable route from a published baseline to one next-minor
  Version Scope and owns its milestone entries;
- Version Scope defines the promises, exclusions, and exit criteria for one
  declared version line;
- Change groups accepted work and evidence for one bounded delivery;
- Release Plan selects one exact release transition and its participating
  Changes;
- Readiness Record owns gate applicability, evidence, blockers, and the
  explicit ready-or-blocked disposition for one exact candidate; and
- Release Record immutably owns the delivered summary, migration notes,
  protected merge SHA, tag, packages, and publisher identity.

No role contains or subclasses another. Applicable roles use explicit stable
references. Version Scope remains the scope anchor, not a root type. Roadmap
references one next-minor Version Scope; Release Plan references one Version
Scope and exact candidate; Readiness Record references its Release Plan,
Version Scope, and candidate commit; Release Record references the accepted
Readiness Record, Release Plan, Version Scope, and protected merge commit.

Version Scope is evergreen while its version line is planned; its published
snapshot becomes immutable evidence. Roadmap remains mutable route planning.
Release Plan and Readiness Record may be refreshed during preparation under the
candidate rules. Release Record is emitted only after publication and is
immutable. Verification supplies assurance but never substitutes for the
Readiness Record's explicit disposition. Forge release notes and changelogs are
mirrors or Derived Views of the Release Record.

Patch releases normally reuse their minor Version Scope. A changed public scope
or compatibility promise requires a new Decision and recompilation. Projects
declare only meaningful version lines; omitted intermediate lines require no
placeholder.

DSET retains these project Version Scopes: `0.3` records the public framework
foundation and `0.3.1` baseline without an adopter-ready claim; `0.4` targets a
complete self-hosted core vertical cut; `0.5` targets the first adopter-ready
multi-language release; and `1.0` targets a fully working stable framework that
passes the RC/final gate. Future scope changes require a new Decision.

This Decision absorbs `DSET-DECISION-OPS-004`. It carries forward that
Decision's flat-role, reference, lifecycle, milestone, release-record, and
Version Scope consequences. It replaces the five-role enumeration by including
Change and classifying all six roles under Delivery in accordance with
`DSET-DECISION-GOV-011`.

## Rationale

Change is the bounded delivery transaction that connects accepted work to the
release candidate, so it belongs in the same carrier family as planning, gate,
and publication records. Keeping the roles flat preserves their separate
authority while the shared Delivery type makes the lifecycle understandable
from IDs and file lists.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
