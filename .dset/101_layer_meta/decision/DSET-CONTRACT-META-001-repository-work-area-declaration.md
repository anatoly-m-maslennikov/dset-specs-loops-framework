---
artifact_type: contract
artifact_id: DSET-CONTRACT-META-001
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
source_refs:
  - "DSET-REQUIREMENT-META-011"
relation_kind: scope_declaration_for
endpoints:
  - role: declarer
    identity: adopting_repository_owner
    origin: internal
  - role: consumer
    identity: dset_governed_workflows
    origin: internal
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-META-011"
---

# Contract — Repository Work Area declaration

An adopting repository owner declares either repository-level scope or one or
more existing repository-relative folders as Work Areas. The declaration may
cover local, deployable, library, documentation, methodology, data, or mixed
content without requiring code or deployability.

DSET lifecycle, Change, proof, supportability, and session-continuity
consumers resolve the current accepted declaration before scope-dependent
work. Session continuity may retain a bounded reference but cannot create,
rename, reclassify, replace, or supersede the boundary.

## Direction

Repository scope declaration → DSET artifacts, workflows, proof, runs, and
handoffs.

## Conformance

Every scope-dependent consumer resolves either repository-level scope or the
applicable declared Work Areas. Absolute paths, paths outside the repository,
missing folders, and stale declarations do not conform.

## Compatibility

Content changes inside a Work Area do not change the boundary. A path rename,
removal, scope split, or scope merge requires an explicit reviewed successor
Contract and refresh of affected references and evidence. A simple repository
may remain one repository-level scope.

## Rationale

Repository folders are neutral governance boundaries. They must support code,
documentation, methodology, data, and mixed projects without silently
inventing services, modules, deployment units, or features.
