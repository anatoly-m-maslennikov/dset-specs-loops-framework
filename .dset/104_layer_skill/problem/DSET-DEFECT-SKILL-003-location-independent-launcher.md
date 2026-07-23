+++
artifact_id = "DSET-ATOMIC-RECORD-066"
semantic_id = "DSET-DEFECT-SKILL-003"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:skill"]
status = "accepted"
priority = "high"
authority = "external:skill-refactor-audit"
claim = "Installed DSET instructions rewrite only selected commands, leaving bare global dset invocations and Windows cmd.exe quoting that break location-independent host execution."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The shared runtime contract is not portable when later workflow commands depend on ambient PATH or a shell dialect different from the active host."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-SKILL-011"
+++

# Defect — Installed commands are not fully location-independent

Rendered wrappers and resolved governance can still instruct `dset init`,
`dset runtime child`, `dset runtime closure`, or `dset rules check` through an
ambient executable. Windows rendering also emits `cmd.exe` syntax that is not a
shell-neutral PowerShell-host invocation.

This emitted Problem atom is immutable. Resolution requires implementation,
proof, and an append-only lifecycle event.
