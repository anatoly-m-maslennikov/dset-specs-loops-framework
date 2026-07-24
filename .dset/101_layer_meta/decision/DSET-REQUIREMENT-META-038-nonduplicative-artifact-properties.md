---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-038
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-094"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
---

# Requirement — Keep artifact properties nonduplicative

Every governed artifact property has one distinct meaning. A property section
contains neither two properties that express the same meaning nor a property
whose value is deterministically derived from another canonical property, the
registered artifact type and subtype, the current project, or repository
placement.

The artifact type and optional direct subtype determine their registered
route. Artifact carriers therefore do not repeat `revision_mode`,
`content_role`, or `governance_locus`. Atomic artifacts do not carry an
acceptance status: emission follows explicit acceptance, while active versus
archived placement represents whether the atom participates in current
authority.

Project identity and internal project authority are ambient. An external
source, issuer, or relation endpoint remains explicit through the precise
type-specific property that owns that meaning.

Repeated relations with the same kind, roles, qualifiers, and meaning use one
non-empty `targets` list. Relations whose roles, qualifiers, or meanings differ
remain separate.

## Primary claim

Artifact properties contain only explicit, non-derived meanings and never
duplicate another canonical property, registered type mapping, ambient project
fact, or repository-placement fact.

## Rationale

Duplicated or derivable properties create competing writable representations
that can disagree. Keeping each meaning in one canonical place preserves
unambiguous interpretation across every downstream layer.
