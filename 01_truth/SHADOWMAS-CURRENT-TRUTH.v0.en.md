# SHADOWMAS-CURRENT-TRUTH.v0.en.md

## Purpose
This file freezes the current minimum truth of shadowMAS before deeper implementation begins.

It is not the final architecture book.  
It is the smallest stable truth that future files must follow.

## System Identity
shadowMAS is a dynamic packetized shadow layer for agentic work.

It is designed to sit behind changing runtimes, agents, memory tools, automation tools, and project rules. The stable unit it defines is the packet: a bounded, inspectable artifact that records what happened, where it came from, which authority layer it belongs to, whether it can be reused, when it must be invalidated, whether it can be promoted, and when human review is required.

Governance in shadowMAS means authority-boundary discipline across these shadow packets. It is not a claim that shadowMAS is itself a runtime governance engine, production safeguard, or replacement for project-specific truth.

It exists to:
- define the packetized shadow unit behind tasks, memory candidates, reviews, handoffs, lessons, runtime signals, and truth-touching outputs
- decompose scoped work into packets that can be delegated to agents or workers
- route, dispatch, and resume work across authority layers while preserving task scope, stop conditions, and supervision mode
- support autonomous execution only when paired with an explicit runtime or automation layer, including bounded retry, rollback, rework, and handoff continuity
- capture execution lessons as memory candidates and surface review packets as compressed human review material
- make truth, memory, promotion, invalidation, merge-back, and write-back boundaries explicit, inspectable, and reviewable
- reduce long-run token cost, semantic friction, repeated rediscovery, and hidden correction cost across changing tools and projects
- preserve human final authority over approval, rejection, revision, escalation, trust elevation, canonical truth, approved shared memory, and canonical product-branch promotion

Within shadowMAS-shaped packet/task flows, the governance shadow is a mandatory internal authority-boundary discipline: information must not be promoted beyond the authority warranted by the T0–T5 layer model and its promotion path, and final authority remains human. This file does not claim that the current repository automatically enforces these boundaries inside downstream application runtimes or guarantees production safety. These responsibilities are the canonical design surface; the current shipped implementation covers only a subset, with items still pending tracked under `## Still Not Final`.

shadowMAS is not:
- the product application itself
- a giant prompt system
- a blind repo traversal bot
- a direct replacement for project-specific canonical truth
- a UI-first platform
- a memory database
- a workflow engine
- a runtime governance engine

## Problem Profile
shadowMAS exists to reduce five recurring failure modes in AI-assisted work:

- authority confusion
- truth confusion
- giant prompt collapse
- blind intake / full-repo traversal by default
- mergeback contamination between authority-boundary artifacts and product repos
- semantic drift across agents, memory, runtime adapters, lessons, and project-local truth

This problem profile explains why shadowMAS is authority-boundary-first, hard-separated, and machine-first at key boundaries.

## Hard Separation Rule
shadowMAS must remain hard-separated from product systems.

A product repo must still be able to:
- develop
- implement
- test
- deploy
- operate

even if shadowMAS is unavailable.

shadowMAS may connect to product repos through controlled integration points only.

Boundary invariant:
- Product repositories must not require shadowMAS authority-boundary artifacts, runtime state, packets, reviews, handoffs, workspace metadata, or shadowMAS workspaces to build, test, deploy, or operate.
- Automation may write product-owned candidate artifacts into controlled product branches or worktrees, but those artifacts must not create a runtime or build-time dependency on shadowMAS authority-boundary state.
- Promotion into canonical product branches remains a human git review / merge decision.

## Integration Model
Preferred model:
- shadowMAS lives in its own root/repo
- product repos consume selected outputs

Typical integration points:
- entry/index files
- truth-priority files
- change-impact maps
- translation policies
- handoff packets
- review outputs
- write-back suggestions
- controlled scripts/hooks

## Shadow Boundary Weight Model
Governance here means authority-boundary discipline, not runtime ownership.

- authority-boundary highest: shadowMAS
- business/domain highest: project canonical truth
- shared core sits between them
- shared core must not directly override project domain facts

## Layer Model

### Shared Core
Cross-project reusable rules.

