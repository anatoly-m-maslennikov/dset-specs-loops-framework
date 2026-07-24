+++
artifact_id = "DSET-ATOMIC-RECORD-256"
semantic_id = "DSET-REQUIREMENT-META-023"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET uses the ordered layers META, GOV, TOOL, SKILL, IMPL, and OPS, with one canonical non-overlapping responsibility assigned to each layer."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Stable layer definitions make ownership and dependency direction understandable without relying on directory names or current implementation details."

[promotion]
affected_children = ["governance", "tool", "skill", "implementation", "operations"]
applies_unchanged = true
local_context_required = false

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-031"

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-META-022"
+++

# Requirement — Define the canonical layers

DSET uses the ordered flow `META → GOV → TOOL → SKILL → IMPL → OPS`.

| Layer | Canonical responsibility |
|---|---|
| META | Meanings, routing axes, universal invariants, layer topology, and inter-layer semantics |
| GOV | Governed carriers, identity, settings, provenance, lifecycle, applicability, scope, and conflict governance |
| TOOL | Executable DSET capabilities, validation, resolution, diagnostics, generation, and repository mechanics |
| SKILL | Thin provider-neutral orchestration, entry gates, workflow chaining, and session continuity |
| IMPL | Development environments, implementation profiles, code, automated Test implementations, Evaluation implementations, and code-quality gates |
| OPS | Post-implementation delivery, release, publication, runtime supportability, investigation, containment, recovery, and hosted evidence |

Each responsibility has one canonical owner. Later layers may realize or refine
earlier truth but cannot redefine an earlier layer's responsibility.
