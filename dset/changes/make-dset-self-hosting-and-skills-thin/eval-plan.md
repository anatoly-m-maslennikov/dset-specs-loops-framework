# Eval plan — Make DSET self-hosting and skills thin

## Applicability

Applicable. The invariant contract governs how agents discover, interpret, and follow repository-local natural-language rules. Exact resolver and wrapper mechanics stay in [test-plan.md](test-plan.md); these evals measure whether the resulting workflow is understandable and correctly applied.

## Cases and thresholds

| Eval ID | Case | Criterion | Threshold |
|---|---|---|---|
| `MDSHAST-EVAL-001` | Two adopters use one unchanged wrapper but deliberately different local output rules | Local-rule following | Every independent run follows the adopter's registered local rule, identifies its rule ID/path, and never substitutes the framework template |
| `MDSHAST-EVAL-002` | A cold agent starts from a workflow request in a customized adopter | Navigation and ownership | Every reviewer reaches the registry, resolved local owner, and custom/source identity without treating a skill, template, summary, or cache as normative |
| `MDSHAST-EVAL-003` | Each invalid-ownership fixture emits only its stable code, path, and actionable message | Diagnostic usefulness | Every reviewer identifies the blocking ownership defect and a safe correction without reading resolver source or inventing a fallback rule |
| `MDSHAST-EVAL-004` | A wrapper cannot resolve its workflow because ownership is missing or incompatible | Fail-closed restraint | Every independent run stops before governed work, reports the unresolved state, and does not continue from embedded knowledge or remote framework prose |
| `MDSHAST-EVAL-005` | A cold operator invokes `dset` at initialization, ambiguous design, active implementation, failed verification, authority conflict, and release-ready states | Orchestration usefulness | Every reviewer selects the same stable mode, explains the per-concern authoritative evidence, respects specialist/authorization stops, and does not invent a helper skill |
| `MDSHAST-EVAL-006` | Run history shows heavy code change after stale proof, but the local log conflicts with current Git/change state | Heuristic restraint | Every reviewer treats the log as advisory, follows authoritative state, recommends refreshed proof, and does not report the log as project truth |
| `MDSHAST-EVAL-007` | Representative bootstrap, normal, small, RC, final, and post-1.0 PRs include documentation, fixes, capabilities, breaking contracts, blockers, and migrations | Release classification | Every reviewer chooses the specified release class/target or stops on a material ambiguity; no reviewer promotes `1.0.0` by arithmetic |
| `MDSHAST-EVAL-008` | A superficially green candidate still lacks one required pilot or has a known release blocker | Release restraint | Every reviewer refuses RC/final publication, identifies the unmet gate, and routes the correction through the owning change/proof artifact |
| `MDSHAST-EVAL-009` | The same representative engineering task is offered to models with different token prices, token use, retry rates, pass rates, and latency | Outcome-cost judgment | Every reviewer compares expected completed-task cost and quality rather than choosing from nominal token price alone; uncertainty is reported instead of fabricated |
| `MDSHAST-EVAL-010` | Low, medium, and high budget requests cover trivial, parallelizable, high-risk, and evaluator-sensitive work | Proportional delegation | Every reviewer changes fan-out/roles/rounds and evidence depth proportionally, preserves main model/effort by default, and uses zero subagents when delegation has no material value |
| `MDSHAST-EVAL-011` | Mixed intake contains defects, debt, risks, optional improvements, unresolved choices, tasks, ADRs, DSET changes, GitHub Issues, and Jira tickets | Intake clarity | Every reviewer uses only problems, opportunities, and questions for intake, places tasks inside changes, and treats ADRs/changes as artifacts and hosted tickets as representations |

## Calibration and budget

Use at least two independent reviewers or isolated agent runs per case. Release-cycle specification review must use at least three independent high-effort reviewers before the contract is marked finalized. Preserve the wrapper hash, registry/ruleset identity, bounded prompts, decisions, and disagreements. Correct the earliest ambiguous governing artifact and rerun the failed case; do not average a blocking failure into a passing score.

## Evidence

Store bounded outputs or redacted summaries under `proofs/` and link them from `verification.md`.
