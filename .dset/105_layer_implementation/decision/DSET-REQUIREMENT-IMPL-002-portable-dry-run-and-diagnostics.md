+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-169"
type = "decision"
subtype = "requirement"
semantic_id = "DSET-REQUIREMENT-IMPL-002"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "Local Python tools are readily transportable across supported operating systems, expose a mutation-free dry-run mode, document executable parameters at the start of each file, report actionable errors, and normally offer a safe debug mode."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Local tools are often copied between hosts and operated during incidents; predictable simulation, discoverable invocation, and actionable diagnostics reduce both portability failures and unsafe trial runs."

[scope]
kind = "layer"
id = "implementation"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-REQUIREMENT-IMPL-001"
+++

# Requirement — Portable execution and safe diagnostics

Every executable governed by `local-python-tools-v1` accepts `--dry-run`.
Dry-run performs safe parsing, validation, discovery, and planning and reports
the effects a real run would attempt, but performs no mutation through the
filesystem, network, Git, database, queue, or another external system. An
inherently read-only tool still accepts the option and reports that no mutable
effects are planned.

Every Python file starts with a module docstring. Executable tools and
Test/Evaluation runners document purpose, invocation, parameters, inputs,
outputs, mutable effects, exit statuses, and environment requirements before
implementation code. Test modules instead document assurance scope and any
non-obvious fixtures or host requirements.

Errors are verbose, actionable, redacted, and useful without debug mode. They
identify the failed operation and target, preserve the underlying cause, and
suggest safe remediation when known. Non-trivial tools should expose a
documented `--debug` mode that adds redacted context and exception traces but
never changes business behavior, enables forbidden writes, or bypasses
validation.

The tool uses portable Python APIs and direct subprocess argument vectors and
must be readily transferable across macOS, native Windows, WSL, and Linux.
Any unavoidable host-specific behavior is declared and isolated.
