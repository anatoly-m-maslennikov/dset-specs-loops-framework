+++
artifact_id = "DSET-ATOMIC-RECORD-072"
semantic_id = "DSET-TEST-PLAN-GOV-042"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove that atomic identity and semantic payload remain immutable across an authorized carrier transition and that unregistered or lossy carrier mutation fails closed."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The carrier exception can be removed safely only when the repository proves semantic equivalence and complete transactional resealing rather than merely deleting YAML paths."
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-DECISION-GOV-018"
+++

# Test Plan — Preserve semantic immutability across carrier transitions

The semantic-atom, authority-ledger, and carrier-transition suites must prove:

- every old carrier digest and new carrier digest is present exactly once in
  `dset/scopes/gov/migrations/carrier-transitions.toml`;
- normalized semantic digests match after null reconstruction;
- stable IDs, claims, provenance, relations, body content, and lifecycle state
  remain unchanged;
- original atom and selector seals remain recorded with a source Git blob
  return address while current-carrier fields follow the validated transition;
- direct seal mutation, missing mapping, undeclared loss, semantic drift,
  transition-chain tampering, or a representation change without explicit
  operator authority fails closed; and
- append-only lifecycle, replacement, absorption, retirement, priority, and
  conflict behavior is unchanged by carrier movement.

This Test definition is immutable; runs and Evidence Records are separate.
