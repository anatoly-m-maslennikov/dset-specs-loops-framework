---
artifact_type: analysis_report
artifact_subtype: technical_investigation
artifact_id: DSET-ANALYSIS-REPORT-004
scope_path: ["layer:gov"]
priority: high
observed_at: 2026-07-24
source_refs:
  - "https://docs.github.com/en/enterprise-cloud@latest/contributing/writing-for-github-docs/using-yaml-frontmatter"
  - "https://toml.io/en/v1.0.0"
  - "https://www.rfc-editor.org/info/rfc8259/"
  - "https://json-schema.org/draft/2020-12/json-schema-core"
  - "https://docs.npmjs.com/files/package.json/"
  - "https://code.visualstudio.com/api/references/extension-manifest"
  - "https://spec.openapis.org/oas/latest.html"
  - "https://jsonlines.org/"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: analysis_of
    targets:
      - "DSET-REQUIREMENT-GOV-056"
      - "DSET-REQUIREMENT-GOV-095"
      - "DSET-CONSTRAINT-GOV-002"
---

# Analysis Report — Artifact carrier format policy

## Conclusion

Markdown with YAML frontmatter should become DSET's default artifact carrier.
TOML should stop being the generic DSET structured-data format and remain only
where it is genuinely better: human-edited executable configuration.

JSON should be used for machine interoperability, standardized JSON documents,
externally prescribed JSON contracts, and generated machine data. JSON
Lines/NDJSON should be used for append-only runtime streams.

The governing principle is:

> Markdown for governed meaning. TOML for human-edited executable
> configuration. JSON for machine interoperability. JSONL for runtime streams.
> External contracts keep their prescribed format.

This is an analysis result, not authority. Adopting it requires a successor to
the current all-TOML Requirement and a bounded migration plan.

## Question

Should DSET continue using TOML as its generic structured-artifact format, or
should carrier format follow the artifact's actual job?

The investigation compared:

- Markdown with YAML frontmatter;
- TOML;
- JSON;
- JSON Lines/NDJSON; and
- externally or ecosystem-prescribed native formats.

## Current repository state

Immediately before this report was added, `.dset` contained:

| Extension | Files |
|---|---:|
| Markdown | 589 |
| TOML | 63 |
| JSON | 23 |

Most committed semantic artifacts are already Markdown. The TOML set consists
mainly of:

- `dset_settings.toml`;
- installed templates, profiles, dependency policies, and fixtures; and
- identity-only reference carriers across the applied layers.

The JSON set consists mainly of installed JSON Schemas plus the generated
Python bootstrap bundle.

The repository source methodology also keeps many JSON Schemas encoded as
`*.schema.toml`, then materializes JSON copies into the installed methodology.
That creates a format-conversion boundary around a standard whose native
document form is already JSON.

## Format selection must not follow revision mode

`revision_mode` does not determine carrier format.

- Atomic artifacts normally need structured identity plus human-readable
  claims, context, rationale, and relations.
- Evergreen artifacts normally need navigable current views, domain
  definitions, diagrams, state tables, and links.
- Maintained artifacts may be documentation, configuration, code, generated
  data, or runtime state.

Therefore maintained artifacts cannot have one universal carrier. A maintained
specification, executable configuration, source file, and generated API
snapshot have different consumers and should use different formats.

## Recommended carrier matrix

| Carrier | Default use |
|---|---|
| Markdown with YAML frontmatter | Human-governed artifacts with narrative meaning |
| TOML | Human-edited configuration executed directly by tools |
| JSON | External contracts, standardized schemas, wire data, and generated machine data |
| JSONL/NDJSON | Append-only runtime logs and event streams |
| Native format | Source code, host manifests, CI workflows, lockfiles, and other prescribed implementation files |

## Markdown with YAML frontmatter

Use Markdown with YAML frontmatter for nearly all semantic DSET artifacts:

- Requirements, Constraints, Contracts, and Implementation Decisions;
- Questions and Problems;
- Rationales and Analysis Reports;
- Test and Evaluation Plans;
- Evidence and Verification records;
- evergreen specifications and plans;
- hubs and architecture views;
- Version Roadmaps, readiness records, and release records;
- human-readable reports; and
- reference or pointer artifacts when a separate pointer carrier is still
  necessary.

