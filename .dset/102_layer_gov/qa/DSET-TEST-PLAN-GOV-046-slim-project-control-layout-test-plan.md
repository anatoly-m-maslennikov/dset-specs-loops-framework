+++
artifact_id = "DSET-ATOMIC-RECORD-102"
semantic_id = "DSET-TEST-PLAN-GOV-046"
revision_mode = "atomic"
content_role = "method"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["project:dset-specs-loops-framework", "layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove schema 1.3 discovery, single-config ownership, direct layer roots, project and Version roots, initialization, relocation integrity, and rejection of competing legacy carriers."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-041"
+++

# Test Plan — Verify the slim project control layout

Run layout, settings, bootstrap, governance, carrier-transition, link,
classification, traceability, and full repository tests. Prove that:

1. current discovery selects only `dset/dset_settings.toml` and schema 1.3;
2. fixed layer roots are direct children of `dset/`;
3. project-wide and Version artifacts resolve through `project/` and
   `versions/`;
4. initialization emits that layout and passes repository validation without a
   follow-up migration;
5. competing current/legacy configuration carriers fail closed; and
6. every immutable relocation remains byte- and Git-source-verifiable.

This Test atom is immutable. Later correction requires a successor Test and an
append-only lifecycle event.
