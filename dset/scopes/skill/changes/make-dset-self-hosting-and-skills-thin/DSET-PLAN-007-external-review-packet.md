+++
schema_version = "1.0"
artifact_type = "plan"
artifact_id = "DSET-PLAN-007"
packet_id = "DSET-REVIEW-PACKET-007"
repository = "dset-specs-loops-framework"
commit = "231c56db48a9d1805efdc42f48767e55387dbbe1"
scope = "DSET 0.4 repaired self-hosted framework, 17-skill distribution, Version lifecycle, TOML carriers, portable PR-merge fixed point, and open release gates; historical external adopters excluded"
criteria = ["Current atomic authority, compiled specifications, settings, implementation, tests, evaluations, tasks, and verification are coherent and traceable", "Version is the unambiguous release-lifecycle artifact Type and its six direct subtypes remain MECE", "The 17-skill surface keeps Overview read-only and outside the sixteen-entry lifecycle topology", "No critical or high contradiction, dead route, unowned claim, stale current surface, or premature 0.4 readiness statement remains"]
allowed_effects = ["read_only_report"]

[[reviewed_inputs]]
path = "README.md"
sha256 = "96e3c43e2a72ace3cb72d2d9bfbba26ddc2bf2a3ae1539a3aecb0bc9fed7b204"

[[reviewed_inputs]]
path = "dset_settings.toml"
sha256 = "06bbccd64d9c24550661152f0a48289a0c69c447ba334724ad2a055ace33338d"

[[reviewed_inputs]]
path = "dset/scopes/gov/governance/architecture.md"
sha256 = "48423de578a784b3ab530823ead80b123ee9bedb5964202e55b0f495eee8d161"

[[reviewed_inputs]]
path = "dset/scopes/gov/governance/artifact-classification.md"
sha256 = "5fd040d62cf3b7e3a49f24d9675da0f7b425f4f488178c0271a44c3b9f027d38"

[[reviewed_inputs]]
path = "dset/scopes/gov/generated/DSET-DERIVED-VIEW-001-project-health.md"
sha256 = "84421cec9467f45b8d7257cefdf7f24d269ed9f85eb2adb886b7da444e39857e"

[[reviewed_inputs]]
path = "dset/scopes/skill/specs/packages/methodology/spec.md"
sha256 = "ea80a29409602ff51db2880a616f284f3d6c842f139ab603dc3b805344e4cd87"

[[reviewed_inputs]]
path = "dset/scopes/skill/governance/lifecycle-orchestration.md"
sha256 = "807c78c31368ee52e8c04bc9c0331b1f32622c53877c8cf44b547bb8f46c023f"

[[reviewed_inputs]]
path = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/tasks.md"
sha256 = "a6b78b8ded1d491c14a097326c92ac7c36870a94f12b716c7eb6344f43f011f1"

[[reviewed_inputs]]
path = "dset/scopes/skill/changes/make-dset-self-hosting-and-skills-thin/verification.md"
sha256 = "19086471387b4dc0542cd862a6b768ddf1d97df16330b00b4503399f3eaa3c89"

[[reviewed_inputs]]
path = "skills/README.md"
sha256 = "ce6033daaa855e52bf825c1d6eb44f7ec5cbf946289b330bfcc2e0217c7956ec"

[[resolved_rules]]
id = "DSET-RULE-ARCHITECTURE"
path = "dset/scopes/gov/governance/architecture.md"
sha256 = "48423de578a784b3ab530823ead80b123ee9bedb5964202e55b0f495eee8d161"

[[resolved_rules]]
id = "DSET-RULE-ARTIFACT-CLASSIFICATION"
path = "dset/scopes/gov/governance/artifact-classification.md"
sha256 = "5fd040d62cf3b7e3a49f24d9675da0f7b425f4f488178c0271a44c3b9f027d38"

[[resolved_rules]]
id = "DSET-RULE-ARTIFACT-MAINTENANCE"
path = "dset/scopes/gov/governance/artifact-maintenance.md"
sha256 = "aeed191896694e94c2fd1265e07328c82bbe1e0b80d831d2bf913e9a7383bfbd"

[[resolved_rules]]
id = "DSET-RULE-BUILD"
path = "dset/scopes/tool/governance/build-rules.md"
sha256 = "1faf0275461d4c95c54f517cb75759292c8a42fd4134e44139b3e2c255b990cb"

[[resolved_rules]]
id = "DSET-RULE-DELEGATION-BUDGET"
path = "dset/scopes/skill/governance/delegation-budget.md"
sha256 = "74f6934ac692cf8faed36bb77227d5d3ccea82531a34f60463fc1629c08f3fec"

[[resolved_rules]]
id = "DSET-RULE-DIAGNOSIS"
path = "dset/scopes/skill/governance/diagnosis.md"
sha256 = "8f5e78a193298fb0e92b2a67891f005464a50760d84cf814dc3901ea30d122e2"

[[resolved_rules]]
id = "DSET-RULE-DOMAIN-SPEC"
path = "dset/scopes/meta/governance/domain-spec-authoring.md"
sha256 = "320c808a833574582c57910be599a37533785419c0560399066dfe11d3e09007"

[[resolved_rules]]
id = "DSET-RULE-EVAL-PLAN"
path = "dset/scopes/meta/governance/eval-planning.md"
sha256 = "569a38f5974e39dc3bd8092c108b3c14213e646c31041a84fe56d1af25956b5a"

[[resolved_rules]]
id = "DSET-RULE-LIFECYCLE"
path = "dset/scopes/skill/governance/lifecycle-orchestration.md"
sha256 = "807c78c31368ee52e8c04bc9c0331b1f32622c53877c8cf44b547bb8f46c023f"

[[resolved_rules]]
id = "DSET-RULE-PROTOTYPING"
path = "dset/scopes/skill/governance/prototyping.md"
sha256 = "c3cb7059d131acb077a6fa82b0b3a51d84c4d59c4ae5b4eb3c4c4ba00e05c8aa"

[[resolved_rules]]
id = "DSET-RULE-RELEASE"
path = "dset/scopes/ops/governance/release.md"
sha256 = "1c17c614b71d48a552517d04fd03f3ad43559b3b25a2758d9d9d394b7769cc34"

[[resolved_rules]]
id = "DSET-RULE-SKILL-RUNS"
path = "dset/scopes/skill/governance/skill-runs.md"
sha256 = "5b33b0eb9e307a0a3819e079e4c9c01f95039ce01148ea2dcf0cc91917b91cf6"

[[resolved_rules]]
id = "DSET-RULE-SUPPORTABILITY"
path = "dset/scopes/ops/governance/supportability.md"
sha256 = "cf1e5c0dea9f1a1690cd962ffd6511fa7e2af6242e3d2340fe7daa603bd1c35f"

[[resolved_rules]]
id = "DSET-RULE-TEST-PLAN"
path = "dset/scopes/meta/governance/test-planning.md"
sha256 = "d35e335fffe73396cc29e7f3d5b268c8a44f249bb8a8426126b8ca15322884b4"

[[resolved_rules]]
id = "DSET-RULE-WORK-ITEMS"
path = "dset/scopes/gov/governance/work-items.md"
sha256 = "61447c22741684e20014f41a1072cdbabba0701779021f11bd6a4dd78731544a"
+++

# External review packet

Review only the exact commit, input digests, rules, scope, and criteria in the envelope. Return a report; do not edit the project or authorize repair.
