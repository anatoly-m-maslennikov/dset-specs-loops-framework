+++
artifact_id = "DSET-ATOMIC-RECORD-168"
semantic_id = "DSET-DECISION-IMPL-001"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "IMPL is the development-realization layer between SKILL and OPS, and it contains any number of peer selectable implementation-profile features rather than nested layers."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Profiles vary orthogonally by language, runtime, deployment shape, and host; peer features with explicit work-area selection preserve one layer order without premature shared abstractions."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-031"
+++

# Decision — Model IMPL as selectable profile features

The canonical ordered flow is:

`META → GOV → TOOL → SKILL → IMPL → OPS`

IMPL owns development environment setup, dependencies, production code,
automated Test code, Evaluation implementations, and code-focused gates. It
does not redefine TOOL behavior or own post-implementation OPS state.

An Implementation Profile is a peer feature within IMPL. A project may select
more than one compatible profile and assigns every selection to explicit work
areas. Selection makes the profile authoritative; Test, Evaluation, evidence,
and Verification artifacts report conformance separately.

The first feature is `local-python-tools-v1`. Future peers may cover long-running
Python tools, containerized Python applications, Electron/TypeScript
applications, and host-specific plugins. A host-specific profile may extend a
broader profile without copying it, but profiles do not create layers inside
IMPL. Reusable components may be factored out only after concrete profiles
demonstrate a stable shared contract.

This emitted Decision is immutable. Later ordering, ownership, or composition
changes require a linked successor artifact.
