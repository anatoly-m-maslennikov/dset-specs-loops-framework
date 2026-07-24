---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-065
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-063"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-026"
      - "DSET-REQUIREMENT-META-029"
      - "DSET-REQUIREMENT-META-052"
      - "DSET-REQUIREMENT-META-057"
      - "DSET-REQUIREMENT-META-059"
      - "DSET-REQUIREMENT-META-066"
      - "DSET-REQUIREMENT-META-067"
      - "DSET-REQUIREMENT-META-068"
---

# Requirement — Use scoped realization layers

DSET uses six ordered layers:

```text
META → GOV → SPEC → PROFILES → IMPL → OPS
```

| Layer | Canonical responsibility |
|---|---|
| META | Meanings, universal invariants, layer topology, and inter-layer semantics |
| GOV | Governed carriers, identity, settings, provenance, lifecycle, applicability, canonical scope registration, and conflict governance |
| SPEC | Current project behavior, obligations, technical and integration choices, assurance definitions, and cross-scope contracts |
| PROFILES | Selectable implementation profiles, environments, dependency policies, authoring practices, portability and security rules, and profile-specific gates |
| IMPL | Concrete source, skill packages, Test and Eval implementations, configuration, schemas, migrations, adapters, commits, pull requests, and implementation traceability |
| OPS | Post-implementation delivery, release, publication, runtime supportability, investigation, containment, recovery, and hosted evidence |

META owns semantic dimensions and layer boundaries but never owns the concrete
artifact Type names assigned by GOV.

## Scope propagation

GOV registers each project scope once. SPEC, PROFILES, and IMPL reuse the same
scope IDs without redefining them.

Each scope forms an aligned realization chain:

```text
SPEC/<scope> → PROFILES/<scope> → IMPL/<scope>
```

The layers answer distinct questions:

| Layer | Question |
|---|---|
| SPEC | What must this scope do, prevent, expose, and satisfy? |
| PROFILES | Which selectable implementation rules apply to this scope? |
| IMPL | Which concrete artifacts realize this scope? |

Project-level surfaces own cross-scope concerns. SPEC owns global obligations,
cross-scope Contracts, Integration Decisions, and end-to-end QA Cases.
PROFILES owns shared profile selections. IMPL owns shared implementation,
repository configuration, build integration, and cross-scope traceability.

QA artifacts retain the scope of the subject they check. A shared `qa` scope
owns only common assurance capabilities, standards, protocols, and
infrastructure.

## Layer authority

Each responsibility has one canonical owner. A layer may depend on earlier
layers and affect later layers, preferably its immediate successor. It cannot
redefine an earlier layer's responsibility. Horizontal, bidirectional, or
cyclic collaboration belongs in scope Contracts rather than layer authority.

PROFILES owns only rules that participate in a selectable implementation
profile. It never owns concrete source or required project behavior.

## Primary claim

DSET separates universal semantics, governance, required behavior, selectable
profiles, concrete realization, and post-implementation operation into the
ordered META → GOV → SPEC → PROFILES → IMPL → OPS topology, with project scopes
propagated consistently through SPEC, PROFILES, and IMPL.

## Rationale

The predecessor mixed universal layer topology with concrete Type names owned
by GOV. The narrower successor keeps META technology-independent and leaves
each downstream responsibility with one owner.
