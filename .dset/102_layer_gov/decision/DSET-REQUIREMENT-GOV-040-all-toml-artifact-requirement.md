+++
artifact_id = "DSET-ATOMIC-RECORD-073"
semantic_id = "DSET-REQUIREMENT-GOV-040"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET exposes operator-selectable behavior through one verbose dset_settings.toml and uses TOML for every DSET-owned structured artifact and Markdown frontmatter, including historical carriers migrated through governed transitions."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "One readable current encoding removes the historical YAML exception while the transition ledger preserves provenance and return paths separately from current authority."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-037"

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-018"
+++

# Requirement — Use TOML for every DSET artifact carrier

The canonical root settings carrier remains `dset_settings.toml` with the same
documented settings, defaults, accepted values, and settings-versus-manifest-
versus-governance ownership boundary defined by its predecessor.

All DSET-owned structured artifact files and DSET Markdown frontmatter use
TOML. This includes emitted atoms, promoted evidence, legacy Decision carriers,
and historical structured editions after an authorized carrier transition.
No DSET-owned `.yaml` or `.yml` artifact and no DSET Markdown YAML frontmatter
remains in the current repository.

Historical standalone editions use adjacent `<stem>.legacy.toml` envelopes
when `<stem>.toml` already owns current truth. Current readers never fall back
to those envelopes. Every migrated carrier is registered in the append-only
transition ledger with semantic-equivalence proof and a Git source-return
address.

Standards-compliant JSON Schema, GitHub Actions, host skill metadata, ecosystem
manifests and lockfiles, wire/CLI formats, and machine-local runtime journals
retain externally prescribed formats. They are not alternative DSET artifact
encodings.

This Requirement atom is immutable. Later correction requires a successor and
append-only lifecycle event.
