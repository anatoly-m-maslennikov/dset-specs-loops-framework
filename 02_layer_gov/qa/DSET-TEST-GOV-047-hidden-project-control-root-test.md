+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-105"
type = "qa"
subtype = "test"
semantic_id = "DSET-TEST-GOV-047"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Deterministic tests prove hidden-root discovery, repository-root-relative canonical paths, runtime-state isolation, direct ownership roots, initialization, migration integrity, and rejection of competing legacy carriers."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "check_of"
target = "DSET-REQUIREMENT-GOV-042"

[[relations]]
type = "replacement_of"
target = "DSET-TEST-GOV-046"
+++

# Test — Verify the hidden project control root

Run layout, settings, bootstrap, governance, carrier-transition, runtime,
link, classification, traceability, and full repository tests. Prove that:

1. current discovery selects only `.dset/dset_settings.toml` and schema 1.3;
2. persisted canonical paths resolve from the repository root;
3. fixed layer roots are direct children of `.dset/`;
4. project-wide and Version artifacts resolve through `project/` and
   `versions/`;
5. replaceable operational state is written under ignored `.dset/runtime/`;
6. initialization emits that layout and passes repository validation without a
   follow-up migration;
7. competing current/legacy configuration carriers fail closed; and
8. every immutable relocation remains byte-, semantic-, and
   Git-source-verifiable through the complete registered transition chain.

This Test atom is immutable. Later correction requires a successor Test and an
append-only lifecycle event.
