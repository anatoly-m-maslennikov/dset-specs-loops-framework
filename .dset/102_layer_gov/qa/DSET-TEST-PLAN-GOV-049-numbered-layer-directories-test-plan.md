---
artifact_type: "test_plan"
artifact_id: "DSET-TEST-PLAN-GOV-049"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-REQUIREMENT-GOV-044"
---

# Test Plan — Verify numbered layer directories

Prove that discovery and every path-owning component map the stable logical
layers to the five numbered current directories. Require:

1. exactly the five numbered layer roots in current self-hosted and initialized
   projects;
2. unchanged layer IDs in semantic artifacts, packages, scopes, relations, and
   public APIs;
3. rejection of missing, mixed, duplicate, or unknown current layer roots;
4. read compatibility for an explicit schema-1.3 `slim-v1` fixture;
5. lossless relocation chains for moved immutable carriers;
6. closed mutable links, schemas, settings, bootstrap files, and generated
   views; and
7. a complete recursive verifier fixed point after regeneration.

This Test atom is immutable. Later correction requires a successor Test and
append-only lifecycle event.

## Primary claim

Deterministic tests prove numbered current layer roots, stable logical layer IDs, lossless relocation, legacy slim-layout reads, and numbered bootstrap output.
