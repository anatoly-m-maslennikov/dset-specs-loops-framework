---
artifact_type: "implementation_decision"
artifact_id: "DSET-DECISION-GOV-015"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "child_of"
    targets:
      - "DSET-REQUIREMENT-GOV-036"
---

# Decision — Keep JSON Schema at its standard boundary

Files whose primary contract is JSON Schema remain canonical JSON. They are an
externally prescribed interoperability boundary, like GitHub Actions or host
skill metadata, rather than ordinary DSET-owned structured artifacts.

The generic TOML migration must classify and retain these files, must not emit
an editable TOML duplicate, and must continue validating them as JSON Schema.
Any future DSET schema DSL and generated JSON adapter require separate accepted
authority, a lossless mapping, and a freshness gate before replacing this
boundary.

## Rationale

A private TOML encoding for mixed JSON values and JSON-Schema keywords would
be harder to read, less interoperable, and another schema language to maintain.
Keeping the standard carrier avoids dual authority while applying TOML to the
project artifacts where it materially improves authoring.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle evidence.

## Primary claim

Standards-compliant JSON Schema files are externally prescribed contract carriers and remain canonical JSON exceptions rather than generated copies of a private TOML schema dialect.
