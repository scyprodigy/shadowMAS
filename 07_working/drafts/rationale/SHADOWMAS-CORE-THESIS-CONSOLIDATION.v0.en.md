# SHADOWMAS-CORE-THESIS-CONSOLIDATION.v0.en.md | draft consolidation note for the shadowMAS core thesis
# related: [README, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, SHADOWMAS-GOVERNANCE-MATRIX, SHADOWMAS-PROMPT-LAYERING-CONTRACT, PACKET-FIELD-DICTIONARY, MEMORY-PLANE-HARNESS, SHADOWMAS-RUNTIME-LOADING-MAP, SHADOWMAS-OPERATOR-GUIDE, SHADOWMAS-POSITIONING-STATEMENT, mdl_compressive_refinement_rationale]
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

## Parallel Capability and Open Core

Concurrent work by multiple agents is a required target capability. A small
reusable core means a small stable boundary, not a one-agent workflow or one
mandatory scheduling, storage, or merge algorithm. Agents may investigate and
produce candidates in parallel. A host-specific execution layer must make
conflicting writes detectable or controlled; candidate handoffs should retain
their bases, dependencies, competing results, and authority context for review.
Neither packet level nor a clean text merge establishes shared task intent.

Single-writer commits, isolated workspaces with version checks, and coordinated
shared drafting are alternative implementation strategies. Their suitability
depends on the current task and host. None is promoted here as a universal
shadowMAS runtime contract. Keep the user's project tree separate from Shadow.

For an unfamiliar user, the entry surface should reveal what can be tried now,
what result to expect, and how to inspect or correct it. Internal candidate
count and packet vocabulary should not be the user's first conceptual model.
This is a design hypothesis informed by Norman's account of discoverability,
feedback, and conceptual models, not evidence that the current onboarding works.

## Candidate Convergence for the Next Trial

The candidate registry currently has ten entries: eight await human review;
two `P5` entries primarily record already landed, approved patch work, with a
release-phase history action still deferred. This paragraph does not change
their statuses or approve a new mechanism.

- `P1-001`: test whether a real review leaves residual information missing
  before adding review-packet fields; reuse existing fields where possible.
- `P2-001/003/004/005/006/007`: treat the signal-field proposals as related,
  unimplemented hypotheses. Evaluate one observed signal path and its collisions
  before choosing fields; do not adopt the cluster as a global ontology.
- `P4-001`: inspect a host's actual shared-state guarantees before proposing
  how its agents coordinate. A capability probe is evidence, not enforcement.
- `P5-001/002`: distinguish retrospective landed work from active unmet user
  needs when ordering future work; preserve their registry record.

A useful next trial gives two agents concurrent, bounded work with both an
independent case and a dependency-conflict case. Record the common base,
candidate outcomes, detected and missed conflicts, human correction effort,
and whether the user could find the raw evidence. Compare coordination
strategies on those observations without inventing a universal score or
requiring new packet fields first.

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
- `07_working/drafts/rationale/SHADOWMAS-POSITIONING-STATEMENT.v0.draft.en.md`
- `07_working/drafts/rationale/mdl_compressive_refinement_rationale.md`

The entry-design hypothesis also draws on Donald Norman's [revised-edition
preface](https://jnd.org/preface-design-of-everyday-things-revised-edition/)
and [Design as Communication](https://jnd.org/design-as-communication/).
The parallelism correction draws on [optimistic concurrency](https://db.cs.cmu.edu/papers/1981/kung-tods1981.pdf),
[software merging](https://researchportal.vub.be/en/publications/a-state-of-the-art-survey-on-software-merging/),
[CRDT convergence](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf),
and the [MAST](https://arxiv.org/pdf/2503.13657v2) and
[AgentRoom](https://arxiv.org/html/2608.23740v1) multi-agent studies reviewed
in full in this session. These sources establish tradeoffs and failure modes,
not a measured shadowMAS outcome.

These filenames are cited as internal evidence only. This note does not update
or supersede them.

## Future Use

This note may later inform README, CURRENT-TRUTH, or TARGET-TRUTH edits.

Such edits require a separate owner decision and change-impact review.

This note itself does not update canonical truth.
