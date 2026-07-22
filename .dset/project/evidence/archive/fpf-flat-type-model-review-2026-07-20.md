# FPF review of the flat DSET Type model — 2026-07-20

## Proof identity

- **Claim:** The DSET Type/subtype model retains a parsimonious four-Type
  application taxonomy while separating typed project claims from operator
  acts, carriers, work, results, evidence, gates, and derived views.
- **Intended use:** Support `DSET-DECISION-GOV-008` and the compiled
  `DSET-REQUIREMENT-GOV-027`; not claim FPF conformance or completed runtime
  enforcement.
- **Producer/performed work:** Main-session inspection of the current DSET
  model and pinned FPF sources, followed by deterministic projection and
  regression checks.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Evaluated DSET revisions:** `73089f3` (Decision), `ca8ff03` (public and
  repository-local governance), and `3257df3` (self-hosted specs and proof
  plans).
- **Evaluated FPF revision:**
  `afa4936541774021c92adb97c3cbf787bf126062`.
- **Observed:** 2026-07-20.
- **Currentness:** current for the cited revisions and the exact mappings in
  `dset/scopes/gov/provenance.yaml`.
- **Reopen when:** a Type or subtype is added, removed, nested, or redefined;
  atom/carrier/work/evidence boundaries change; ordinary classification cases
  repeatedly produce reviewer disagreement; or a cited FPF source changes.
- **Unsupported uses:** this proof does not import FPF ontology, identifiers,
  schemas, publication forms, or process; grant a license not present upstream;
  prove semantic equivalence; or close `DSET-PROBLEM-GOV-007` and
  `DSET-TASK-GOV-049`.

## Review method

The review tested the model against five independently re-expressed FPF
principles: A.7 strict distinction, A.11 ontological parsimony, A.2.9
communicative work, C.32.PAD decision/publication separation, A.10 evidence
boundaries, and E.17.AUD publication-unit stability. Exact source paths, line
ranges, adaptation scopes, and exclusions are recorded in the repository
provenance registry.

## Findings and disposition

| FPF-derived review question | Finding | DSET disposition |
|---|---|---|
| Does each Type change an action-facing governance rule? | Yes. Decision owns authority, Question unresolved knowledge/choice, Problem current insufficiency, and QA assurance definitions. | Keep exactly four Types; do not promote Work, Evidence, Carrier, Verification, Change, or Release into new Types. |
| Is “Decision” collapsing content, acceptance, and publication? | It was ambiguous. | Define the Decision atom as directive content; model operator acceptance as a lifecycle act and the file/record as a carrier. |
| Is QA collapsing the check with its run or result? | The prior prose was vulnerable to that reading. | Keep QA atoms as definitions; execution is work, outputs/logs are evidence, and Verification is derived. |
| Can one subtype be selected without arbitrary overlap? | Only with recognition precedence and a safe fallback. | Classify the smallest primary claim, split multi-head statements, and use the Type's empty subtype plus a Question for irreducible ambiguity. |
| Do the direct Decision subtypes have usable boundaries? | Yes after refinement. | Contract owns relied-on boundary obligations; Constraint narrows solutions; User Story owns actor/want/value; Outcome intended change; Scenario accepted example; Invariant always-hold condition; Requirement the residual observable obligation. |
| Are Problem and QA edge cases honest? | Two corrections were needed. | Debt cannot conceal Defect/Gap. Deterministic code still implements an Evaluation when the conclusion depends on judgment, sampling, calibration, probability, statistics, or a model. |

## Result

No fifth Type or subtype nesting is warranted. The revised model passes the
FPF-style parsimony test because every retained Type changes a distinct routing
and authority rule, while the concepts that would otherwise inflate the Type
list are represented honestly as acts, roles, relations, implementation,
evidence, or derived views.

The accepted Type and subtype lists are unchanged. The material correction is
the classification boundary: one primary governed claim, split mixed heads,
fail closed to the general Type when necessary, and never infer semantic Type
from workflow or carrier.

## Deterministic evidence

- `python -m dset_toolchain check .` — passed.
- Ruff format check over 46 source files — passed.
- Ruff lint — passed.
- mypy over `dset_toolchain` and `tests` — passed.
- 133 unit and fixture tests — passed.
- `git diff --check` — passed before proof promotion.

The qualitative `DSET-EVAL-GOV-017` reviewer-agreement run remains a separate
pending Evaluation; deterministic checks prove projection consistency, not
human classification reliability.
