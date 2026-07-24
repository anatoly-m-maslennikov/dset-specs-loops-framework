+++
artifact_id = "DSET-ATOMIC-RECORD-098"
semantic_id = "DSET-DEFECT-TOOL-010"
revision_mode = "atomic"
content_role = "observation"
governance_origin = "external"
relation_shape = "standalone"
scope_path = ["layer:tool"]
status = "accepted"
priority = "high"
authority = "external:github-actions-run-29844770302"
claim = "Byte-sensitive temporary Git fixtures inherit host newline and autocrlf policy, so native Windows can compare CRLF working bytes with normalized LF Git blobs and produce platform-dependent assurance failures."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The repository pins LF, but independently initialized temporary repositories do not inherit its tracked attributes; byte-identity tests therefore need an explicit local fixture policy."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Defect — Windows fixtures inherit ambient byte policy

GitHub Actions run `29844770302` passed on Ubuntu and macOS and completed the
full verifier on native Windows. The remaining failures were concentrated in
byte-sealed carrier-transition fixtures: text written with host newline rules
was staged by temporary repositories using ambient Git autocrlf behavior, so
recorded working bytes and source Git blobs disagreed.

This emitted Defect atom is immutable. Resolution requires explicit byte policy
for every temporary Git repository, exact fixture writes where bytes are the
assertion, deterministic regressions, and fresh hosted proof.
