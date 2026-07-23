+++
artifact_id = "DSET-ATOMIC-RECORD-053"
semantic_id = "DSET-REQUIREMENT-SKILL-013"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Each project selects lazy or strict dset-implement preparation through workflows.implement.mode in dset_settings.toml, with lazy as the default."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The workflow behavior remains accepted, but its source must reference the canonical settings filename and key."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-037"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-SKILL-012"
+++

# Requirement — Select implementation preparation in canonical settings

Root `dset_settings.toml` selects `lazy` or `strict` through
`workflows.implement.mode`; the default is `lazy`.

Lazy mode reconciles accepted session intent into missing atoms, completes
separate Test and applicable Evaluation definitions or plans, completes the
implementation plan when required, and then implements. It never invents
acceptance or silently resolves material ambiguity.

Strict mode performs implementation only from already sufficient accepted
inputs. It does not create, repair, or compile missing authority, QA, or plans;
missing or ambiguous inputs produce an exact stop.

Both modes resolve repository-local governance, preserve run/session and
commit provenance, obey authorization, and stop before claiming Verification
or release readiness.

## Rationale

This successor preserves the two-mode workflow while correcting the active
settings carrier reference.

This emitted Requirement atom is immutable. Later correction requires a
successor and append-only lifecycle evidence.
