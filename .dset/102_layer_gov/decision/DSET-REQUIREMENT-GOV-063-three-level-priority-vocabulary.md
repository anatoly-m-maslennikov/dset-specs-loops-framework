---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-063"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-058"
---

# Requirement — Use a three-level stored priority vocabulary

The only stored priority values are:

- `high`;
- `medium`; and
- `low`.

`highest` remains a virtual comparison result and is never stored.

The former `critical` value is recoded to `high` because the active comparison
policy already treated both as the same base priority. This is a
meaning-preserving vocabulary migration, not reprioritization.

`deferred` is not a priority value. Current work that is intentionally ordered
later uses `low`. Work outside the active version is removed from current
atomic scope and placed in a named future Version Roadmap. For this repository,
the next such target is DSET 0.6.

## Primary claim

DSET stores only high, medium, or low priority; the former critical label is migrated to high, while deferred is not a priority and future work belongs in a named Version Roadmap.

## Rationale

Critical already normalized to high, so recoding its stored label preserves effective meaning. Deferred mixed execution order with future scope; low represents current low-priority work, while a Version Roadmap represents work that is not current.
