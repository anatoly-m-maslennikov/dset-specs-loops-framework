# Methodology SKILL public contract

## Skill release target

`dset` is the primary operator entrypoint for initialization, decomposition, landscape/decision/spec/proof/implementation planning, implementation, verification, work-item routing, and next-step advice through registered project-local workflows. `dset-clarify`, `dset-diagnose`, `dset-prototype`, and `dset-release` are explicit specialist triggers. Helper operations are modes or chained workflows, not additional public skill names. All five repository-native source wrappers listed in [the skills hub](../../../../../../skills/README.md) are implemented; runtime, host-distribution, and publication capability must still be claimed only when its separate proof passes.

All five target skills are thin wrappers over the repository governance registry. The registered `DSET-RULE-LIFECYCLE`, `DSET-RULE-SKILL-RUNS`, `DSET-RULE-RELEASE`, `DSET-RULE-DELEGATION-BUDGET`, and `DSET-RULE-WORK-ITEMS` documents own substantive behavior. Versioned bounded local run records under `.dset/runs/` are operational evidence only and are excluded from committed project truth.

Subagents request the main session's model and reasoning effort by default and report effective attestation or uncertainty. Medium budget targets two and caps the whole tree at three unique subagents, depth one, and two rounds. Scope, proof, and safety are invariant; model overrides require dated task-relevant evidence and remain visible in run records.

Intake routing uses only problems, opportunities, and questions in `dset/scopes/gov/intake.yaml`. Decision is the durable entity and artifact and uses the full `DECISION` type. Decisions and DSET Changes are artifacts, tasks live inside Changes, and GitHub Issues and Jira/support tickets are external representations. IDs use the `DSET` project prefix: project-wide IDs omit the optional layer, while layer-owned IDs insert `META`, `GOV`, `TOOL`, `SKILL`, or `OPS` between the full type and sequence. Optional accepted User Stories use the compact full `STORY` ID type, measurable intended effects use the full `OUTCOME` type, and authoritative boundaries use the full `CONTRACT` type.

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
