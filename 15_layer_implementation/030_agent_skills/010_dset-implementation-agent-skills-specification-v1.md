# Agent Skills profile v1

## Scope

`agent-skills-v1` applies to reusable filesystem-based agent skills containing
`SKILL.md` plus optional scripts, references, assets, and host adapters. It
applies whenever a skill is created or updated. It does not define the
substantive domain rules wrapped by a skill and does not imply compatibility
with a provider or host that has not passed its declared adapter and Evaluation
matrix.

The reusable core is LLM-provider agnostic. Codex, Claude, Grok, Chinese model
providers, and future hosts may need different discovery, metadata,
installation, or invocation adapters. Those differences remain outside the
canonical workflow instructions and cannot redefine DSET semantics.

## Discovery and metadata

1. A skill directory contains `SKILL.md` with externally mandated YAML
   frontmatter. `name` and `description` are required.
2. The name is lowercase kebab-case, matches the directory, and is no longer
   than 64 characters. Use a concrete activity or capability name; avoid vague
   names such as `helper`, `utils`, or `tools`.
3. The description states both what the skill does and when it should be used.
   Put the highest-signal use case and natural trigger terms first. State
   important non-trigger boundaries when nearby skills could compete.
4. Discovery metadata remains concise because hosts preload it and may truncate
   or omit low-priority descriptions under catalog pressure.
5. Host-owned metadata, such as Codex `agents/openai.yaml`, is an adapter. A
   missing adapter limits the supported-host claim; it does not invalidate the
   host-neutral skill core.

## Instructions and progressive disclosure

1. `SKILL.md` owns routing, judgment, ordered workflow, authorization, safety,
   validation, and stop conditions. State each instruction once.
2. Keep the body below 500 lines and target materially less. Remove duplicated
   explanations, stale paths, repeated checklists, and generic advice the model
   already knows.
3. Put deterministic or fragile mechanics in scripts. Put large templates,
   examples, schemas, prompts, and reference material in focused `references/`
   or `assets/` files loaded only when a named condition applies.
4. References from `SKILL.md` are relative to the skill root and one level deep.
   Avoid chains in which one reference must be read merely to find another.
5. Match freedom to risk: use judgment-oriented prose when several approaches
   are valid, parameterized helpers when a preferred pattern allows variation,
   and exact scripts with narrow inputs for fragile operations.
6. The normal route is one short ordered sequence. Preserve load-bearing
   triggers, outputs, side effects, safety gates, overwrite rules, verification,
   and stop behavior during refactoring.

## Scripts, portability, and local state

1. Reusable helpers prefer dependency-light, self-documented Python using
   `pathlib`, direct subprocess argument arrays, platform-native temporary
   directories, and explicit UTF-8. Third-party dependencies are declared and
   fail with actionable installation guidance.
2. The core workflow must work on Linux, macOS, native Windows, and WSL unless
   the skill explicitly declares a narrower external Constraint. Do not rely on
   Bash, GNU-only tools, executable permission bits, symlinks, case-sensitive
   filesystems, LF-only input, `/tmp`, `~`, drive letters, or one shell's quoting.
3. Use placeholders, environment discovery, or project-local settings instead
   of absolute machine paths. A copy install must work even when a local author
   also uses symlinks.
4. Potentially damaging write helpers default to read-only or dry-run and
   require explicit apply/execute authority. Errors name the failed operation,
   target, cause, and safe remediation while redacting secrets.
5. Machine-local settings and logs use explicit local/runtime carriers and are
   excluded from the reusable package. Private assistant memory is never a
   runtime dependency.

## Security and trust

1. Treat an installed skill like executable software. Inventory scripts,
   commands, tools, filesystem access, network access, redirects, credentials,
   and external data flows before distribution.
2. Reject hidden behavior, safety bypasses, credential material, unbounded
   sensitive reads, undeclared network writes, or instructions that conceal
   actions from the operator.
3. A script's behavior must match the skill description and declared side
   effects. Security review is separate from output-quality Evaluation.

## Mandatory create/update workflow

1. Resolve the target skill and read `SKILL.md` plus adjacent files.
2. Inventory load-bearing behavior and the claimed host/model matrix.
3. Run the deterministic Agent Skills profile audit before editing.
4. Make the smallest contract-preserving change. Separate redesign from
   refactoring and record new authority before changing behavior.
5. Run the audit again, validate host metadata and scripts, and execute the
   required skill Evaluation cases.
6. Compare trigger coverage and `SKILL.md` size before and after. Do not accept,
   install, distribute, or publish a changed skill while a required gate fails.

## Evaluation contract

Every changed skill has at least three representative cases and covers the
dimensions that apply:

- should trigger;
- should not trigger;
- ambiguous or neighboring-skill routing;
- isolation without undeclared files or memory;
- coexistence without stealing another skill's trigger;
- instruction following, authorization, and stop behavior; and
- output quality against the skill's accepted purpose.

Run the matrix on each provider, host, and model configuration the project
claims. Record exact versions and effective configuration. A pass on one model
does not prove another. Preserve failed cases, calibrate automated judgment
against reviewed examples, and rerun the full affected matrix before promoting
a skill version.

## Sources

- [Open Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices)
- [OpenAI — Build skills](https://developers.openai.com/codex/build-skills)
- [Anthropic — Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic — Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
