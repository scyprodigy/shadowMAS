# shadowMAS

![cover](shadowMAS.png)

shadowMAS is an authority-boundary evaluation construct and open testbed for multi-agent AI systems.
It is not yet a polished open-source agent framework.
It does not replace agent orchestration frameworks.
Its core problem is authority-bounded interpretation.
Seeing a runtime signal is not the same as trusting it, storing it, promoting it, or acting on it.

## Start here

- [Minimal demo](#minimal-demo)
- [Expected output](#expected-output)
- [Inspect an L2 fixture](#inspect-an-l2-fixture)
- [Current status](#current-status)
- [Repository map](#repository-map)
- [What shadowMAS is not](#what-shadowmas-is-not)

## Minimal demo

```bash
python3 tools/shadowmas_minimal_validator.py examples/demo_signal_governance.json
```

### Expected output

```text
PASS: runtime_signal_truth_status_runtime_only - runtime signal truth_status remains runtime_signal_only
PASS: runtime_signal_cannot_promote_truth_directly - runtime signal cannot promote truth directly
PASS: runtime_signal_cannot_write_memory_directly - runtime signal cannot write memory directly
PASS: runtime_signal_requires_human_review_for_promotion - runtime signal requires human review for promotion
PASS: no_t4_t5_to_t2_t3_direct_promotion - T4/T5 signals cannot directly promote into T2/T3
PASS: no_silent_memory_write - runtime signals cannot silently write memory
PASS: audit_projection_is_read_only - audit projection is read-only
PASS: audit_projection_has_no_approval_authority - audit projection has no approval authority
PASS: audit_projection_has_no_truth_authority - audit projection has no truth authority
PASS: recommended_action_is_advisory_only - recommended_action is advisory only
PASS: recommended_action_cannot_authorize_runtime_action - recommended_action cannot authorize runtime action
PASS: recommended_action_cannot_authorize_packet_change - recommended_action cannot authorize packet change
PASS: recommended_action_cannot_promote_truth - recommended_action cannot promote truth
PASS: dashboard_does_not_become_authority - dashboard does not become authority
PASS: human_final_authority_preserved - human final authority is preserved
```

This demo is not a runtime engine. It checks the shadowMAS authority-boundary contract: runtime signals and audit projections may be visible as evidence, but must not silently become truth, memory, approval, or decision authority.

## Inspect an L2 fixture

For L2 handoff trace fixture inspection, see `examples/README.md` or run:

```bash
python3 tools/inspect_l2_fixture.py examples/traces/l2_handoff/ephemeral_handoff_memory_promotion.json
```

This helper prints a JSON report for one fixture and does not make runtime or production-safety claims. Exit code is `0` on pass and `1` on fail.

Run the full unit-test suite with:

```bash
python3 -m unittest discover
```

## Current status

shadowMAS is currently in research/spec/testbed stage.

Available now:
- minimal authority-boundary validator
- minimal demo JSON
- candidate registry
- packet and truth-boundary specifications

Not available yet:
- production runtime engine
- full agent orchestration layer
- stable public API

## Repository map

- `01_truth/` — canonical truth and authority-boundary contracts
- `02_packets/` — packet schemas and field definitions
- `03_memory/` — candidate registry and memory-related artifacts
- `examples/` — runnable minimal examples
- `tools/` — lightweight validators and utilities

shadowMAS is an authority-boundary evaluation construct and open testbed for multi-agent and multi-session work.

It is not the product application itself.  
It is not a runtime engine, an agent framework, or a production safeguard.

shadowMAS is local-first, fixture-oriented evaluation material. It focuses on how authority-bounded interpretation is preserved across signals, traces, memory candidates, and audit projections.

Execution agents such as Codex, Claude Code, Cursor, or local models may do the work; shadowMAS defines the packet, workspace, review, handoff, and promotion boundaries around that work as evaluation-oriented fixture material.

Licensed under the Apache License 2.0. See `LICENSE`.

## What problem shadowMAS solves

shadowMAS exists to reduce five failure modes that become common once AI work grows beyond a single chat:

- **authority confusion** — who may decide, who may execute, and who may promote results
- **truth confusion** — execution output, cache, and drafts being mistaken for canonical truth
- **giant prompt collapse** — reusable rules, governance, project truth, and runtime-specific constraints being flattened into one blob
- **intake chaos** — blind full-repo traversal instead of controlled entry and compiled intake
- **mergeback contamination** — authority-boundary artifacts spilling into product repos or overriding project-domain truth

## What shadowMAS is not

shadowMAS is not:
- the product application itself
- a giant prompt system
- a blind repo traversal bot
- a direct replacement for project-specific canonical truth
- a UI-first platform
- a DB-first platform
- just another general-purpose agent framework

shadowMAS is not a replacement for LangGraph, CrewAI, Dapr, OpenAI Agents SDK, MCP, or A2A.
It can sit beside existing agent runtimes and focus on how their signals, traces, memory candidates, and audit projections are interpreted, reviewed, and prevented from becoming hidden authority.

## Boundary model

Authority boundary outside, candidate work writable, promotion controlled.

The shadowMAS source repo contains the system contracts, docs, scripts, and evaluation surfaces.

An external shadowMAS workspace stores authority-boundary artifacts such as packets, reviews, handoffs, and runs.

shadowMAS authority-boundary artifacts should not be written into product repos by default. This includes packets, reviews, handoffs, runs, memory candidates, and raw authority-boundary state.

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
Formal truth drafts and promoted authority-boundary documents.

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
Files under `07_working/` are working-area materials such as drafts, intake rules, integration notes, and handoff support. They are not canonical truth unless later promoted through an explicit promotion path.

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
