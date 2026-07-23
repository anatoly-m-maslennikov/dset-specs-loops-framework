+++
artifact_id = "DSET-ATOMIC-RECORD-086"
semantic_id = "DSET-DEFECT-GOV-007"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "repository:dset-verify"
claim = "A commit containing only generated derived views becomes a new commit-trailer relation input, making the committed views stale again and preventing a clean fixed point."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The derived relation index currently scans every provenance-bearing commit, including commits whose only changed paths are the outputs generated from that same index."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-024"
+++

# Defect — Generated refresh commits self-reference

After a substantive implementation commit, DSET can refresh traceability and
health successfully. Committing those generated files adds another
`implementation_of` relation because commit trailers are scanned without
considering changed paths. That relation changes the generated inventory, so a
clean checkout immediately reports stale health and traceability again.

The fixed point is therefore impossible even though the generated-only commit
does not change project truth or implementation coverage.

This emitted Defect atom is immutable. Resolution requires a Decision, Test,
implementation, and proof.
