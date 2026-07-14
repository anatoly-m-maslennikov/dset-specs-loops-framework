# Eval plan — Make DSET self-hosting and skills thin

## Applicability

Applicable. The invariant contract governs how agents discover, interpret, and follow repository-local natural-language rules. Exact resolver and wrapper mechanics stay in [test-plan.md](test-plan.md); these evals measure whether the resulting workflow is understandable and correctly applied.

## Comparison controls

- **Comparator/baseline:** accepted package and registered local-rule behavior
  at the candidate base commit, or an explicit case-specific baseline.
- **Environment and versions:** record candidate commit, operating environment,
  DSET/tool version, wrapper and ruleset identities, and effective
  model/reviewer configuration for every run.
- **Freshness window:** evidence is current only for those identities and must
  be reopened when a named input, governing rule, fixture, or hosted state
  changes.
- **Budget:** use the declared delegation profile plus the case-specific limits
  below; preserve actual run count, token/cost data when available, and elapsed
  time without treating nominal token price as completed-task cost.
- **Abstain/inconclusive:** stop and record `inconclusive` when evidence cannot
  distinguish remaining outcomes, identities are unverified, or reviewers
  disagree on a blocking criterion after one clarification/rerun. Never average
  a blocking failure or abstention into a pass.

Results remain criterion- and context-specific. This plan does not compute a
universal winner score across rule following, usability, cost, restraint,
platforms, or delivery contexts.

## Cases and thresholds

| Eval ID | Case | Criterion | Threshold |
|---|---|---|---|
| `DSET-EVAL-TOOL-001` | Two adopters use one unchanged wrapper but deliberately different local output rules | Local-rule following | Every independent run follows the adopter's registered local rule, identifies its rule ID/path, and never substitutes the framework template |
| `DSET-EVAL-TOOL-002` | A cold agent starts from a workflow request in a customized adopter | Navigation and ownership | Every reviewer reaches the registry, resolved local owner, and custom/source identity without treating a skill, template, summary, or cache as normative |
| `DSET-EVAL-SKILL-002` | Each invalid-ownership fixture emits only its stable code, path, and actionable message | Diagnostic usefulness | Every reviewer identifies the blocking ownership defect and a safe correction without reading resolver source or inventing a fallback rule |
| `DSET-EVAL-GOV-009` | A wrapper cannot resolve its workflow because ownership is missing or incompatible | Fail-closed restraint | Every independent run stops before governed work, reports the unresolved state, and does not continue from embedded knowledge or remote framework prose |
| `DSET-EVAL-SKILL-003` | A cold operator invokes `dset` at initialization, ambiguous design, active implementation, failed verification, authority conflict, and release-ready states | Orchestration usefulness | Every reviewer selects the same stable mode, explains the per-concern authoritative evidence, respects specialist/authorization stops, and does not invent a helper skill |
| `DSET-EVAL-SKILL-004` | Run history shows heavy code change after stale proof, but the local log conflicts with current Git/change state | Heuristic restraint | Every reviewer treats the log as advisory, follows authoritative state, recommends refreshed proof, and does not report the log as project truth |
| `DSET-EVAL-SKILL-005` | Representative bootstrap, normal, small, RC, final, and post-1.0 PRs include documentation, fixes, capabilities, breaking contracts, blockers, and migrations | Release classification | Every reviewer chooses the specified release class/target or stops on a material ambiguity; no reviewer promotes `1.0.0` by arithmetic |
| `DSET-EVAL-OPS-006` | A superficially green candidate still lacks one required pilot or has a known release blocker | Release restraint | Every reviewer refuses RC/final publication, identifies the unmet gate, and routes the correction through the owning change/proof artifact |
| `DSET-EVAL-SKILL-006` | The same representative engineering task is offered to models with different token prices, token use, retry rates, pass rates, and latency | Outcome-cost judgment | Every reviewer compares expected completed-task cost and quality rather than choosing from nominal token price alone; uncertainty is reported instead of fabricated |
| `DSET-EVAL-SKILL-007` | Low, medium, and high budget requests cover trivial, parallelizable, high-risk, and evaluator-sensitive work | Proportional delegation | Every reviewer changes fan-out/roles/rounds and evidence depth proportionally, preserves main model/effort by default, and uses zero subagents when delegation has no material value |
| `DSET-EVAL-GOV-010` | Mixed intake contains defects, debt, risks, improvements, unresolved choices, tasks, Decisions, DSET Changes, hosted tickets, and examples from all five stable layers | Intake clarity | Every reviewer uses only problems, opportunities, and questions for intake, treats Decision as the entity and Decision record as its canonical artifact, places tasks inside Changes, treats hosted tickets as representations, and uses only `META`, `GOV`, `TOOL`, `SKILL`, or `OPS` in canonical IDs |
| `DSET-EVAL-SKILL-009` | A cold operator receives clean declared Claude/Codex/other-host fixtures and the published installation path | Host-native usability | Every operator installs or links the real skill, confirms host discovery, invokes its trigger, reaches the project-local workflow, and identifies the stop boundary without editing the wrapper or copying governing rules |
| `DSET-EVAL-TOOL-005` | Operators run the same utility workflow on macOS, native Windows, WSL, and Linux, including spaces, Unicode, failures, and interrupted writes | Platform usefulness | Every supported platform produces equivalent safe outcomes; any narrower applicability is visible before execution and is not misrepresented as cross-platform support |
| `DSET-EVAL-TOOL-006` | Reviewers assess an allowed dependency, a denied package, an unknown registry, an incompatible license, provenance drift, and an expired exception | Dependency-governance usefulness | Every reviewer reaches the same accept/stop result, identifies the authoritative lockfile/rule and exception authority, and does not invent approval from package popularity or prior memory |
| `DSET-EVAL-OPS-008` | A cold operator investigates the implementing PR's live GitHub workflow/run/check and protected-target state | Hosted delivery usefulness | Every operator binds the evidence to the actual PR SHA, distinguishes local proof from hosted authority, and selects the safe merge/block/retry action without bypassing protection |
| `DSET-EVAL-META-008` | Reviewers compare measurable state changes with features, outputs, milestones, ambiguous proxies, and incomplete baseline/target claims | Outcome clarity | Every reviewer identifies the measurable state change, baseline, target, source/method, and window; preserves relevant links or explicit non-applicability; and never relabels an output as an Outcome |

## Calibration and budget

Use at least two independent reviewers or isolated agent runs per case. Release-cycle specification review must use at least three independent high-effort reviewers before the contract is marked finalized. Preserve the wrapper hash, registry/ruleset identity, bounded prompts, decisions, and disagreements. Correct the earliest ambiguous governing artifact and rerun the failed case; do not average a blocking failure into a passing score.

## Evidence

Store bounded outputs or redacted summaries under `proofs/` and link them from `verification.md`.
