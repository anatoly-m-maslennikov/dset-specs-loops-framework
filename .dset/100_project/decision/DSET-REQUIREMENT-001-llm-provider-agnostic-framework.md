+++
artifact_id = "DSET-ATOMIC-RECORD-194"
semantic_id = "DSET-REQUIREMENT-001"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = []
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET remains LLM-provider agnostic: its semantic model, governance, workflows, skill contracts, and evaluation methodology must work without depending on Codex, Claude, Grok, any Chinese model provider, or any other single host or model family."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Provider-neutral authority keeps DSET reusable as models and hosts change, while explicit adapters and capability declarations can preserve real host differences without turning one vendor into framework truth."
promotion = {}
+++

# Requirement — Keep DSET LLM-provider agnostic

DSET's canonical concepts and rules must use host-neutral language and must not
assume a particular model family, tool namespace, installation directory,
session identifier format, or proprietary invocation mechanism.

Provider- or host-specific packaging is allowed only in an explicit adapter or
compatibility surface. Each adapter declares supported capabilities,
limitations, installation shape, invocation proof, and any external host
Constraint. Unsupported behavior is reported honestly rather than approximated
through an undocumented vendor fallback.

Skill and Evaluation profiles must be usable across providers. Their assurance
matrices cover the providers, hosts, and model configurations the project
actually claims; they do not claim universal compatibility from one successful
Codex or Claude run.
