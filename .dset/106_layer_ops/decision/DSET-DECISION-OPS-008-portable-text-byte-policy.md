+++
artifact_id = "DSET-ATOMIC-RECORD-084"
semantic_id = "DSET-DECISION-OPS-008"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:ops"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The repository pins all Git-controlled text worktree content to LF so byte-sealed artifacts remain stable on Linux, macOS, native Windows, and WSL."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "DSET validates immutable carrier bytes, so the repository must own text materialization instead of inheriting host-specific Git defaults."
promotion = {}

[[relations]]
type = "resolution_of"
target = "DSET-DEFECT-OPS-002"

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Decision — Pin portable text bytes to LF

The repository root owns a `.gitattributes` rule of `* text=auto eol=lf`.
Git classifies text automatically and materializes it with LF on every declared
platform. Binary content remains binary and is not line-ending normalized.

The policy applies to source, documentation, governance, generated text, and
sealed migration carriers. It does not redefine semantic hashing or weaken
immutable-byte validation; it makes checkout bytes conform to the byte policy
against which the artifacts were sealed.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
