+++
artifact_id = "DSET-ATOMIC-RECORD-013"
semantic_id = "DSET-REQUIREMENT-TOOL-021"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:tool"]
status = "accepted"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Derive the TypeScript profile from a pinned pilot

DSET must provide an executable `typescript-v1-candidate` applied language
profile derived from a pinned revision of the owned `obsidian-your-harness`
pilot. It maps the six language-neutral gate categories to the pilot's actual
Node, TypeScript, ESLint, Jest, esbuild, package-lock, source, test, generated
output, and architectural boundaries without translating Python thresholds.

The profile must preserve hard failures as failures. Existing advisory
complexity, function-size, or ecosystem warnings may enter a revision-bound
machine-readable baseline that can only shrink; errors cannot enter that
baseline. The profile records source repository, exact revision, upstream
revision, license, observed tool versions and scripts, file populations,
threshold semantics, exclusions, and known blockers.

The framework may distribute and validate the candidate, but it must not call
it `typescript-v1` or active until the owned pilot passes the complete local
and required hosted proof. Product-specific names, provider behavior, vault
storage, and UI rules remain in the pilot's local governance and never become
language-profile defaults.

## Rationale

An evidence-derived candidate makes the profile useful immediately while its
status and blocker list prevent one project snapshot from masquerading as a
finished cross-project standard. This successor removes the invalid legacy
Decision lineage edge from `DSET-REQUIREMENT-TOOL-020`; the Decision remains a
compilation source, not an immediate lineage parent.

This emitted Requirement atom is immutable. Later correction, promotion, or
retirement requires a linked atom or append-only lifecycle event.
