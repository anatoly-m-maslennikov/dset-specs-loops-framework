---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-072"
scope_path:
  - "layer:gov"
priority: "high"
promotion:
  affected_children:
    - "governance"
    - "tool"
    - "skill"
    - "implementation"
    - "ops"
  applies_unchanged: true
  local_context_required: false
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "resolution_of"
    targets:
      - "DSET-QUESTION-GOV-011"
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-048"
---

# Requirement — Allow atomic refactoring before compilation

The governing flow is:

```text
Atomic intake
    ↓
Optional atomic refactoring
    ↓
Evergreen compilation
```

Atomic refactoring is optional. Skipping it never prevents compilation when
the active atoms already satisfy the compilation entry gate.

DSET should propose refactoring when one or more active clusters:

- substantially overlap in the claim they govern;
- repeatedly update, qualify, or supersede parts of the same claim;
- require a reviewer to resolve a long successor chain to find current truth;
- contain duplicated authority or competing formulations; or
- make evergreen compilation unnecessarily ambiguous.

Raw atom count is not a trigger. A large set of independent, well-scoped atoms
does not need refactoring.

When invoked, atomic refactoring may:

- consolidate redundant or overlapping atoms;
- split a multi-claim atom into independently reviewable successors;
- correct or clarify an obsolete claim through a new successor;
- normalize scope and relation boundaries; and
- resolve contradictions by emitting the accepted successor atoms.

Refactoring never edits governed atomic meaning in place. It creates new
immutable atoms with new identities and explicit successor relations.
Completely replaced predecessors move to the archive. Partially reused atoms
remain active unless a complete successor set preserves every still-governing
claim.

Several predecessors may be consolidated only when the successor still owns
one primary claim. Refactoring must not create a convenient aggregate that
violates atomicity.

Evergreen compilation consumes only the resulting active atomic frontier.
Generated indexes may describe the refactoring, but they do not establish
governing truth.

## Primary claim

DSET supports optional atomic refactoring between atomic-artifact intake and evergreen compilation; DSET proposes it when active atoms substantially overlap, repeatedly update the same claims, or obscure the current authority frontier, and refactoring emits immutable successors while archiving only fully replaced predecessors.

## Rationale

Semantic-density signals identify when consolidation improves clarity without making every compilation pay the cost or treating a large but well-partitioned atom set as defective.
