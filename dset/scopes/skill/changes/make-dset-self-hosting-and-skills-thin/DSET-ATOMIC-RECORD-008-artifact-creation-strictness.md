+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-008"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-035"
status = "accepted"
priority = "high"
child_of = ["DSET-REQUIREMENT-GOV-032", "DSET-REQUIREMENT-GOV-033"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Gate atom creation and propose broader scope

Artifact-creation strictness is an independently selectable optional
capability in root `dset.toml`, not part of one bundled advanced mode. Its
default value is `medium`; a project may select `high`.

At `medium`, DSET may emit one accepted atomic claim when its authority,
primary claim, semantic Type, owning structural scope, provenance, and material
links are clear. Non-authoritative optional detail may remain explicitly
unknown, and a separate Question records any uncertainty that would otherwise
change the claim.

At `high`, DSET must not emit an atom while any material part of its authority,
meaning, boundary, Type, scope, priority, lineage, acceptance, conflict state,
or verification obligation is ambiguous. It asks focused questions until the
atom is precise enough to be immutable, or stops without writing it. A draft
or conversation checkpoint is not an emitted atom.

Before emission at either strictness, DSET checks whether the claim is eligible
for the immediately broader enabled structural scope: feature to feature
group, feature or feature group to project, or layer to project. Eligibility
requires the claim to apply unchanged to every affected child of that broader
scope and to belong to that scope under narrowest-common-scope ownership. If
eligible, DSET proposes the one-step promotion and explains the affected
children; it never promotes without operator acceptance and never skips an
enabled intermediate scope.

Promotion assessment is an emission gate, not a requirement to generalize.
Feature-specific evidence, implementation detail, exceptions, or vocabulary
remain local. If an already emitted local atom is later generalized, promotion
creates a new immutable broader-scope atom linked to the local source; it does
not move or edit the older atom.

## Rationale

Medium strictness preserves useful capture without pretending optional detail
is known. High strictness supports repositories where an immutable artifact
must be precise before it exists. The promotion check prevents accidental
duplication while preserving local ownership and explicit operator authority.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
