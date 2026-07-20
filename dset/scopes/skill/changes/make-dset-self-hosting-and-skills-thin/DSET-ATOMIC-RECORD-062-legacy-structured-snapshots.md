+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-062"
type = "decision"
semantic_id = "DSET-DECISION-GOV-017"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "A YAML carrier required by immutable historical links or selector-sealed authority remains byte-stable only as an exactly registered historical snapshot while its TOML sibling is the sole current owner."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Physical byte-stable snapshots preserve GitHub links and historical identity without making pointer stubs, symlinks, virtual resolution, or YAML fallback part of the current authority model."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-GOV-037"

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-TOOL-004"
+++

# Decision — Retain exact legacy structured snapshots

The artifact-classification registry owns one exact, no-wildcard
`legacy_structured` entry for every retained YAML snapshot. Each entry records
the old path, whole-file SHA-256, TOML `current_owner`, artifact type and
optional subtype, and the exact historical carrier IDs plus retention reason.

Readers use TOML only and never fall back to a registered snapshot. Validation
fails when a snapshot changes, its current owner is missing, a YAML/TOML pair
is unregistered, an entry is duplicated, a mutable carrier still links to the
old path, or new immutable evidence links to an unregistered legacy carrier.

Migration creates the TOML owner and registration transactionally, updates only
mutable references, preserves registered source bytes, and is a no-op on a
second run. Selector fragment seals and whole-carrier snapshot digests remain
separate checks with separate purposes.

This emitted Decision atom is immutable. Later correction requires a successor
and append-only lifecycle evidence.
