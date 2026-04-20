# shadowMAS

shadowMAS is a governance-oriented, memory-aware, human-AI collaboration system.

It is not the product application itself.
It is a separate system used to govern:
- agent collaboration
- truth boundaries
- memory and promotion flow
- review and mergeback
- controlled write-back into project repos

## v0 Repo Purpose
This repo is the minimum landing zone for shadowMAS v0.

Current direction:
- docs-as-code
- machine-readable registry
- CLI-first
- no UI in v0
- no DB-first design
- hard-separated from product repos

## Top-level directory guide

### `00_entry/`
Entry and navigation files for agents and humans.
Use this layer to avoid blind repo traversal.

### `01_truth/`
Formal truth drafts and promoted governance documents.

### `02_packets/`
Packet schemas, packet field definitions, and shared machine-stable exchange structures.

### `03_memory/`
Minimum memory-plane structure:
- session_log
- working_memory
- shared_memory
- registry

### `04_runtime/`
Runtime state folders for inbox, packetized artifacts, indexing, review, approval, rejection, and writeback.

### `05_scripts/`
CLI-oriented scripts grouped by function:
- ingest
- packetize
- validate
- embed
- review
- writeback

### `06_human_docs/`
Human-facing documents.
- `zh-TW/` is the primary human explanation and navigation area
- `en/` contains the English operator onboarding entry

### `07_working/`
Working integration area for handoffs, merged drafts, temporary working files, and archive state.

## Current reading policy
Do not treat this README as the only truth source.
It is an entry file.

First human-facing onboarding entry points:
- English: `06_human_docs/en/onboarding/SHADOWMAS-OPERATOR-GUIDE.v0.en.md`
- zh-TW: `06_human_docs/zh-TW/onboarding/SHADOWMAS-OPERATOR-GUIDE.v0.zh-TW.md`

Primary formal truth lives in:
- `01_truth/`

## v0 design bias
- text-first
- local-first
- inspectable
- index-first
- schema-first
- minimal dependencies
- explicit review gates
- bounded write-back

<!-- SHADOWMAS_PRINCIPLES_PATCH:BEGIN -->
## Core governance additions
- capability routing: do not route by model name alone; route by task shape and data shape
- machine-first normalization: machine-first files must converge toward minimal, parseable, low-ambiguity structure
- compiled intake: zero-memory intake should first be composed from existing canonical files; if a compact intake artifact is added later, it should be treated as a compiled artifact, not a new handwritten truth source
<!-- SHADOWMAS_PRINCIPLES_PATCH:END -->
