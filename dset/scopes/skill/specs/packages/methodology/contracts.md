# Methodology SKILL public contract

## Skill release target

`dset` is the primary operator entrypoint for lifecycle and next-step advice. Every stable lifecycle mode also has an explicit public direct-entry skill listed in [the skills hub](../../../../../../skills/README.md). Governed wrappers resolve registered project-local workflows; `dset-init` and `dset-repair-governance` are the only bounded pre-resolution exceptions. Runtime, host-distribution, and publication capability must still be claimed only when its separate proof passes.

All governed target skills are thin wrappers over the repository governance registry. The registered `DSET-RULE-LIFECYCLE`, `DSET-RULE-SKILL-RUNS`, `DSET-RULE-RELEASE`, `DSET-RULE-DELEGATION-BUDGET`, and `DSET-RULE-WORK-ITEMS` documents own substantive behavior. Versioned bounded local run records under `.dset/runs/` are operational evidence only and are excluded from committed project truth.

The distributed skill packages are project-agnostic. They do not ship one
global project policy: every governed invocation discovers its target's owning
DSET root and uses that project's local governance layer. Switching projects
switches registry, rule documents, customization, and ruleset identity without
changing the installed skill package.

Subagents request the main session's model and reasoning effort by default and report effective attestation or uncertainty. Medium budget targets two and caps the whole tree at three unique subagents, depth one, and two rounds. Scope, proof, and safety are invariant; model overrides require dated task-relevant evidence and remain visible in run records.

Intake routing uses only problems, opportunities, and questions in `dset/scopes/gov/intake.yaml`; open Conflicts use a separate governed register/view. Type follows semantic content and authority/lifecycle role, never the workflow or skill. Decision is the durable entity and artifact and uses the full `DECISION` type. Decisions and DSET Changes are artifacts, tasks live inside Changes, and GitHub Issues and Jira/support tickets are external representations. IDs use the `DSET` project prefix: project-wide IDs omit the optional layer, while layer-owned IDs insert `META`, `GOV`, `TOOL`, `SKILL`, or `OPS` between the full type and sequence. Optional accepted User Stories use the compact full `STORY` ID type, measurable intended effects use the full `OUTCOME` type, verified incompatible applicable claims use the full `CONFLICT` type, and authoritative boundaries use the full `CONTRACT` type.

### DSET-CONTRACT-SKILL-001 — Released skills are host-native

| Field | Value |
|---|---|
| Authority | DSET maintainers |
| Source | Official skill/package formats for every declared target host, each pinned by version or digest in release evidence |
| Version or digest | `1.0` |
| Direction | DSET release artifacts to declared host skill loaders |
| Producer | DSET skill release workflow |
| Consumer | Each declared target host, including Claude and Codex when claimed |
| Conformance | Every released DSET skill is a real installable host-native skill, not descriptive Markdown alone; each target has artifact, install, load, and representative invoke proof |
| Compatibility | The release declares a host matrix and passes every claimed target against its pinned format; unsupported targets are omitted rather than implied |
| Lifecycle | `active` |

### DSET-CONTRACT-SKILL-002 — Skills resolve target-project governance

| Field | Value |
|---|---|
| Authority | DSET maintainers own the discovery/resolution protocol; each adopting project owns its resolved local rules |
| Source | The invocation target, discovered project manifest, selected repository-local governance registry, and registered governing documents |
| Version or digest | `1.0` |
| Direction | One installed DSET skill distribution to the governance layer of the project owning the invocation target |
| Producer | DSET host-native skill wrapper and resolver adapter |
| Consumer | Any initialized DSET repository or declared monorepo Work Area |
| Conformance | Begin from the explicit target; discover exactly one owning DSET root; validate and resolve the requested workflow from that root; report root and ruleset identity; read only returned local rule documents before governed work; never retain or substitute another project's policy |
| Compatibility | Byte-identical skills must resolve independent projects differently when their local rules differ; nested targets use their owning root; no root routes only to initialization, invalid or competing roots stop, and source templates remain bootstrap/update provenance rather than runtime project truth |
| Priority | unknown pending the registered project scale |
| Creation state | accepted |
| Absorbs | none |
| Rationale | Stable reusable skills and mutable project-owned policy can evolve independently only when every invocation re-resolves the target project's authority boundary |
| LLM session IDs | `codex:019f591f-04f6-70f2-8de7-828b7cccc69d` |
| Lifecycle | `active` |
