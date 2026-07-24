---
artifact_type: specification
scope_path: []
priority: medium
artifact_subtype: governance
---

# Atomic artifact meanings and routing

**Rule ID:** `DSET-RULE-WORK-ITEMS`

## Direct registered types

DSET classifies an atom directly by `artifact_type` and, when useful, one
registered `artifact_subtype`. It has no separate parent semantic-Type field.
The catalog derives route and identity kind from that pair.

| Type | Optional direct subtypes | Primary meaning |
|---|---|---|
| `requirement` | — | Required observable project result or obligation |
| `constraint` | — | Outside-imposed limitation on acceptable project choices |
| `contract` | — | Obligations between explicit providers, consumers, or boundaries |
| `implementation_decision` | — | Material selected architecture, design, algorithm, data, tooling, or operating approach |
| `question` | `conflict`, `risk`, `opportunity` | Missing knowledge, unresolved choice, incompatible authority, uncertain harm, or optional value |
| `problem` | `defect`, `gap`, `debt` | Present evidence-backed insufficiency |
| `test_plan` | — | Deterministic check definition with reproducible pass/fail semantics |
| `evaluation_plan` | — | Judgment-, sampling-, calibration-, probability-, statistics-, or model-dependent assessment definition |
| `rationale` | — | Preserved explanation of why a Definition or Method was selected |
| `analysis_report` | `solution_landscape`, `root_cause_analysis`, `proposal`, `technical_investigation`, `external_audit_analysis` | Bounded interpretation of named inputs that does not authorize its conclusion |
| `evidence_record` | `test_result`, `evaluation_result`, `review_report`, `run_record` | Immutable observation bound to subject, method, revision, provenance, and limits |
| `verification` | — | Bounded conclusion about what named evidence supports |

Additional native atomic types, including `git_commit` and
`external_git_commit`, are registered by the catalog when enabled. Maintained
and append-only types use the same catalog but are not atomic claims.

## Definition authority

A Requirement states what the project must provide or prevent. A Constraint
records an obligation imposed by an external source such as law, platform,
existing schema, environment, or operator-declared external boundary. A
Contract governs an explicit relation and therefore declares role-bearing
endpoints. An Implementation Decision selects how accepted Definition
authority will be realized.

These types are peers, not subtypes of Decision. Routine code detail stays in
implementation; emit an Implementation Decision only when the choice is
material enough to govern later work. Record rationale inline when concise or
as a linked Rationale atom when it deserves independent history.

Atomic sources: `DSET-REQUIREMENT-GOV-057`,
`DSET-REQUIREMENT-GOV-101`, and `DSET-IMPL-GOV-003`.

## Inquiry and observation feedback

A Question records missing knowledge or an unresolved choice and authorizes no
implementation by itself.

- `conflict` requires exact incompatible active authority over the same
  concern, scope, applicability, and effective time;
- `risk` records uncertain future harmful conditions; and
- `opportunity` records possible beneficial improvement when no current
  obligation is unmet.

A Problem records a presently true, evidence-backed insufficiency:

- `defect` means something present behaves contrary to applicable authority;
- `gap` means a required capability, artifact, proof, or obligation is absent;
  and
- `debt` means a known compromise works now but creates continuing or future
  cost.

Debt never conceals a current Defect or Gap. A wording difference, stale view,
failed check, implementation mismatch, or contrary observation is not a
Conflict unless incompatible authority is established.

A Question or Problem may lead directly to work only when existing authority
already defines the answer. Otherwise analysis informs a new Requirement,
Constraint, Contract, or Implementation Decision. The canonical feedback loop
is Inquiry → Analysis → Definition → Method → Implementation → Observation →
Inquiry. Sources: `DSET-REQUIREMENT-META-047` and
`DSET-REQUIREMENT-META-048`.

## Assurance meanings

Test Plan and Evaluation Plan are direct atomic Method types.

- Test Plans define deterministic checks under controlled conditions.
- Evaluation Plans define judgment-dependent or uncertainty-bearing
  assessments with a method, rubric or metric, threshold, and treatment of
  uncertainty.

Executable tests, evaluation prompts, datasets, fixtures, and harnesses are
Maintained Implementation artifacts. Their runs produce Evidence Records.
Verification interprets named evidence for one bounded reliance claim.
Definition authority, checking method, execution, evidence, and Verification
remain distinct.

## Identity

The canonical identity shape is:

```text
<PROJECT?>-<SCOPE_PATH?>-<ARTIFACT_KIND>-<NNN>-<summary>
```

Settings may omit the project prefix for a small isolated namespace and may
include an ordered extensible scope path. The visible registered type or
enabled subtype owns one project-wide number sequence. The registered
type/subtype determines identity kind; there is no family-level fallback
sequence. Native Git and host entities retain repository-qualified native
identities.

A naming-policy migration recodes the complete identity graph in one
collision-free transaction and removes old aliases after cutover. It may change
representation, not governed atomic meaning. Sources:
`DSET-REQUIREMENT-GOV-060`, `DSET-REQUIREMENT-GOV-064`,
`DSET-REQUIREMENT-GOV-071`, and `DSET-IMPL-GOV-003`.

## Lifecycle and relations

Atomic meaning is immutable. The repository has only active and archived
Atomic-artifact storage states.

- `replacement_of` completely replaces an older atom;
- `resolution_of` resolves a Question or Problem;
- `override_of` creates an explicit narrower exception;
- `recurrence_of` links a new Question or Problem to a closed predecessor;
- `child_of` narrows, decomposes, or specializes a claim;
- `implementation_of`, `check_of`, and `evidence_for` connect realization and
  assurance;
- `analysis_of`, `projection_of`, and `solution_for` own their precise
  semantics; and
- `relates_to` is a non-semantic fallback with no coverage value.

Reverse links are derived. Reopening is forbidden. After a successor or
resolver is committed, the predecessor moves byte-for-byte to its type-local
`archive/`. Withdrawal archives the atom; future intent is recorded in a
Version Roadmap. Archive commits use `Archives`, `Archive-Reason`,
`Archive-Reference` when applicable, and `Session` trailers. Source:
`DSET-DECISION-GOV-035` and `DSET-REQUIREMENT-GOV-096`.

## Git and provenance

Git is mandatory. Every implemented authority has at least one commit with an
`Implements:` trailer; every resolved Problem has a commit with `Resolves:`.
Every governed commit has one host-prefixed `Session:` trailer. One commit may
name several artifacts only when the technical change is indivisible.

Every new atomic Markdown carrier records `llm_session_ids`; an explicit empty
list denotes human-only creation. Provenance enables investigation but does
not confer authority. Internal Git commits use `git_commit`; outside-owned
commits use `external_git_commit`. Pull requests are maintained relational
Method artifacts with independent source and target endpoint origins. Sources:
`DSET-REQUIREMENT-GOV-065`, `DSET-REQUIREMENT-GOV-080`, and
`DSET-REQUIREMENT-GOV-103`.

## Classification procedure

1. End Exploration Mode only after the operator accepts a durable conclusion.
2. Split independent primary claims.
3. Select one enabled direct type and at most one direct subtype.
4. Resolve its route and identity kind from the artifact catalog.
5. Assign the narrowest correct structural scope.
6. Add only non-derived provenance, priority, endpoints, relations, and
   type-specific facts.
7. Fail closed when classification, authority, scope, applicability, or
   relation meaning remains materially ambiguous.

Workflow, queue, ticket, skill, tool, host, filename, folder, and desired next
action never determine artifact meaning.
