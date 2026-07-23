+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-201"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-IMPL-009"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Scripts store only stable environment-variable key names and resolve every runtime login, email, API key, password, or other secret value from those keys at the runtime boundary."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Key-based runtime lookup keeps mutable identities and credentials out of source and DSET while giving local .env files, CI injection, and production secret stores one stable application interface."

[scope]
kind = "layer"
id = "implementation"

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-IMPL-008"
+++

# Requirement — Resolve runtime identities and secrets by key

When a script uses a login, email address, account identifier, API key,
password, token, or other secret, its source and DSET artifacts contain only a
stable environment-variable key name such as `SERVICE_LOGIN`, `SERVICE_EMAIL`,
or `SERVICE_API_KEY`. The script resolves and validates the associated value at
its outer runtime boundary and injects it into the smallest consumer scope.

For local development, an ignored `.env` supplies the values. CI, production,
and other managed hosts may inject values for the same keys through their
environment or secret facility without creating a `.env` file. Key names,
field descriptions, and dummy examples are safe metadata; resolved values are
never emitted to help text, diagnostics, logs, prompts, evidence, or errors.
