# FPF governance-constitution review — 2026-07-16

## Proof identity

- **Claim:** DSET's governance constitution independently adapts the useful FPF
  distinctions between authority, precedence, dependency, decision discharge,
  and risk-proportionate assurance without importing FPF ontology or making FPF
  a live DSET authority.
- **Intended use:** Support `DSET-DECISION-GOV-002` and review the bounded GOV
  constitution change; not claim full FPF conformance or certify unrelated
  DSET behavior.
- **Producer/performed work:** Three independent high-effort subagent reviews
  plus main-thread inspection of the current DSET registry, schema, validator,
  templates, specs, and pinned FPF sources.
- **LLM session IDs:**
  - `codex:019f591f-04f6-70f2-8de7-828b7cccc69d`
- **Method/setup:** Compare the proposed DSET principle with FPF E.3, E.5.3,
  E.9, E.19, and A.10 at revision
  `afa4936541774021c92adb97c3cbf787bf126062`; then run an adversarial overlap
  and bootstrap review against the DSET governance graph.
- **Evaluated DSET version:** the commit containing this proof and
  `DSET-DECISION-GOV-002`.
- **Observed:** 2026-07-16.
- **Evidence polarity:** supporting with bounded corrections and one explicit
  future limitation.
- **Currentness:** current for the cited FPF revision and the containing DSET
  governance/schema/validator version.
- **Reopen when:** a cited FPF source/revision, DSET Architecture rule,
  governance registry relation, Decision discharge rule, or assurance boundary
  changes.
- **Unsupported uses:** this proof does not grant an FPF license, import FPF
  taxonomy or canonical IDs, prove semantic equivalence, or show that
  `precedence_over` can model every future conflict family.

## Review result

| Candidate concern | Result | DSET disposition |
|---|---|---|
| One canonical authority | Supported | Keep `DSET-RULE-ARCHITECTURE` as the sole dependency-free root instead of creating a sibling authority rule. |
| Scope and applicability | Supported | Use registered layer/path, applicability/reason, selected profile edition, and customization identity. |
| Dependency versus precedence | Supported with correction | Keep `depends_on` and `precedence_over` as separate acyclic relations; registry order implies neither. |
| Provenance | Supported with boundary | Retain material-change provenance, but never treat provenance as truth, permission, or rule authority. |
| Transactional compile-down | Supported | Decisions temporarily converge rationale and selected consequences; evergreen governing artifacts own current normative truth. |
| Proof obligation | Supported with correction | Require an applicable test, eval, review, or justified non-applicability disposition; scale depth by risk and reliance. |
| Missing or stale proof | Corrected | Stale assurance blocks the relying claim or gate and triggers bounded reopening; it does not silently erase valid authority. |
| New governance root | Rejected | A sibling root duplicates Architecture and adds bootstrap circularity without a separate owning question. |

## FPF boundary

The exact adapted concepts and excluded semantics are recorded in
`dset/scopes/gov/provenance.yaml`. DSET does not adopt the FPF Pillar taxonomy,
default class ordering, Core/Tooling/Pedagogy family model, DRR publication
format, evidence ontology, or FPF quality-result semantics.

## Remaining limitation

The current registry validates declared precedence targets and cycles. It
cannot automatically discover a semantic conflict that authors failed to
declare. The qualitative authority-versus-assurance eval therefore remains
necessary; a later Decision may add typed conflict declarations if real adopter
evidence shows that per-rule precedence is insufficient.
