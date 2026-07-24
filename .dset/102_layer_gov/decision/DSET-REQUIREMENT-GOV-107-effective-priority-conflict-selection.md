---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-107
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-058"
      - "DSET-REQUIREMENT-GOV-059"
      - "DSET-REQUIREMENT-GOV-063"
---

# Requirement — Derive one effective priority for conflict selection

Persisted priority uses exactly `high`, `medium`, or `low`. `highest` is a
virtual comparison result and is never stored. `critical` and `deferred` are
not accepted values: historical `critical` is migrated to `high`; current
low-order work uses `low`; work outside the current version belongs in a
Version Roadmap.

During a direct conflict comparison:

1. start with each artifact's stored priority;
2. add one level when its scope is a strict ancestor of the competing scope;
3. add one level when its ordered layer precedes the competing layer; and
4. cap the result at virtual `highest`.

An unrelated or incomparable scope receives no scope increment.

`.dset/dset_settings.toml` exposes exactly two selection modes:

- `ask_always`, the default, explains the conflict and asks the operator; and
- `auto_by_effective_priority`, which may select only one uniquely eligible
  winner.

Ties, incomparable structure, uncertainty, or multiple winners always ask.
Mutually unsatisfiable external obligations stop for operator or external
resolution. Deterministic replacement, explicit scoped override, stale-view
routing, and implementation drift follow their own semantics rather than this
selection mode.

## Primary claim

DSET derives effective priority from stored priority, ancestor scope, and
earlier layer position, while automatic conflict selection is opt-in and
requires one unique eligible winner.

## Rationale

One artifact now owns the complete stored vocabulary, structural comparison,
and operator-versus-automatic selection boundary.
