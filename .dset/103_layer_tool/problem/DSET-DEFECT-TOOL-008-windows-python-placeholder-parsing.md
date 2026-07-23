+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-092"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-TOOL-008"
status = "accepted"
priority = "high"
authority = "external:github-actions-run-29837254275"
claim = "Aggregate verification expands the Python executable placeholder before POSIX shell parsing, so a native-Windows executable path loses its backslashes and cannot be launched."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Executable identity must remain an argument value; converting a platform-native path back into shell text makes correctness depend on another platform's escaping rules."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-CONTRACT-TOOL-001"
+++

# Defect — Windows Python placeholder is parsed as POSIX shell text

GitHub Actions run `29837254275` reached the canonical verification-command
sequence on native Windows and then stopped with `DSET-E900: [WinError 2]`.
The verifier substituted `sys.executable` into a command string before calling
POSIX `shlex.split`. Backslashes in the native Windows path were interpreted as
escape characters, producing a nonexistent executable name.

This emitted Defect atom is immutable. Resolution requires tokenizing the
portable command template before substituting the executable argument, a
deterministic Windows-path regression Test, and fresh hosted proof.
