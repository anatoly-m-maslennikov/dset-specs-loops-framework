---
schema_version: "1.0"
artifact_type: plan
artifact_id: APP-PLAN-001
packet_id: APP-REVIEW-PACKET-001
repository: owner/repository
commit: 0000000000000000000000000000000000000000
scope: Bounded review scope
criteria:
  - One explicit review criterion
reviewed_inputs:
  -
    path: path/to/artifact
    sha256: 0000000000000000000000000000000000000000000000000000000000000000
resolved_rules:
  -
    id: APP-RULE-001
    path: dset/governance/rule.md
    sha256: 0000000000000000000000000000000000000000000000000000000000000000
allowed_effects:
  - read_only_report
---

# External review packet

Review only the exact commit, inputs, rules, scope, and criteria above. Return a
report; do not edit the project or authorize repair.
