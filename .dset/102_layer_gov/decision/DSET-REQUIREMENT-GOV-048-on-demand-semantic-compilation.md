+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-119"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-048"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Semantic compilation of atomic artifacts into evergreen specifications and plans is demand-driven and need not run after every new atomic artifact."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]
+++

# Requirement — Compile evergreen truth on demand

New atomic artifacts may accumulate as pending compilation input. Compilation
runs when explicitly requested or when an implementation, verification, or
release entry gate needs current evergreen truth. It updates only affected
specifications and plans and records the atomic frontier it considered.

Deterministic tooling may inventory inputs, calculate pending frontiers, and
validate references. It must not claim semantic compilation by concatenating
or mechanically projecting source text.

## Rationale

Batching related atoms avoids noisy rewrites while preserving a clear gate
before downstream work relies on evergreen truth.
