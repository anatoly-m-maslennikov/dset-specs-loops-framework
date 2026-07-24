---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-093
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets: ["DSET-REQUIREMENT-GOV-040"]
---

# Requirement — Use YAML frontmatter for Markdown

DSET-owned Markdown artifacts use YAML frontmatter. Standalone DSET-owned
structured artifacts use TOML unless an external contract requires another
format.

Markdown frontmatter begins and ends with `---`. TOML files remain ordinary
valid TOML files and do not contain Markdown frontmatter. YAML is not a
standalone DSET artifact format.

Externally prescribed formats—including GitHub Actions workflows, ecosystem
manifests, wire formats, and standards-compliant schemas—retain their required
encoding.

## Rationale

YAML frontmatter is the established Markdown metadata convention and works with
GitHub's Markdown and GitHub Pages tooling. TOML remains the more readable
format for standalone DSET settings and structured records.
