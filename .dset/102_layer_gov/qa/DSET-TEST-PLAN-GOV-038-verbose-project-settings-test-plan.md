+++
artifact_id = "DSET-ATOMIC-RECORD-049"
semantic_id = "DSET-TEST-PLAN-GOV-038"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove the verbose settings filename, settings-manifest boundary, compatibility rules, selected behavior, bootstrap output, and immutable historical exceptions."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-037"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-PLAN-GOV-037"
+++

# Test Plan — Validate verbose project settings

Tests must prove that new and bootstrapped repositories emit
`dset_settings.toml` only; its defaults load without hidden fallback; each
registered value selects the documented behavior; invalid values fail with the
owning key; and the skill context exposes the selected strictness,
implementation mode, workspace default, and delegation budget profile.

The suite must also prove that a legacy root `dset.toml` remains readable,
that new writers never emit it, and that simultaneous legacy and canonical
files fail deterministically. Project manifests must no longer own Change
workspace or delegation budget selection, while continuing to own project
identity, topology, contracts, release, verification, and provenance facts.

Repository-wide reference checks must accept only deliberate immutable
historical references to the retired filename. Existing sealed atoms and
legacy Decision carriers must retain their recorded digests.

This emitted Test definition is immutable. Runs and evidence are separate.
