+++
artifact_id = "DSET-ATOMIC-RECORD-123"
semantic_id = "DSET-REQUIREMENT-SKILL-014"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET provides a public dset-compile skill that semantically reconciles pending atomic artifacts into affected evergreen specifications and plans under repository-local governance."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-048"
+++

# Requirement — Provide semantic compilation as a skill

`dset-compile` resolves the target repository's local governance, finds atomic
artifacts beyond each affected evergreen frontier, synthesizes their current
consequences, updates only applicable specs/plans or shared references, and
reports unresolved conflicts instead of silently choosing.

The skill may be called explicitly or chained by implementation, verification,
or release entry criteria. It does not run automatically after every atom and
does not delegate semantic judgment to a deterministic concatenation command.

## Rationale

Compilation requires contextual interpretation and reconciliation. Keeping the
skill thin while repository governance owns the rules preserves one adaptable
source of truth across projects.
