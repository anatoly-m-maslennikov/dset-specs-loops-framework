---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-046
type: decision
semantic_id: DSET-DECISION-GOV-014
status: accepted
priority: high
authority: "operator:anatoly-m-maslennikov"
claim: "TOML migration may omit an explicit null only for a governed field whose declared meaning is exactly optional and unset; every other null blocks migration."
scope:
  kind: project
  id: dset-specs-loops-framework
promotion:
  parent_scope: null
relations:
  - type: child_of
    target: DSET-REQUIREMENT-GOV-036
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Decision — Normalize only declared optional-unset nulls

TOML has no null value. During canonical TOML migration, DSET may omit a source
null only when the owning schema and runtime give absence exactly the same
meaning as “optional and unset.” The initial allowlist is:

- `promotion.parent_scope` in atomic-record frontmatter;
- `items[].decision` in the intake registry; and
- `pull_requests[].merge_commit` in pull-request history.

The migration report records every omission by source and key path. A null at
any other path is non-representable and blocks the migration. Adding another
path requires new accepted authority and deterministic equivalence proof; the
migration tool must never generalize from field names alone.

## Rationale

Encoding a sentinel string or private inline table would make project TOML
harder to read and would leak a codec convention into every consumer. Omitting
only fields already defined as optional and unset preserves their governed
meaning while retaining a visible, reviewable exception boundary.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle evidence.
