+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-160"
type = "decision"
subtype = "none"
semantic_id = "DSET-DECISION-GOV-025"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET-to-DSET references use unique identities only, and every skill discovers settings, methodology documents, evergreen artifacts, atomic artifacts, and lifecycle events by identity within the target repository's .dset control root without storing their physical carrier paths."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "replacement_of"
target = "DSET-DECISION-GOV-023"
+++

# Decision — Discover project artifacts by identity

Every DSET skill begins at the target repository's `.dset` control root. It
finds the uniquely named settings carrier and searches that bounded tree for
the requested semantic ID, artifact ID, rule ID, document ID, or unique carrier
name. Zero matches and multiple matches stop.

Authored relations, methodology references, evergreen references, settings
registries, and skill wrappers store identities rather than carrier paths. A
tool may hold the resolved path in memory while reading or writing the selected
carrier, but it does not persist that path as the reference.

Implementation files outside `.dset` remain project content and may be located
after an accepted artifact identifies the implementation subject. They are not
alternative owners of DSET settings or project artifacts.

## Rationale

Identity-only discovery makes numbered reorganization and artifact archival
safe, keeps skills independent of repository topology details, and guarantees
that the project-local `.dset` edition—not a global installation, remote copy,
or root framework source—governs every run.
