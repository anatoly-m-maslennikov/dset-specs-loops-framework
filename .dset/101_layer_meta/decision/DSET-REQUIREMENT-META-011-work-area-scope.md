+++
artifact_id = "DSET-ATOMIC-RECORD-280"
semantic_id = "DSET-REQUIREMENT-META-011"
revision_mode = "atomic"
content_role = "definition"
governance_locus = "internal"
scope_path = ["layer:meta"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET supports repository-level scope or declared repository-relative Work Areas without assuming code, deployability, service, feature, module, or architecture type."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Monorepos and mixed repositories need bounded governance without forcing every governed folder into a software-service taxonomy."
+++

# Requirement — Work Area scope

A Work Area may contain local tools, deployable services, libraries,
documentation, methodology, data, or mixed content. Repository governance owns
the declaration; session continuity may reference it but cannot redefine it.
