> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through governance
> source basis: SHADOWMAS-RUNTIME-ADAPTER-MERGEBACK.v0.md

# AGENT-JOIN-CONTRACT.v0

## Purpose
Define how a new agent joins shadowMAS without undefined authority.

This is a working draft, not canonical truth. It does not modify `01_truth/`, `02_packets/`, `03_memory/`, or `04_runtime/`.

Runtime adapters adapt execution and do not redefine truth.

## Scope
- agent registration for runtime-adapter planning
- join-time declaration of host, capability, role layer, writable locations, and forbidden actions
- routing expectations before an agent receives or produces packet-shaped work
- authority boundaries for Claude Code, Cursor, Codex, Ollama, hooks, and skills

## Non-Scope
- no production agent registry implementation
- no hook scripts, validators, CI, installer, or distributor
- no write-back into product repos
- no change to canonical L/T/R layer definitions
- no approval of dynamic or self-claim role assignment

## Minimum Agent Join Record
A draft join record SHOULD include:
- `agent_id`
- `runtime_or_host`
- `provider`
- `capabilities`
- `intended_role_layer`
- `truth_layer_limit`
- `allowed_output_types`
- `writable_locations`
- `forbidden_actions`
- `prompt_delivery_method`
- `hook_support`
- `skill_support`
- `delegation_input_contract`
- `delegation_output_contract`
- `human_owner`
- `source_refs`

## Authority Boundary
Agents may join dynamically, but no agent joins with undefined authority.
Agents may be added during an active workflow through a governed hot-join process.
Hot-join does not mean dynamic role assignment, self-claim authority, or automatic write permission.

Rules:
- new agents must declare runtime/host, capability, intended role layer, allowed output types, writable locations, and forbidden actions
- dynamic/self-claim role assignment remains disabled for v0 unless later approved
- agents must not promote T4/T5 material directly into T2 truth
- an agent join record is evidence for routing, not approval to modify canonical truth
- runtime or host capability does not create governance authority or write permission

## Required Intake Files
Before joining work, an agent SHOULD receive or be pointed to:
- current task packet or human task scope
- relevant shadowMAS truth boundary files
- project-local truth or entry docs when project work is involved
- applicable runtime-adapter draft constraints
- any packet compatibility or legacy-intake notes needed for the task

## Allowed Outputs by L/T Layer
- `L2/T1`: bounded plans, routing proposals, task packets, review requests
- `L3/T4`: execution feed, patches, test results, artifact summaries
- `L4/T4`: mergeback packages, sync notes, unresolved questions
- `R`: runtime signals, hook warnings, logs, tool capability metadata

Outputs from T4 or T5 MAY become candidates only through governed review.

## Writable Locations
Draft default:
- `07_working/drafts/` for runtime-adapter working drafts
- task-scoped product repo paths only when separately authorized by a governed task
- temporary runtime state only when it is not represented as truth

Agents must treat `01_truth/`, canonical `02_packets/`, canonical `03_memory/registry/`, and `04_runtime/` as non-writable for this draft lane.

## Forbidden Actions
- promote draft or execution feed into canonical truth
- claim authority from runtime identity alone
- write AGENTS.md symlinks
- create hook scripts, validators, CI, `install.sh`, or `distribute.sh`
- rewrite project-local truth from shadowMAS adapter material
- treat skills, hooks, cache, retrieval hits, or host-native prompts as truth sources

## Packet Output Expectations
Delegation SHOULD use packet-shaped output with:
- task goal
- scope
- out_of_scope
- truth_touchpoints
- required_capabilities
- acceptance_criteria
- stop_conditions
- review output expectations

Packet compatibility is not binary. Raw output may need adapter wrapping or packet-candidate normalization before routing.

## Stop / Escalation Conditions
Stop and escalate when:
- authority is undefined
- requested writes exceed declared writable locations
- the agent needs to change protected truth layers
- dynamic or self-claim mode is requested for v0
- a runtime-specific instruction conflicts with canonical truth
- source evidence is missing or ambiguous

## Rules
- MUST declare authority before work starts.
- SHOULD keep agent records small and machine-readable.
- MAY add runtime-specific metadata when it does not override shared semantics.
- MUST keep `owner` and `writable_by` distinct.

## Open Decisions
- final agent registry schema
- persistent scoring location for future dynamic mode
- self-claim transport and locking model
- Codex and Cursor hook-equivalent mapping
- packet storage location for delegated work

## Promotion Requirements
Before promotion, this draft needs:
- human governance review
- reconciliation with the canonical governance matrix
- validation against at least Claude Code, Codex, Cursor, and Ollama examples
- approved registry schema or explicit decision not to use one
- review of write-back and packet routing impacts

## Do Not Promote Yet
This remains draft because v0 dynamic/self-claim mode is not approved, adapter-specific validation is incomplete, and the registry location for agent join records is unresolved.
