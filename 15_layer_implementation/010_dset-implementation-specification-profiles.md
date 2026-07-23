# Implementation Profile selection

## Role

An Implementation Profile is a versioned feature of the IMPL layer. It defines
concrete, inspectable rules for setting up the development environment, writing
code, implementing Tests and Evaluations, and applying code-focused gates for
one implementation family. It is not a universal engineering standard and does
not become authority merely because a language or framework name matches.

## Selection

A project may select any number of compatible Implementation Profiles. Every
selection names the profile identity and the declared implementation work
areas to which it applies. A work area may select more than one profile only
when their rules are compatible; an unresolved collision stops implementation.

Profiles are composable by explicit selection, not inheritance by directory
accident. A host-specific profile may extend a broader runtime profile while
owning only the additional constraints. For example, a future Obsidian plugin
profile may extend an Electron/TypeScript application profile without copying
its baseline rules.

An artifact-specific profile may also be mandatory by accepted Requirement.
When work creates or updates an artifact in that profile's declared scope, the
profile applies even if a caller did not remember to select it interactively.
Project settings declare the work areas that currently realize the profile;
the accepted Requirement owns the create/update gate.

Canonical profile rules are provider neutral. Provider, model, host, operating
system, and installation differences belong in explicit adapters and claimed
compatibility matrices. One passing adapter never proves another, and a
missing adapter narrows the supported matrix rather than changing the profile
semantics.

## Profile contents

Every profile defines:

- its stable ID, version, implementation family, scope, and exclusions;
- machine-readable code thresholds, switches, and verification rule identities;
- layout, boundary, portability, failure, and supportability expectations that
  are implementable within its scope;
- compatibility or extension relationships with other profiles; and
- the conditions under which a project must select a different profile.

Profiles for agent-authored behavior additionally define trigger/isolation
assurance, provider/host/model evidence boundaries, and deterministic gates
that run whenever the governed artifact is created or updated.

The prose specification explains intent and edge cases. Its TOML carrier owns
the selected machine values. Neither may silently broaden the profile beyond
its declared scope.

## Layer boundary

IMPL turns accepted upstream truth into environment, code, Test, Evaluation,
and code-gate rules. TOOL still owns the DSET executable's behavior and
repository-governance machinery; OPS owns CI, release, publication, and runtime
configuration. OPS then evaluates and operates the resulting implementation.
It must not retroactively redefine an Implementation Profile; an operationally
discovered deficiency is routed to a new or corrected upstream artifact and a
later implementation.
