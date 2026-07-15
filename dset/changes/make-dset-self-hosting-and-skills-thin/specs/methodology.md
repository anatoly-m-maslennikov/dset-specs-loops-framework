# Methodology delta — DSET 0.2 invariants

## ADDED — MDSHAST-REQ-001 Framework-first release applicability

A DSET version may release a capability only after this repository adopts it under every applicable selected profile. A profile-specific capability that is not applicable to this repository must pass through a versioned in-repository adopter fixture before an external pilot may depend on it.

**Scenario MDSHAST-SCN-001:** A TypeScript-only gate is not applied to Python sources, but its versioned adopter fixture must pass before the gate can be presented to Your Harness as released DSET behavior.

## ADDED — MDSHAST-REQ-002 Self-hosting terminates at a fixed point

The self-hosting release gate must have exactly three bounded levels: the last released validator checks the candidate change, the candidate checks this repository, and the candidate materializes and checks one temporary adopter. The temporary adopter must not recursively create another adopter.

**Scenario MDSHAST-SCN-002:** A candidate run records released-to-candidate, candidate-to-repository, and candidate-to-temporary-adopter results, then terminates without discovering or traversing unrelated nested `dset/` roots.

## ADDED — MDSHAST-REQ-003 Local governing documents own selected rules

Every selected normative rule must resolve to one editable governing document inside the adopting repository. Framework templates may seed that document, but the materialized local document becomes authoritative and the template remains provenance rather than a live fallback.

**Scenario MDSHAST-SCN-003:** After materialization, editing the framework template does not change the adopter's resolved rule set; editing the registered local governing document does.

## ADDED — MDSHAST-REQ-004 Skills remain thin wrappers

A DSET skill may own trigger metadata, repository/root discovery, workflow identity, resolver invocation, rule-set reporting, output handoff, authorization boundaries, and stop behavior. It must not own substantive workflow, architecture, authoring, proof, threshold, safety, or supportability rules.

**Scenario MDSHAST-SCN-004:** Static inspection finds the `domain-clarification` workflow ID and resolver handoff in `dset-clarify` but no copied checklist, concrete threshold, or embedded fallback procedure.

## ADDED — MDSHAST-REQ-005 Unchanged wrappers apply changed local rules

Wrapper behavior must depend on the resolved repository-local rule set rather than copied or cached normative prose. A local rule change must affect the next invocation without modifying the canonical wrapper.

**Scenario MDSHAST-SCN-005:** Two otherwise identical adopters use the same wrapper hash but define different registered output conventions; each invocation follows its own local convention and reports the corresponding rule identity.

## ADDED — MDSHAST-REQ-006 Invalid selected ownership fails closed

Missing, duplicate, cyclic, outside-root, or profile-incompatible selected rule ownership must stop before governed work begins and emit a stable diagnostic. A rule or profile explicitly marked not applicable with a valid reason must remain a successful disposition rather than being converted into a failure.

**Scenario MDSHAST-SCN-006:** A selected rule pointing outside the repository stops with its stable code and path, while an unselected TypeScript profile in a documentation-only adopter passes as justified not applicable.

## ADDED — MDSHAST-REQ-007 Customization identity remains honest

A locally changed materialized rule set remains valid project truth but must identify itself as local/custom and retain its source profile/version provenance. It must not claim byte-equivalence to the unchanged framework profile.

**Scenario MDSHAST-SCN-007:** Changing one normative local rule changes the resolved ruleset identity to custom while preserving the originating framework profile and version as provenance.

## ADDED — MDSHAST-REQ-008 Proof categories remain separate

Exact resolver, ownership, path, identity, wrapper, and recursion behavior belongs to deterministic tests. Agent interpretation, rule-following, navigation, and diagnostic usefulness belong to qualitative or probabilistic evals. Automation does not move proof between categories.

**Scenario MDSHAST-SCN-008:** A scripted assertion that a cycle emits one code remains a test; an independent agent's ability to use that diagnostic to correct the governing document remains an eval even when the eval runner is automated.

## ADDED — MDSHAST-REQ-009 Every normative rule ID has one editable owner

Each normative rule ID must resolve to exactly one editable governing document. Agent instructions, skills, templates, generated installations, indexes, summaries, and caches may point to or reproduce derived metadata about the owner but must never become additional writable rule authorities.

**Scenario MDSHAST-SCN-009:** The registry rejects two governing documents claiming the same rule ID and accepts multiple navigation or generated surfaces that link to the single owner without restating its normative text.
