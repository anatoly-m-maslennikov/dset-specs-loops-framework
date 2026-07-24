+++
artifact_type = "analysis_report"
artifact_subtype = "technical_investigation"
artifact_id = "DSET-ANALYSIS-REPORT-001"
priority = "high"
child_of = ["DSET-EVAL-PLAN-TOOL-003"]
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
+++

# Analysis report — clean-upstream TypeScript boundary

## Question

Which parts of the OYOHA-derived `typescript-v1-candidate` are reusable
TypeScript framework policy, and which are applied evidence or product policy
that each adopter must own locally?

## Compared subjects

- OYOHA through `badbd69b5e8b6e847fc096a21db1c8fab3fb194b`.
- Clean upstream Claudian commit
  `783df1ceb149ac9cd9a00a3444c3dadf83bbacf4`.
- DSET runtime through `581714c`.

Claudian was inspected through a detached sparse worktree and an isolated
disposable copy. No DSET file was written to the upstream checkout, and no
upstream remote operation was attempted.

## Boundary

| Classification | Generalizes | Remains project-local |
|---|---|---|
| Gate model | Six neutral categories; enforced, ratcheted, blocked, and not-applicable states; zero hard-error rule | Which gates apply, their owners, commands, thresholds, reasons, and blocker IDs |
| Toolchain | Read package-manager/lock/runtime contracts from the target; use target-owned typecheck, lint, test, and isolated-build scripts | Runtime range, package manager, lockfile, exact script strings, required files, source/test roots, and generated outputs |
| Evidence | Read-only structural inspection; exact revision binding; environment failures stay separate from product baselines | Repository/license/revision, file population, warning counts/rules, CI topology, observations, and validity window |
| Static analysis | Syntax-aware boundary enforcement and shrink-only debt ratchets | OYOHA's complexity `15`, function-size `80`, warning inventory, Obsidian rules, provider/UI boundaries, and brand vocabulary |
| Delivery and safety | Hosted proof and secret hygiene must be explicit before promotion | Workflow paths/jobs/actions, full-history scanner selection, artifact composition, redaction, and supportability implementation |
| Governance | Skills resolve only the adopter's local registry and rules | OYOHA architecture, chat, provider, style, release, supportability, and product-spec owners |

The direct framework template is therefore a pinned **candidate reference**, not
a ready-to-install universal TypeScript profile. Its schema and neutral
categories generalize; an adopter must instantiate the applied fields from its
own repository evidence. Promotion must not replace those fields with OYOHA
values or mechanically transfer OYOHA thresholds.

## Claudian observations

The exact upstream revision uses the same Node/npm/TypeScript/ESLint/Jest/build
script family and the same broad source/test roots. Its scoped `CLAUDE.md`
files own product architecture and design guidance; it has no DSET control
plane. A dry run and then an isolated execution of `dset init` produced a valid
schema 1.2 project, detected active hosted automation, selected applicable
supportability, and resolved an independent unmodified `core-v1` ruleset.

The framework's OYOHA-pinned profile rejected Claudian only for the expected
exact-revision and file-population differences. On the isolated copy,
typecheck and lint passed with zero errors; upstream has no OYOHA complexity
ratchet, so it also produced zero warnings. The build passed. Of 5,754 Tests,
5,744 passed and ten were host-blocked: one attempted a home-directory temp
write and nine required a local listening socket. The host used Node 26.5.0,
not the declared Node 24 range, so these executions are comparative evidence,
not promotion evidence.

## Conclusion

Keep `typescript-v1-candidate`. The clean-upstream half of the comparison is
now executed, but promotion still requires a project-instantiation boundary,
an eligible Node 24/hosted run, a complete OYOHA candidate run, and a fresh
independent reviewer convergence result at one exact revision.
