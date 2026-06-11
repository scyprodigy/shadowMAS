# PERSONALIZATION-ADAPTATION-READINESS-CONTRACT.v0.en.md | draft readiness boundary for future personalization and dynamic adaptation surfaces
# related: [SHADOWMAS-TARGET-TRUTH, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-GOVERNANCE-MATRIX, SHADOWMAS-PROMPT-LAYERING-CONTRACT, MEMORY-PLANE-HARNESS, SHADOWMAS-CORE-THESIS-CONSOLIDATION]
# phase: personalization_adaptation_readiness_contract_draft

# Personalization Adaptation Readiness Contract v0 Draft

## Status

NON-CANONICAL DRAFT.

This document is not implementation.
It is not a memory backend.
It is not runtime behavior.
It is not an authority validator.
It is not learned personalization.
It is not automatic adaptation.
It does not modify user project truth.
It does not absorb user memory.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`,
validators, runtime adapter code, workspace tooling, tests, packet fixtures, or
product repositories.

This draft requires owner review before any promotion, schema work,
implementation work, or downstream update.

## Purpose

This document defines a readiness contract for future dynamic adaptation and
personalization surfaces in shadowMAS.

It records the minimum boundary a later personalization design would need before
any adaptation packet schema, personalization profile, memory backend, runtime
adapter behavior, authority validator, or implementation work can safely begin.

The contract exists to preserve the gap between current v0 readiness and future
target capability. It should help future work reason about adaptation without
turning reviewable evidence into hidden authority.

## Core Definition

Personalization / adaptation means shadowMAS may learn or record reviewable
patterns about a user's project, workflow, tools, memory boundaries, and
repeated agent-work issues.

Examples include repeated review friction, recurring boundary hits, repeated
handoff failures, recurring verifier edge cases, memory invalidation patterns,
or tool adapter mismatches.

Personalization / adaptation must not silently promote those patterns into:

- truth
- approved shared memory
- authority
- runtime behavior
- product-repo write-back
- user preference

Every adaptation must remain:

- layer-labeled
- source-linked
- reviewable
- invalidatable
- resettable
- exportable
- deletable
- human-gated

Repeated evidence may justify a candidate. It does not create authority.

## User-Owned Layers

### `project_truth_layer`

Meaning:
The user's project-local canonical truth, including domain facts, repo
structure, schemas, APIs, business rules, release decisions, and project-local
truth-priority files.

What shadowMAS may observe:

- declared project truth sources
- explicit project entry files supplied by the user or task
- scoped truth touchpoints named in a task or packet
- conflicts between execution feed and project-local truth
- repeated review friction caused by missing or ambiguous project truth

What shadowMAS must not take over:

- project domain facts
- schema or API authority
- business-rule decisions
- canonical product branch promotion
- project-local truth-priority rules

What requires human approval:

- treating a project-specific pattern as reusable guidance
- proposing a project truth update
- exporting any shadowMAS-derived artifact into the project repo
- changing project-local truth sources or truth-priority interpretation

### `user_memory_layer`

Meaning:
The user's private, project-local, team-local, or tool-local memory material,
including preferences, historical notes, working memory, approved shared
memory, and private context outside shadowMAS.

What shadowMAS may observe:

- memory boundaries explicitly declared by the user
- memory invalidation events reported as review evidence
- approved memory packet candidates
- user-approved summaries of recurring memory failures

What shadowMAS must not take over:

- private memory content
- external memory stores
- memory backend selection
- approved shared memory promotion
- deletion or retention decisions for user-owned memory

What requires human approval:

- importing or summarizing user memory
- treating a pattern as approved shared memory
- converting an adaptation candidate into a memory packet candidate
- retaining, exporting, deleting, or resetting adaptation state tied to memory

### `tool_layer`

Meaning:
The user's toolchain and automation environment, including editors, agents,
local models, scripts, hooks, CI, MCP tools, workflow tools, and external
automation platforms.

What shadowMAS may observe:

- declared tool capabilities
- repeated tool adapter mismatch
- host/runtime constraints reported by a scoped task
- tool outputs captured as execution feed or evidence
- user-approved tool notes

What shadowMAS must not take over:

- tool selection
- tool account state
- host-native prompts
- automation credentials
- tool permission models
- workflow tool graphs

What requires human approval:

- turning a repeated tool mismatch into adapter guidance
- enabling a runtime adapter behavior
- creating hooks, validators, CI, or workflow automation
- treating tool output as anything above execution feed

### `governance_workflow_layer`

Meaning:
The user's or team's approval habits, review cadence, escalation expectations,
handoff style, branching practice, merge decision process, and human-last-mile
workflow.

What shadowMAS may observe:

- explicit review requirements
- repeated human correction
- repeated review friction
- repeated handoff failure
- repeated escalation or stop-condition patterns

What shadowMAS must not take over:

- final review authority
- approval standards
- escalation ownership
- release or merge decisions
- whether automation is allowed in a workflow

What requires human approval:

- treating recurring correction as a preference candidate
- compressing review surfaces for a user or team
- changing review defaults or escalation defaults
- enabling any delegated authority envelope

### `repo_architecture_layer`

Meaning:
The structure, ownership, build/test/deploy independence, and history of the
user's product repository or project workspace.

What shadowMAS may observe:

- repo architecture facts supplied by the user or scoped task
- declared allowed read and write scopes
- repeated architecture-related boundary hits
- stale adaptation candidates caused by repo structure changes

What shadowMAS must not take over:

- product repo layout
- product repo build, test, deploy, or runtime dependencies
- branch protection or merge authority
- repo history cleanup decisions
- product-owned artifact placement

What requires human approval:

- writing any adaptation state into a product repo
- linking a project workspace to shadowMAS
- using project architecture patterns as reusable guidance
- changing adaptation scope after repo architecture changes

### `runtime_host_layer`

Meaning:
The provider, IDE, local runner, model host, or opaque host environment that
shapes execution behavior outside shadowMAS source truth.

What shadowMAS may observe:

- runtime host name and declared constraints
- host capability evidence
- repeated runtime adapter mismatch
- runtime signals captured as execution feed
- host anomalies reported for review

What shadowMAS must not take over:

- host-native hidden prompts
- provider policy
- runtime execution permission
- host credential state
- runtime signal authority

What requires human approval:

- promoting host-specific behavior into adapter guidance
- changing runtime adapter prompts
- treating runtime output as reusable evidence
- enabling runtime-side adaptation behavior

## Readiness Fields

A future personalization / adaptation readiness record should include at least:

- `adaptation_contract_id`: stable identifier for the readiness record.
- `contract_version`: contract version, initially `v0`.
- `contract_status`: lifecycle status such as `draft`, `inactive`,
  `candidate_for_review`, `blocked`, `rejected`, or `retired`.
- `user_scope_ref`: bounded reference to the user, team, or operator scope
  without exposing private identity where not needed.
- `project_scope_ref`: bounded reference to the project or workspace scope.
- `project_truth_sources`: explicit project-local truth sources used as
  boundary anchors.
- `memory_scope`: declared memory boundary, such as none, session-local,
  project-local, team-local, or approved shared memory.
- `tool_scope`: declared toolchain or runtime hosts being considered.
- `workflow_scope`: declared governance / review / handoff workflow boundary.
- `allowed_adaptation_signals`: evidence classes allowed to become adaptation
  candidates.
- `forbidden_adaptation_signals`: evidence classes that must not be used for
  adaptation.
- `adaptation_candidate_types`: candidate categories this record may describe.
- `promotion_required`: explicit promotion path required before reuse.
- `invalidation_triggers`: events that make the adaptation candidate stale or
  require re-review.
- `reset_required`: whether user/project adaptation state must support reset.
- `export_required`: whether user/project adaptation state must support export.
- `delete_required`: whether user/project adaptation state must support
  deletion.
- `human_review_required`: human review requirement before use, reuse,
  promotion, export, deletion, or write-back.
- `claim_ceiling`: strongest claim this record may support.
- `non_claim_record`: explicit list of claims not made by this record.

## Allowed Adaptation Signals

Allowed adaptation signals are evidence classes only. They may support
adaptation candidates when source-linked, scoped, and reviewed.

- repeated review friction
- repeated `boundary_hit`
- repeated `seam_gap`
- repeated verifier edge case
- repeated packet field ambiguity
- repeated handoff failure
- repeated memory invalidation event
- repeated tool adapter mismatch
- repeated human correction

Allowed signals must still obey data minimization. The signal should carry the
least sensitive evidence needed for review, not raw private context.

## Forbidden Adaptation Signals

The following must not be used as adaptation signals:

- secrets
- credentials
- raw logs
- raw external repo content
- private memory content
- n8n workflow graph content
- unreviewed runtime output
- unreviewed recommendations
- tool capability
- model confidence score
- cache hit
- retrieval hit
- external project identity
- user private preference unless explicitly approved

If a forbidden signal appears, the adaptation candidate must stop, reject, or
route to human review according to the future authority boundary. It must not be
silently normalized into usable personalization state.

## Adaptation Candidate Types

Future adaptation candidates may include:

- `review_preference_candidate`
- `recurring_boundary_warning_candidate`
- `seam_contract_candidate`
- `verifier_edge_case_candidate`
- `memory_invalidation_rule_candidate`
- `prompt_layering_note_candidate`
- `tool_adapter_note_candidate`
- `handoff_review_note_candidate`

These names are draft candidate categories only. They are not packet families,
schema enum values, approved shared memory, runtime rules, or canonical truth.

## Claim Ceiling

Allowed claim ceilings for this draft:

- `adaptation_candidate_only`
- `evidence_only`
- `rejected`

Rules:

- An adaptation candidate is not truth.
- An adaptation candidate is not memory.
- An adaptation candidate is not authority.
- An adaptation candidate is not runtime behavior.
- An adaptation candidate is not user preference until approved.
- `evidence_only` may support review but cannot be reused as a preference,
  memory, tool rule, project rule, or runtime rule.
- `rejected` means the candidate must not return without new evidence and human
  review.

## Invalidation / Reset / Export / Delete Requirements

User/project adaptation state must be:

- resettable
- exportable
- deletable

Adaptation state must become stale or require re-review when:

- project truth changes
- memory boundary changes
- toolchain changes
- human reverses a prior preference
- repo architecture changes
- runtime host assumptions change
- cited source references break
- the adaptation scope no longer matches the active project or workflow

Reset, export, and delete behavior must be designed before any implementation.
An adaptation surface that cannot be reset, exported, and deleted must remain
blocked.

## Promotion Rules

- No automatic promotion.
- Human review is required before reuse, promotion, write-back, or runtime use.
- Repeated signal is evidence, not authority.
- Candidate registry is not approval.
- Lessons queue is not learned personalization.
- Memory plane harness is not memory backend.
- Runtime adapter draft is not tool adaptation implementation.
- Review packet recommendation is advisory unless a separate authority boundary
  approves action.
- Cache, retrieval, or confidence may support investigation but must not promote
  an adaptation candidate.

## Unsafe Implementation Paths

The following are unsafe and must not be implemented from this draft:

- learning from lessons queue automatically
- treating candidate registry as memory
- using runtime signals as authority
- using model confidence as authority
- writing adaptation state into product repo
- absorbing user memory
- importing external workflow graphs
- overriding user project truth
- adapting without reset/export/delete
- treating a recurring correction as preference without approval
- turning tool capability into write permission
- treating external intake as external repo ingestion

## Human-Last-Mile Decisions

Human authority remains the last mile for:

- whether adaptation is enabled
- what scope it applies to
- whether a candidate becomes reusable guidance
- whether project-specific pattern becomes shared memory
- whether a tool mismatch becomes adapter guidance
- whether a recurring correction becomes preference
- whether adaptation state should be reset, exported, or deleted
- whether a rejected candidate may be reopened with new evidence
- whether any future schema, validator, memory backend, or runtime adapter work
  should begin

## Future Unlocks

Before implementation or promotion work may begin, the repo needs:

- owner review of this draft
- paper simulation of adaptation candidates
- inactive adaptation packet schema draft
- inactive personalization profile draft
- memory backend decision
- authority validation boundary
- runtime adapter boundary closure
- deletion/export/reset policy
- explicit decision on where adaptation candidates may be stored
- explicit decision on whether any candidate type belongs in packet schemas,
  memory packets, registries, or runtime adapter contracts

## Non-Goals

This draft does not create or authorize:

- personalization engine
- memory store
- runtime adapter implementation
- automatic learning
- automatic write-back
- automatic promotion
- external repo scanning
- user memory absorption
- authority validator
- active intake behavior
- product repo artifact writes
- packet schema changes
- validator code

## Do Not Promote Yet

This remains draft because personalization scope, adaptation candidate schema,
memory backend behavior, authority validation, runtime adapter boundaries, and
reset/export/delete policy are unresolved.
