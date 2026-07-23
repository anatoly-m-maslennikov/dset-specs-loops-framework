+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-202"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-058"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET assigns high, medium, or low base priority by artifact role and derives a capped virtual effective priority from structural-scope and upstream-layer bonuses only while comparing applicable artifacts."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Role defaults express normal authority weight, while bounded comparison bonuses let broader project authority and earlier-layer authority govern narrower or downstream realizations without permanently inflating stored priority or adding separate precedence fields."

[scope]
kind = "layer"
id = "governance"

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "ops"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-010"
+++

# Requirement — Derive effective priority during comparison

New artifacts use only the stored priorities `high`, `medium`, and `low`.
`highest` is a virtual comparison result and must never be written into an
atomic artifact, evergreen file, implementation carrier, or priority event.

Creation defaults are:

- Constraint: `high`;
- Contract, Requirement, and empty-subtype Decision: `medium`; and
- implementation code, configuration, commits, and other implementation
  carriers: `low`, normally inherited from their owning authority.

Other artifact roles inherit from their canonical owner or use the project
default of `medium`. An authorized append-only priority event may change an
artifact's stored base priority without changing these creation defaults.

For one eligible conflict comparison, start from each artifact's current base
priority and add one step when its structural scope is a strict ancestor of the
other applicable artifact's scope. A project artifact therefore receives one
step over a conflicting feature, feature-group, or layer artifact. Add one
further step when its owning layer is earlier in the configured layer order
than the other's layer. Scope and layer bonuses are additive, apply once per
axis rather than once per distance, and cap at `highest`:

`low → medium → high → highest`.

Peer features are not ordered. Unrelated or inapplicable scopes receive no
bonus. Explicit lifecycle, absorption, override, authority, applicability, and
conflict-class rules are applied before effective priority.

Immutable legacy values remain readable without rewriting their atoms:
`critical` normalizes to base `high`, and `deferred` normalizes to base `low`.
New writers never emit either legacy value.
