---
artifact_type: "evaluation_plan"
artifact_id: "DSET-EVAL-PLAN-GOV-026"
scope_path:
  - "layer:gov"
priority: "medium"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "check_of"
    targets:
      - "DSET-DECISION-GOV-013"
---

# Evaluation Plan — Judge typed-relation clarity

Given representative project, feature, analysis, specification,
implementation, QA, evidence, Problem, Conflict, override, and replacement
cases, independent reviewers must select the same precise relation without
using `child_of` as generic causality or `relates_to` to avoid a known type.

They must distinguish scoped override from complete replacement, QA definition
from evidence, evergreen projection from implementation, and ordinary links
from traceability. At least 90% of representative cases must be classified
correctly, with no authority or lifecycle error.

This emitted Evaluation definition is immutable. Execution and evidence are
separate.

## Primary claim

Independent reviewers consistently select the narrowest correct relation and use relates_to only as a non-semantic fallback.
