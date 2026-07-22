+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-182"
type = "question"
semantic_id = "DSET-QUESTION-IMPL-001"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Does applying the latest decision mean refactoring every Python tool and test under .dset to the Local Python Tools profile, or reclassifying the Requirements and implementation Decisions that govern those Python files?"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The first interpretation changes ninety-seven Python carriers and their root sources; the second changes the authority model and traceability without necessarily editing Python implementation."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "relates_to"
target = "DSET-QUESTION-GOV-008"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-IMPL-001"
+++

# Question — Scope of applying the latest rule to Python

Choose one implementation boundary:

1. Refactor all Python tools and Tests installed under `.dset` so their root
   sources conform to the Local Python Tools profile, then explicitly
   synchronize the installed methodology.
2. Reclassify the authority governing those tools and Tests into observable
   Requirements and material implementation Decisions, without a blanket
   Python refactor.

The choices may both be required, but they are separate changes and should not
be silently combined.
