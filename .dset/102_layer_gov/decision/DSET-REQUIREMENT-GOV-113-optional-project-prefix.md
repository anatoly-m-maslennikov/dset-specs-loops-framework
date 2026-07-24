---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-113
scope_path: ["layer:gov"]
priority: medium
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-064"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-GOV-108"
---

# Requirement — Configure an optional project prefix

`.dset/dset_settings.toml` records whether artifact identities use a project
prefix and records its value when enabled.

Project initialization recommends:

- no prefix for one small project with one artifact namespace; and
- a prefix for a monorepo, multiple DSET projects in one repository, or any
  shared namespace where otherwise valid identities could collide.

Changing the setting after governed identities exist requires one complete
lossless whole-graph migration. It updates active and archived identities,
filenames, relations, maintained-artifact references, settings,
implementation references, evidence, and commit provenance together. The
project never retains two accepted identity vocabularies.

## Primary claim

Each project explicitly enables or disables its identity prefix, with defaults
chosen to balance readability and collision safety.

## Rationale

A small single-project repository gains no disambiguation from a mandatory
prefix, while a shared namespace requires one.
