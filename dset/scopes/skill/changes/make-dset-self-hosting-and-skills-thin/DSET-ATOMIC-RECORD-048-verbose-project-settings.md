+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-048"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-037"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET exposes operator-selectable behavior through one verbose dset_settings.toml file while project identity, topology, contracts, and verification remain manifest truth."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A descriptive filename and in-file explanations make settings discoverable without mixing preferences with facts about the project being governed."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-036"
+++

# Requirement — Publish verbose project settings

The canonical root settings carrier is `dset_settings.toml`. It must explain
its purpose, its boundary with the project manifest and governing documents,
every setting, every accepted value, the behavior each value selects, and the
default. Examples must cover artifact naming, artifact-creation strictness,
implementation preparation, Change workspace selection, delegation budget
selection, and priority ordering.

Settings own operator-selectable behavior. The project manifest owns project
identity, repository and Work Area structure, runtime-risk and durability
topology, external contracts, release targets, verification commands, and
commit-provenance boundaries. Governing documents own definitions and policy;
settings select only registered behavior.

The settings schema must expose these independent choices:

- whether new artifact names include their optional direct subtype;
- medium or high atomic-artifact creation strictness;
- lazy or strict implementation preparation;
- integration-branch or branch-worktree as the default Change workspace;
- low, medium, or high as the delegation budget profile; and
- an ordered project priority scale plus default priority.

New writers and bootstraps emit only `dset_settings.toml`. A root `dset.toml`
may be read only as an explicit migration compatibility input. If both names
exist, validation must stop rather than guess which file owns settings.

DSET-owned mutable structured artifacts and new DSET Markdown frontmatter use
TOML without parallel writable YAML or JSON copies. Existing sealed atomic
carriers and registered legacy Decision carriers remain byte-stable historical
exceptions; correction uses a successor artifact rather than rewriting them.
Host skill metadata, GitHub Actions, ecosystem manifests and lockfiles,
standard JSON Schema, CLI or wire JSON, and machine-local runtime journals may
retain their prescribed formats.

## Rationale

The expanded settings surface centralizes real operator choices while keeping
descriptive project truth independently reviewable. Compatibility is a read
boundary, not a second write path.

This emitted Requirement atom is immutable. Later correction requires a
successor and append-only lifecycle evidence.
