---
artifact_type: "evidence_record"
artifact_subtype: "test_result"
artifact_id: "DSET-EVIDENCE-RECORD-024"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "evidence_for"
    targets:
      - "DSET-TEST-PLAN-GOV-036"
  - type: "relates_to"
    targets:
      - "DSET-DEFECT-TOOL-002"
      - "DSET-EVIDENCE-RECORD-023"
---

# Test result — Legacy relation sealing boundary

**LLM session IDs:**

- `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

Corrective implementation commit
`23fe405a9c705b323ffcf2fb8d82d7151c27cfb5` for
`DSET-DECISION-GOV-013`, resolved Problem `DSET-DEFECT-TOOL-002`, and
deterministic Test `DSET-TEST-PLAN-GOV-036`.

This record replaces the current deterministic conclusion drawn from Evidence
Record 023 without editing that historical observation. It does not satisfy
qualitative Evaluation `DSET-EVAL-PLAN-GOV-026`, hosted CI, release
readiness, or publication.

## Observed result

The sealing command rejects every newly authored atom that contains top-level
legacy `child_of` metadata and directs authors to canonical `relations`.
Repository validation still reads all already sealed legacy atoms as
compatibility `child_of` edges, so the admission restriction does not rewrite
or invalidate immutable history.

The first complete run after the corrective commit failed only because the new
commit-derived `implementation_of` edge made generated health and traceability
stale. Their explicit refresh restored the repository fixed point. The second
complete sequential run passed.

## Commands and results

```text
python -m unittest discover -s tests -q
  239 tests passed

ruff check .
  passed

mypy
  passed with strict configuration

python -m dset_toolchain check .
  DSET validation passed

git diff --check
  passed
```

Focused relation, atom, compilation, traceability, health, and bootstrap gates
also passed before the implementation commit. The complete suite and DSET
validation were run sequentially because self-host fixtures temporarily create
adopter repositories near the workspace.

## Reopen conditions

Reopen this evidence when relation vocabulary or meaning, legacy relation
compatibility, atom admission, projection ranges, commit provenance, relation
validation, generated traceability/health, or either cited implementation
commit changes.
