+++
artifact_id = "DSET-ATOMIC-RECORD-005"
semantic_id = "DSET-REQUIREMENT-GOV-034"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "unknown"
child_of = ["DSET-REQUIREMENT-GOV-033"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Requirement — Trace every child through its immediate parents

Every governed artifact that descends from another governed artifact stores a
non-empty `child_of` list containing one or more canonical immediate-parent
IDs. A parent may have any number of children, and a child may have more than
one parent. Root artifacts omit `child_of`.

`parent_to` is always a derived reverse view. An author, generator, or workflow
must never write it into a canonical artifact or edit an immutable parent to
register a later child.

The relation provides neutral lineage across planning, authority,
understanding, implementation, proof, and release. It covers, among other
valid chains:

- an APP-PLAN producing one or more Decision, Requirement, Constraint,
  Contract, Question, Problem, Test, or Evaluation atoms;
- a Question or Problem producing an Analysis Report and the report producing
  accepted atomic conclusions;
- Requirements, Constraints, Contracts, and Decisions producing compiled
  truth, QA definitions, and implementation;
- Test and Evaluation execution producing Evidence Records;
- Evidence producing Verification, a Problem when it demonstrates failure, or
  a Question when its meaning remains uncertain; and
- Verification and release planning producing Readiness and Release Records.

Store only immediate causal parents. Full upstream and downstream traceability
is the transitive closure of `child_of` plus its derived `parent_to` view; do
not create dense links to every ancestor. Implementation commits contribute
lineage through their `Implements: <artifact-id>` trailers.

`child_of` does not imply agreement or authority. The child content states
whether it implements, refines, replaces, cancels, verifies, or reveals a
problem in its parent. Unresolved IDs, empty or duplicate lists, self-links,
and lineage cycles fail closed.

## Rationale

A single many-to-many lineage primitive gives DSET end-to-end traceability
without mutating older artifacts or maintaining reverse links twice. Immediate
edges keep atomic records small, while a derived graph can still calculate
APP-PLAN decomposition, specification, implementation, Test, Evaluation,
evidence, Verification, and release coverage.

This emitted Requirement atom is immutable. Later correction, absorption, or
retirement requires a new linked atom or append-only lifecycle event.
