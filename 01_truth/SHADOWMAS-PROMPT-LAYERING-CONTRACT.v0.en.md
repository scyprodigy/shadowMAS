# SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md

## Purpose
This file defines the layering contract for reusable system rules, shadowMAS governance rules, project-local execution rules, runtime-specific adapter prompts, and host-native opaque prompts.

Its goal is to prevent:
- giant prompt collapse
- scope collision
- governance overreach
- project-truth overwrite
- runtime-specific confusion
- hidden host-prompt misunderstanding

## Why this exists
A large multi-agent system cannot safely rely on one flattened mega-prompt.

shadowMAS needs layered rule sources so that:
- reusable rules stay reusable
- governance stays above execution without corrupting project truth
- project truth stays local
- runtime-specific tool prompts remain isolated
- opaque host/platform prompts are acknowledged but not mistaken for maintainable truth

## The 5 Layers

### Layer 1: Shared Core
Definition:
Cross-project reusable agent rules.

This layer covers:
- first discuss, then implement
- first converge, then create tasks
- undefined is not decided
- minimal necessary changes
- no blind repo traversal
- explicit conflict/gap reporting
- token discipline
- inspectability and reversibility principles

This layer must be:
- reusable
- stable
- low-domain
- low-project-specific

This layer must not contain:
- project-specific business truth
- repo-local field truth
- one-project naming rules
- domain-specific API contracts

### Layer 2: shadowMAS Governance
Definition:
Global governance layer for routing, memory, promotion, invalidation, indexing, review, registry, mergeback, and write-back boundaries.

This layer covers:
- packet discipline
- handoff discipline
- memory-plane governance
- promotion/invalidation
- file-status logic
- mergeback boundaries
- write-back safety rules
- cross-session integration discipline
- routing/orchestration policy
- review gate logic

This layer may govern process and structure above projects, but must not replace project-domain truth.

### Layer 3: Project Execution
Definition:
Repo-local execution constraints and business/domain truth for one project workspace.

This layer covers:
- project repo structure
- truth priority inside that project
- domain model
- API contracts
- field dictionary
- ERD
- schema/migration governance
- implementation landing zones
- project-specific role/scope rules

This layer must be:
- readable inside the project repo
- independently maintainable
- authoritative for project-domain facts

This layer must not be overridden by Shared Core or shadowMAS Governance for domain facts.

### Layer 4: Runtime Adapter Prompt
Definition:
Tool/runtime-specific compiled prompt layer used to adapt shadowMAS + project rules to a specific execution environment.

Examples:
- Claude Code adapter prompt
- Cursor adapter prompt
- GPT / Codex adapter prompt
- Ollama local-task adapter prompt

This layer covers:
- tool-specific operating assumptions
- runtime-safe instruction shaping
- tool capability boundaries
- tool-specific formatting/handoff adjustments
- adapter-side prompt compression choices
- runtime-specific safety fences that do not redefine truth

This layer must not:
- replace project canonical truth
- replace shadowMAS governance
- redefine reusable shared-core rules
- pretend to be the top authority

### Layer 5: Host Native / Opaque Prompt
Definition:
The platform-native hidden or semi-hidden instruction layer outside shadowMAS control.

Examples:
- model provider hidden system instructions
- IDE host-native instruction injection
- platform-native built-in routing/safety behavior

This layer is:
- real
- influential
- partly opaque
- not maintainable by shadowMAS directly

It must be documented as an external constraint, not treated as writable truth.

## Reading Order
Default reading order for an agent operating under shadowMAS:

1. Shared Core
2. shadowMAS Governance
3. Project Execution
4. Runtime Adapter Prompt
5. Host Native / Opaque Prompt (acknowledged as external runtime context, not maintained source truth)

## Why this reading order
- Shared Core gives baseline conduct
- shadowMAS Governance gives global operating contract
- Project Execution gives project-local truth
- Runtime Adapter Prompt shapes execution for the current tool/runtime
- Host Native / Opaque Prompt is treated as unavoidable runtime influence

## Maintainability Rule
Only Layers 1 to 4 are actively maintainable source layers.

Layer 5 must be:
- acknowledged
- documented
- treated as an environment constraint

Layer 5 must not become:
- the canonical source of truth
- a writable governance file
- an excuse to flatten the other layers

## Override and Boundary Rules

### Shared Core may
- define reusable baseline behavior
- constrain unsafe general behavior
- define reporting discipline
- define traversal discipline
- define reusable agent conduct

