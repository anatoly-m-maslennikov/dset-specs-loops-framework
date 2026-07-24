---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-116
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-110"
      - "DSET-DECISION-GOV-014"
      - "DSET-DECISION-GOV-015"
      - "DSET-ANALYSIS-REPORT-004"
  - type: relates_to
    targets:
      - "DSET-CONSTRAINT-GOV-002"
---

# Requirement — Select carriers by their governed job

Every governed Markdown artifact starts with valid YAML frontmatter containing
its applicable non-derived properties. Frontmatter is non-empty, does not
duplicate narrative body content, and does not repeat semantic route
coordinates already determined by the registered artifact type.

DSET uses these default carrier boundaries:

| Carrier | Governed job |
|---|---|
| Markdown with YAML frontmatter | Human-governed atomic and maintained artifacts with narrative meaning |
| TOML | Human-edited configuration executed directly by tools |
| JSON | External contracts, standardized schemas, wire data, and generated machine data |
| NDJSON | Append-only journals and ordered record streams under `.dset_journal` |
| Native format | Source code, Tests, Evaluations, CI workflows, lockfiles, host manifests, and other prescribed implementation files |

Carrier selection follows the artifact's authoring and consumption boundary,
not its layer or implementation language. A binding standard, ecosystem, or
external obligation keeps its prescribed format and does not gain a parallel
writable representation.

Markdown frontmatter uses `---`. YAML is not a standalone DSET artifact format.
Embedded source examples are content rather than separate artifacts.

## Primary claim

DSET uses Markdown with YAML frontmatter for human-governed artifacts, TOML for
executable human configuration, JSON for standardized machine boundaries,
NDJSON for append-only journals, and native formats for implementation.

## Rationale

This complete successor carries forward the job-based carrier policy and
explicitly absorbs the retired TOML null-normalization, JSON-Schema boundary,
and carrier-analysis artifacts whose useful conclusions it contains.
