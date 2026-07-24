+++
artifact_id = "DSET-ATOMIC-RECORD-120"
semantic_id = "DSET-REQUIREMENT-GOV-049"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:gov"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The canonical dset_settings.toml owns project settings, structural roots, artifact classification, artifact areas, profiles, and other non-artifact registries without competing aggregate settings files."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
promotion = {}
+++

# Requirement — Keep one settings and catalog carrier

`dset_settings.toml` absorbs the active content of `artifact-types.toml`,
`artifacts.toml`, the governance registry, project/version configuration, and
other non-artifact registries. It does not absorb atomic claims or evergreen
specification prose.

The obsolete `legacy_evidence_paths` compatibility list is not carried into
the active catalog. Historical classification inputs remain in the explicit
root legacy archive when provenance requires them.

## Rationale

One verbose settings carrier makes selected behavior and structural ownership
reviewable without reconciling several mutable aggregate registries.
