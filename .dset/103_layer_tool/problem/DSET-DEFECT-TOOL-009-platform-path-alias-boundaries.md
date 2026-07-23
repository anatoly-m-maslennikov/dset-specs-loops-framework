+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-095"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-TOOL-009"
status = "accepted"
priority = "high"
authority = "external:github-actions-run-29839085218"
claim = "Repository operations canonicalize roots without consistently canonicalizing related paths, and relative Path inputs are validated through host-native text, causing alias mismatches on macOS and Windows and separator rejection on Windows."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "macOS exposes the same temporary directory through /var and /private/var, while Windows may expose short and long path names; comparing mixed lexical and canonical identities or treating native Path rendering as portable syntax makes equivalent filesystem objects disagree."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Defect — Platform path aliases cross canonical boundaries

GitHub Actions run `29839085218` passed on Ubuntu but failed after completing
the full verifier on macOS and native Windows. macOS compared `/var` fixture
paths with their `/private/var` canonical identity. Windows compared short and
long user-directory names and rejected a relative `Path` after its native
backslash rendering entered the POSIX-relative syntax validator.

This emitted Defect atom is immutable. Resolution requires one canonical
filesystem-identity boundary, portable serialization for relative Path values,
alias regressions, and fresh hosted proof.
