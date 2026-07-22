# Documentation architecture hub

## Purpose

This is the helicopter-view entry point for DSET artifact governance. It explains how methodology, specifications, architecture, rationale, decisions, procedures, proof, evidence, hubs, and agent workflows remain understandable and mechanically navigable alongside code.

Artifact governance is independent from implementation-language enforcement. A project can combine `documentation-v1` with Python, JavaScript/TypeScript, another code profile, or no code profile.

## Boundaries

This area owns artifact types, authoring boundaries, hub/navigation rules, and the applied documentation profile. It does not own the DSET delivery stages, project-specific behavioral truth, code-style tools, or archived implementation evidence.

## Start here

1. [Artifact architecture](artifact-architecture.md) — the profile axes, authority graph, and hierarchy.
2. [Semantic Types and artifact types](artifact-types.md) — canonical Decision,
   Question, Problem, and QA subtypes plus the independent MECE carrier-role
   classification.
3. [Authoring rules](authoring-rules.md) — universal and type-specific writing rules.
4. [Hub rules](hub-rules.md) — helicopter navigation without exhaustive indexes.
5. [Documentation v1](documentation-v1.md) — deterministic gates and qualitative review contract.

## Operating surfaces

- [Maintenance playbook](maintenance-playbook.md) — how to add, split, move, or revise governed artifacts.
- [Rationale](rationale.md) — why the architecture separates profiles, authority, navigation, procedures, and history.
- [Methodology hub](../methodology/README.md) — the DSET stage and cross-cutting methodology map.
- [Project-control hub](../00_project/README.md) — this repository's accepted truth, changes, schemas, templates, and evidence.

This hub lists stable owning documents, not every Markdown file. Governed areas
and parent relationships are declared in
`00_project/artifacts.toml`; the canonical DSET command validates their
structure and links.
