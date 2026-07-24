---
artifact_type: requirement
artifact_id: DSET-REQUIREMENT-META-061
scope_path: ["layer:meta"]
priority: high
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-REQUIREMENT-META-047"
  - type: relates_to
    targets:
      - "DSET-REQUIREMENT-META-023"
      - "DSET-REQUIREMENT-META-041"
      - "DSET-REQUIREMENT-META-049"
      - "DSET-REQUIREMENT-META-060"
---

# Requirement — Use seven content roles and a downstream QA layer

DSET classifies artifact meaning through seven Content roles:

1. Problem;
2. Analysis;
3. Definition;
4. Method;
5. Assurance;
6. Implementation; and
7. Observation.

Governance locus remains an independent axis with exactly three values:
`internal`, `external`, and `relation`. Revision mode remains an independent
axis with exactly three values: `atomic`, `append_only`, and `maintained`.
`scope_path` remains structural and is not a semantic axis.

The canonical role-and-locus naming model is:

| Content role | Internal | External | Relation |
|---|---|---|---|
| Problem | Problem | External Problem | Conflict |
| Analysis | Analysis Report | External Analysis Report | Conflict Analysis |
| Definition | Requirement | Constraint | Contract |
| Method | Technical Decision | Implementation Methodology | Integration Decision |
| Assurance | QA Case | Assurance Standard | Review Protocol |
| Implementation | Git Commit | External Git Commit | Pull Request |
| Observation | Evidence Record | External Evidence Record | Verification Record |

Every concrete artifact classification resolves through its full
Revision-mode, Content-role, and Governance-locus route. Authority,
provenance, priority, lifecycle, and `scope_path` remain separate metadata.

The ordered framework layers become:

```text
META → GOV → TOOL → SKILL → IMPL → QA → OPS
```

QA owns Test and Eval definitions, maintained QA planning surfaces, executable
checks, evaluation prompts and rubrics, result reconciliation, QA evidence,
and verification. QA derives checks from authoritative Definitions and
observes Implementations; it does not establish product behavior. A failed or
inconclusive check produces new feedback for a later cycle rather than a
backward QA-to-IMPL authority edge.

## Rationale

Separating Assurance from Method prevents Technical Decisions and QA
definitions from sharing one semantic route. A downstream QA layer also keeps
post-implementation assurance distinct from implementation construction while
preserving forward-only layer authority.
