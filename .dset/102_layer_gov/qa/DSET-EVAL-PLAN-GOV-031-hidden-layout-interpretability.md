+++
artifact_id = "DSET-ATOMIC-RECORD-106"
semantic_id = "DSET-EVAL-PLAN-GOV-031"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "medium"
authority = "operator:anatoly-m-maslennikov"
claim = "A reviewer can identify DSET as a distinct project control plane, find its sole configuration owner, and distinguish repository-root-relative stored paths from file-relative Markdown links."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-042"

[[relations]]
type = "replacement_of"
target = "DSET-EVAL-PLAN-GOV-030"
+++

# Evaluation Plan — Interpret the hidden project control layout

Give independent reviewers a repository tree that includes hidden entries and
the DSET artifact filenames. Pass when they consistently:

- recognize `.dset/` as the project control plane rather than product content;
- identify `.dset/dset_settings.toml` as the sole settings/manifest carrier;
- distinguish project-wide records, Version lifecycle artifacts, and direct
  layer-owned truth;
- interpret stored `.dset/...` paths from the repository root;
- allow file-relative Markdown links without treating them as stored control
  paths; and
- identify `.dset/runtime/` as replaceable operational state rather than
  authority.

Record ambiguities rather than resolving them by majority vote. Any materially
different authority or path-base interpretation keeps this Evaluation
inconclusive.

This Evaluation atom is immutable. Later correction requires a successor
Evaluation and append-only lifecycle event.
