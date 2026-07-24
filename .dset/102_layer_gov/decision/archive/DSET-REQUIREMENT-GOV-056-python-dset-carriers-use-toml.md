---
artifact_type: "requirement"
artifact_id: "DSET-REQUIREMENT-GOV-056"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-040"
  - type: "override_of"
    targets:
      - "DSET-DECISION-GOV-015"
  - type: "replacement_of"
    targets:
      - "DSET-CONSTRAINT-GOV-001"
---

# Requirement — Python-owned DSET carriers use TOML

All DSET-owned structured artifacts, settings, generated structured state,
portable bundle data, and schema definitions in this Python framework use
TOML. Python code reads and writes those carriers through the TOML boundary.

YAML is permitted only for externally prescribed host files whose consumers
require YAML, including GitHub Actions workflows and Codex skill metadata.
JSON is permitted only inside a genuinely JavaScript or TypeScript-owned work
area, or as transient command output where an external protocol requires it;
it is not a repository artifact format for this Python project.

This Requirement overrides the former project Decision that kept JSON Schema
files as a canonical exception and replaces the misclassified Constraint. The
semantic validation contracts remain, but their project-owned carriers move
to TOML.

## Primary claim

The Python-owned DSET framework uses TOML for every DSET-owned structured carrier and schema; YAML remains only where an external host contract mandates YAML, and JSON remains only in genuinely JavaScript or TypeScript-owned areas.

## Rationale

This is a required project result selected by the operator, not an externally imposed limitation, so Requirement is the correct direct Decision subtype.
