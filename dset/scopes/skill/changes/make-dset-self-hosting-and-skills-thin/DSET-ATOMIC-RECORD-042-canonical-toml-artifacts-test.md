---
artifact_type: atomic_record
artifact_id: DSET-ATOMIC-RECORD-042
type: qa
subtype: test
semantic_id: DSET-TEST-GOV-037
status: accepted
priority: high
authority: "operator:anatoly-m-maslennikov"
claim: "Deterministic migration and validation prove canonical TOML artifact equivalence, reference closure, freshness, and external-format boundaries."
scope:
  kind: project
  id: dset-specs-loops-framework
promotion:
  parent_scope: null
relations:
  - type: check_of
    target: DSET-REQUIREMENT-GOV-036
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
---

# Test — Validate canonical TOML migration

The migration test must inventory every governed source, preview without
writing, preserve parsed values and stable IDs, reject collisions and
unsupported values, rewrite every owned reference, and produce a deterministic
old/new digest map. A second apply must be a no-op.

The migrated repository and a generated adopter must pass all validators,
schemas, compilation, traceability, health, bootstrap, release, archive,
runtime, and skill-distribution tests. The gate must reject writable DSET-owned
YAML/JSON authority while accepting only registered host/ecosystem/wire/runtime
exceptions and fresh generated compatibility adapters.

This emitted Test definition is immutable. Runs and evidence are separate.
