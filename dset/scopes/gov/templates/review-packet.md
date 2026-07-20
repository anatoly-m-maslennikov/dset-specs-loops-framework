+++
schema_version = "1.0"
artifact_type = "plan"
artifact_id = "APP-PLAN-001"
packet_id = "APP-REVIEW-PACKET-001"
repository = "owner/repository"
commit = 0
scope = "Bounded review scope"
criteria = ["One explicit review criterion"]
allowed_effects = ["read_only_report"]

[[reviewed_inputs]]
path = "path/to/artifact"
sha256 = 0

[[resolved_rules]]
id = "APP-RULE-001"
path = "dset/governance/rule.md"
sha256 = 0
+++

# External review packet

Review only the exact commit, inputs, rules, scope, and criteria above. Return a
report; do not edit the project or authorize repair.