GitHub uses YAML frontmatter to attach structured metadata to Markdown pages.
The carrier keeps machine-readable properties together with the human-readable
meaning and renders usefully in repository previews.

### Restricted YAML property profile

DSET should not expose the full complexity of YAML merely because frontmatter
uses YAML syntax. Its property profile should:

- reject tags, anchors, aliases, and merge keys;
- reject duplicate properties;
- quote ambiguous strings;
- keep nesting shallow and schema-bounded;
- keep large tables, diagrams, explanations, and claims in the Markdown body;
- prohibit properties that duplicate body content or type-derived route
  coordinates; and
- validate properties against the registered artifact type.

Source material embedded in a Markdown artifact is body content and does not
need nested frontmatter.

## TOML

Keep TOML for:

- `.dset/dset_settings.toml`;
- human-edited executable configuration;
- tool and profile settings consumed directly by deterministic code;
- dependency and enforcement configuration when the file itself is executable
  policy rather than explanatory methodology;
- fixtures specifically testing TOML configuration; and
- ecosystem-owned TOML files such as `pyproject.toml` and generated `uv.lock`.

TOML is explicitly designed as a human-readable configuration format that maps
unambiguously to a hash table. That makes it a strong configuration carrier but
not a reason to encode every document, schema, record, or pointer in TOML.

TOML should not remain the default for:

- atomic claims;
- evergreen specifications;
- proof and analysis records;
- narrative plans;
- reference-pointer records;
- JSON Schemas; or
- generated interchange data.

Profiles that combine explanation with executable selection should separate
the concerns without duplicating truth: Markdown owns the profile definition
and rationale, while `dset_settings.toml` selects the profile by stable ID.
Only fields that deterministic code executes belong in TOML.

## JSON

JSON is a lightweight, language-independent data-interchange format. It is
widely supported and has strict portable syntax, but it has no comments and is
poor for narrative or frequently hand-edited project governance.

Use JSON when interoperability is more important than authoring comfort.

### Canonical JSON Schema documents

JSON Schemas should use canonical `*.schema.json` carriers. The JSON Schema
specification defines schemas as JSON documents and assigns the
`application/schema+json` media type.

Encoding the canonical schema as TOML and generating a JSON copy introduces:

- two representations;
- a conversion step;
- possible semantic drift;
- tooling friction; and
- an unnecessary distinction between source and distributed schema.

The recommended end state has one canonical JSON Schema that source tools,
installed methodology, editors, and external validators consume directly.
Schema explanations remain available through `description`, `$comment`, and
linked Markdown methodology.

### Ecosystem and host contracts

Use JSON when an ecosystem requires or conventionally consumes it, including:

- `package.json`;
- TypeScript/JavaScript tool manifests;
- VS Code and compatible extension manifests;
- Obsidian plugin manifests;
- language, grammar, snippet, and contribution-point declarations;
- SARIF and other standardized JSON reports; and
- host-owned settings or metadata whose contract names JSON.

NPM requires `package.json` to be actual JSON. VS Code extensions require a
root `package.json` manifest. These are external contracts, not DSET format
preferences.

### API and wire contracts

Use JSON for:

- HTTP request and response payloads;
- JSON-RPC and comparable protocols;
- API fixtures;
- externally exchanged review or audit packets;
- OpenAPI when the project selects `openapi.json` rather than YAML;
- machine-readable CLI output; and
- imports or exports whose consumer expects JSON.

The OpenAPI specification recommends `openapi.json` or `openapi.yaml`; DSET may
choose JSON when both are valid and no external contract selects YAML.

### Generated machine data

Use JSON for:

- bootstrap bundles;
- generated indexes intended for programs rather than human review;
- deterministic snapshots;
- runtime checkpoints exchanged between tools;
- test fixtures for JSON behavior; and
- caches or intermediate data when a persisted machine-readable carrier is
  justified.

Generated JSON is not semantic authority merely because it is committed. Its
authority and regeneration source remain explicit.

## JSON Lines and NDJSON

Use one JSON value per line for append-only operational streams:

- skill-run logs;
- tool execution logs;
- Evaluation run events;
- supportability traces;
- runtime audit events; and
- resumable local processing journals where the selected risk profile requires
  them.

These normally belong under `.dset_runtime` and are excluded from semantic
artifact discovery and Git. A promoted observation becomes a separate Evidence
Record rather than making the raw log authoritative.

