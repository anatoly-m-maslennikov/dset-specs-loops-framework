+++
artifact_id = "DSET-ATOMIC-RECORD-177"
semantic_id = "DSET-REQUIREMENT-IMPL-003"
revision_mode = "atomic"
content_role = "definition"
governance_origin = "internal"
relation_shape = "standalone"
scope_path = ["layer:implementation"]
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Python module settings and constants are grouped immediately after module documentation and imports and each constant documents its responsibility, while a separate settings file remains optional."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Predictable placement makes operational limits and behavioral switches visible during first-pass reading, while mandatory per-constant explanations prevent names alone from hiding responsibility or interpretation."
promotion = {}

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-IMPL-001"
+++

# Requirement — Place and explain settings and constants

A separate TOML settings file is optional for a small local Python tool. When
operator-tunable or environment-specific values justify one, the tool uses a
typed settings model, loads one stable snapshot at its invocation boundary,
and injects it into owned logic.

Whether values are external or local, every Python module groups its
module-level settings, defaults, thresholds, and constants immediately after
the module docstring and imports and before classes, functions, or runtime
statements.

Every constant is self-documented at its declaration. Its explanation states
what it controls or is responsible for, its unit or interpretation when
relevant, and its authority or override boundary. Descriptive naming is still
required but does not replace the explanation.

Machine-enforced profile thresholds—including the exclusive function-line
limit of 40, which permits at most 39 measured lines—remain explicit settings
in the profile TOML and never become hidden checker literals.
