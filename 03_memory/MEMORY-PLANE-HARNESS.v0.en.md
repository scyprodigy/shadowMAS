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
- `T5 -> T4` through runtime assembly only
- `T4 -> T3` through approval gate
- `T3 -> T2` through stronger promotion gate

Meaning:
- `T5` may become `T4` when ephemeral material is assembled into task-serving evidence
- `T4` may become `T3` only after review confirms reusable value and acceptable source discipline
- `T3` may become `T2` only through stronger approval because reusable memory is still below canonical truth

### Forbidden shortcuts
- `T5 -> T2`
- `T5 -> T3`
- `T4 -> T2` without formal promotion
- retrieval result -> canonical truth

`T5` must not jump directly to `T3` or `T2`.

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

## Status Semantics

### stale
Meaning:
The source or prerequisite changed, so the memory may still be interpretable but must not remain trusted by default.

Use when:
- a cited source changed
- a truth file was superseded
- an assumption behind the memory no longer matches current repo state

### broken_reference
Meaning:
The cited target no longer resolves, exists, or can be reliably linked.

Use when:
- a referenced file was deleted
- a reference points to a path or artifact that no longer resolves
- a move or rename left the memory without a valid updated target

### superseded
Meaning:
The memory still exists historically, but a newer approved memory has replaced it for active use.

### archived
Meaning:
The memory is retained for history or audit only and should not be used as active reusable guidance.

Difference summary:
- `stale` means re-check is required because the source basis changed
- `broken_reference` means the source basis cannot currently be resolved
- `superseded` means a newer active replacement exists
- `archived` means historical retention without active use

## Ghost Dependency Rule
Deleted, moved, renamed, or superseded sources must not remain silently usable through old memory, old index entries, retrieval cache, or old summaries.

A shared-memory artifact is not safe merely because a cached retrieval still returns it.
If the cited source is gone, moved without resolution, or replaced by newer truth, the old memory must not continue to behave as active reusable memory.

This rule exists to prevent ghost dependencies:
- old summary pretending a deleted file still exists
- cached retrieval pretending a renamed source is still valid without re-resolution
- reusable memory pretending superseded truth is still the active basis

## Shared Memory Impact Rules
Shared memory and other reusable memory must absorb invalidation from the sources they cite.

Required effects:
- source changed -> mark `stale` until rechecked
- source deleted -> mark `broken_reference`
- source moved or renamed -> mark `broken_reference` unless references are explicitly repaired and revalidated
- truth superseded -> mark `stale` at minimum, and move to `superseded` if a newer approved memory replaces it
- manual reject or discard -> remove from active reusable use and treat as rejected or archived according to review outcome

Retrieval output, cache output, and old summaries may help investigation, but after source invalidation they must not be presented as approved shared memory or active reusable memory until revalidated.

## Reuse-Safety Metadata
Reusable memory may carry structured reuse-safety metadata in addition to `source_refs`.

This metadata may include:
- `validity.applies_to` to express intended reuse boundary
- `validity.stale_on` to express which changes should make the memory stale
- `validity.review_after` to express when reuse should trigger re-review
- `invalidation.current_state` to express current invalidation condition
- `invalidation.source_hashes` to help compare whether cited sources changed

These fields help make reuse inspectable, especially for shared memory and other reusable memory below canonical truth.
They are support metadata only:
- not promotion proof
- not authority source
- not a shortcut from memory to truth

`validity.applies_to` is about intended scope, such as modules or task types.
`validity.stale_on` is about which changes should force revalidation.
`review_after` is a re-review hint, not automatic invalidation by itself.
`source_hashes` are comparison aids, not proof that a memory is approved or currently correct.

## Status and Invalidation Boundary
Reusable memory may have both lifecycle status and invalidation snapshot metadata.

Use this boundary:
- packet `status` describes lifecycle and reuse standing
- `invalidation.current_state` describes current source-condition snapshot

This means a memory may still carry `status: approved_shared` while also carrying `invalidation.current_state: stale`.
That combination means the memory was once approved for reuse, but current reuse should pause until revalidation occurs.

Local or agent-specific memory may also carry this metadata.
That can improve execution quality and reduce repeated rereading, but local memory still does not become final truth.

Invalidation and revalidation exist to support safer memory reuse.
They do not elevate memory into canonical authority.

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
- validity metadata where reuse boundary matters
- summary + structured payload
- invalidation triggers
- invalidation snapshot where current source condition matters
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
