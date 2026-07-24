+++
artifact_id = "DSET-ATOMIC-RECORD-110"
semantic_id = "DSET-REQUIREMENT-GOV-044"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "A current DSET project names its five layer directories 01_layer_meta, 02_layer_gov, 03_layer_tool, 04_layer_skill, and 05_layer_ops while retaining stable semantic layer IDs."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Visible numeric ordering makes the architectural sequence immediately legible in filesystem and GitHub views without changing semantic IDs, artifact IDs, or layer ownership."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-043"
+++

# Requirement — Use visibly ordered layer directories

The current direct layer roots are:

1. `.dset/01_layer_meta/` — framework identity, semantic foundations, and
   authoring contracts;
2. `.dset/02_layer_gov/` — governance, schemas, registries, and templates;
3. `.dset/03_layer_tool/` — executable toolchain and validation behavior;
4. `.dset/04_layer_skill/` — agent-facing wrappers and orchestration; and
5. `.dset/05_layer_ops/` — delivery, release, and supportability.

The directory prefix is presentation and ordering, not semantic identity.
Layer values in IDs, manifests, relations, scopes, package records, and APIs
remain `meta`, `gov`, `tool`, `skill`, and `ops` (or their established uppercase
forms). No artifact or semantic ID is renumbered because its carrier moves.

Schema 1.3 selects this topology with
`[structure].layout = "numbered-layers-v1"`. Existing schema-1.3 projects using
`slim-v1` remain readable migration inputs. New initialization emits only the
numbered layout. A cutover preserves immutable bytes and source Git return
addresses through append-only carrier-relocation records, rewrites mutable
current paths and links, and rejects coexistence of numbered and unnumbered
current layer roots.

This Requirement atom is immutable. Later correction requires a successor and
append-only lifecycle event.
