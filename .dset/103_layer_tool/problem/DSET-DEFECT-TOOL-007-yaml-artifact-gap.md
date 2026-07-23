+++
artifact_id = "DSET-ATOMIC-RECORD-076"
semantic_id = "DSET-DEFECT-TOOL-007"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
authority = "repository:self-host-review"
claim = "The current DSET tree still contains ten YAML artifact files and seventy-one Markdown YAML-frontmatter carriers contrary to the accepted all-TOML requirement."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The representation gap is present and countable now; it is not a future risk or an unresolved product choice."
promotion = {}

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-040"
+++

# Defect — DSET artifact carriers still use YAML

At acceptance time, `dset/` contains ten standalone `.yaml` artifact carriers
and seventy-one Markdown artifacts with YAML frontmatter. They must migrate to
TOML without changing their semantic records or losing historical editions.

Resolution requires the complete transition ledger, updated seals and
references, zero remaining DSET YAML artifact encodings, fresh generated views,
the complete deterministic suite, and a current Evidence Record.

This Problem atom is immutable. Resolution is an append-only lifecycle event
after the completion condition is proved.
