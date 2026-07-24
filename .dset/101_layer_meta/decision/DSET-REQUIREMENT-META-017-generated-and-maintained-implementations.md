---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-META-017"
scope_path:
  - "layer:meta"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-META-018"
---

# Requirement — Generated and maintained Implementations

A generated current projection declares its generator and source provenance.
A Merge Commit is an atomic relational Implementation with explicit parents.

## Primary claim

Generated reproducible current projections are evergreen Implementations, hand-maintained executable truth is maintained Implementation, and Commits are separate atomic Implementations.

## Rationale

Generator output, maintained source, and commit history have different revision semantics and must not collapse into one artifact identity.
