---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-096
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-DECISION-GOV-035"
      - "DSET-REQUIREMENT-GOV-065"
---

# Requirement — Use explicit archive commit trailers

Every Git commit that moves one or more Atomic Artifact carriers into a
Type-local `archive/` directory records the transition with explicit commit
trailers.

The minimum trailers are:

```text
Archives: <artifact-id>
Archive-Reason: replaced|resolved|withdrawn
Archive-Reference: <successor-resolver-or-version-id>
Session: <host-prefixed-session-id>
```

Repeat `Archives:` for every carrier moved by the commit. All archived
artifacts in one commit must share the declared reason and reference; otherwise
the transitions use separate commits.

`Archive-Reference:` is required for replacement, resolution, and withdrawal
into future Version work. It may be omitted only for a terminal withdrawal
whose commit body explains why no successor or future intent exists.

Git owns the archive time and committer identity. Typed artifact relations own
the semantic replacement or resolution. The trailers provide a searchable
binding between the physical move and that semantic history; they do not
modify the archived atom or create a lifecycle-event artifact.

Rebase, squash, or another history-rewriting delivery step must preserve the
archive trailers in the surviving mainline commit.

## Rationale

Git can establish when a carrier moved, but an unstructured rename commit does
not reliably expose which atoms moved or why. Explicit trailers make archive
history deterministic and machine-readable without introducing another
lifecycle authority.
