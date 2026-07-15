# Methodology TOOL domain

This is one layer-owned fragment of the logical methodology package. Use the sibling layer hubs for connected definitions; this file owns only the entities and invariants below.

## Entities

| Entity | Definition |
|---|---|
| **DSET toolchain** | The dependency-light CLI, schemas, templates, fixtures, traceability generator, migration guidance, CI gate, and focused skills that execute the accepted methodology contract |
| **Self-hosting gate** | Bounded release proof in which the last released validator checks the candidate change, the candidate checks this repository, and the candidate materializes and checks one non-recursive temporary adopter |
| **Diagnostic** | A stable code, artifact path, and actionable message emitted by a deterministic DSET gate |
| **Traceability index** | A deterministic committed view from changes to intake, packages, User Stories, Outcomes, Requirements, tests, evals, Contracts, Decisions, evidence, and repository-qualified PRs; it is derived evidence rather than the owner of GitHub state or code diffs |
| **Project health renderer** | A deterministic projection that derives a portable Markdown health view from canonical repository artifacts and traceability without becoming another truth store |
| **Priority conflict resolver** | A deterministic evaluator for every governed artifact pairing that emits a role-aware disposition, selects an effective claim only when policy permits resolution, and stops on unsatisfiable obligations, ties, or uncertainty |

## Invariants

- **DSET-INVARIANT-TOOL-001:** The canonical validator is read-only; scaffolding, trace updates, and archival require explicit write commands and never overwrite existing project truth.
- **DSET-INVARIANT-TOOL-002:** Stable diagnostic codes and deterministic trace ordering are compatibility surfaces; explanatory prose may improve without changing their meaning.
- **DSET-INVARIANT-TOOL-003:** Self-hosting terminates after released-to-candidate, candidate-to-repository, and candidate-to-temporary-adopter proof; the temporary adopter never recursively creates another adopter.
- **DSET-INVARIANT-TOOL-004:** Health rendering is deterministic, applicability-aware, and read-only unless an explicit write command refreshes the declared generated destination; an optional interactive renderer never owns data absent from canonical artifacts.
- **DSET-INVARIANT-TOOL-005:** Automatic conflict handling never guesses: every governed artifact pairing receives a role-aware classification and disposition; active atoms beat stale compiled projections, absorbing atoms beat absorbed predecessors, immutable authority beats mutable truth, unsatisfiable immutable obligations stop, authority/evidence conflicts update assurance, implementation mismatches create Problems, generated drift routes to its owner, and selectable policy conflicts apply explicit precedence before effective priority. The resolver records its inputs and result and stops on equal, unknown, cyclic, or incomparable priority when claim selection is required.
