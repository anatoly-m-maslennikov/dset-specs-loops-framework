# 06_External Grounding — LLM Power-User Practice

**Thesis:** The 00–05 tool-development standard is the production-grade complement to Karpathy-style Software 3.0 / vibe-coding practice: natural language becomes a high-leverage programming interface, but durable tools still need explicit specs, deterministic tests, probabilistic or qualitative evals where applicable, plans, architecture, safety chokepoints, and machine-verifiable gates. This note is the external grounding map, not a replacement for the stage docs.

---

## §1 | Source map

<details>

<summary>Power-user / research sources</summary>

| Source | What it grounds in these docs | Use it for |
|---|---|---|
| [Andrej Karpathy — Software 2.0](https://karpathy.medium.com/software-2-0-a64152b37c35) (2017) | Programming shifts from hand-written instructions to specifying desired behavior and optimizing against examples/evaluation. | The move from prose-only requirements to executable specs, datasets, evals, and gates. |
| [Andrej Karpathy — Software Is Changing (Again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ) (YC AI Startup School, 2025) | Software 3.0 / English-first programming: the developer increasingly states intent and steers agents rather than typing every line. | Why 00 starts with authored artifacts and why 03 treats implementation as supervised agentic execution. |
| [Simon Willison — Here's how I use LLMs to help me write code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) (2025) | Context management, exact instructions, tests, safe execution sandboxes, human takeover, and codebase Q&A are the practical craft of LLM-assisted coding. | 01 precise context, 02 tests, 03 plan/execute, 04 boring/stable dependencies, 05 agent ergonomics. |
| [Simon Willison — Not all AI-assisted programming is vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/) (2025) | Vibe coding is valuable for low-stakes learning/prototyping, but production AI-assisted development requires understanding, review, and tests. | The boundary between prototypes and durable tools; the reason these docs are stricter than “accept all”. |
| [Simon Willison — The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) (2025) | Agent risk spikes when private data access, untrusted content, and external communication combine. Prompt-only guardrails are insufficient. | 03 mode/role/kill-switch chokepoints, 04 fail-fast/error handling, 05 injection canaries and tool boundaries. |
| [Anthropic — Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) (live docs) | Give the agent a check it can run; explore first, then plan, then code; provide specific context; keep CLAUDE.md concise; use hooks/subagents/adversarial review. | Direct reinforcement for the whole 00→05 pipeline, especially 02 and 05. |
| [Addy Osmani — The 70% problem](https://addyo.substack.com/p/the-70-problem-hard-truths-about) (2024) | AI quickly gets to a plausible first draft, but the final production-grade slice depends on human judgment: architecture, edge cases, security, maintainability, and polish. | 04 small modules/typed seams/error handling and 05 gates as the “final 30%” discipline. |
| [Shreya Shankar et al. — PROMPTEVALS](https://arxiv.org/abs/2504.14738) (2025) | Production LLM pipelines need task-specific assertions/guardrails because models routinely miss developer intent at scale. | 02 eval assertions and 05 rules-as-tests. |
| [Shankar et al. — Who Validates the Validators?](https://arxiv.org/abs/2404.12272) (2024) | LLM-as-judge evals inherit failure modes and need human validation; criteria often drift as humans inspect outputs. | 02 evaluator calibration and 05 adversarial review / second-opinion gates. |
| [Galster et al. — Configuring Agentic AI Coding Tools](https://arxiv.org/abs/2602.14690) (2026) | Repository-level context files, skills, and subagents are becoming the configuration layer for coding agents; adoption is broad but shallow. | 05 directory-scoped AGENTS/CLAUDE files, reusable skills, and avoiding static-instruction-only workflows. |
| [dos Santos et al. — Configuration Smells in AGENTS.md Files](https://arxiv.org/abs/2606.15828) (2026) | Agent config files fail through context bloat, leaking irrelevant instructions, conflicting guidance, and lint leakage. | Keep 05 agent ergonomics compact, specific, and testable. |
| [Dai et al. — ABTest: Behavior-Driven Testing for AI Coding Agents](https://arxiv.org/abs/2604.03362) (2026) | Agent failures can be mined into repository-grounded behavior tests; coding agents need their own fuzzing/behavioral test layer. | 02 regression/pinning tests and 05 agent-specific gates. |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) — [overview](https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md), [writing specs](https://github.com/Fission-AI/OpenSpec/blob/main/docs/writing-specs.md) (2025–) | Delta-spec/change-folder/archive model: specs are current truth; changes are bounded work units with delta specs (`ADDED`/`MODIFIED`/`REMOVED`); archiving folds deltas back into truth. | 01 spec delta conventions, 03 change-folder packaging, and the pipeline notion that specs evolve through bounded, mergeable changes. |
| [superpowers](https://github.com/obra/superpowers) — [TDD](https://github.com/obra/superpowers/tree/main/skills/test-driven-development), [verification](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion), [subagent development](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) (2025–) | Stricter executable agent skills: red/green TDD evidence, verification-before-completion with fresh command output, and fresh-subagent implementation/review loops. | 02 test-plan and eval-plan rigor, 05 TDD/verification gates, and 05 subagent review workflow. |

</details>

## §2 | How the sources strengthen the 00–05 docs

<details>

<summary>Mapping to this folder</summary>

| Doc | External grounding to emphasize |
|---|---|
| `00_Tool Development Playbook.md` | Karpathy + Anthropic: natural-language programming raises the value of a stage pipeline; fast agentic implementation must be wrapped in spec → deterministic test plan plus applicable eval plan → implementation plan → implementation → gates. |
| `01_Spec Authoring Patterns — Service Spec Conventions.md` | Karpathy + Willison: “English as programming language” only works when intent is precise, context is explicit, examples are available, and non-goals are fenced. OpenSpec adds specs-as-current-truth and delta-spec changes that archive back into that truth. |
| `02_Test and Eval Plan Patterns — Proof Artifact Conventions.md` | Anthropic + Shankar + ABTest: give agents runnable checks, assertions, behavior tests, evaluator calibration, and pinning tests before trusting generated code. superpowers sharpens this into red/green evidence and verification-before-completion. |
| `03_Implementation Plan Patterns — Service Build Conventions.md` | Anthropic + Willison: explore first, plan second, implement third; use safe rungs, chokepoints, and human takeover for unfamiliar/high-risk areas. OpenSpec adds bounded change folders; DSET opens a draft PR early, archives after pre-merge verification inside that PR, and uses the stable PR identity to avoid a merge-SHA lifecycle cycle. |
| `04_General Build Rules — Tool Code Conventions.md` | Willison + Osmani: AI accelerates drafts, but maintainability comes from small modules, boring dependencies, explicit types, error handling, security review, and tests. |
| `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` | Anthropic + agent-config research: durable agent ergonomics need concise context files, deterministic hooks, subagents for isolated review, and gates that make correctness visible. superpowers adds strict red/green TDD evidence, completion evidence, and per-task subagent review. |

</details>

## §3 | Applied deltas in the 00–05 docs

<details>

<summary>Applied improvements</summary>

- **Separate test and eval plans for LLM-facing tools** — folded into `00_Tool Development Playbook.md` and `02_Test and Eval Plan Patterns — Proof Artifact Conventions.md`: deterministic checks stay in the test plan; LLM assertions, evaluator calibration, adversarial/drift cases, and budgets stay in the eval plan.
- **Agent can verify its own work** — folded into `01_Spec Authoring Patterns — Service Spec Conventions.md`, `02_Test and Eval Plan Patterns — Proof Artifact Conventions.md`, `03_Implementation Plan Patterns — Service Build Conventions.md`, `04_General Build Rules — Tool Code Conventions.md`, and `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` as runnable checks, milestone gates, and canonical verification commands.
- **Vibe coding vs production AI-assisted engineering** — folded into `00_Tool Development Playbook.md` as the prototype-vs-durable-tool boundary and into `04_General Build Rules — Tool Code Conventions.md` as generated-code-is-draft review discipline.
- **Context as a scarce runtime resource** — folded into `01_Spec Authoring Patterns — Service Spec Conventions.md` and `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` as context-budget hygiene for specs, AGENTS/CLAUDE files, and skills.
- **Skills/subagents/hooks must enforce a real workflow** — folded into `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` as workflow-bearing hooks/skills/subagents only.
- **Design against the lethal trifecta** — folded into `03_Implementation Plan Patterns — Service Build Conventions.md`, `04_General Build Rules — Tool Code Conventions.md`, and `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` as sandboxing, approval gates, logging, least privilege, and injection canaries.
- **Expect the 70% problem** — folded into `00_Tool Development Playbook.md` and `04_General Build Rules — Tool Code Conventions.md` as the reason to spend saved agent time on architecture, edge cases, verification, security, observability, and polish.
- **OpenSpec delta-spec/change-folder/archive model** — folded into `01_Spec Authoring Patterns — Service Spec Conventions.md` as a named spec-change pattern and into `03_Implementation Plan Patterns — Service Build Conventions.md` as change-folder packaging for implementation plans.
- **superpowers strict executable agent skills** — folded into `02_Test and Eval Plan Patterns — Proof Artifact Conventions.md` as red/green evidence, verification-before-completion, and subagent-review checkpoints; and into `05_Layered Build Standard — DDD, TDD, Small Functions, Typed Gates.md` as stricter TDD/verification/subagent gates.

</details>

## §4 | Citation hygiene

¶1 Prefer these sources as links/provenance, not long quotations. The docs should stay as a compact operating standard; third-party material belongs here as a map and in separate source notes if full local copies are needed later.

*Accessed: 2026-07-09; OpenSpec and superpowers local repo snapshots checked 2026-07-12.*
