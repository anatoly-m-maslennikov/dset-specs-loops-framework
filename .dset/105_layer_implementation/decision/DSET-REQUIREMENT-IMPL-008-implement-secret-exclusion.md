+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-200"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-IMPL-008"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Every applicable Implementation Profile realizes DSET secret exclusion through environment-boundary loading, redaction, scanning, least privilege, short-lived credentials, and immediate revocation or rotation after exposure."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "A prose prohibition is insufficient unless implementations constrain every ingress, execution, diagnostic, build, assurance, and incident boundary through which secret material can be copied."

[scope]
kind = "layer"
id = "implementation"

[promotion]
affected_children = ["implementation"]
applies_unchanged = false
local_context_required = true

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-002"
+++

# Requirement — Implement secret exclusion

Each applicable Implementation Profile defines and enforces all of these
boundaries:

- load local-development secrets from ignored `.env` values at the outer
  runtime boundary, validate their presence without printing them, and inject
  only the minimum required value into the consumer;
- keep secrets out of source, TOML settings, command-line arguments, process
  titles, build arguments, images, caches, logs, exceptions, debug output,
  fixtures, snapshots, prompts, evidence, and generated artifacts;
- use platform or dedicated secret injection for CI and production, with
  least-privileged, attributable, revocable, and preferably short-lived
  credentials;
- redact before serialization or agent ingestion, and scan tracked and
  publishable surfaces for known and project-specific secret patterns;
- fail closed and name the missing variable or capability—not its value—when a
  required secret is absent or invalid; and
- after suspected exposure, stop further copying and make revocation or
  rotation the first remediation step before cleanup or history repair.

Non-secret emails, usernames, and account IDs may be documented when necessary.
Profiles still minimize them, avoid placing them in logs by default, and source
their mutable runtime values from the environment boundary.
