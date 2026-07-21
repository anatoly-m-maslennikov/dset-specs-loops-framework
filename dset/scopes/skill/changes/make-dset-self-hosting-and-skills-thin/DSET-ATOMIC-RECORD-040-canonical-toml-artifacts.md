+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-040"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-GOV-036"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "TOML is the canonical encoding for DSET-owned structured artifacts and DSET Markdown frontmatter, with explicit generated or host-mandated format boundaries."
promotion = {}
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "TOML makes configuration and artifact metadata easier to scan and removes indentation-dependent authority from DSET-owned structured files."

[scope]
kind = "project"
id = "dset-specs-loops-framework"
+++

# Requirement — Use canonical TOML artifacts

DSET-owned structured artifact files must use TOML. Markdown artifacts remain
Markdown but use TOML frontmatter. Root `dset.toml` must document every
operator setting, valid value, behavioral effect, and reasonable default in
the file itself.

One canonical source must not coexist with an editable YAML or JSON copy.
Externally prescribed carriers may retain their required format: host skill
metadata, GitHub Actions, ecosystem manifests and lockfiles, wire/CLI output,
and machine-local runtime journals. Interoperable JSON Schema files may be
generated from canonical DSET schema sources, but generated adapters are not
authority and must pass freshness checks.

Migration must be deterministic and dry-run-first. It must inventory every
source and reference, preserve values and stable IDs, emit an old/new digest
map, refuse collisions and unsupported values, rewrite repository references,
validate the complete migrated tree before cutover, and leave no writable
YAML/JSON DSET authority behind. Legacy read compatibility, if retained for an
adopter transition, must be explicit and must never become a write path.

## Rationale

TOML makes scalar, list, and table boundaries explicit without using
indentation as structure. Explicit external-format exceptions preserve host
and ecosystem compatibility without allowing adapters to become a second
source of truth.

This emitted Requirement atom is immutable. Later correction requires a
successor and append-only lifecycle event.
