![cover](shadowMAS.png)
# shadowMAS

shadowMAS is a governance research artifact and testbed for multi-agent AI systems.
It is not yet a polished open-source agent framework.
It does not replace agent orchestration frameworks.
Its core problem is authority-bounded interpretation.
Seeing a runtime signal is not the same as trusting it, storing it, promoting it, or acting on it.

## Minimal demo

```bash
python3 tools/shadowmas_minimal_validator.py examples/demo_signal_governance.json
```

This demo is not a runtime engine. It checks the shadowMAS governance boundary: runtime signals and audit projections may be visible as evidence, but must not silently become truth, memory, approval, or decision authority.

shadowMAS is a governance-oriented, memory-aware, human-AI collaboration system.

It is not the product application itself.  
It is a separate governance system for multi-agent and multi-session work.

shadowMAS is not an agent framework. It is a local-first governance contract layer for multi-agent development work.

Execution agents such as Codex, Claude Code, Cursor, or local models may do the work; shadowMAS defines the packet, workspace, review, handoff, and promotion boundaries around that work.

Licensed under the Apache License 2.0. See `LICENSE`.

## What problem shadowMAS solves

shadowMAS exists to reduce five failure modes that become common once AI work grows beyond a single chat:

- **authority confusion** — who may decide, who may execute, and who may promote results
- **truth confusion** — execution output, cache, and drafts being mistaken for canonical truth
- **giant prompt collapse** — reusable rules, governance, project truth, and runtime-specific constraints being flattened into one blob
- **intake chaos** — blind full-repo traversal instead of controlled entry and compiled intake
- **mergeback contamination** — governance artifacts polluting product repos or overriding project-domain truth

## What shadowMAS is not

shadowMAS is not:
- the product application itself
- a giant prompt system
- a blind repo traversal bot
- a direct replacement for project-specific canonical truth
- a UI-first platform
- a DB-first platform
- just another general-purpose agent framework

## Boundary model

Governance outside, candidate work writable, promotion controlled.

The shadowMAS source repo contains the system contracts, docs, scripts, and governance surfaces.

An external shadowMAS workspace stores governance artifacts such as packets, reviews, handoffs, and runs.

shadowMAS governance artifacts should not be written into product repos by default. This includes packets, reviews, handoffs, runs, memory candidates, and raw governance state.

Product repos may still receive product-owned outputs in controlled branches or worktrees as candidate changes. Product canonical branches should receive promoted changes only through human git review / merge decision.

## Why hard separation matters

shadowMAS must remain hard-separated from product repos.

A product repo should still be able to:
- develop
- implement
- test
- deploy
- operate

even if shadowMAS is unavailable.

Preferred model:
- shadowMAS lives in its own root/repo
- product repos consume selected outputs only

Typical outputs:
- entry/index files
- truth-priority files
- change-impact maps
- handoff packets
- review outputs
- write-back suggestions
- controlled scripts/hooks

## Why machine-first artifacts matter

shadowMAS uses human-facing docs and machine-first artifacts for different jobs.

Human-facing docs are for:
- onboarding
- navigation
- explanation
- design rationale
- review support

Machine-first artifacts are for:
- packets
- registries
- routing
- validation
- automation surfaces

Machine-first artifacts should converge toward:
- minimal format
- parseability
- low ambiguity
- explicit structure
- stable contract boundaries

## v0 repo purpose

This repo is the minimum landing zone for shadowMAS v0.

Current direction:
- docs-as-code
- machine-readable registry
- CLI-first
- no UI in v0
- no DB-first design
- hard-separated from product repos

## First run

Run commands from the repository root.

`<project-path>` must be an existing product project directory.

```bash
python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py inspect --project <project-path>
python3 05_scripts/validate/shadowmas_validate.py examples/packets/task_packet.valid.v0.yaml
```

The workspace commands create and inspect an external shadowMAS workspace outside the product project directory.

The validator command validates the non-canonical example packet under `examples/packets/`. The validator checks packet shape and contract rules; it does not execute tasks or run agents.

Examples under `examples/` are non-canonical illustrative examples. They are not truth files and not packet schemas.

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
Current direct script surfaces live here. Installed package commands are not available yet. The labels below are grouping names for current and possible future scripts:
- ingest
- packetize
- validate
- embed
- review
- writeback

Current executable surfaces are direct script commands, not installed package commands:

```bash
python3 05_scripts/validate/shadowmas_validate.py <packet-file>
python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py inspect --project <project-path>
```

Current scripts do not run agents, modify product repos, or perform write-back.

Logical future command shapes:

```bash
shadowmas validate <packet-file>
shadowmas workspace init --project <project-path>
shadowmas workspace where --project <project-path>
shadowmas workspace inspect --project <project-path>
```

### `06_human_docs/`
Human-facing documents.
- `zh-TW/` is the primary human explanation and navigation area
- `en/` contains the English operator onboarding entry

### `07_working/`
Working integration area for handoffs, merged drafts, temporary working files, and archive state.
Files under `07_working/` are working-area materials such as drafts, intake rules, integration notes, and handoff support. They are not canonical truth unless later promoted through an explicit governance path.

## Reading policy

Do not treat this README as the only truth source.  
It is an entry file.

Primary formal truth lives in:
- `01_truth/`

Primary human-facing navigation lives in:
- `06_human_docs/zh-TW/`

Current v0 intake pack:
1. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
2. `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
3. `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md`
4. `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

For deeper governance review, also read:
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`

## v0 design bias
- rules-first
- text-first
- local-first
- inspectable
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
