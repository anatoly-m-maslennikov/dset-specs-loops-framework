+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-096"
type = "decision"
semantic_id = "DSET-DECISION-OPS-011"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Repository roots and filesystem paths are compared by resolved identity, while relative Path values are serialized with POSIX separators before canonical-relative validation."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Resolution handles filesystem aliases and Windows short names; POSIX serialization keeps persisted repository paths platform-neutral without accepting noncanonical string input."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-TOOL-009"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Canonicalize filesystem identity at repository boundaries

DSET resolves a repository root before using it as path authority. Any
caller-supplied filesystem path compared with that root is resolved at the same
boundary, including future destinations through non-strict resolution.

A relative `Path` object is native filesystem input, so DSET serializes it with
`as_posix()` before enforcing canonical repository-relative syntax. A string is
already serialized input and must independently use canonical POSIX separators;
backslashes in strings remain invalid.

Public operations may return canonical paths rather than preserving an input
alias. Tests compare canonical identities when path spelling is not itself the
subject of the test.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
