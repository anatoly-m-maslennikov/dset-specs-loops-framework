# IMPL — Implementation Profiles

## Purpose

Own concrete, selectable profiles for setting up a development environment,
writing production and automated-test code, implementing evaluations, and
running code-focused quality gates. Profiles are features within this layer,
and a project may select more than one for different work areas.

## Layer flow

`META → GOV → TOOL → SKILL → IMPL → OPS`

IMPL consumes the accepted workflow and tool contracts, then governs how code
realizes them. OPS consumes the resulting implementation for delivery, release,
operation, investigation, recovery, and publication evidence.

## Current features

- `local-python-tools-v1` — small local Python command-line tools, scheduled
  utilities, repository automation, and single-host workers.

## Boundaries

This layer currently defines no language-neutral engineering standard. Each
profile owns only its declared implementation scope. Shared rules may be
factored out only after accepted profiles demonstrate a genuinely common
contract.

Implementation Profiles follows SKILL and precedes OPS. It does not define
project artifact semantics, agent skill behavior, framework CLI behavior, or
post-implementation operational truth. Profile-selected development
configuration belongs here; repository-governance machinery stays in TOOL and
delivery/runtime configuration stays in OPS.

## Start here

- `010_dset-implementation-specification-profiles.md`
- `030_dset-implementation-specification-methodology.md`
- `000_dset-implementation-local-python-tools-hub.md`
- `000_dset-implementation-python-hub.md`
- `000_dset-implementation-tests-hub.md`
- `000_dset-implementation-evaluations-hub.md`
- `000_dset-implementation-schemas-hub.md`
- `000_dset-implementation-templates-hub.md`
