+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-166"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-IMPL-001"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "DSET provides and selects a concrete Local Python Tools profile covering environment setup, code, Tests, Evaluations, measurable gates, portability, and conditional diagnostic logging."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]

[scope]
kind = "layer"
id = "implementation"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-IMPL-001"
+++

# Requirement — Local Python Tools implementation profile

DSET must provide and select a concrete `local-python-tools-v1` Implementation
Profile for small local Python tools. It must directly define environment and
dependency setup, source structure, measurable limits, reuse rules, data
modeling, schema ownership, typed settings and constants, naming, docstrings,
failure behavior, portability, Test implementation, Evaluation implementation,
and conditional NDJSON diagnostic logging.

The function-size gate is hard and exclusive at 40 measured code lines: a
function may contain at most 39. All thresholds and behavioral switches live in
the profile TOML rather than being hidden in prose or checker code.

The profile must require only executable Python entrypoints at a tool's top
level; reusable modules live in an import package. Repeated package-local code
is extracted to shared modules or combined behind parameters. Classes,
dataclasses, protocols, abstract bases, and inheritance are used where they
express cohesive state or a stable shared contract and remove real boilerplate;
composition remains the default for replaceable I/O.

Pydantic owns validation at untrusted and serialized boundaries. Standard
dataclasses own trusted internal records when runtime validation is unnecessary.
Schemas remain separate from workflow and I/O code and have one authoritative
definition.

Every testable accepted claim and use case has explicit automated-test
coverage. Every fixed defect has a pinning regression test. Percentage coverage
supplements, but never replaces, semantic traceability.

Local NDJSON log emission is conditional. It is required for multi-step,
retrying, scheduled, externally effecting, or production-investigated tools,
and may be not applicable for a pure one-shot transform. When enabled, emitted
records are structured, correlated, redacted, bounded, and derived evidence;
they are not business-state authority or a mandatory WAL. OPS owns runtime
retention, access, deletion, investigation, and recovery.

## Rationale

A concrete profile avoids premature language-neutral abstractions while making
the current Python expectations usable immediately. The rules preserve the
original DSET emphasis on small functions, a pure core, typed boundaries,
executable gates, pinning tests, supportability, and risk-based durability. The
research adjustment replaces unconditional OOP with purposeful reuse, separates
Pydantic boundary validation from dataclass domain records, prefers PyPA's
`src` layout for new packages while allowing a dedicated package root,
supplements physical line limits with complexity, and makes NDJSON logging
conditional on investigation value.

This emitted Requirement is immutable. Later correction, generalization, or
replacement requires a linked atomic artifact and recompilation of the selected
profile.
