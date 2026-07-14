# Design — Add artifact governance profiles

## Boundaries

```text
README.md                         repository root hub
├── documentation/README.md      artifact-governance hub
│   ├── artifact-architecture.md normative system model
│   ├── artifact-types.md        ownership catalog
│   ├── authoring-rules.md       universal and type-specific rules
│   ├── hub-rules.md             navigation contract
│   ├── documentation-v1.md      executable applied profile
│   ├── maintenance-playbook.md  repeatable update procedure
│   └── rationale.md             why this architecture exists
├── methodology/README.md        pipeline/methodology hub
├── dset/README.md               project-control hub
└── skills/README.md             agent-workflow hub

dset/artifacts.yaml              repository adoption and governed-area graph
dset/schemas/artifacts.schema.json
```

The documentation area is a framework surface, not pipeline stage 7. `methodology/00` continues to own stage routing. The root README gives area-level navigation; area hubs give a local helicopter view; atomic documents own rules, rationale, or procedures.

## State and durability

| Concern | Authority | Writer model | Refresh boundary | Failure/recovery proof |
|---|---|---|---|---|
| Artifact-profile selection | `dset/dset.yaml` | Reviewed repository change | Every validation run | ART-TEST-001 |
| Governed area graph | `dset/artifacts.yaml` | Reviewed repository change | Every validation run | ART-TEST-002/003 |
| Artifact-type rules | `documentation/` normative docs | Reviewed methodology change | When rules change | ART-TEST-004 + ART-EVAL-002/003 |
| Rationale | `documentation/rationale.md` | Reviewed methodology change | When reasoning changes | Link and navigation checks |
| Runtime evidence | GitHub checks and archived DSET proof | GitHub plus evidence-only commits | Per PR head | ART-TEST-006 |

## Supportability

The implementation extends existing stable DSET diagnostics and hosted CI. It stores no user content or runtime telemetry. A failed artifact-profile check identifies the registry or hub path and leaves source files unchanged.

## Decisions

No ADR is required unless implementation reveals a material compatibility decision. The change package owns the initial candidate comparison; accepted cross-cutting rules reconcile into package truth and public documentation.
