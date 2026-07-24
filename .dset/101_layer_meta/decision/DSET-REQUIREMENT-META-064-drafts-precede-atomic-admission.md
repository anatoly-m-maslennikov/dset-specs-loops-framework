---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-064
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-038"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-058"
---

# Requirement — Drafts precede atomic admission

A Draft is a mutable pre-admission candidate for a governed artifact. It is
not an Atomic Artifact, has no stable artifact ID, consumes no sequence number,
and carries no project authority.

Promotion admits the candidate as a new Atomic Artifact. Admission assigns its
stable identity and begins semantic immutability. All later lifecycle handling
preserves the accepted content: an active atom may move unchanged into an
archive, but it cannot be edited into a different meaning or reverted to a
Draft.

Active, Draft, and archived placement are derived structural facts rather than
properties stored in artifact frontmatter. Atomic artifacts therefore carry no
duplicated lifecycle status.

## Primary claim

Mutable Drafts exist only before admission; promotion creates the immutable
Atomic Artifact, whose later active or archived placement never changes its
accepted meaning.

## Rationale

Large reports and other substantial atoms often need iterative authoring before
their meaning is precise enough to freeze. Keeping that work outside the atomic
set permits revision without weakening the immutability of admitted artifacts.
