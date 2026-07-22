+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-116"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-046"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "A DSET framework repository separates the distributable framework surface under .dset from the repository's recursive self-hosting project artifacts at the repository root."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]
+++

# Requirement — Separate framework and recursive project truth

`.dset/` contains only current, distributable DSET framework material plus the
single project settings carrier needed to select it. The DSET repository's own
atomic artifacts and evergreen project truth live in visible root scope and
use the framework exactly as another adopter would.

This separation prevents framework templates, schemas, and rules from being
confused with the Decisions, Problems, Questions, QA, evidence, specs, and
plans created while developing the framework itself.

## Rationale

DSET must prove recursive use without making its distributable framework files
and its self-hosting project records compete for the same paths or ownership.
