---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-042"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-REQUIREMENT-GOV-041"
---

# Requirement — Use the hidden project control root

The canonical current layout is:

- `.dset/dset_settings.toml` — the only writable settings and project-manifest
  carrier;
- `00_project/` — project-wide evergreen artifacts, atomic/context records,
  evidence, verification, registries, migrations, and generated views;
- `10_versions/` — project-wide Version lifecycle artifacts, Changes,
  archives, and pull-request history;
- `.dset/<layer>/` — direct META, GOV, TOOL, SKILL, and OPS roots containing
  layer evergreen artifacts plus layer-owned atomic/context and proof records;
  and
- `.dset/runtime/` — ignored run, session, cache, migration-backup, and other
  replaceable operational state, except its committed ignore policy.

Persisted paths in DSET settings, registries, manifests, relations, reports,
and generated artifacts are relative to the repository root, for example
`.dset/gov/plan-tests.md`. They are never interpreted relative to `.dset/`.
Markdown links may remain relative to the Markdown file that owns the link.

Features and feature groups, when enabled, add a structural segment below the
appropriate project owner; they do not restore a generic `scopes` carrier.
Schema 1.0–1.2 layouts and root settings remain read-only compatibility inputs.
New initialization emits schema 1.3 directly. A migration preserves immutable
carrier bytes, stable semantic IDs, source Git blobs, and registered relocation
chains; mutable references and generated views are rewritten to current paths.

This Requirement atom is immutable. Later correction requires a successor and
append-only lifecycle event.

## Primary claim

A current DSET project owns its control plane under .dset, stores canonical paths relative to the repository root, and isolates ignored operational state under .dset/runtime.

## Rationale

A hidden, distinctive control-plane root separates DSET governance from product content without sacrificing portable, unambiguous repository-local paths.
