+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-060"
type = "decision"
semantic_id = "DSET-DECISION-GOV-016"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "A selector-sealed legacy package YAML remains immutable historical authority for its registered fragments while one native package TOML succeeds it as the current editable package registry."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Whole-file conversion would mutate sealed history, while freezing the shared carrier without a successor would prevent current package registration."

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

# Decision — Cut over shared package registries through native successors

When a package YAML contains selector-sealed legacy Decision fragments, DSET
must preserve that YAML byte-for-byte as a historical compatibility carrier.
The migration emits one sibling `package.toml` as the current editable package
registry, initializes it from the preserved semantic values, and reconciles it
with active native atoms and current evergreen artifact paths.

After cutover, readers prefer `package.toml`; YAML remains finite read-only
legacy input only for the fragments whose digests are registered in the legacy
authority ledger. New package IDs and paths are written only to TOML. The two
files are not competing writable owners: TOML owns current registry state and
YAML owns immutable historical fragments.

Migration readiness binds both the preserved legacy digest and the exact
native successor output. Missing, changed, ambiguous, or competing successors
stop before cutover.

## Rationale

This preserves the identity and evidence of legacy claims while giving current
package truth a format-compliant owner that can evolve.

This emitted Decision atom is immutable. Later correction requires a successor
and append-only lifecycle evidence.
