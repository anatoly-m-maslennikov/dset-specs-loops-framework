# Local Python Tools profile v1

## Scope

`local-python-tools-v1` applies to small Python command-line tools, scheduled
utilities, repository automation, and single-host workers whose code and tests
form one package. It is not authority for network services, high-throughput
multi-writer systems, reusable public libraries, notebooks, or GUI applications.

The selected project configuration owns the actual limits. The accompanying
TOML profile publishes the defaults and makes every threshold and behavioral
switch inspectable instead of hiding policy in a checker.

## Development environment

1. Declare the supported Python range, build backend, package metadata,
   command entrypoints, development dependencies, and code-tool configuration
   in `pyproject.toml`.
2. Use an isolated project environment. Resolve dependencies from the declared
   registry into a committed lockfile and run project commands through the
   selected environment manager; do not depend on ambient global packages.
3. Keep runtime dependencies separate from development-only format, lint,
   typing, test, coverage, and security tools. Every allowed dependency records
   its exact version, registry, license, provenance, and rationale in the
   selected dependency policy.
4. New packaged tools prefer `src/<package>/`. An existing dedicated top-level
   package directory is allowed when it contains only importable package code
   and the canonical checks prevent accidental imports from unrelated
   repository files.
5. The canonical local commands and CI commands use the same locked environment
   and project configuration. Platform-specific setup is explicit; a passing
   shell shortcut on one host is not cross-platform proof.
6. The tool is transportable across macOS, native Windows, WSL, and Linux when
   its declared capabilities exist there. It uses platform-native path and
   temporary-directory APIs, passes subprocess arguments without shell
   reparsing, and explicitly handles any unavoidable OS-specific behavior.

## Code structure

1. Keep modules cohesive and functions single-purpose. A function may contain
   at most 39 measured code lines: the configured exclusive limit is 40.
   Decorators, the signature, blank lines, comment-only lines, and the leading
   docstring do not count. Nested function bodies are measured independently.
2. A module may contain at most 400 measured code lines. Split by responsibility,
   not by arbitrary file fragments. Cyclic imports are prohibited.
3. Any Python file directly in a tool's top-level directory must be an executable
   entrypoint. Importable code lives under `src/<package>/`; tests live under
   `tests/`. Prefer a `[project.scripts]` entrypoint over a thick root script.
4. Entrypoints parse input, construct dependencies, call one application
   function, render the result, and map failures to exit codes. Domain behavior
   and reusable I/O code do not live in entrypoints.
5. When code is reused by entrypoints in the same package, extract a shared
   module. When scripts differ only by options, combine them behind one
   parameterized entrypoint. Copy-pasted boilerplate is prohibited.
6. Use functions for stateless transformations. Use classes when state and
   behavior form one cohesive object. Use dataclasses for trusted internal data;
   use Pydantic models for configuration, serialized data, and other untrusted
   boundaries. Use protocols, abstract bases, mixins, or inheritance only when
   they express a stable shared contract and remove real repetition.
7. Prefer composition and injected collaborators for replaceable I/O. Do not
   create an inheritance hierarchy merely to share a few coincidentally similar
   lines.

