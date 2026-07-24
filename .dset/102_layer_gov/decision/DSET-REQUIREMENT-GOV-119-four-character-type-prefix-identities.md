---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-GOV-119
scope_path: ["layer:gov"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-GOV-102"
      - "DSET-REQUIREMENT-GOV-113"
      - "DSET-REQUIREMENT-GOV-114"
      - "DSET-REQUIREMENT-GOV-118"
---

# Requirement — Use four-character Type prefixes in artifact identities

Every registered artifact Type has exactly one globally unique, immutable,
four-character uppercase identity prefix. The artifact catalog owns the
mapping. Frontmatter keeps the full semantic `artifact_type`; the short prefix
is an identity token and never replaces the semantic name.

The canonical filename grammar is:

```text
<PROJECT>-<SCOPE_PATH>-<TYPE_PREFIX>-<NNN>[-<SUBTYPE>]--<SUMMARY>.<ext>
```

Project-prefix and scope-path segments follow the project’s governed identity
settings. Omitted optional segments do not leave empty separators.

The stable artifact ID ends at `<NNN>`. A subtype segment is semantic filename
metadata but is not part of the stable ID. The `--` token unambiguously
separates identity metadata from the human-readable summary. Correcting a
summary does not change artifact identity.

Numbering is one monotonically increasing sequence per registered Type across
all of its subtypes. A Type that requires a subtype, including QA Case, must
include the canonical subtype segment in its filename. Other Types omit the
segment when no subtype applies.

## Canonical prefix registry

| Type | Prefix |
|---|---|
| Problem | `PROB` |
| External Problem | `XPRB` |
| Conflict | `CNFL` |
| Analysis Report | `ANRP` |
| External Analysis Report | `XARP` |
| Conflict Analysis | `CFAN` |
| Requirement | `REQU` |
| Constraint | `CNST` |
| Contract | `CNTR` |
| Technical Decision | `TDEC` |
| Implementation Methodology | `IMET` |
| Integration Decision | `IDEC` |
| QA Case | `QACS` |
| Assurance Standard | `AUST` |
| Review Protocol | `RVPR` |
| Git Commit | `GCOM` |
| External Git Commit | `XGCM` |
| Pull Request | `PULL` |
| Evidence Record | `EVRC` |
| External Evidence Record | `XEVR` |
| Verification Record | `VERC` |

## Examples

```text
DSET-GOV-REQU-001--github-compatible-artifacts.md
DSET-GOV-QACS-002-EVAL-CASE--relation-interpretability.md
DSET-TOOL-TDEC-001--use-project-local-resolver.md
DSET-TOOL-IDEC-001--connect-cli-to-governance.md
DSET-GOV-EVRC-001--structural-validation-result.md
```

The corresponding stable IDs are `DSET-GOV-REQU-001`,
`DSET-GOV-QACS-002`, `DSET-TOOL-TDEC-001`, `DSET-TOOL-IDEC-001`, and
`DSET-GOV-EVRC-001`.

## Migration boundary

Changing a registered prefix requires one governed, complete identity
migration across active and archived carriers, relations, plans, generated
views, implementations, and proofs. A project cannot accept two current
prefixes for the same Type.

## Rationale

Fixed-width prefixes make identities compact and mechanically parseable while
remaining recognizable in file lists and relation targets. Placing subtype
after the sequence preserves one Type-owned number line and keeps the stable
identity independent of optional filename detail.
