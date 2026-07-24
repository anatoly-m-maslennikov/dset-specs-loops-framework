+++
artifact_id = "DSET-ATOMIC-RECORD-184"
semantic_id = "DSET-REQUIREMENT-IMPL-004"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every Python tool, library module, runner, and Test distributed inside .dset conforms to the selected Local Python Tools profile through its authoritative root source and explicit installed-methodology synchronization."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The framework must satisfy its own implementation profile recursively; limiting conformance to examples or future adopters would leave the executable methodology outside its own rules."

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[promotion.parent_scope]
kind = "project"
id = "dset-specs-loops-framework"

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-IMPL-001"

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-IMPL-001"
+++

# Requirement — Apply the Local Python Tools profile recursively

All Python carriers distributed below `.dset` must derive from authoritative
repository-root sources that satisfy the Local Python Tools profile. This
includes the CLI package, executable launchers, shared Test helpers, Test
modules, and any future Python support module included by methodology sync.

Refactoring happens in the root source first. The installed copy changes only
through the explicit synchronization authorized by this Requirement. Generated
or synchronized copies never become independent code owners.
