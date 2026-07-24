---
artifact_type: "implementation_decision"
artifact_id: "DSET-DECISION-GOV-027"
scope_path:
  - "layer:gov"
priority: "high"
llm_session_ids:
  - "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
relations:
  - type: "replacement_of"
    targets:
      - "DSET-DECISION-GOV-018"
  - type: "child_of"
    targets:
      - "DSET-DECISION-GOV-025"
---

# Decision — Atomize carrier transitions

Moving a carrier between directories while preserving its globally unique name
and bytes is not a semantic transition and needs no location record. The
identity resolver finds its current location inside the selected `.dset`.

A carrier-name or representation migration is one immutable transition record,
not an entry in a shared ledger. It records the semantic ID, old and new unique
carrier names, old and new digests, semantic-equivalence proof, Git return
identity, implementation commit, session provenance, and declared loss. It
never stores the old or new physical path as current authority.

A semantic change is not a carrier transition; it requires a successor atom
and the applicable lifecycle relation.

## Rationale

Atomized transition evidence preserves auditability without recreating the
path coupling or multi-artifact aggregate files removed by the current control
model.

## Primary claim

A DSET carrier representation transition is one immutable atomic record identified by old and new globally unique carrier names and digests; directory placement is never identity, aggregate path-transition ledgers are legacy only, and current DSET lookup never consumes stored paths.
