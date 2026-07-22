+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-165"
type = "decision"
subtype = "none"
semantic_id = "DSET-DECISION-GOV-030"
status = "accepted"
priority = "critical"
authority = "operator:anatoly-m-maslennikov"
claim = "Installed methodology includes its executable Python toolchain, deterministic Test implementations, and qualitative Evaluation prompt implementations under the TOOL layer; applied QA definitions, plans, evidence, and verification remain project artifacts outside methodology, while deterministic materialization keeps installed executors equal to their repository sources."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "Project-local methodology is not operational when it contains rules but omits the tools and proof implementations that enact those rules. Keeping implementations in TOOL while retaining applied QA state in project layers preserves both executability and ownership separation."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-022"
+++

# Decision — Install executable methodology

The installed TOOL methodology contains three executable implementation
surfaces:

- `120_python` — the local DSET Python package and its portable launcher;
- `130_tests` — deterministic Test implementations and their runner; and
- `140_evaluations` — independent-review and result-reconciliation prompts for
  qualitative Evaluation execution.

Applied Test/Evaluation definitions, layer plans, run evidence, and
Verification conclusions remain under the applied project and layer owners.
They are not copied into methodology. TOOL owns reusable execution mechanisms;
the applicable project scope owns what must be checked and what happened.

The repository-root Python package and Test package remain development sources
required by the Python packaging ecosystem. Methodology synchronization copies
them byte-for-byte into the numbered installed TOOL surface, ignores generated
Python caches, detects drift, and never uses symlinks. Evaluation
implementations are ordinary numbered TOOL source carriers and follow the
normal source-to-installed synchronization path.

Python package names and `test_*.py` module names retain ecosystem-required
spellings inside their numbered owner directories. The exception does not
create unnumbered methodology ownership areas.

## Rationale

Rules without their executors cannot provide a self-contained project-local
methodology. Separating reusable executors from applied QA authority keeps the
methodology operational without mixing it with this project's proof state.
