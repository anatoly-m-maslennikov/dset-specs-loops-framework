---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-060"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-DECISION-GOV-034"
---

# Requirement — Identity migration preserves atomic content

Atomic artifacts remain immutable during a naming migration. The migration may
change the canonical semantic ID, carrier filename, heading label, and every
stored reference needed to address the same artifact. It must preserve the
artifact's claim, rationale, provenance, relations except for migrated target
identifiers, lifecycle meaning, and other governed content.

Historical terminology inside an immutable claim may remain as the content the
artifact originally asserted. Current execution follows active successor and
lifecycle authority; it does not rewrite the predecessor's claim to make the
predecessor appear current.

## Primary claim

A governed identity migration must update an atomic artifact's canonical identifier and all identifier references without changing the artifact's immutable governed claim.

## Rationale

An identifier is the governed name of an artifact, not the claim asserted by that artifact. Renaming an identifier is therefore a graph-wide identity migration, while rewriting the claim would be an impermissible mutation.
