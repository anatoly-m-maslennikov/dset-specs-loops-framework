# Artifact governance rationale

## Why artifact profiles are separate

Programming-language profiles enforce code with language-native compilers, type checkers, linters, tests, and thresholds. Knowledge artifacts fail differently: duplicated authority, missing rationale, mixed document purposes, broken hierarchy, weak navigation, stale history, and definitions that depend on concepts not yet introduced. Calling documentation another language would hide these distinct failure modes and incorrectly apply code rules to prose.

## Why hubs stay thin

Repositories with many files need a helicopter view, but exhaustive hand-maintained indexes become stale and bury ownership. The [hub rules](hub-rules.md) require root and area hubs to route readers to stable owners. Machine-readable area configuration and link validation provide structural completeness; the hub body remains curated for human orientation.

## Why what, why, how, and history separate

Normative rules change when accepted behavior changes. Rationale changes when the explanation or trade-off understanding changes. Procedures change when an operation changes. Evidence and changelogs are historical observations. The [artifact-type catalog](artifact-types.md) assigns each of these a separate owning question. Combining them makes a document hard to review and encourages a historical explanation or one-time command to become accidental current truth.

The separation is not absolute isolation. The artifacts link bidirectionally where useful, but only one owns each concern.

## Why atomic rationale is optional

A Decision is easier to review, investigate, and replace when its reasoning is
preserved, so every Decision template prompts for a concise rationale. The same
context can help with other atomic artifacts, especially when their scope,
priority, interpretation, or relationship is not obvious. Making rationale a
universal validity gate would reward placeholder prose and would make simple
facts, deterministic run records, and self-explanatory atoms unnecessarily
ceremonial. DSET therefore recommends rationale, validates a supplied structured
value, and accepts a missing one. Normative behavior, lifecycle state, and
evidence still belong to their typed owners.

## Why semantic ordering matters

A reader or agent should be able to build the domain model incrementally. The [specification authoring rules](authoring-rules.md#specifications) require definitions to use earlier vocabulary. When an entity definition depends on a later undefined entity, a forward link provides navigation but not meaning. Defining entities first and then describing later connections produces specifications that can guide implementation and proof without hidden context.

## Why some gates remain evals

Schemas can prove that hubs, owners, parents, and links exist. They cannot reliably prove that rationale is sufficiently separated, a lifecycle is complete, or a definition is understandable. Pretending otherwise creates keyword-driven compliance. DSET automates stable structural signals and evaluates semantic quality with explicit cases and thresholds.

## Adaptation source boundary

This design adapts general patterns already used in the author's knowledge-governance system: thin hubs, current-rule ownership, separate rationale and playbooks, one structural parent, and validation of the navigation tree. The public framework re-expresses those ideas in DSET terminology and portable GitHub Markdown; it does not expose private paths, Obsidian-only links, backlink queries, or vault-specific taxonomy.
