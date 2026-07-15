# Governance architecture and bootstrap

**Rule ID:** `DSET-RULE-ARCHITECTURE`

## Authority

The adopting repository's `dset/dset.yaml` selects a local governance profile. `dset/governance.yaml` maps workflow and rule IDs to exactly one editable governing document inside the repository. A materialized document is project truth immediately; its source template and version remain provenance only.

Resolution precedence is project-local registered rule, then an explicitly selected local profile, then failure. Never fall back to wrapper prose, agent memory, a generated cache, an installed copy, or remote framework text.

## Bootstrap

1. Walk upward from the working path until `dset/dset.yaml` is found.
2. Read the selected `repository_governance` profile.
3. Validate `dset/governance.yaml`, local ownership, dependencies, documents, applicability, customization, and wrapper identity.
4. Resolve the requested workflow in registry order.
5. Stop before governed work when any selected owner is unresolved or incompatible.

Explicit justified non-applicability is valid. Missing or invalid selected ownership is not.

## State boundaries

The project manifest selects the profile; the registry owns resolution metadata; governing documents own rules; wrappers own invocation only; generated indexes and caches are derived. Writes that change customization status are explicit and never overwrite governing documents.
