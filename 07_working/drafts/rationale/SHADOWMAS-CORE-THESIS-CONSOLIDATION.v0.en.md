# SHADOWMAS-CORE-THESIS-CONSOLIDATION.v0.en.md | draft consolidation note for the shadowMAS core thesis
# related: [README, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, SHADOWMAS-GOVERNANCE-MATRIX, SHADOWMAS-PROMPT-LAYERING-CONTRACT, PACKET-FIELD-DICTIONARY, MEMORY-PLANE-HARNESS, SHADOWMAS-RUNTIME-LOADING-MAP, SHADOWMAS-OPERATOR-GUIDE, SHADOWMAS-MANIFESTO-DRAFT, mdl_compressive_refinement_rationale]
# phase: core_thesis_consolidation_draft

# shadowMAS Core Thesis Consolidation v0 Draft

## Status

DRAFT ONLY.

This note is non-canonical. It is not promotion, not implementation, not a
product claim, and not marketing copy. It does not modify canonical truth and
does not replace any file under `01_truth/`.

This note requires owner review before any promotion or downstream update.

## Purpose

This note consolidates the corrected core thesis of shadowMAS for later owner
review. It is a working draft that may help future edits align README,
current truth, target truth, operator guidance, and rationale language without
silently changing canonical truth.

## Corrected Core Thesis

shadowMAS is a local-first control-and-record layer around agent-generated
work.

Its core problem is authority-bounded interpretation under change. As
runtimes, agents, tools, memory backends, project rules, and user workflows
change, agent-produced information must not silently become trusted, stored,
reused, promoted, or acted upon beyond its warranted authority.

shadowMAS manages that work through packets, gates, role/duty separation,
review surfaces, memory-plane discipline, runtime/tool adapter boundaries, and
final human review.

## What shadowMAS Is Not

shadowMAS is not:

- a runtime engine
- a workflow engine
- a replacement for project truth
- a memory backend
- a tool owner
- a governance owner over user projects
- an automatic merge, promote, or approve system
- a system that scans or absorbs external repos by default

## Defensive Mechanisms vs Core Mechanisms

Core mechanisms:

- packet IR
- authority layers
- gate / promotion discipline
- human review surface
- memory-plane boundaries
- runtime/tool adapter boundaries
- non-interference with project truth

Defensive mechanisms:

- external intake quarantine
- pollution / history hygiene
- no raw repo ingestion
- no raw memory/n8n ingestion
- no product-repo write-back by default

Pollution prevention is a defensive mechanism. It is not the full shadowMAS
thesis.

## Dynamic Adaptation Thesis

shadowMAS is intended to adapt to each user's own project, truth layer, memory
layer, toolchain, governance habits, and workflow shape.

It should support individuals and groups using different agents and tools. It
should not force one fixed workflow. It should provide review and control
around 1-to-many agent work.

This dynamic adaptation axis is not fully implemented yet. The current repo
mostly contains packet/gate/boundary scaffolding, validators, workspace
tooling, and draft contracts.

## Packet / Gate / Review Thesis

Packets are bounded, inspectable artifacts.

Gates handle validity and authority boundaries.

Review surfaces compress decision load for humans.

Schema-valid is not authority-valid. Readable output is not truth closure.
Advisory recommendation does not decide.

## MDL Usage Note

Do not collapse all MDL usage into one meaning.

MDL may appear as a compression / refinement idea. MDL may appear in external
mission packet naming. MDL may appear as a small execution kernel. These can
coexist as related uses.

This note does not force repo-wide terminology consolidation.

## Non-Interference Thesis

User project truth remains authoritative for domain facts.

A user repo can develop and operate without shadowMAS.

The user memory layer is not absorbed.

The user tool layer is not owned by shadowMAS.

The user governance/workflow is not overridden.

shadowMAS records, gates, and reviews agent work around those layers.

## Claims To Avoid

Do not claim:

- dynamic personalization is fully implemented
- runtime enforcement exists
- production safety
- schema-valid packets are authority-valid
- empirical human oversight improvement
- shadowMAS replaces LangGraph, CrewAI, MCP, OpenAI Agents SDK, or similar
  tooling
- shadowMAS is reducible to external pollution prevention

Do not use this note as promotional copy. Keep future use technical,
bounded, and tied to implementation state.

## Evidence Basis

This note was drafted against the following internal surfaces:

- `README.md`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-TARGET-TRUTH.v0.en.md`
- `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`
- `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
- `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md`
- `03_memory/MEMORY-PLANE-HARNESS.v0.en.md`
- `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md`
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md`
- `06_human_docs/en/onboarding/SHADOWMAS-OPERATOR-GUIDE.v0.en.md`
- `06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md`
- `07_working/drafts/rationale/SHADOWMAS-MANIFESTO-DRAFT.v0.md`
- `07_working/drafts/rationale/mdl_compressive_refinement_rationale.md`

These filenames are cited as internal evidence only. This note does not update
or supersede them.

## Future Use

This note may later inform README, CURRENT-TRUTH, or TARGET-TRUTH edits.

Such edits require a separate owner decision and change-impact review.

This note itself does not update canonical truth.
