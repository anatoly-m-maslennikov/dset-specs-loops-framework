---
artifact_type: specification
artifact_subtype: version_scope
artifact_id: "{{project_key}}-SPECIFICATION-{{sequence}}"
version_line: "{{version_line}}"
status: draft
llm_session_ids: []
---

# Version Scope — {{version_line}}

## Promise

Define the coherent result this version line provides.

## Included outcomes and capabilities

- Link accepted Outcome, Requirement, Contract, and Decision IDs.

## Exclusions

- State promises deliberately outside this version line.

## Exit criteria

- Link applicable Test, Evaluation, supportability, adoption, migration, and
  release-gate criteria without copying their definitions.

## Governing provenance

- **Compiled from:** pending Decision and direct Decision-subtype IDs
- **Supersedes:** none
- **Recompile trigger:** a governing atom changes the version promise,
  exclusion, or exit criterion
