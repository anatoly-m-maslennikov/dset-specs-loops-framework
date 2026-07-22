+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-164"
type = "decision"
subtype = "none"
semantic_id = "DSET-DECISION-GOV-029"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Repository and third-party legal files live in the repository-root LICENSES distribution surface rather than .dset; provenance stores only each globally unique legal carrier name, and legal validation resolves that name exclusively within LICENSES without widening DSET artifact or skill discovery beyond .dset."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Licenses govern repository distribution, while .dset governs current project development state. Keeping legal carriers outside the control plane preserves that boundary and gives standard repository readers a predictable location."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-028"
+++

# Decision — Keep legal files outside the control plane

The repository license remains the root `LICENSE` carrier. Retained third-party
licenses and no-license notices live in the root `LICENSES` directory.

These legal carriers are distribution inputs, not DSET methodology, applied
artifacts, settings, runtime state, or historical DSET data. They therefore do
not live inside `.dset` and are not visible to skill discovery or semantic
compilation.

Source provenance stores each legal carrier's globally unique filename.
Provenance validation resolves that filename only within `LICENSES`; it does
not perform a repository-wide search or treat the legal file as DSET authority.

## Rationale

Legal notices must ship with the repository but answer a different governance
question from project-local DSET truth. A separate conventional distribution
surface keeps both responsibilities clear.
