---
artifact_type: implementation_decision
artifact_id: DSET-DECISION-GOV-008
scope_path: ["layer:gov"]
priority: high
decided_at: 2026-07-20
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: replacement_of
    targets:
      - "DSET-DECISION-GOV-007"
---

# Decision — FPF-aligned boundaries for the flat Type model

- **Resolves Question:** operator request to revise the new DSET Type/subtype
  system against FPF
- **Replaces claims:** the four-Type list and direct subtype list remain
  unchanged; this successor sharpens what an atom is, how one subtype is
  recognized, and how authority, acceptance, carriers, work, and evidence stay
  separate
- **Selected option:** retain exactly four application-level semantic Types and
  one optional flat subtype level, but require one primary governed claim,
  explicit act/content/carrier/work/result boundaries, split multi-head atoms,
  and fail-closed classification when a direct subtype is ambiguous

## Context and reviewed source

The flat model removed nested classifications, but its first definition could
still be read as a universal ontology. It also used “Decision” for both the
operator's act of accepting authority and the durable directive that later
governs the project. Several direct Decision subtypes overlap in ordinary
language: an invariant is also a requirement, an outcome may be required, and
a Contract may contain constraints. Without a recognition rule, one-subtype
enforcement would force arbitrary classification.

This revision independently adapts bounded principles from FPF revision
`afa4936541774021c92adb97c3cbf787bf126062`:

- A.7 Strict Distinction: keep the entity or condition under concern, its
  description, its carrier, methods, work occurrences, and evidence separate;
- A.11 Ontological Parsimony: add a durable kind only after composition fails,
  require a sharp boundary, and reopen on material overlap;
- A.2.9 SpeechAct and C.32.PAD: distinguish an acceptance/authorization act,
  the decision relation or directive it institutes, and a publication record;
- A.10 Evidence Graph: evidence supports bounded reliance but does not itself
  authorize work, pass a gate, or become the governed claim; and
- E.17.AUD PublicationUnit Stability: keep one primary concern and one honest
  publication move per atomic unit.

The exact mappings and exclusions are owned by
[`dset/scopes/gov/provenance.yaml`](../../../gov/provenance.yaml). DSET does not
import FPF ontology, `U.*` kinds, identifiers, record formats, or publication
syntax and does not claim FPF conformance.

## Canonical model

| Type | Empty subtype means | Direct subtypes |
|---|---|---|
| **Decision** | General operator-accepted project directive | `requirement`, `constraint`, `contract`, `user_story`, `outcome`, `scenario`, `invariant` |
| **Question** | General unresolved knowledge, interpretation, or choice | `conflict`, `risk`, `opportunity` |
| **Problem** | General current evidence-backed insufficiency claim | `defect`, `gap`, `debt` |
| **QA** | Not permitted for an emitted QA atom | `test`, `evaluation` |

Every atom has exactly one Type and at most one direct subtype. User Story and
Requirement remain sibling Decision subtypes. There is no subtype path,
sub-subtype, second subtype, or Type-repeating subtype.

## Application-level scope

DSET Types classify durable project atoms for governance and routing. They are
not universal kinds of people, systems, real-world conditions, work, or files.

- A **Decision atom** is the identified directive content that may govern the
  project. The operator's acceptance is an act or lifecycle event that grants
  authority to that content; it is not the directive content itself.
- A **Question atom** records an unresolved question; it is not the act of
  asking or investigating it.
- A **Problem atom** records an evidence-backed claim about a current
  insufficiency; it is not the affected system or condition itself.
- A **QA atom** defines a check; it is not the execution of that check, its
  output, evidence, gate decision, or Verification view.
- A Markdown, YAML, database, or hosted record is a carrier or representation
  of the identified atom. File format and location never determine Type.
- Implementation, investigation, Test or Evaluation execution, and operator
  acceptance are work occurrences. Results and logs are evidence. They link to
  atoms without becoming atoms of the same semantic kind merely by existing.

An implementation may initially store an accepted atom and the acceptance
effect in one repository record for practicality. Their semantics remain
distinct, and a future append-only lifecycle representation may separate the
acceptance event without changing the directive's identity.

## One atom, one primary governed claim

Classify the smallest independently reviewable claim, not an entire file,
ticket, workflow, or paragraph. One document may publish many linked atoms.

If a statement contains multiple independently enforceable or independently
verifiable semantic heads, split it into sibling atoms and link them. For
example, an API boundary Contract may link an always-valid Invariant, an
implementation Constraint, and an Outcome target. Calling the whole bundle one
Contract would hide the other acceptance conditions; assigning several
subtypes would recreate nesting.

If a claim cannot be split without losing its meaning and remains plausibly
classifiable under more than one subtype, use the empty subtype of its Type and
record a Question when the ambiguity affects implementation, assurance, or
priority. Never guess, silently choose by file location, or encode several
subtypes.

## Direct Decision subtype recognition

Choose the subtype whose defining acceptance condition owns the atom:

- **Contract:** named provider/consumer or component-boundary obligations,
  interface, compatibility, failure, or exchange conditions.
- **Constraint:** a restriction on otherwise acceptable solutions, including
  required or forbidden technologies, resources, environments, or formats,
  when no boundary participant relies on it as a Contract.
