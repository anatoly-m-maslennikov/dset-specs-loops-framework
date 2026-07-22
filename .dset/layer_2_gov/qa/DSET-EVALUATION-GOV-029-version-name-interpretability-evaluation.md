+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-080"
type = "qa"
subtype = "evaluation"
semantic_id = "DSET-EVALUATION-GOV-029"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "Independent reviewers can correctly interpret Version and assign all six release-lifecycle artifacts without needing an additional explanation of the primary Type name."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "layer"
id = "gov"

[promotion]
affected_children = ["gov", "ops"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-019"

[[relations]]
type = "check_of"
target = "DSET-DECISION-OPS-007"
+++

# Evaluation — Interpret the Version artifact Type

Give independent reviewers the current artifact catalog, filenames, and short
artifact examples without explaining the former name. Pass only when every
reviewer identifies Version as the release-lifecycle Type; assigns Roadmap,
Version Scope, Change, Release Plan, Readiness Record, and Release Record as
flat direct subtypes; preserves their distinct roles; and does not confuse the
Type with product-version strings, source-control versions, deployment state,
or semantic Decision Types.

Record ambiguity and rival interpretations. A majority vote does not conceal
one materially different classification; reconcile it or keep the Evaluation
inconclusive.

This emitted Evaluation atom is immutable. Later correction requires a
successor Evaluation and append-only lifecycle event.