### Shared Core may not
- define project business truth
- replace project canonical files
- invent local project structures
- override project field/API/domain truth

### shadowMAS Governance may
- define global coordination rules
- define memory/promotion/write-back boundaries
- define file-status and packet rules
- define cross-session merge discipline
- define routing and review policy

### shadowMAS Governance may not
- rewrite project-domain facts by itself
- replace project-local canonical truth
- silently promote execution feed into approved truth
- bypass human authority gates for protected truth layers

### Project Execution may
- define business truth for that project
- define local execution constraints
- define local repo structure and local truth priorities
- define project-specific contracts and schemas

### Project Execution may not
- redefine reusable cross-project rules as if global
- bypass shadowMAS governance for promotion/review/write-back control
- claim authority over other project repos

### Runtime Adapter Prompt may
- adapt the layered rules to one tool/runtime
- constrain formatting and operating style for that runtime
- encode tool-specific boundary reminders
- optimize instruction delivery for that runtime

### Runtime Adapter Prompt may not
- redefine canonical truth
- redefine governance boundaries
- silently override project-domain facts
- act as a hidden replacement constitution

### Host Native / Opaque Prompt may
- influence behavior in practice

### Host Native / Opaque Prompt may not
- be treated as maintainable shadowMAS truth
- replace the explicit written governance layers
- justify skipping formal source artifacts

## Conflict Resolution Rules

### Conflict type A
Shared Core vs Project Execution

Resolution:
- Shared Core wins for reusable behavioral baseline
- Project Execution wins for project-domain facts

### Conflict type B
shadowMAS Governance vs Project Execution

Resolution:
- shadowMAS Governance wins for process/governance/memory/write-back rules
- Project Execution wins for project-domain truth

### Conflict type C
Shared Core vs shadowMAS Governance

Resolution:
- Shared Core remains the reusable behavioral floor
- shadowMAS Governance adds governance-specific constraints without breaking shared-core principles

### Conflict type D
Runtime Adapter Prompt vs Project Execution

Resolution:
- Runtime Adapter Prompt may adapt delivery
- Project Execution wins for project-domain truth

### Conflict type E
Runtime Adapter Prompt vs shadowMAS Governance

Resolution:
- Runtime Adapter Prompt may adapt runtime execution
- shadowMAS Governance wins for governance process, memory, review, and write-back boundaries

### Conflict type F
Host Native / Opaque Prompt vs maintained source layers

Resolution:
- do not treat the host layer as canonical
- document runtime anomalies if observed
- preserve explicit source layers as the maintainable contract
- create adapter mitigations where needed

### Conflict type G
Two project-local truths conflict

Resolution:
- the project's own truth-priority rules decide
- shadowMAS does not invent a domain winner

## Practical Rule for Agents
An agent must always ask:

1. Is this a reusable cross-project behavior rule?
   - if yes, Shared Core

2. Is this a governance/routing/memory/review/write-back rule?
   - if yes, shadowMAS Governance

3. Is this a project-local business/domain/repo truth?
   - if yes, Project Execution

4. Is this a tool/runtime-specific adaptation rule?
   - if yes, Runtime Adapter Prompt

5. Is this only a host/platform hidden influence?
   - if yes, treat as Host Native / Opaque Prompt, not maintainable truth

If uncertain:
- do not guess
- mark as unresolved
- escalate for human or governance review

## Anti-Collapse Rule
Do not flatten these five layers into one giant prompt or one giant truth file.

The layers may be composed operationally,
but they must remain separately maintainable as source artifacts where possible.

## Composition Rule
A runtime may assemble a composed execution context from:
- Shared Core
- shadowMAS Governance
- Project Execution
- Runtime Adapter Prompt

But the source files must remain separate.

Host Native / Opaque Prompt remains outside direct composition ownership.

That means:
- composition is allowed
- flattening source-of-truth ownership is not allowed

## Relationship to Product Repos
shadowMAS should preferably live in its own system root/repo.

Project repos may receive selected exported artifacts such as:
- START-HERE files
- MASTER-INDEX files
- TRUTH-PRIORITY files
- CHANGE-IMPACT files
- translation policy files
- write-back suggestions

These exports do not make the project repo equal to shadowMAS itself.

## Human Authority Rule
Human authority remains above all layers.

No layer may erase the final human decision boundary.

## Still Not Final
The following are still open:
- exact future shared-core source file names
- exact future composed runtime prompt format
- final promotion automation rules
- final upgrade migration contract between shadowMAS and project-local rules
- final runtime-adapter file naming policy
- final host-anomaly reporting policy
