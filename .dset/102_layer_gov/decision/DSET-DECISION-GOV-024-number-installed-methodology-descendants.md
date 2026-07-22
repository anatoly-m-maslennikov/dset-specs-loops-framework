+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-159"
type = "decision"
subtype = "none"
semantic_id = "DSET-DECISION-GOV-024"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every committed file and directory below .dset/000_dset_methodology uses a stable numeric prefix within its parent, including hubs, schemas, templates, fixtures, guides, and supportability material."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-022"
+++

# Decision — Number installed methodology descendants

The installed methodology keeps the accepted `00_project` through `05_ops`
layer roots. Every descendant entry uses a zero-padded numeric prefix that is
unique among its siblings. Hubs sort first; remaining siblings use stable
semantic grouping and then name order.

Reusable framework source may keep author-facing names. Deterministic
materialization maps that source into the numbered installed edition and owns
the source-to-installed path map.

## Rationale

Visible ordering makes a large local methodology navigable without mixing it
with applied project state. Generating the installed names avoids forcing
authoring-oriented source paths into adopter repositories.
