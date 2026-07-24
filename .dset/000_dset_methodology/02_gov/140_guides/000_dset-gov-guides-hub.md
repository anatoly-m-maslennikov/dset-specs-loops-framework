---
artifact_type: navigation
artifact_subtype: hub
scope_path:
  - layer:gov
priority: medium
---

# Documentation architecture hub

## Purpose

This is the helicopter-view entry point for DSET artifact governance. It explains how methodology, specifications, architecture, rationale, decisions, procedures, proof, evidence, hubs, and agent workflows remain understandable and mechanically navigable alongside code.

Artifact governance is independent from implementation-language enforcement. A project can combine `documentation-v1` with Python, JavaScript/TypeScript, another code profile, or no code profile.

## Boundaries

This area owns artifact types, authoring boundaries, hub/navigation rules, and the applied documentation profile. It does not own the DSET delivery stages, project-specific behavioral truth, code-style tools, or archived implementation evidence.

## Start here

1. `artifact-architecture.md` — the profile axes, authority graph, and hierarchy.
2. `artifact-types.md` — direct registered type/subtype meanings and their
   route-selection boundaries.
3. `authoring-rules.md` — universal and type-specific writing rules.
4. `hub-rules.md` — helicopter navigation without exhaustive indexes.
5. `documentation-v1.md` — deterministic gates and qualitative review contract.

## Operating surfaces

- `maintenance-playbook.md` — how to add, split, move, or revise governed artifacts.
- `rationale.md` — why the architecture separates profiles, authority, navigation, procedures, and history.
- Framework source hub — the reusable DSET source map.
- Applied project-control hub — this repository's accepted truth, plans, analysis, and evidence.

This hub lists stable owning documents, not every Markdown file. Governed areas
and parent relationships are declared in the `artifact_structure` section of
`.dset/dset_settings.toml`; the canonical DSET command validates their structure
and links.
