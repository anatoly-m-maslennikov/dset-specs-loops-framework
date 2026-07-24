---
artifact_type: implementation_decision
artifact_id: DSET-IMPL-GOV-002
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-021"
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-GOV-052"
---

# Implementation Decision — Materialize installed methodology

The reusable methodology is authored in the repository-root source and copied
unidirectionally into `.dset/000_dset_methodology/` only by an explicit
operator synchronization command.

Installed methodology carriers contain the actual governed content. They are
not symbolic links or repository-relative reference carriers. Skills resolve
all methodology, settings, artifacts, and maintained views only inside the
selected project's `.dset/` control root.

Synchronization computes the destination layout deterministically, stages and
validates the complete result, refuses unresolved collisions, and replaces only
the installed methodology snapshot. Ordinary source edits never trigger an
implicit mirror.

## Primary claim

Project-local installed methodology is a validated materialized snapshot under
`.dset/`, produced only by explicit one-way synchronization.

## Rationale

Materialization keeps project governance self-contained for every supported
host and avoids symlink behavior, reference traversal, or dependence on a
repository-specific source layout at skill runtime.