JSON Lines supports independent record processing, streaming, concatenation,
and line-oriented diagnostics. Its media type is not standardized, so external
contracts must use the exact format and name their consumer expects.

## Native and externally prescribed formats

Carrier selection never overrides a binding external contract. Preserve:

- GitHub Actions YAML;
- implementation source languages;
- ecosystem manifests and lockfiles;
- CSV/XLSX outputs;
- OpenAPI, database DDL, or other interface formats selected by a Contract;
- binary artifacts; and
- host-native skill metadata.

DSET classifies and links these artifacts but does not re-encode them merely to
make the repository look uniform.

## Likely repository changes if adopted

### Strong migration candidates

- Convert all atomic Markdown carriers to YAML frontmatter.
- Give every evergreen or maintained Markdown artifact valid YAML
  frontmatter.
- Convert identity-only `.dset/**/references/*.toml` carriers to
  human-readable Markdown properties or remove them where a direct stable
  identity link is sufficient.
- Convert canonical `*.schema.toml` sources to `*.schema.json`.
- Remove generated duplicate schema authority after consumers use the one
  canonical JSON carrier.
- Convert narrative TOML plans and records to Markdown with frontmatter.

### TOML carriers likely to remain

- `.dset/dset_settings.toml`;
- the settings template;
- executable dependency and enforcement configuration;
- selected machine-consumed profile configuration where it cannot be expressed
  as a stable profile ID plus Markdown definition;
- TOML configuration fixtures; and
- external ecosystem TOML files.

### JSON carriers likely to remain

- JSON Schemas;
- bootstrap bundles;
- JavaScript/TypeScript and extension manifests;
- machine output and snapshots;
- API/wire fixtures; and
- externally prescribed JSON documents.

## Risks and required controls

### YAML parsing complexity

Markdown frontmatter is only safer when DSET defines and enforces a restricted
profile. Accepting arbitrary YAML would reintroduce ambiguous typing, complex
constructs, and cross-parser variance.

### Mixed human and machine truth

A Markdown body must not become a second structured-data authority beside its
frontmatter. Properties own identity and routing metadata; the body owns the
human-readable primary meaning. Type-specific methodology must define any
additional boundary.

### Generated-copy drift

When a native canonical format is already usable by every consumer, DSET should
not maintain a second source format merely to generate it. Generated adapters
are justified only by a real consumer boundary and must declare their source.

### Migration versus semantic mutation

Changing a carrier format or identity representation is not a semantic
modification when the complete artifact meaning, relations, provenance, and
content are preserved. Migration still requires collision checks,
reference closure, deterministic comparison, and Git return evidence.

### Existing authority conflict

`DSET-REQUIREMENT-GOV-056` currently requires TOML for all Python-owned DSET
structured carriers and schemas and restricts JSON to JavaScript/TypeScript or
external protocol use. The recommendation in this report conflicts with that
active Requirement.

Implementation must not begin from this report alone. Adoption requires a new
Requirement that explicitly replaces the all-TOML policy, followed by a
bounded migration plan.

## Recommended next decision

If the operator accepts this analysis, emit one Requirement with the carrier
policy:

> DSET uses Markdown with restricted YAML frontmatter for human-governed
> artifacts, TOML for human-edited executable configuration, JSON for native
> JSON standards and machine interoperability, JSONL for runtime streams, and
> externally prescribed native formats where contracts require them.

That Requirement should replace `DSET-REQUIREMENT-GOV-056`, specialize
`DSET-REQUIREMENT-GOV-095`, preserve
`DSET-CONSTRAINT-GOV-002`, and authorize a separate migration plan.

## Sources

- [GitHub: Using YAML frontmatter](https://docs.github.com/en/enterprise-cloud@latest/contributing/writing-for-github-docs/using-yaml-frontmatter)
- [TOML 1.0 specification](https://toml.io/en/v1.0.0)
- [RFC 8259: JSON](https://www.rfc-editor.org/info/rfc8259/)
- [JSON Schema Core 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
- [npm package.json documentation](https://docs.npmjs.com/files/package.json/)
- [VS Code extension manifest](https://code.visualstudio.com/api/references/extension-manifest)
- [OpenAPI specification](https://spec.openapis.org/oas/latest.html)
- [JSON Lines](https://jsonlines.org/)
