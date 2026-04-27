> status: draft / source-evidence
> authority: none
> do not promote without governance review
> source lane: runtime-adapter missing contract drafts

# PROJECT-INTAKE-CONTRACT.v0

## Purpose
Define how an arbitrary project attaches to shadowMAS while preserving project-local truth.

This is a working draft, not canonical truth. It does not modify `01_truth/`, `02_packets/`, `03_memory/`, or `04_runtime/`.

Runtime adapters adapt execution and do not redefine truth.

## Scope
- project hot-intake for a repo or workspace that wants shadowMAS assistance
- project-local truth boundary discovery
- allowed intake sources and minimal intake record
- write-back and traversal constraints

## Non-Scope
- no product repo implementation
- no project business truth creation
- no broad repo traversal mandate
- no installer, distributor, hook, validator, or CI creation
- no canonical shadowMAS truth change

## Minimum Project Intake Record
A draft project intake record SHOULD include:
- `project_id`
- `project_root`
- `project_owner`
- `intake_reason`
- `project_truth_sources`
- `shadowmas_truth_refs`
- `allowed_read_scope`
- `allowed_write_scope`
- `forbidden_paths`
- `current_phase`
- `known_decisions`
- `known_gaps`
- `runtime_hosts`
- `write_back_policy`
- `source_refs`

## Project Truth Boundary
shadowMAS may assist any project, but project-domain truth remains project-local.

Rules:
- shadowMAS governance may structure work, review, memory, routing, and promotion boundaries
- shadowMAS must not replace project domain facts, API contracts, schema decisions, or business rules
- product repos must remain able to develop, implement, test, deploy, and operate without shadowMAS
- runtime adapter drafts must not write back into product repos without explicit governed approval

## Repo Traversal Policy
No blind full-repo traversal by default.
Curated entry files are preferred; broad traversal requires separate governed approval.

Allowed traversal MUST be:
- scoped by task
- tied to explicit intake purpose
- reported in output
- stopped when protected or irrelevant areas are encountered

## Write-Back Boundary
Default write-back state is no write-back.
Write-back must not be inferred from project intake.

Write-back MAY occur only after separate governed approval and when a separate governed task declares:
- target repo
- target paths
- allowed changes
- out-of-scope paths
- review owner
- rollback or review expectation

## Allowed Intake Sources
- project README or entry file
- project-local truth or decision files
- scoped source files named by the task
- prior packets or handoffs
- issue/task descriptions
- screenshots, chats, or external docs as evidence only

## Hot-Intake Status
Hot-intake means a project can be attached while work is already in progress.

Hot-intake does not mean:
- all legacy history is trusted
- project truth is imported into shadowMAS truth
- adapter material can write into the project immediately
- missing decisions can be inferred as decided

## Stop / Escalation Conditions
Stop and escalate when:
- no project truth source can be identified
- the requested action needs business truth not provided by the project
- repo traversal would become broad or blind
- write-back is requested without governed approval
- product repo independence would be weakened
- runtime adapter evidence conflicts with project-local truth

## Rules
- MUST keep project-domain truth local to the project.
- MUST report missing project truth as a gap.
- SHOULD prefer curated entry files over full traversal.
- MAY produce project intake candidates under `07_working/drafts/`.
- MUST NOT treat runtime-adapter drafts as product repo authority.

## Open Decisions
- final project intake record schema
- where project intake packets should be stored
- how project-local decisions are discovered without blind traversal
- write-back contract location
- handling of contaminated or inconsistent project history

## Promotion Requirements
Before promotion, this draft needs:
- human governance review
- examples across more than one project
- alignment with future write-back contract files
- review against prompt layering and governance matrix boundaries
- explicit storage and lifecycle policy for intake records

## Do Not Promote Yet
This remains draft because the write-back contract is not formalized, project intake storage is unresolved, and no multi-project validation has been completed.
