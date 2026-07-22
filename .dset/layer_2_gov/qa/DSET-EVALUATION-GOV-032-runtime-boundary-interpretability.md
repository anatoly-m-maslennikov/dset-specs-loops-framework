+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-109"
type = "qa"
subtype = "evaluation"
semantic_id = "DSET-EVALUATION-GOV-032"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "A reviewer can distinguish committed DSET control truth, ignored resumable runtime state, and disposable process scratch from the repository tree and governing text."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-043"

[[relations]]
type = "replacement_of"
target = "DSET-EVALUATION-GOV-031"
+++

# Evaluation — Interpret the three state boundaries

Give independent reviewers a repository tree including hidden entries and the
governing description. Pass when they consistently identify:

- `.dset/` as committed project control truth;
- `.dset_runtime/` as ignored but resumable project-local operational state;
- `/tmp` on POSIX, or the native Windows temporary root, as disposable process
  scratch; and
- same-directory atomic swap state as a bounded publication mechanism rather
  than durable runtime or governance.

Record ambiguity instead of resolving it by majority vote. This Evaluation
atom is immutable; later correction requires a successor Evaluation and an
append-only lifecycle event.
