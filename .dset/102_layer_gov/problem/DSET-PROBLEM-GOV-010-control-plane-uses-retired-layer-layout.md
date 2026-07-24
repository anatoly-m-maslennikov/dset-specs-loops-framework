---
artifact_type: problem
artifact_id: DSET-PROBLEM-GOV-010
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-065"
      - "DSET-IMPL-GOV-007"
      - "DSET-EVALUATION-CASE-GOV-038"
      - "DSET-TEST-CASE-GOV-057"
---

# Problem — Control plane uses the retired layer layout

The installed methodology, applied project authority, and reusable root source
still use the former TOOL → SKILL → IMPLEMENTATION directory topology.

Current META authority instead requires:

```text
META → GOV → SPEC → PROFILES → IMPL → OPS
```

The old numbered-layout decision and its deterministic and interpretive checks
therefore describe and validate a structure that is no longer authoritative.
The repository needs one governed physical-layout decision, a lossless
migration of all three owner trees, updated discovery and synchronization, and
new assurance tied to the accepted topology.

## Primary claim

The repository's three physical control-plane trees still implement and check
a retired layer topology rather than the active scoped realization model.

## Rationale

Archiving the false layout authority without recording the remaining
implementation discrepancy would hide a real governance-to-repository gap.
