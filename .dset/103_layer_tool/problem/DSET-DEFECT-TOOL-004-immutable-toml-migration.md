+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-055"
type = "problem"
subtype = "defect"
semantic_id = "DSET-DEFECT-TOOL-004"
status = "accepted"
priority = "high"
authority = "repository:self-host-review"
claim = "The TOML migration plans writes to byte-stable sealed atoms, promoted proof, and registered legacy Decision carriers."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A representation migration cannot prove self-application by rewriting the immutable history that authorizes and evidences it."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "relates_to"
target = "DSET-REQUIREMENT-GOV-037"
+++

# Defect — TOML migration rewrites immutable history

The current migration planner treats all DSET Markdown YAML frontmatter as
mutable. Its preview therefore includes sealed atomic carriers, promoted proof
records, and registered legacy Decision carriers, and reconciliation attempts
to legitimize the mutation by rebasing digests.

## Completion condition

Immutable carriers are explicitly classified, excluded byte-for-byte from
conversion and reference rewriting, and covered by pre/post digest tests. Seal
rebasing is removed. Only mutable DSET-owned authority and projections are
eligible for the format cutover.
