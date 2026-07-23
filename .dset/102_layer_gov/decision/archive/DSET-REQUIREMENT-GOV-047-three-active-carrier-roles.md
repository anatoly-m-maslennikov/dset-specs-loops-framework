+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-117"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-047"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Active DSET project truth uses only atomic artifacts, semantically compiled evergreen specifications or plans, and settings or README navigation carriers."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]
+++

# Requirement — Keep three active carrier roles

An active project-owned DSET file is exactly one of:

1. one immutable atomic artifact or lifecycle event;
2. one evergreen specification or plan semantically compiled from applicable
   atomic artifacts; or
3. project settings or README navigation.

Mechanically generated indexes, dashboards, caches, run state, and scratch are
runtime material and remain outside committed active truth. Historical legacy
and migration records may be retained in explicitly named root archives, but
they are not active framework or project authority.

## Rationale

This closes the carrier taxonomy, removes mutable aggregate ledgers as shadow
truth, and keeps each active file's role obvious from its location and content.
