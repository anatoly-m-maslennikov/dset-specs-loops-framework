---
artifact_type: "problem"
artifact_subtype: "gap"
artifact_id: "DSET-GAP-GOV-003"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-CONSTRAINT-GOV-001"
---

# Gap — Live YAML and JSON remain in Python-owned DSET carriers

The active toolchain still exposes YAML parsing through `yaml_subset`, accepts
legacy YAML paths in production discovery and validation, distributes schema
contracts as JSON, and packages bootstrap content as JSON.

Resolution requires migrating those current carriers and callers to TOML,
retiring the live YAML parser, converting the bootstrap bundle, and retaining
only externally mandated YAML files. Migration fixtures may contain YAML or
JSON text as inert test input, but current project truth and runtime state may
not use them.

## Primary claim

The current Python-owned DSET implementation still ships a live YAML compatibility parser, JSON schema carriers, and a JSON bootstrap bundle despite the TOML-only project constraint.

## Rationale

The repository cannot claim a TOML-only Python artifact boundary while production code and distributed resources continue to depend on YAML and JSON carriers.
