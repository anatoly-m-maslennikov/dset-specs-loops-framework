+++
artifact_type = "evidence_record"
artifact_subtype = "test_result"
artifact_id = "DSET-EVIDENCE-RECORD-013"
priority = "high"
child_of = ["DSET-REQUIREMENT-SKILL-011"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Test result — OYOHA local-rule cutover

**LLM session IDs:**
`codex:019f591f-04f6-70f2-8de7-828b7cccc69d`

## Subject and intended use

The owned OYOHA pilot through local `dev` commit
`badbd69b5e8b6e847fc096a21db1c8fab3fb194b`, using DSET runtime commit
`c9207f33b052bc757badf146e015fafd5b221789`. This record verifies that one
real adopter moved substantive engineering rules into its repository-local
governance registry while keeping agent-host files thin. It does not prove
native Codex or Claude installation or invocation. It provides real-adopter
evidence for `DSET-REQUIREMENT-SKILL-011`; the accepted compatibility Test
mappings remain `DSET-TEST-PLAN-SKILL-010` and `DSET-TEST-PLAN-GOV-017`.

## Result

OYOHA's root `AGENTS.md` and root/scoped `CLAUDE.md` files are navigation
surfaces. Six registered OYOHA rule documents own architecture, core-runtime,
chat, Claude-provider, Codex-provider, and style behavior. Repository-root and
nested `src/providers/codex` invocations of
`dset skills context --skill dset-implement` resolved the same local ruleset,
selected target-sensitive scope, and did not fall back to DSET framework rules
as project authority.

The candidate profile validates at the cited OYOHA descendant with zero
diagnostics and three explicit blocker Problems. DSET structure, rule-owner,
compiled-truth, trace, health, and diff checks pass. Generated health now lists
all seven open OYOHA Problems/Questions instead of reporting no unresolved
work.

## Boundaries and reopen conditions

Native-host discovery/invocation, clean upstream comparison, hosted results,
supportability, and legacy product-truth cutover remain open in OYOHA. Reopen
this result if its rule registry, rule bodies, host-navigation files, Work
Areas, shared runtime, or wrapper identity changes.
