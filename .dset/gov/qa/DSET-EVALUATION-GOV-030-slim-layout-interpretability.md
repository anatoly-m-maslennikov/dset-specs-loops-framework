+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-103"
type = "qa"
subtype = "evaluation"
semantic_id = "DSET-EVALUATION-GOV-030"
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "A reviewer can identify project-wide, Version-wide, and layer-owned authority plus the sole configuration owner from the schema 1.3 tree without explanatory prose."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-041"
+++

# Evaluation — Interpret the slim project control layout

Give independent reviewers only the `dset/` tree and artifact filenames. Pass
when they consistently identify the sole settings/manifest carrier, distinguish
project-wide records from Version lifecycle artifacts, assign layer-owned truth
to the correct direct layer root, and do not infer a second manifest or generic
scope owner.

Record ambiguities rather than resolving them by majority vote. Any materially
different authority interpretation keeps this Evaluation inconclusive.

This Evaluation atom is immutable. Later correction requires a successor
Evaluation and append-only lifecycle event.
