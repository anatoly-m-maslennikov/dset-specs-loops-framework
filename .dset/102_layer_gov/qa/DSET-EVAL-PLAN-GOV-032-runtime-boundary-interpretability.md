+++
artifact_id = "DSET-ATOMIC-RECORD-109"
semantic_id = "DSET-EVAL-PLAN-GOV-032"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "A reviewer can distinguish committed DSET control truth, ignored resumable runtime state, and disposable process scratch from the repository tree and governing text."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-043"

[[relations]]
type = "replacement_of"
target = "DSET-EVAL-PLAN-GOV-031"
+++

# Evaluation Plan — Interpret the three state boundaries

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