- **User Story:** actor or stakeholder, desired capability or outcome, and its
  value; it frames intent but does not absorb linked acceptance criteria.
- **Outcome:** an intended measurable state change with baseline, target,
  observation method, and window where applicable; an observed result is
  evidence, not a Decision/Outcome atom.
- **Scenario:** one concrete accepted behavior example with preconditions,
  event or interaction, and expected observable result; an executed run is
  work/evidence, not a Decision/Scenario atom.
- **Invariant:** an accepted condition that must hold for every state in its
  declared scope; an observation that it currently holds is evidence.
- **Requirement:** the remaining observable obligation, capability, behavior,
  quality, or prevention condition not more precisely owned by another direct
  Decision subtype.
- **General Decision:** any other operator-accepted directive, including a
  consequential choice among alternatives or a governance/implementation
  instruction.

These recognition rules make the direct subtype field a DSET routing
classification. They do not claim that the same words form disjoint universal
ontological sets outside DSET.

## Question and Problem subtype recognition

Question subtypes distinguish the uncertainty being recorded:

- **Conflict:** verified mutually incompatible active applicable authority over
  the same scope, concern, and effective time;
- **Risk:** uncertain future harm; and
- **Opportunity:** possible beneficial improvement while no current obligation
  is unmet.

Problem subtypes distinguish the current insufficiency claim:

- **Defect:** something exists or behaves now in contradiction with active
  authority;
- **Gap:** a required capability, artifact, proof, or obligation is absent now;
  and
- **Debt:** an explicitly accepted compromise works sufficiently now but
  creates continuing or future cost.

Debt must never conceal a Defect or Gap. If a compromise also violates active
authority or leaves a required item absent, link separate Defect or Gap atoms
or emit an explicit Decision that changes the applicable authority. A cause,
effect, future risk, and current problem may coexist as linked atoms, but one
atom retains one primary claim.

## Test and Evaluation recognition

A Test atom defines an exact reproducible predicate under controlled declared
conditions. An Evaluation atom defines an assurance conclusion that depends on
judgment, sampling, calibration, probability, statistics, or a model, even
when deterministic code executes its procedure.

A compound proof plan may contain linked Tests and Evaluations. It must not
create a hybrid subtype. Test code, Evaluation prompts, datasets, executions,
results, evidence, gate decisions, and Verification remain distinct
implementation, work, evidence, or derived-view roles.

## Authority, assurance, and lifecycle

Operator input remains source intent. An explicit operator acceptance act
institutes or confirms Decision authority. Active Decision atoms compile into
evergreen projections. Implementation realizes those projections. QA atoms
define checks; executions produce evidence; Verification derives a bounded
current reliance statement or gate disposition.

All emitted atoms remain immutable. Status, acceptance, answer, correction,
absorption, and retirement are lifecycle relations or events. A successor atom
may absorb an older one, but a carrier rewrite, status label, passing check, or
newer timestamp never changes semantic identity or authority by itself.

## Consequences and migration

This Decision must compile into the public Type catalog, README workflow,
repository-local work-item and architecture rules, self-hosted META/GOV truth,
proof plans, FPF provenance mapping, and current Change verification.

`DSET-PROBLEM-GOV-007` and `DSET-TASK-GOV-049` remain open. Their schema and
runtime migration must now enforce both the flat model and these recognition
boundaries without editing legacy atoms. Existing `DSET-DECISION-GOV-007`
remains immutable history and is removed from the active authority set only by
this explicit absorption.

## Rationale

The four-Type surface still passes FPF-style parsimony: each Type changes an
action-facing rule—Decision owns authority, Question owns unresolved choice,
Problem owns current insufficiency, and QA owns assurance definitions. Adding
Work, Evidence, Carrier, Verification, Change, or Release as new semantic Types
would duplicate roles and relations already represented elsewhere.

The necessary correction is sharper separation, not more taxonomy. One
primary claim, direct subtype recognition, split multi-head atoms, and explicit
act/content/carrier/work/result boundaries make the small model usable without
pretending ordinary language categories are perfectly disjoint.

## Lifecycle policy at emission

- **Expected confirmation evidence:** independent reviewers classify mixed
  examples consistently, split multi-head cases, preserve general-Type fallback
  on irreducible ambiguity, and distinguish atoms from acts, carriers, work,
  evidence, and derived views
- **Known counter-evidence:** current schemas and emitted legacy atoms do not
  yet encode the general Type/subtype envelope or the new recognition fields
- **Reopen when:** two reviewers applying the boundary rules repeatedly cannot
  agree on an ordinary case, or a fifth application-level Type changes a
  necessary action-facing rule that roles and relations cannot express
- **If reopened, retain:** four-way authority/uncertainty/insufficiency/
  assurance separation, one direct subtype maximum, User Story as a direct
  Decision subtype, and Test/Evaluation separation
- **Retirement condition:** a validated successor absorbs every active claim
  and no current projection or implementation relies on this Decision

This emitted Decision atom is immutable. Any later correction, status change,
counter-evidence, absorption, or retirement must be a new atom or append-only
lifecycle event.
