+++
schema_version = "1.0"
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-032"
priority = "high"
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
context = ["repository=anatoly-m-maslennikov/dset-specs-loops-framework", "environment=local-macos", "transition_records=85", "converted_carriers=81"]
observed_at = "2026-07-21T04:13:20+04:00"
evidence_location = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/proofs/DSET-EVIDENCE-RECORD-032-semantic-carrier-transitions.md"
polarity = "supports"
currentness = "current"
reopen_when = "A transitioned carrier, original/current seal, transition schema, normalization rule, source-return address, or subject revision changes."

[subject]
id = "DSET-TEST-PLAN-GOV-042"
revision = "483ea2af321505f40713a73a51b3b68f327ba7f3"
intended_use = "Support the bounded claim that carrier conversion preserves immutable semantic identity and lossless source return."

[producer]
identity = "codex:019f591f-04f6-70f2-8de7-828b7cccc69d"
performed_work = "Validated every registered carrier transition, original and current digest, normalized semantic digest, declared loss, source Git blob, current path, and physical retained link."

[method]
description = "Ran the carrier-transition validator and repository checks over 85 registered transitions: 81 converted carriers and four immutable proof-link carrier changes."
setup = "Commit 483ea2af321505f40713a73a51b3b68f327ba7f3; Python 3.14; local macOS repository with the canonical transition ledger."

[[relations]]
type = "evidence_for"
target = "DSET-TEST-PLAN-GOV-042"
+++

# Test result — Semantic carrier transitions

All transition chains validate with no declared loss. Original seals and Git
blob return addresses remain registered, current paths and digests resolve,
normalized semantic payloads match, and retained links are physically valid.

This record supports representation-transition integrity only. The complete
zero-YAML and repository-gate result is recorded separately.
