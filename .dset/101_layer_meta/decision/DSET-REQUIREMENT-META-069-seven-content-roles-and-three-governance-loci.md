---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-069
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-061"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-048"
      - "DSET-REQUIREMENT-META-049"
      - "DSET-REQUIREMENT-META-051"
      - "DSET-REQUIREMENT-META-052"
---

# Requirement — Use seven Content roles and three Governance loci

DSET classifies governed artifact meaning through exactly seven Content roles:

1. Problem;
2. Analysis;
3. Definition;
4. Method;
5. Assurance;
6. Implementation; and
7. Observation.

Governance locus is an independent semantic axis with exactly three values:

- `internal` for project-owned meaning;
- `external` for meaning imposed or owned outside the project; and
- `relation` for meaning that exists between explicit endpoints.

Revision mode remains the independent change-semantics axis owned by its own
META requirement. `scope_path` remains a structural coordinate rather than a
semantic axis.

Concrete artifact Type names, subtype vocabulary, identity prefixes, and
carrier rules are downstream GOV responsibilities. META defines only the
stable semantic dimensions and their meanings.

## Primary claim

DSET uses seven Content roles and three Governance loci as independent
technology-neutral semantic dimensions, without assigning concrete artifact
Type names in META.

## Rationale

The predecessor correctly introduced Assurance and the seven-role model but
coupled them to a later-retired QA layer and duplicated GOV-owned Type names.
The successor preserves only the universal semantic invariant.
