---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-070
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-060"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-035"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-051"
      - "DSET-REQUIREMENT-META-069"
---

# Requirement — Keep the semantic route catalog total and one-to-one

Every possible combination of one Revision mode, one Content role, and one
Governance locus has exactly one canonical `artifact_type`.

Under the current semantic dimensions, the catalog therefore contains exactly
63 full routes:

```text
3 Revision modes × 7 Content roles × 3 Governance loci
```

No semantic route may be empty or occupied by multiple top-level Types. Direct
subtypes may refine a canonical Type but inherit its complete route and do not
create another top-level occupant.

## Primary claim

The semantic route catalog is a total one-to-one mapping from all 63 full
routes to 63 canonical artifact Types.

## Rationale

The predecessor preserved the totality rule but depended on a retired
six-role authority. The successor binds the same invariant to the current
seven-role model and makes the expected route count explicit.
