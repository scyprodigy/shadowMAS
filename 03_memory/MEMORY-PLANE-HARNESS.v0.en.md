# MEMORY-PLANE-HARNESS.v0.en.md

## Purpose
This file defines the minimum memory-plane harness for shadowMAS v0.

Its goal is to:
- separate truth from memory
- separate durable memory from temporary state
- separate reusable knowledge from execution residue
- define promotion and invalidation boundaries
- provide a stable base for future packet and retrieval work

This is a minimum harness, not a full memory platform.

## Core Rule
Memory is not truth by default.

Truth must stay repo-first.
Memory may support work, retrieval, review, and continuity,
but memory must not silently replace approved truth.

## Memory Plane Layers

### 1. session_log
Meaning:
Recorded trace/history of a session or run.

Purpose:
- preserve what happened
- preserve what was discussed
- preserve what was decided during one session/run
- support later audit, mergeback, and continuity

Typical contents:
- session handoff files
- run summaries
- task execution traces
- mergeback notes
- reviewer notes tied to one run/session

Properties:
- historical
- useful for traceability
- not automatically reusable as stable guidance
- not canonical truth

### 2. working_memory
Meaning:
Current task-critical active state used during ongoing work.

Purpose:
- support current task continuity
- keep temporary structured context
- reduce repeated re-reading during one active chain

Typical contents:
- current extraction summaries
- temporary packet interpretations
- temporary normalized notes
- current task context fragments
- active route hints

Properties:
- active and short-lived
- replaceable
- allowed to be incomplete
- may be rebuilt
- must not be treated as approved shared memory

### 3. shared_memory
Meaning:
Reusable approved memory that can help across sessions or tasks.

Purpose:
- preserve reusable knowledge
- keep stable patterns below canonical truth
- reduce rediscovery of recurring operational knowledge

Typical contents:
- approved heuristics
- recurring known-good patterns
- stable interpretation notes
- reusable governance knowledge
- reusable tooling notes

Properties:
- more stable than working_memory
- still below canonical truth
- may support planning and review
- requires explicit promotion discipline

## Truth Relationship

### repo-first rule
Approved repo truth remains first truth source.

That includes:
- formal truth docs
- approved governance docs
- approved packet definitions
- approved project canonical docs when shadowMAS touches a project

### support-not-arbitrate rule
Memory may:
- support retrieval
- support continuity
- support summarization
- support routing
- support review preparation

Memory may not:
- auto-overwrite approved truth
- masquerade as canonical
- bypass promotion gates
- turn cache hits into truth

## Relationship to T-layers

### T2 Approved Truth Artifacts
- canonical truth
- not memory by default

### T3 Approved Shared Memory
- reusable approved memory
- stable enough for reuse
- below T2 unless promoted

### T4 Execution Feed
- active outputs/evidence
- often the raw source for memory candidates
- not stable truth

### T5 Ephemeral / Cache / Session State
- temporary state and cache
- never direct truth
- should be cheap to drop or rebuild

## Promotion Paths

### Allowed direction
- `T4 -> T3` through approval gate
- `T3 -> T2` through stronger promotion gate

### Forbidden shortcuts
- `T5 -> T2`
- `T5 -> T3` without validation
- `T4 -> T2` without formal promotion
- retrieval result -> canonical truth

## Invalidation Rule
Every reusable memory should have explicit invalidation logic.

Examples of invalidation triggers:
- source truth changed
- referenced file removed
- policy superseded
- packet schema changed
- source hash mismatch
- project-local truth replaced
- runtime assumption no longer valid

If invalidation occurs:
- mark memory as stale or broken_reference
- do not keep presenting it as active reusable memory
- review before re-promotion

## Minimum Data Model Direction

### session_log direction
Should prefer:
- append-friendly records
- session_id linkage
- task_id linkage
- run_id linkage
- human-readable trace value

### working_memory direction
Should prefer:
- compact structured fragments
- task-bound scope
- easy overwrite/rebuild
- low ceremony
- fast discardability

### shared_memory direction
Should prefer:
- explicit scope
- source_refs
- summary + structured payload
- invalidation triggers
- confidence
- promotion candidate handling
- approval metadata later

## Memory Storage Direction v0
shadowMAS v0 prefers:
- file-first durable memory
- repo-visible inspectability
- no DB-first dependency
- registry-assisted control
- local retrievable artifacts where needed

This means:
- durable memory may live as files
- registry tracks status/role
- cache may live outside truth layers
- vector retrieval may exist later, but does not become truth authority

## Relationship to Packets

### task_packet
May create:
- working-memory fragments
- session-log artifacts

### memory_packet
Main structured vehicle for:
- reusable memory candidates
- shared_memory content
- invalidation and promotion metadata

### review_packet
May be generated when:
- promotion decision is needed
- memory/truth conflict exists
- invalidation impact is non-trivial

## Relationship to Runtime
Runtime infrastructure may manage:
- indexing
- retrieval
- cache
- temporary state
- transport of packets

But runtime substrate is not memory truth by itself.

## Human Review Rule
Human review is required when:
- a memory candidate may influence broad future behavior
- promotion to shared memory is non-trivial
- promotion to canonical truth is proposed
- invalidation affects previously reused knowledge
- cross-project reuse risk is meaningful

## v0 Minimum Practical Interpretation
For v0, shadowMAS only needs this minimum shape:

- session_log = historical continuity
- working_memory = current active state
- shared_memory = approved reusable knowledge
- cache = acceleration only
- truth = separate and higher

That is enough to begin.

## Does Not Require Yet
This v0 harness does not require:
- a database
- a full memory graph engine
- Letta/MemGPT runtime
- automatic promotion engine
- vector DB as first-class truth source
- UI memory console

## Still Not Final
The following remain open:
- exact file naming patterns for memory artifacts
- exact approval metadata for shared_memory
- exact retention policy
- exact indexing backend
- exact cache implementation
- exact automation around promotion/invalidation
