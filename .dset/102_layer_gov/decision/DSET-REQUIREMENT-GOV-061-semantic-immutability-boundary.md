+++
artifact_id = "DSET-ATOMIC-RECORD-208"
semantic_id = "DSET-REQUIREMENT-GOV-061"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET atomic immutability protects governed meaning rather than a particular identifier spelling or carrier representation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "An atom must survive canonical naming and carrier migrations without permitting a migration to disguise a changed claim, provenance fact, scope, relation meaning, or QA criterion."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-060"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-062"
+++

# Requirement — Semantic immutability boundary

The immutable part of an atomic artifact is its governed meaning:

- primary claim, question, problem statement, or proof intent;
- rationale and accepted authority or creation state;
- provenance facts and creation-session provenance;
- scope and applicability meaning;
- priority recorded at creation;
- relation types and the artifact identities they connect; and
- for QA, conditions, criteria, thresholds, and expected disposition.

An append-only event may derive later lifecycle state or effective priority. A
governed migration may recode an ID, classification-label spelling, filename,
path, heading label, carrier format, seal, or stored target spelling only when
the immutable meaning and connected artifact identities remain equal. Any
other change requires a successor atom.