### Project Execution
Repo-local execution constraints and domain-specific truth.

### shadowMAS Authority-Boundary Orchestration
Global shadow-boundary discipline for packet routing, memory, promotion, invalidation, indexing, review, lessons, mergeback, and write-back boundaries.

## Current Operational Layer Model

### Role / Operation Layer
- `L1`: Human + high-level AI authority review
- `L2`: Delegated decision / planning
- `L3`: Execution / repo implementation
- `L4`: Mergeback / sync

### Truth / Authority Layer
- `T0`: Human Authority
- `T1`: Delegated Decision Authority
- `T2`: Approved Truth Artifacts
- `T3`: Approved Shared Memory
- `T4`: Execution Feed
- `T5`: Ephemeral / Cache / Session State

### Runtime / Substrate Layer
`R-layer` is required, but not yet finalized.

Its responsibility includes:
- queue
- worker pool
- retry
- lock
- timeout
- concurrency
- backpressure

## Current Core Principles
- rules-first
- repo-first truth
- no blind full-repo traversal
- no giant prompt
- human-readable and machine-stable artifacts must be separated
- quality first, then token efficiency
- bounded write-back only
- promotion gate required before reusable truth elevation
- retrieval, cache, or vector hits cannot arbitrate truth

## Artifact Strategy
Use a mixed two-form strategy.

### Human-readable form
For:
- review
- explanation
- onboarding
- authority-boundary reasoning
- design rationale

Language preference:
- zh-TW first
- English technical terms when necessary

### Machine-stable form
For:
- packets
- registries
- agent bootstrap
- routing
- validation
- automation surfaces

Format preference:
- minimal
- structured
- token-efficient
- parse-friendly

## Canonical Language Policy
- English is the canonical execution language for agent-facing formal docs
- Chinese is the companion/navigation language for human-facing reasoning, onboarding, and rationale
- not every file requires a Chinese companion
- only high-value core files should normally receive bilingual treatment

## Packet Direction
shadowMAS internal main exchange direction currently prefers a self-defined minimum packet system rather than ACP/A2A as the internal primary protocol.

Packet fields and semantics belong to the logical packet contract.  
For v0, the default packet codec is YAML.

Minimum packet families:
- `task_packet`
- `memory_packet`
- `review_packet`

## Packet Rules

### task_packet
Must carry:
- goal
- scope
- out_of_scope
- truth_touchpoints
- worker_plan
- acceptance_criteria
- stop_conditions

### memory_packet
Must carry:
- memory_kind
- memory_scope
- summary
- structured_payload
- source_refs
- invalidation_triggers
- confidence
- promotion_candidate

### review_packet
Must carry the smallest human review surface needed for decision and mergeback.

## Control Surface Separation
The following must remain separate:
- supervision mode
- risk
- execution budget
- prompt policy

### supervision mode
- `human_live_pair`
- `human_available_delegate`
- `human_away_autonomous`

### risk tiers
- `r0_trivial`
- `r1_routine`
- `r2_guarded`
- `r3_sensitive`
- `r4_human_only`

### risk dimensions
- `truth_impact`
- `blast_radius`
- `dependency_risk`
- `recovery_cost`

### prompt policy
Current direction:
- rules-first
- few-shot off by default
- minimal skill examples only when needed

## Memory Direction
Current minimum memory-plane direction:
- `session_log`
- `working_memory`
- `shared_memory`

Rules:
- repo, formal docs, and approved artifacts remain the first truth source
- cache is acceleration only
- retrieval supports but does not decide truth
- promotion gate is mandatory
- invalidation must be explicit

## Memory Plane Principles
Memory is a core shadowMAS design surface.

Memory strategy is task-dependent. The memory plane should optimize semantic cleanliness, token economy, handoff continuity, lesson extraction, and cross-agent reuse.

Memory backend selection is an implementation detail. Filesystem, vector, graph, and hybrid stores may all be valid R-layer implementations, but v0 does not select any canonical backend and does not implement a memory store.

Retrieval hits, cache hits, or memory lookups do not arbitrate truth. Memory promotion must pass through the review / promotion boundary.

`memory_packet` is the minimum cross-agent memory handoff contract. It is not a memory store design.

