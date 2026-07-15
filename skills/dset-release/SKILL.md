---
name: dset-release
description: Prepare or verify a governed DSET release transaction and, only with separate explicit publication authority, publish it. Use for an explicit release request or a verified release-ready Change; stop on identity, gate, ownership, or authorization mismatches.
---

# DSET Release

This thin wrapper invokes the registered `release` workflow. Repository-local governing documents own all substantive release behavior; this wrapper supplies no release engine or publisher.

## Resolve and prepare

1. Locate the repository root by walking upward to schema 1.2 `dset/scopes/meta/dset.yaml` or legacy `dset/dset.yaml`; stop if neither or both authorities exist.
2. Run `dset rules resolve release --format json` or `python -m dset_toolchain rules resolve release --format json`.
3. Stop on any nonzero result. Never fall back to this wrapper, memory, templates, or remote framework prose.
4. Report the workflow ID, profile/version, registry and ruleset identities, customization, ordered rule IDs/paths, wrapper identity, and conflicts.
5. Through the available runtime adapter and resolved `DSET-RULE-SKILL-RUNS`, join a matching explicit session or start a bounded one; report session/run/persistence identity and obey its stop behavior when continuity is unavailable.
6. Read and apply the resolved documents in order. Prepare or verify only actions already authorized by them, refreshing Git, proof, and configured-forge state when those owners control the result.

## Stop and hand off

Stop on any mismatch, missing gate, identity collision, ambiguity, or newly required authority. Return prepared/verified state, diagnostics, session ID, and the next handoff. Publication requires separate explicit authority; never infer it from preparation, verification, or a release request, and never claim absent automation completed it.
