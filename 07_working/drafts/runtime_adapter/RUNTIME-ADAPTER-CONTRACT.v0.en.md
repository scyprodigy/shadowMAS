> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through governance
> source basis: SHADOWMAS-RUNTIME-ADAPTER-MERGEBACK.v0.md

# RUNTIME-ADAPTER-CONTRACT.v0

## Purpose
Define the general runtime adapter contract for Claude Code, Cursor, Codex, Ollama, hooks, and skills.

This is a working draft, not canonical truth. It does not modify `01_truth/`, `02_packets/`, `03_memory/`, or `04_runtime/`.

A runtime adapter adapts execution. It does not redefine truth.

## Scope
- runtime adapter identity and host constraints
- prompt delivery boundaries
- tool, hook, and skill capability boundaries
- delegation input/output contract
- protected actions and audit expectations
- adapter-specific non-truth rule

## Non-Scope
- no implementation of hooks, scripts, validators, CI, installer, or distributor
- no final runtime adapter architecture
- no canonical promotion into `04_runtime/`
- no product repo write-back
- no resolution of version-governance edge cases

## Runtime Adapter Identity
A draft runtime adapter identity SHOULD include:
- `adapter_id`
- `target_runtime`
- `target_host`
- `supported_roles`
- `prompt_delivery_method`
- `tool_capabilities`
- `hook_support`
- `skill_support`
- `known_host_constraints`
- `protected_actions`
- `delegation_contract_refs`
- `audit_expectations`
- `source_refs`

## Minimum Contract Elements
Each runtime adapter draft SHOULD declare:
- identity
- host constraints
- prompt delivery boundary
- tool capability boundary
- hook support boundary
- skill support boundary
- delegation input and output contract
- protected actions
- audit expectations
- adapter-specific non-truth rule

## Host Constraints
Host-native / opaque prompts are external constraints, not shadowMAS truth.

Rules:
- host behavior may influence execution
- host behavior must not be treated as maintainable truth
- runtime-specific limitations should be documented as constraints
- adapter rules must yield to canonical shadowMAS and project-local truth

## Prompt Delivery Boundary
Runtime adapter prompts are Layer 4 material.

Rules:
- prompts may compress or adapt layered rules for one host
- prompts must not redefine Shared Core, shadowMAS Governance, or Project Execution truth
- prompt compression or adaptation must not drop must-see governance constraints
- generated prompt files are projections unless separately approved
- prompt delivery paths remain draft until validated per host

## Tool Capability Boundary
Tools MAY enable execution, inspection, editing, or delegation only inside task-declared writable scope.
Tool capability and host capability are execution capacity, not authority.

Tool capability does not grant authority to:
- promote truth
- infer missing project decisions
- bypass human escalation
- write outside declared scope

## Hook Support Boundary
Hooks are runtime guards, not truth sources.

Rules:
- hooks may warn, block, log, or request retry
- hooks must not promote artifacts
- hook output is evidence or runtime signal only
- hook bypass risk must be recorded before promotion

## Skill Support Boundary
Skills are runtime support material.

Rules:
- skills may provide reusable methods or task-specific workflows
- skills must not become canonical truth by invocation
- skill output must be reviewed like other execution feed
- adapter-specific skill behavior requires host validation

## Delegation Input / Output Contract
Delegation SHOULD declare:
- source agent
- target agent or target capability
- task goal
- scope and out_of_scope
- truth_touchpoints
- required capabilities
- writable locations
- acceptance criteria
- stop conditions
- expected review output

Returned output SHOULD include:
- files or artifacts touched
- tests or checks run
- blockers
- scope exceeded status
- acceptance result
- unresolved questions

## Protected Actions
Protected actions include:
- editing canonical truth layers
- writing product repo files without governed task approval
- changing schema, auth, security, or architecture outside scope
- creating hooks, validators, CI, `install.sh`, or `distribute.sh`
- creating AGENTS.md symlinks
- promoting draft material

## Audit / Logging Expectations
Runtime adapters SHOULD record or report:
- source refs used
- task scope
- protected-action attempts
- delegated packets or packet candidates
- files changed
- checks run
- unresolved risks
- host constraints encountered

## Adapter-Specific Non-Truth Rule
Claude Code, Cursor, Codex, Ollama, hooks, and skills require adapter-specific validation before promotion.

Runtime adapter evidence MAY support later canonical work, but it does not become canonical truth by being useful, executable, or host-compatible.

## Rules
- MUST treat runtime adapters as execution adaptation only.
- MUST keep Layer 4 material below canonical truth.
- SHOULD validate each host separately before promotion.
- MAY preserve adapter-specific details as draft/source-evidence.
- MUST NOT decide full runtime adapter architecture in this draft.

## Open Decisions
- final adapter manifest schema
- Codex hook-equivalent model
- Cursor hook and rule-file validation
- Ollama transport
- prompt path policy
- audit log location
- runtime adapter promotion target

## Promotion Requirements
Before promotion, this draft needs:
- human governance review
- host-specific validation for Claude Code, Cursor, Codex, Ollama, hooks, and skills
- reconciliation with prompt layering and governance matrix truth
- explicit decision on adapter manifest ownership
- review of protected actions and write-back boundaries

## Do Not Promote Yet
This remains draft because adapter-specific validation is incomplete, host constraints differ, and full runtime adapter architecture has not been decided.
