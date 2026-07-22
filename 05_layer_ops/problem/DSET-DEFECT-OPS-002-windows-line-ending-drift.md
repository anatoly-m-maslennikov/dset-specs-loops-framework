+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-083"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-OPS-002"
status = "accepted"
priority = "critical"
authority = "external:github-actions-run-29799045908"
claim = "GitHub's native Windows checkout changes immutable DSET carrier bytes because the repository does not pin text line endings."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The Linux and macOS jobs reported only a stale derived trace, while the native Windows job also reported changed current-carrier digests across the migrated immutable corpus."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Defect — Windows checkout changes byte-sealed artifacts

GitHub Actions run `29799045908` checked the same pull-request merge commit on
Linux, macOS, and native Windows. Linux and macOS stopped on a stale generated
trace. Native Windows additionally reported `DSET-E168` for current-carrier
digests throughout the immutable TOML/Markdown migration corpus.

The repository has no `.gitattributes` policy. A Windows worktree may therefore
materialize tracked text with CRLF while carrier-transition authority seals LF
bytes. The validator correctly detects different bytes, but the checkout
boundary makes a valid immutable corpus appear mutated.

This emitted Defect atom is immutable. Resolution requires an explicit
repository text policy, a deterministic Test, and fresh hosted proof.
