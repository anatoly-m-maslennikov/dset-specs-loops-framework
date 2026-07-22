+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-101"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-041"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "A current DSET project uses one documented dset/dset_settings.toml for settings and manifest facts, dset/project for project-wide truth and records, dset/versions for Version lifecycle artifacts, and direct dset/<layer> roots for layer-owned truth."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Removing the redundant scopes segment and split manifest makes ownership visible from the filesystem while preserving project, Version, and layer boundaries."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-040"
+++

# Requirement — Use the slim project control layout

The canonical current layout is:

- `dset/dset_settings.toml` — the only writable settings and project-manifest
  carrier;
- `dset/project/` — project-wide evergreen artifacts, atomic/context records,
  evidence, verification, registries, migrations, and generated views;
- `dset/versions/` — project-wide Version lifecycle artifacts, Changes,
  archives, and pull-request history; and
- `dset/<layer>/` — direct META, GOV, TOOL, SKILL, and OPS roots containing
  layer evergreen artifacts plus layer-owned atomic/context and proof records.

Features and feature groups, when enabled, add a structural segment below the
appropriate project owner; they do not restore a generic `scopes` carrier.
Schema 1.0–1.2 layouts and root settings remain read-only compatibility inputs.
New initialization emits schema 1.3 directly. A migration preserves immutable
carrier bytes, stable semantic IDs, source Git blobs, and registered relocation
aliases; mutable references and generated views are rewritten to current paths.

This Requirement atom is immutable. Later correction requires a successor and
append-only lifecycle event.
