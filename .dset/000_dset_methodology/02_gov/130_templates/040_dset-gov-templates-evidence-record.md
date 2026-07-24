---
schema_version: "1.0"
artifact_type: evidence_record
artifact_subtype: test_result
artifact_id: APP-EVIDENCE-RECORD-001
scope_path: []
priority: medium
llm_session_ids: []
context:
  - repository=owner/repository
  - environment=local
observed_at: 2026-01-01T00:00:00Z
evidence_location: path/to/evidence
polarity: inconclusive
reopen_when: The subject revision, method, setup, or applicable context changes.
subject:
  id: APP-TEST-PLAN-001
  revision: "0000000000000000000000000000000000000000"
  intended_use: Support one bounded Verification claim.
producer:
  identity: human-or-agent-identity
  performed_work: Describe the work actually performed, including deviations.
method:
  description: Describe the observation or execution method.
  setup: Describe the exact tools, versions, inputs, and setup.
relations:
  - type: evidence_for
    targets:
      - APP-TEST-PLAN-001
---

# Evidence Record

Record concise observed results and evidence addresses here. The frontmatter is
the mandatory machine-checkable envelope. Use `validity_window` instead of
`observed_at` only when the evidence genuinely covers an explicit interval.

For high-reliance evidence, add `independent_producer`, `rival_explanations`,
and `limitations`. These extensions never replace the bounded core fields.
Currentness is derived by comparing the immutable record with its subject,
method, context, validity window, and reopen trigger; never edit a status into
the Evidence Record.
