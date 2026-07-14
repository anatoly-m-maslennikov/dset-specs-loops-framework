# Contract delta — Work Areas, distribution, platform, dependencies, and hosted delivery

Contracts define externally observable conformance boundaries. They are not
Decisions: a Decision records a choice and its rationale, while a Contract states
the interface, compatibility, provenance, or hosted behavior an implementation
must satisfy.

## ADDED — DSET-CONTRACT-META-001 Repository Work Area declaration

| Field | Contract value |
|---|---|
| Authority | Accepted DSET methodology META package; each adopting repository owner supplies that repository's conforming declaration |
| Source | `DSET-REQUIREMENT-META-011` and this Contract record |
| Record version | `1.0` |
| Direction | Repository scope declaration → DSET artifacts, workflows, proof, runs, and handoffs |
| Producer | Adopting repository owner or authorized project governance writer |
| Consumer | DSET lifecycle, Change, proof, supportability, and session-continuity consumers |
| Conformance rule | Declare either repository-level scope or one or more existing repository-relative folders as Work Areas; allow local, deployable, library, documentation, methodology, data, and mixed content without requiring code or deployability; require scope-dependent consumers to resolve the current declaration |
| Compatibility rule | Content changes inside a Work Area do not change the boundary; a path rename, removal, or scope split/merge requires an explicit reviewed declaration update and refresh of affected references and evidence. Legacy or simple repositories may remain one repository-level scope |
| Lifecycle state | `active` |

Session continuity may store a bounded reference to a Work Area, but this
Contract and the adopting repository's accepted declaration remain authoritative.
A checkpoint cannot create, rename, reclassify, or supersede the boundary.

## ADDED — DSET-CONTRACT-SKILL-001 Host-native skill distribution

Every declared Claude, Codex, or other supported agent host must receive a real,
installable host-native skill artifact generated or linked from the canonical
wrapper source. Proof must install or link the artifact in a clean supported-host
fixture, load it through that host's actual discovery mechanism, invoke its
declared trigger, resolve the repository-local workflow, and observe the expected
handoff and stop boundary. Markdown structure checks or source-tree presence alone
do not satisfy this contract.

**Scenario DSET-SCENARIO-SKILL-009:** A clean Codex fixture discovers and invokes
the installed `dset` wrapper, reports the resolved local workflow and ruleset, and
stops at the declared authorization boundary without reading a copied normative
rule from the installation.

## ADDED — DSET-CONTRACT-TOOL-001 Declared platform compatibility

Published scripts and utilities must work on macOS, native Windows, WSL, and Linux
when those platforms are declared supported. A narrower implementation is valid
only when the artifact records its exact applicability and the product does not
claim broader support. Proof must exercise real platform-native path, process,
shell, encoding, temporary-file, and exit-status behavior; syntax review on one
platform is insufficient.

**Scenario DSET-SCENARIO-TOOL-008:** The same public verification entry point runs
in clean macOS, native Windows, WSL, and Linux jobs, or an unsupported platform is
rejected by the published applicability contract before any partial write.

## ADDED — DSET-CONTRACT-TOOL-002 Dependency provenance and exceptions

Every distributable tool or generated host artifact must resolve dependencies
through an explicit allowlist/denylist contract that records exact package names,
versions or constraints, registries, retained licenses, provenance, and lockfile
authority. An exception must name its approving authority, reason, bounded scope,
and expiry or review date. Deterministic proof must reject unapproved registries,
denied packages, unpinned or lockfile-divergent resolution where pinning is
required, missing/incompatible licenses, stale exceptions, and provenance drift.

**Scenario DSET-SCENARIO-TOOL-009:** Introducing a package from an unapproved
registry or allowing an exception to expire fails before publication with the
package, registry, governing rule, and required correction identified.

## ADDED — DSET-CONTRACT-OPS-001 Hosted protected-delivery evidence

CI conformance requires real GitHub Actions workflow artifacts and run/check
evidence for the actual pull-request SHA integrated through the configured
protected branch. The proof must bind workflow file, run ID and URL, check name and
conclusion, repository, PR, head SHA, protected target, ruleset/required-check
state, and resulting merge or blocked disposition. Local scripts, mocked payloads,
or specification prose alone do not satisfy this contract.

**Scenario DSET-SCENARIO-OPS-012:** For the implementing PR head, an operator can
resolve the committed workflow to the exact GitHub run and required check, verify
that the checked SHA matches the PR head, and confirm that protected integration
either accepted that evidence or blocked the merge without a bypass.

## ADDED — DSET-CONTRACT-OPS-002 Integration-first delivery topology

| Field | Value |
|---|---|
| Authority | Project release and Change contract in `dset/scopes/meta/dset.yaml` |
| Source | Schema 1.2 project and Change workspace declarations |
| Version or digest | `1.2` |
| Direction | Local integration branch to remote integration branch to protected release PR; optional isolated Change branch/worktree to integration branch first |
| Producer | Contributor or governed automation writing the declared Change workspace |
| Consumer | Review, traceability, release preparation, hosted CI, and archival |
| Conformance | Default `integration-branch`; optional explicit `branch-worktree`; configured branch roles; no permanent layer branches; separate Change identity, scope, authorization, and proof in either mode |
| Compatibility | Archived branch-worktree Changes remain valid; changing configured branch roles or a Change's selected mode requires refreshed affected evidence |
| Lifecycle | `active` |