New packages prefer PyPA's `src` layout, which prevents the working tree from
being imported accidentally and keeps non-package repository files off the
import path. Console entrypoints use `[project.scripts]` and delegate to a
package function. See the
[PyPA src-layout guidance](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
and [entry-point specification](https://packaging.python.org/en/latest/specifications/entry-points/).

## Models, schemas, settings, and constants

1. All owned functions and methods carry type annotations. Strict static typing
   applies to owned code; any suppression is narrow and explains why it is safe.
2. Pydantic validates data at external boundaries and rejects unexpected fields
   unless compatibility explicitly requires them. Internal trusted records use
   standard-library dataclasses when runtime validation is unnecessary.
3. Schemas live in dedicated schema files or schema modules, separate from
   workflow and I/O implementation. Each serialized shape has one authoritative
   definition. Generated JSON Schema may be published as a separate derived
   file, but it must not become a second hand-edited owner.
4. A separate settings file is optional. When operator-tunable or
   environment-specific values justify one, runtime settings live in a typed
   settings model with a declared TOML carrier, are loaded at the invocation
   boundary, and are injected into owned logic. A scheduled loop may reread
   settings at its declared tick boundary; a single run otherwise keeps one
   stable settings snapshot.
5. Every Python module groups its module-level settings, defaults, thresholds,
   and constants immediately after the module docstring and imports and before
   classes, functions, or runtime statements. This placement is mandatory even
   when the module also loads a separate settings file.
6. Every constant is self-documented at its declaration: state what it controls
   or is responsible for, its unit or interpretation when relevant, and its
   override or authority boundary. Descriptive naming does not replace this
   explanation.
7. Tunable values, limits, paths, timeouts, retry counts, format versions, and
   behavior switches are named settings or constants. The exclusive 40-line
   function limit is explicitly owned by the profile TOML and is never a hidden
   checker literal. Secrets are credentials, not settings or constants, and
   never enter source, logs, fixtures, or durable artifacts.
8. Use descriptive `snake_case` names for modules, functions, variables, and
   fields; `CapWords` for classes; and `UPPER_SNAKE_CASE` for constants. Prefer a
   longer precise name to a short ambiguous abbreviation.

Pydantic models are appropriate at validation and serialization boundaries;
dataclasses generate common data-object methods without handwritten boilerplate.
See the [Pydantic model guidance](https://pydantic.dev/docs/validation/latest/concepts/models/),
the [Python dataclasses documentation](https://docs.python.org/3/library/dataclasses.html),
and [mypy strict-mode guidance](https://mypy.readthedocs.io/en/stable/existing_code.html).

## Documentation and failures

1. Every Python file begins with a module docstring. An executable tool or
   Test/Evaluation runner documents its purpose, invocation, parameters
   including `--dry-run` and `--debug` where applicable, inputs, outputs,
   mutable effects, exit statuses, and environment requirements before its
   implementation. A test module documents its assurance scope and any
   non-obvious fixtures or host requirements; ordinary test functions do not
   pretend to accept command parameters.
2. Every class, function, and method has a useful docstring unless it is
   a trivial private helper whose name and type signature fully state its
   contract. Public docstrings describe behavior, inputs, results, side effects,
   raised exceptions, and important restrictions. Entrypoint module docstrings
   explain command syntax, environment inputs, and files.
3. Comments explain reasons, invariants, or external constraints; they do not
   restate the code.
4. Expected failures use explicit exception types or result objects. CLI errors
   are verbose and actionable: they identify the failed operation and target,
   preserve the underlying cause, suggest a safe correction when known, go to
   standard error, and return a non-zero documented exit code. They never expose
   secrets or represent failure as valid empty data.
5. Every executable exposes a documented `--dry-run` mode. It performs safe
   parsing, validation, discovery, and planning and reports the effects that a
   real run would attempt, but performs no project, filesystem, network, Git,
   database, queue, or external-system mutation. An inherently read-only tool
   still accepts the flag and reports that no mutable effects are planned.
6. A `--debug` mode is recommended for non-trivial tools. It adds redacted
   diagnostic context and exception traces without changing business behavior,
   enabling writes that normal mode forbids, or bypassing validation. Normal
   errors remain useful without debug mode.
7. Filesystem behavior uses `pathlib`, explicit UTF-8 text, platform-native
   temporary files, and atomic replacement when a durable snapshot must not be
   partially visible. Commands must work on macOS, Linux, Windows, and WSL
   without relying on a POSIX-only shell.

The docstring rules follow [PEP 257](https://peps.python.org/pep-0257/) and the
identifier forms follow [PEP 8](https://peps.python.org/pep-0008/). Project
clarity takes precedence over shortening a meaningful name.

## Automated assurance

1. Every testable accepted Decision, Requirement, Constraint, Contract, User
   Story, use case, invariant, and fixed Defect maps to at least one automated
   test. The mapping is explicit; a line-coverage percentage cannot substitute
   for semantic traceability.
2. Test pure behavior with unit tests and boundary behavior with contract or
   integration tests. Every fixed defect receives a regression test that fails
   on the defective behavior. Important invariants receive property-oriented or
   table-driven tests where practical.
3. Measure both line and branch coverage. Projects may raise the profile's
   numeric floors, but they may not lower semantic claim coverage.
4. The canonical check runs formatting, lint/static analysis, the configured
   40-line-exclusive function gate, module and complexity gates, strict typing,
   automated tests, branch coverage, claim-to-test traceability, and secret
   scanning. Every failure returns non-zero and identifies the file and rule.
5. Ruff is the default formatter/linter and its McCabe and statement-count rules
   supplement physical line limits; complexity is checked because line count
   alone does not measure control flow. Pytest's recommended separate test tree
   and `src` layout are the default.

See Ruff's [complexity rule](https://docs.astral.sh/ruff/rules/complex-structure/),
[pytest integration practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html),
and [coverage.py branch coverage](https://coverage.readthedocs.io/en/latest/branch.html).

## Evaluation implementations

1. Tests and Evaluations remain different QA mechanisms. A Test has a
   deterministic expected result; an Evaluation applies an authored criterion,
   cases, threshold, and reconciliation method where judgment is required.
2. Each selected Evaluation has a reusable prompt or Python harness that names
   the Evaluation ID, exact target revision, bounded inputs, output schema, and
   permitted tools and writes.
3. Independent Evaluation runs do not share prior results. Reconciliation
   preserves disagreement, uncertainty, exclusions, and threshold failures; it
   never turns majority vote or averaging into an unauthorized pass.
4. Evaluation implementations live separately from production modules and
   from evidence records. An execution result cannot rewrite the Evaluation
   definition or the implementation it assessed.

## Conditional local NDJSON logs

Local NDJSON logs are required when the tool has multiple operational steps,
retries, scheduled runs, external effects, or a realistic need for later
production investigation. A pure one-shot transform may use standard error
only and mark NDJSON logging not applicable.

When enabled:

- write UTF-8, one complete JSON object per line, under the configured runtime
  log directory;
- include schema version, UTC timestamp, severity, event name, run ID, tool
  version, and safe structured context; include a correlation ID when work
  crosses an effect boundary;
- redact secrets and bounded sensitive values before serialization;
- use one writer per file, bounded file size, rotation compatibility, and
  explicit handling of disk-full or malformed-record failures;
- treat logs as derived investigation evidence, not business-state authority or
  an automatic WAL; select durable replay separately when the tool requires it;
- let OPS own runtime retention, access, deletion, investigation, and recovery
  policy for the emitted records.

Python's logging cookbook describes structured machine-readable logging, and
the [NDJSON specification](https://github.com/ndjson/ndjson-spec) defines the
UTF-8 one-JSON-value-per-line carrier.
