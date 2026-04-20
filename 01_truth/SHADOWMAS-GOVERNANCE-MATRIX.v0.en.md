# SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md

## Purpose
This file formalizes the current governance matrix of shadowMAS.

It maps:
- role/operation layers
- truth/governance layers
- runtime substrate concerns

Its goal is to prevent:
- authority confusion
- truth confusion
- execution overreach
- cache/retrieval misclassification
- mergeback ambiguity

## Layer Families

### Role / Operation Layer
- `L1` Human + high-level AI governance
- `L2` Delegated decision / planning
- `L3` Execution / repo implementation
- `L4` Mergeback / sync

### Truth / Governance Layer
- `T0` Human Authority
- `T1` Delegated Decision Authority
- `T2` Approved Truth Artifacts
- `T3` Approved Shared Memory
- `T4` Execution Feed
- `T5` Ephemeral / Cache / Session State

### Runtime / Substrate Layer
- `R` Runtime substrate / execution base

`R` is not a truth layer.
`R` is the execution substrate that carries work.

## Core Interpretation Rule
- `L-layer` answers: who acts
- `T-layer` answers: what kind of authority/state/truth exists
- `R-layer` answers: how execution is carried

These must not be collapsed into one axis.

---

## Governance Matrix

| Layer | Name | Primary Meaning | May Decide? | May Write? | May Promote? | Trust Level |
|---|---|---|---|---|---|---|
| T0 | Human Authority | Final human governance authority | Yes | Yes | Yes | Highest |
| T1 | Delegated Decision Authority | Bounded delegated decision layer | Yes, within scope | Yes, within scope | No direct final promotion without gate | High but bounded |
| T2 | Approved Truth Artifacts | Approved canonical truth | No by itself | Yes, only through governed update | Already promoted truth | Canonical |
| T3 | Approved Shared Memory | Reusable approved memory below canonical truth | No by itself | Yes, if allowed by workflow | May become T2 through gate | Stable but non-canonical |
| T4 | Execution Feed | Outputs, evidence, working results, task flow | No final authority | Yes | No direct promotion | Unstable |
| T5 | Ephemeral / Cache / Session State | Temporary memory, retrieval, cache, short-lived state | No | Yes, temporary only | Never directly | Lowest |

---

## Role Matrix

| Role Layer | Name | Responsibility | Owns Final Authority? | Normal Output Type |
|---|---|---|---|---|
| L1 | Human + high-level AI governance | boundaries, decisions, promotion gates, final judgment | Yes, with human final control | governance decisions, approved directives |
| L2 | Delegated decision / planning | decomposition, bounded decisions, planning, routing suggestions | No | plans, scoped decisions, task packets |
| L3 | Execution / repo implementation | implementation, evidence gathering, edits, retrieval assembly, tests | No | execution feed, patches, structured outputs |
| L4 | Mergeback / sync | consolidation, summary, integration, unresolved-item surfacing | No | mergeback packages, review packets, sync outputs |

---

## Runtime / Substrate Matrix

| Runtime Concern | Belongs to R-layer? | Notes |
|---|---|---|
| queue | Yes | runtime execution infrastructure |
| worker pool | Yes | execution capacity layer |
| retry | Yes | execution policy, not truth policy |
| timeout | Yes | execution control |
| concurrency | Yes | execution substrate |
| lock | Yes | state protection and conflict control |
| backpressure | Yes | workload control |
| cache | Partly | cache as runtime acceleration, not truth |
| vector retrieval engine | Partly | retrieval support only, not truth arbiter |
| packet transport | Yes | runtime movement of machine-stable artifacts |

---

## Truth Handling Rules by Layer

### T0 Human Authority
Meaning:
- final human decision boundary
- may approve, reject, defer, or redefine direction

Rules:
- cannot be bypassed for protected decisions
- remains above all automation

### T1 Delegated Decision Authority
Meaning:
- bounded authority granted inside approved scope

Rules:
- may decompose
- may route
- may decide within allowed bounds
- may not silently redefine protected truth
- may not bypass human escalation rules

### T2 Approved Truth Artifacts
Meaning:
- current canonical truth

Rules:
- must be treated as source of truth
- may only be changed through governed update
- must not be overwritten by T4 or T5

### T3 Approved Shared Memory
Meaning:
- reusable memory that is stable enough to reuse
- not yet equal to canonical truth unless promoted

Rules:
- may support decision/planning
- must retain promotion boundaries
- may not masquerade as T2

### T4 Execution Feed
Meaning:
- outputs from current runs, implementations, retrieval passes, evidence gathering, active task flow

Rules:
- valuable, but unstable
- must not directly become canonical truth
- must pass review and promotion gates

### T5 Ephemeral / Cache / Session State
Meaning:
- temporary memory, cache, short-lived context, retrieval staging

Rules:
- never direct truth
- may accelerate work
- must be safe to drop or rebuild

---

## Promotion Rules

### Allowed promotion directions
- `T4 -> T3` through approval gate
- `T3 -> T2` through stronger approval gate

### Forbidden direct jumps
- `T5 -> T2`
- `T5 -> T3` without validation
- `T4 -> T2` without formal promotion
- runtime cache or retrieval hit -> canonical truth

---

## Role-to-Truth Interaction Matrix

| From Role | May Produce | Typical Target Truth Layer | Notes |
|---|---|---|---|
| L1 | governance decisions, promotion outcomes | T1 / T2 / T3 | final human boundary stays here |
| L2 | task decisions, bounded plans, routing outputs | T1 or T4 | scoped only |
| L3 | implementation outputs, evidence, patches | T4 | execution does not equal truth |
| L4 | merge summaries, integration outputs, unresolved packs | T4, sometimes T3 candidates | mergeback prepares, not finalizes |

---

## Ownership Rule
`owner` and `writable_by` must remain separate concepts.

### owner
Stable responsibility holder.

### writable_by
State-gated writer permissions.

## Retrieval and Cache Rule
Retrieval, vector search, cache, and session state may support work but cannot arbitrate truth.

This means:
- a hit is not approval
- relevance is not authority
- recall is not promotion

## Runtime Adapter Note
Tool-specific prompt adapters such as:
- Claude Code adapter prompts
- Cursor adapter prompts
- GPT/Codex adapter prompts

do not replace this governance matrix.

They are runtime-facing compiled layers, not the top truth source.

## Human Authority Rule
No combination of L2, L3, L4, T3, T4, T5, or R-layer may erase the final human authority boundary.

## Still Not Final
The following remain open:
- final exact R-layer implementation
- final promotion gate checklists
- final file-status registry schema evolution
- final runtime adapter contract
- final write-back automation policy
