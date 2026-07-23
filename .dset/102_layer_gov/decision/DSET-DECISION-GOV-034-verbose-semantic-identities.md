+++
artifact_id = "DSET-ATOMIC-RECORD-205"
semantic_id = "DSET-DECISION-GOV-034"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET uses the canonical semantic ID kinds REQUIREMENT, CONSTRAINT, CONTRACT, IMPL, TEST-PLAN, and EVAL-PLAN; QA atoms are plans rather than executable checks, and adopting this vocabulary requires a complete historical identity migration without retained short aliases."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Verbose identity kinds are understandable from a file list, while Test Plan and Evaluation Plan preserve the boundary between a QA definition and its executable implementation or evidence. IMPL remains short to keep the implementation kind readable and distinct from the longer authority kinds."
promotion = {}

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-033"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-038"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-054"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-055"
+++

# Decision — Verbose semantic identities

The four semantic Types remain Decision, Question, Problem, and QA.

Decision uses the direct subtypes `requirement`, `constraint`, `contract`, and
`implementation_decision`. Their ID kinds are `REQUIREMENT`, `CONSTRAINT`,
`CONTRACT`, and `IMPL`. An empty-subtype Decision continues to use `DECISION`.

QA uses the required direct subtypes `test_plan` and `evaluation_plan`. Their
ID kinds are `TEST-PLAN` and `EVAL-PLAN`. A QA atom defines intended proof; Test
code and Evaluation prompts, datasets, fixtures, harnesses, and runners are
Implementation artifacts, while observed results are Evidence Records.

A naming-policy change is one complete governed migration. It updates current
and historical semantic IDs, carrier names, relations, lifecycle targets,
compiled documents, settings, implementation references, proof references,
and generated views together. The previous short tokens do not remain accepted
aliases after cutover. Numeric suffixes are preserved when the migrated
project-wide sequences do not collide.