## Local Model Baseline
Current recorded baseline:
- `qwen3:8b` for small and cheap text tasks
- `mxbai-embed-large` for embeddings

Preferred current deployment direction:
- Linux / WSL side primary
- data-locality first
- Windows not treated as the main long-term path for shadowMAS runtime

## Technology Bias v0
Prefer:
- tree-sitter
- pydantic or jsonschema
- typer or click
- PyYAML or ruamel.yaml
- Chroma first, Qdrant later if needed

Do not adopt early:
- DSPy runtime framework
- LangGraph
- Letta / MemGPT
- CrewAI / AutoGen
- heavy orchestration frameworks

Concepts may be studied without adopting the full framework.

## Compression Position
Prompt and context compression is not foundation, but it is a default optimization subsystem for selected scenarios.

Use it by default for:
- long natural-language background
- long history summary
- oversized RAG context
- pre-merge condensation
- pre-small-model context reduction

Do not use it for:
- packet YAML
- review schemas
- JSON contracts
- API contracts
- migrations
- field-level dictionaries
- code patches and diffs

Direction:
- learn from LLMLingua-like ideas
- implement local sentence/paragraph-level filtering
- keep the design inspectable and reversible

## WFGY Position
WFGY is currently a reference source for extraction and adaptation.

It is not approved shadowMAS truth.  
It is not yet the official shadowMAS DSL.  
It may inform future control-language or routing design.

## v0 Boundary
shadowMAS v0 does not require:
- UI
- database-first design
- cloud deployment
- heavyweight orchestration frameworks
- direct overwrite of project domain truth

shadowMAS v0 does require:
- entry and index discipline
- truth-priority discipline
- change-impact discipline
- packet schema direction
- file-status discipline
- memory-plane direction
- mergeback boundaries
- human review gates

## Still Not Final
Do not hard-finalize yet:
- final `R-layer` runtime substrate
- final handoff common shell
- final promotion gate semantics
- final file-status registry schema
- final DSL form
- final git review / merge procedure
- final bilingual sync lifecycle
- final write-back automation contract

<!-- SHADOWMAS_PRINCIPLES_PATCH:BEGIN -->
## Core Principles Patch v0

### Capability Routing Principle
Do not choose models by model name alone.

Choose lanes by:
- task shape
- data shape
- required output shape
- acceptable error surface
- authority level required

This means:
- structured schema tasks should prefer structure-safe lanes
- embedding/retrieval tasks should prefer embedding lanes
- low-cost normalization tasks may prefer small local text models
- final authority-boundary decisions must not be delegated to cheap helper models

### Machine-First Normalization Principle
Files under machine-first layers must converge toward:
- minimal format
- parseability
- low ambiguity
- explicit enums where needed
- explicit timestamps and version fields where needed
- MUST/SHOULD/MAY style for high-risk normative rules

Machine-first layers include:
- `01_truth/`
- `02_packets/`
- `03_memory/registry/`
- machine-facing parts of `04_runtime/`

Human-facing explanation may stay richer under:
- `06_human_docs/zh-TW/`

### Compiled Intake Principle
Zero-memory intake should not begin with blind full-repo traversal.

The default v0 intake approach is:
- use a small canonical intake pack
- request more files only after calibration
- if a compact intake artifact is introduced later, it should be compiled from canonical sources rather than maintained as an independent handwritten truth file

### Compiled Intake Rule
The current v0 intake pack is the default intake profile, not a closed forever list.

Intake packs must be derived from canonical files. Handwritten standalone intake content is forbidden.

An intake pack is a compiled, extracted, or compressed onboarding view for zero-memory agents. It is not canonical truth.

If an intake pack conflicts with canonical files, the canonical files win.

Intake must not regress into blind full repo traversal.

v0 does not implement a dynamic intake compiler or role-specific intake profiles. Future task / memory / review intake profiles may exist only if they remain derived from canonical files.

### Current v0 Intake Pack
Single maintained owner for the exact current zero-memory intake pack:
1. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
2. `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
3. `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md`
4. `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`

Other landing files should reference this section instead of repeating the exact 4-file list.
<!-- SHADOWMAS_PRINCIPLES_PATCH:END -->
