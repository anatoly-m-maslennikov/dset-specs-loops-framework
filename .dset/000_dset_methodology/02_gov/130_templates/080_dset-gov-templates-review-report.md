---
schema_version: "1.0"
artifact_type: evidence_record
artifact_subtype: review_report
artifact_id: APP-EVIDENCE-RECORD-001
packet_id: APP-REVIEW-PACKET-001
priority: medium
llm_session_ids: []
reviewed_commit: 0
method: Review method
observed_at: 2026-01-01T00:00:00Z
limitations: []
reviewer:
  identity: reviewer identity
  host: agent or human host
  model: available model or not-applicable
  tool_version: available tool version or not-applicable
reviewed_inputs:
  - carrier: APP-DECISION-001-example.md
    sha256: 0
findings:
  - id: APP-REVIEW-FINDING-001
    priority: medium
    evidence: Exact observation or evidence address
    confidence: medium
    impact: Consequence if the finding is correct
    proposed_disposition: route_problem
---

# External review report

The findings body is free-form. The envelope above remains mandatory and
machine-checkable.
