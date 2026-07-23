+++
artifact_type = "atomic_record"
artifact_id = "DSET-ATOMIC-RECORD-163"
type = "decision"
subtype = "none"
semantic_id = "DSET-DECISION-GOV-028"
status = "accepted"
priority = "high"
authority = "operator:anatoly-m-maslennikov"
claim = "The project .dset tree contains only current settings, installed methodology, applied artifacts, and Version truth; historical aggregates, completed migration records, and compatibility snapshots live in the repository's inert legacy archive outside .dset and are never skill-discovery or current-compilation inputs."
llm_session_ids = ["codex:019f591f-04f6-70f2-8de7-828b7cccc69d"]
rationale = "The project-local DSET tree is an active data-governance plane. Mixing historical transport records with current authority makes discovery ambiguous and obscures the state that skills must use."

[scope]
kind = "project"
id = "dset-specs-loops-framework"

[promotion]

[[relations]]
type = "child_of"
target = "DSET-DECISION-GOV-022"
+++

# Decision — Keep the control plane current

`.dset` owns only current project-local DSET truth:

- the unique settings carrier;
- installed methodology;
- applied project, layer, and Version atoms;
- current evergreen specifications and plans; and
- current evidence and verification records.

Historical aggregate registries, completed migration records, compatibility
snapshots, pre-current change folders, and retained pre-current documentation
belong to the inert repository archive outside `.dset`.

Skills and current semantic compilation search only `.dset`. They do not
consult the external archive, use it as fallback authority, or include it in
current coverage. Git history and the archive's own readme provide historical
return paths when an operator deliberately investigates the past.

## Rationale

The active control plane should answer what governs the project now. Historical
transport and compatibility material answers a different question and must not
compete with current data governance.
