---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-095
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-GOV-093"
---

# Requirement — Give every Markdown artifact frontmatter

Every governed artifact whose carrier is a Markdown file starts with valid YAML
frontmatter. This requirement applies to atomic, evergreen, and maintained
artifacts and to internal, external, and relational governance loci.

The frontmatter contains the artifact's applicable non-derived properties.
It must not be empty, duplicate body content, or repeat route coordinates that
the registered artifact type already determines.

Markdown frontmatter begins and ends with `---`. Standalone DSET-owned
structured artifacts use TOML unless an external contract requires another
format. YAML is not a standalone DSET artifact format.

Source material embedded inside a Markdown artifact, such as a fenced example,
is content rather than a separate artifact and does not require its own
frontmatter.

## Rationale

Mandatory frontmatter gives every Markdown artifact a uniform machine-readable
identity and governance surface while preserving GitHub-native rendering. The
rule applies to artifact carriers rather than all Markdown-like text, avoiding
empty or ceremonial metadata blocks.
