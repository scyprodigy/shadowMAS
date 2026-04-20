# SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md

## Purpose
This file defines which formal files, registries, packets, or human-facing documents must be reviewed when a certain kind of change happens.

Its goal is to prevent:
- silent drift
- partial updates
- broken alignment
- hidden stale references
- false truth consistency

## Core Rule
A change is not considered aligned until all impacted truth layers are checked.

Not every impacted file must always be changed,
but every impacted layer must be reviewed.

## 1. Governance identity change
Examples:
- redefining what shadowMAS is
- changing hard separation rule
- changing governance weight model
- changing layer meanings

Must review/update:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

May also require:
- ADR / rationale files later
- core diagram later

## 2. Prompt layering change
Examples:
- changing Shared Core meaning
- changing shadowMAS Governance scope
- changing Project Execution boundary
- adding/modifying Runtime Adapter Prompt rules
- recognizing new host-native prompt constraints

Must review/update:
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md`
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

## 3. Governance matrix change
Examples:
- changing L-layer meaning
- changing T-layer meaning
- changing promotion direction
- changing authority interpretation
- introducing formal Runtime Adapter layer handling

Must review/update:
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

May also require:
- future packet rules
- future file-status registry rules

## 4. Packet family or packet field change
Examples:
- adding a new packet family
- changing required packet fields
- changing packet naming
- changing shared shell fields
- changing invalidation field names

Must review/update:
- relevant packet field dictionary and packet schema files under `02_packets/`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` if packet identity changes
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md` if human explanation changes

May also require:
- future validator scripts
- memory-plane harness if memory packet changes

## 5. Memory-plane change
Examples:
- changing memory layers
- changing what counts as shared memory
- changing promotion rules
- changing invalidation behavior
- changing registry meaning

Must review/update:
- relevant memory-plane harness files under `03_memory/`
- `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- relevant packet files under `02_packets/` if packet memory structure is affected
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

## 6. File-status / truth-status change
Examples:
- adding a new file status
- changing promotion candidate meaning
- changing approved truth handling
- changing handoff-only rules
- changing draft vs canonical interpretation

Must review/update:
- `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `07_working/` handling rules when formalized
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md` if needed for human explanation

## 7. Local model baseline change
Examples:
- changing text model
- changing embedding model
- changing Ollama deployment side
- changing retrieval-first workflow
- changing Chroma/Qdrant choice

Must review/update:
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- relevant memory-plane harness files under `03_memory/` if retrieval/memory behavior changes
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

## 8. Compression strategy change
Examples:
- changing default compression scenes
- changing no-compression protected formats
- changing sentence/paragraph filtering strategy
- changing whether compression is default or optional in a given lane

Must review/update:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md`
- future runtime-adapter documents
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`
- future rationale/decision docs in zh-TW

## 9. Runtime adapter change
Examples:
- adding Claude Code adapter rules
- adding Cursor adapter rules
- adding GPT/Codex adapter rules
- changing tool-specific prompt shaping
- adding runtime-specific safety fences

Must review/update:
- relevant runtime-adapter contract files when they exist
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` if baseline meaning changes

## 10. Entry / navigation structure change
Examples:
- changing START-HERE logic
- changing master index structure
- changing reading order
- adding/removing quickref layers

Must review/update:
- current entry files under `00_entry/`
- `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md`
- `README.md`
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

## 11. Project write-back policy change
Examples:
- changing what shadowMAS may export into project repos
- changing decoupling rules
- changing project contamination handling
- changing write-back safety boundaries

Must review/update:
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- relevant write-back contract files when they exist
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

## 12. Human-facing explanation change
Examples:
- changing design rationale
- changing historical explanation
- changing reference notes
- changing onboarding wording

Must review/update:
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`
- related zh-TW docs in:
  - `06_human_docs/zh-TW/onboarding/`
  - `06_human_docs/zh-TW/decisions/`
  - `06_human_docs/zh-TW/rationale/`
  - `06_human_docs/zh-TW/references/`

Formal truth docs only need updating if the explanation reflects a true governance/truth change.

## 13. Rule for canonical vs human-doc update
If a formal English truth file changes:
- check whether the change affects high-value human explanation
- if yes, update the zh-TW single-source and related explanation docs

If only human explanation wording changes:
- do not modify formal truth unless the actual truth changed

## 14. Rule for historical preservation
Canonical files should usually be updated in place.

History should normally be preserved through:
- git history
- milestone snapshots
- explicit rationale/decision documents when needed

Do not create daily duplicate truth files by default.

## 15. Agent reporting rule
When proposing or making a change, an agent must report:
- what changed
- which truth layers were checked
- which files were updated
- which impacted files were intentionally deferred
- whether zh-TW human-facing update is needed

## 16. Still Not Final
The following may later refine this map:
- final runtime-adapter file set
- final ADR structure
- final write-back contract docs
- final normalization workflow for contaminated project repos
