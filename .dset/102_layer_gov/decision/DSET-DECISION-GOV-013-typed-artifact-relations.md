+++
artifact_id = "DSET-ATOMIC-RECORD-035"
semantic_id = "DSET-DECISION-GOV-013"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET artifact traceability uses ten mutually exclusive typed relations, derived inverses, and range-based evergreen projection frontiers."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[[relations]]
type = "resolution_of"
target = "DSET-QUESTION-GOV-004"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-033"

[[relations]]
type = "replacement_of"
target = "DSET-REQUIREMENT-GOV-034"
+++

# Decision — Use typed artifact relations

DSET uses these ten general artifact relations:

| Relation | Meaning |
|---|---|
| `child_of` | A claim narrows, decomposes, or specializes another claim; both remain active. |
| `analysis_of` | An Analysis Report investigates an artifact without becoming authority. |
| `projection_of` | An evergreen artifact compiles a range of current project artifacts. |
| `implementation_of` | Code, configuration, documentation, migration, or a commit realizes authority or QA. |
| `check_of` | A Test or Evaluation defines how a claim is checked. |
| `evidence_for` | An Evidence Record supports an explicit result, finding, or Verification. |
| `resolution_of` | A Decision or recorded outcome closes a Question, Conflict, or Problem. |
| `override_of` | Narrower authority replaces inherited authority only in its declared scope. |
| `replacement_of` | A successor atom completely replaces an older atom. |
| `relates_to` | A symmetric trace association used only when no precise relation applies. |

Each authored edge is stored on its source as one `type` plus one canonical
`target`. One source-target pair has one primary relation. Reverse relations
are derived and never authored. `relates_to` carries no authority, dependency,
assurance, precedence, or lifecycle meaning and does not satisfy implementation
or QA coverage.

`child_of`, `override_of`, and `replacement_of` are exclusive. `child_of`
keeps both claims applicable. `override_of` changes behavior only in a narrower
scope. `replacement_of` requires append-only absorption of the predecessor and
removes it from the active set everywhere.

`projection_of` normally stores a range frontier rather than one edge for every
compiled atom. Each range selects one semantic Type and exact structural scope
through one globally ordered immutable `ATOMIC-RECORD` carrier. The projection
includes every applicable, active atom in that range and applies lifecycle
state; a newer applicable atom makes the projection stale. Individual targets
are reserved for explicit exceptions.

The rule-registry fields `depends_on` and `precedence_over` remain specialized
governance controls. They are not general artifact-traceability relations.
Ordinary citations, folder membership, shared subject matter, and chronology
remain metadata or Markdown links.

Sealed historical `child_of` fields remain readable compatibility input and
are projected as typed `child_of` edges. New artifacts use `relations`.

This Decision completely replaces `DSET-REQUIREMENT-GOV-033` and
`DSET-REQUIREMENT-GOV-034`, and resolves `DSET-QUESTION-GOV-004`.

## Rationale

The former neutral lineage edge could not distinguish refinement,
implementation, assurance, evidence, resolution, scoped exception, and full
replacement. A bounded typed vocabulary makes coverage and lifecycle meaning
deterministic without forcing every contextual link into governance.

This emitted Decision atom is immutable. Later correction requires a successor
Decision and append-only lifecycle event.
