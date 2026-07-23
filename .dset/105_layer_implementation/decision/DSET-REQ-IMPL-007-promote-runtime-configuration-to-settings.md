+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-198"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQ-IMPL-007"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every Implementation Profile defines explicit heuristics for keeping invariants as code constants and promoting operator-controlled or environment-varying values to a typed settings carrier."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A settings file is useful only when it separates runtime policy from code invariants; moving every literal out of code creates indirection, while leaving deployment and operator controls in code forces unnecessary edits and releases."

[scope]
kind = "layer"
id = "implementation"

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-IMPL-003"
+++

# Requirement — Promote runtime configuration deliberately

Each Implementation Profile distinguishes code invariants from runtime
configuration and publishes the distinction as inspectable rules.

Keep a value in code when it is valid for every supported environment, changes
only with the implementation, expresses an algorithm, schema, protocol, or
safety invariant, and is not a supported operator control.

Move a value to the profile's settings carrier when any of these are true:

- operators must change it without editing or releasing code;
- it varies by host, workspace, deployment, or external integration;
- multiple entrypoints or modules consume it as one coherent runtime policy;
- it is a path, endpoint, resource limit, timeout, retry policy, logging level,
  feature switch, or similar operational control expected to vary;
- it needs typed validation, compatibility handling, documented precedence, or
  an auditable override boundary.

Do not create a settings file merely to collect literals or internal constants.
Test variation alone does not require external settings when dependency
injection, function parameters, or fixtures express the variation more clearly.
When a settings carrier exists, it is typed, rejects unknown fields by default,
documents defaults and units, and is loaded once at the declared boundary.
Secrets are never settings values.
