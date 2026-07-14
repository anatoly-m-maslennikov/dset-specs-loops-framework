# Contract delta — Distribution, platform, dependencies, and hosted delivery

Contracts define externally observable conformance boundaries. They are not
Decisions: a Decision records a choice and its rationale, while a Contract states
the interface, compatibility, provenance, or hosted behavior an implementation
must satisfy.

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
