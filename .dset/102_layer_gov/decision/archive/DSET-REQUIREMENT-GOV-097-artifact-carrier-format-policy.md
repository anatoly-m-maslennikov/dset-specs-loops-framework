---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-097
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: child_of
    targets:
      - "DSET-REQUIREMENT-GOV-095"
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-056"
  - type: relates_to
    targets:
      - "DSET-ANALYSIS-REPORT-004"
      - "DSET-CONSTRAINT-GOV-002"
---

# Requirement — Select artifact carriers by their actual job

DSET uses the following default carrier policy across every layer:

| Carrier | Best use |
|---|---|
| Markdown with YAML frontmatter | Human-governed artifacts with narrative meaning |
| TOML | Human-edited configuration executed directly by tools |
| JSON | External contracts, standardized schemas, wire data, and generated machine data |
| JSONL/NDJSON | Append-only runtime logs and event streams |
| Native format | Source code, CI workflows, lockfiles, host manifests, and other prescribed implementation files |

Markdown with restricted YAML frontmatter is the default carrier for atomic,
evergreen, and maintained artifacts whose primary meaning is reviewed by
humans. TOML is not DSET's generic structured-data format.

Carrier selection follows the artifact's consumer and job rather than its
layer, implementation language, or revision mode. A maintained specification,
executable configuration, source file, generated snapshot, and runtime log may
therefore use different carriers.

A binding external or ecosystem contract overrides the defaults and keeps its
prescribed native format. When a standard is itself JSON—such as JSON
Schema—its canonical carrier is JSON rather than a TOML encoding used to
generate JSON.

JSONL and NDJSON runtime streams normally live under `.dset_runtime`; a
promoted observation becomes a separate governed Evidence Record rather than
making the raw stream authoritative.

## Rationale

Format should optimize the artifact's real authoring and consumption boundary.
Markdown combines structured properties with readable meaning, TOML remains
strong for human-edited executable configuration, and JSON provides broad
machine interoperability. This division removes unnecessary format conversion
and competing representations without forcing implementation or external
contracts into one universal carrier.
