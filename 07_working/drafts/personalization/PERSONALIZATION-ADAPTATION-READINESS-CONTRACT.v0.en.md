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

It records unresolved boundaries for a later persisted personalization profile,
memory backend, runtime adapter, or authority validator. Ordinary conversation
repair within an authorized task does not require creating such a profile.

The contract exists to preserve the gap between current v0 readiness and future
target capability. It should help future work reason about adaptation without
turning reviewable evidence into hidden authority.

## Core Definition

Personalization / adaptation means shadowMAS may propose changes to explanation,
grounding, or working context using provisional evidence from the current task.
Persisted patterns about projects, tools, or recurring issues are a separate,
consent-dependent design question. A person is not a global expertise level.

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

## Task-Local Interaction Before Persistent Profiles

This is a design proposal, not an implemented personalization service. The
examples below are not a task ontology, questionnaire, document template, or new
packet vocabulary.

Distinguish the current collaboration partner, task, concept or dependency,
purpose, decision, interaction context, observation time, expiry condition,
uncertainty, and evidence source in ordinary prose when relevant. These need not
be separate packet fields. Concept boundaries come from the work: knowing HTTP
does not establish knowledge of WebSocket replay, and migration planning does
not establish competence in an implementation language.

An explicit correction or demonstrated task result may justify a local adjustment
immediately; repetition is not a prerequisite. A request for less explanation
changes the presentation assumption, not an expertise estimate. Successful
transfer to a related step is evidence for that step only. Silence, response
speed, jargon, verbosity, confidence, and job title are not competence evidence.
Do not diagnose fatigue or cognitive state from these proxies.

When an assumption matters, make it visible with its scope and an easy repair
path. If the user corrects it, stop applying the contradicted assumption and
reconsider dependent explanations. A new task or changed purpose requires fresh
scope checks. No history means unknown, not novice. Session-local use expires
with the session unless the user explicitly chooses a narrower or longer scope.

Current corrections and already authorized, reversible work need no additional
profile approval ceremony. Persistence, cross-task reuse, changed authority,
and external actions retain their own consent and review boundaries. Before
any persistent model is enabled, the user must be able to inspect what will be
stored, choose its scope and retention, and delete or reset it without changing
the product repo. A local result log is not consent to infer a lasting user model.

### Grounding and sentence precision

Choose grounding effort by uncertainty, consequence, reversibility, repair cost,
and the user's declared current constraints. For a low-consequence reversible
step, proceed under a visible local assumption. For material ambiguity, ask one
question whose answer changes the decision. For a high-consequence or irreversible
commitment, check the particular consequence and intended action explicitly
before acting. Confirmation is not authenticated human presence or proof of
understanding. Do not insert artificial delays or universal teach-back.

For example: "For this retry decision, may I assume you distinguish reconnecting
the transport from replaying an application operation?" Ask only if that
distinction changes the result; do not ask "Are you an expert?" or "Is this clear?"

Prefer sentences that identify the actor, action, object, scope, and consequence
where needed. Keep source observations, inference, proposed action, and actual
commitment distinguishable without requiring labels on every sentence. Reuse
accepted terminology provisionally, leaving a direct way to repair its meaning.

### Document transformations and decision order

Assemble a view from the material needed for this decision. Immediate action,
decision required, delay consequences, evidence, disagreement, uncertainty,
reversible next steps, explanation, and raw sources are composable moves, not
an exhaustive menu. A scan, decision, learning, or audit view is a hypothesis
about usefulness in context, not a stored cognitive mode or universal template.
There is no fixed 15-second summary requirement.

For declared time pressure, reduce branching and expose the next decision with
its critical consequence. For learning, expose the rationale and a transferable
dependency. For audit, make provenance, exclusions, and disconfirming evidence
accessible. Preserve the source revision, locators, and omitted material so the
user can reopen it. A shorter rendering must not erase disagreement or make
missing coverage look like negative evidence. Offer a changed order without
silently moving the user's current reading position or replacing the source.

### Architecture comparison

| Option | Benefit | Cost or boundary | Disposition |
|---|---|---|---|
| Fixed profiles and summary templates | Predictable authoring and simple routing | Misclassifies long-tail work and transfers expertise too broadly | Reject as the global semantic model |
| Session-local, task/concept evidence and composable views | Immediate correction without a database or new packet fields | Context may need re-establishing next session; effectiveness untested | Recommend as the next design/evaluation direction |
| Opt-in project-local persistent evidence | Could reduce repeated grounding across tasks | Requires consent, expiry, dependency invalidation, deletion, and storage decisions | Defer implementation to the existing unlock conditions |

### Design walkthroughs, not user-study results

| Scenario | Proposed behavior | Failure or cost to examine |
|---|---|---|
| HTTP understood; WebSocket replay unfamiliar | Explain the replay dependency only when relevant | Incorrect expertise transfer; needless HTTP explanation |
| Migration planning understood; language unfamiliar | Preserve planning autonomy; explain the implementation seam | Collapsing planning and coding competence |
| Learning now; execution under time pressure later | Change detail and order when purpose changes | Stale preference; lost critical consequence |
| AI inferred expertise incorrectly | Accept correction and remove dependent assumptions | Correction effort; persistence of the error |
| New user without history | Start from task evidence and minimal useful context | Questionnaire burden or unsupported expertise inference |
| User refuses persistence | Use current context only; create no persistent profile | Hidden state or cross-session leakage |
| High-risk irreversible change | Check the specific intended consequence before commitment | Under-clarification; ritual approval without comprehension |
| Low-risk reversible change | Proceed with an inspectable assumption and correction path | Unnecessary interruption or repeated permission requests |
| Raw source requested after compression | Return the source and identify omissions or unavailability | Retrieval effort; false completeness |
| Previously unseen work pattern | Compose or revise the view directly from the task | Forcing work into the nearest fixed category |

Compare composable views with a fixed-template baseline on real task decisions,
including deliberately wrong AI advice and changed user context. Examine both
over-clarification cost and under-clarification risk, incorrect expertise transfer,
privacy exposure, correction effort, and long-tail fit. Record assistance and
information omitted as well as outcomes. Satisfaction, agreement with the AI,
or ability to predict its output is insufficient evidence of decision quality.
No performance threshold, sample-size promise, or improvement claim is set here.
Educational knowledge tracing remains an analogy, not a validated transfer.

### Additional full-text evidence reviewed for this revision

These papers were read in full, including methods, results, limitations,
references, and the Amershi appendix. PDFs remain outside this repository.
Proposals above are shadowMAS inferences; the studies did not evaluate shadowMAS.

| Source and stable access | Evidence type | Supported conclusion | Transfer limitation | Disposition and difference |
|---|---|---|---|---|
| Griffiths, Lieder, Goodman (2015), [Rational Use of Cognitive Resources](https://doi.org/10.1111/tops.12142), [author full text](https://cocolab.stanford.edu/papers/GriffithsEtAl2015-TiCS.pdf), 13 pages | Conceptual / formal | Relates computational strategies to assumed operations, costs, and decision goals | Optimality depends on assumed architecture and costs; no measured Shadow clarification utility | Adapt with attribution: ask qualitatively whether further inquiry could change the decision, without invented scores or universal stopping thresholds |
| Amershi et al. (2019), [Guidelines for Human-AI Interaction](https://doi.org/10.1145/3290605.3300233), [author full text](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf), 19 pages including appendix | Empirical design evaluation | 49 practitioners evaluated guideline relevance and clarity across 20 products; correction, control, and cautious updates were observable design concerns | Heuristic evaluation is not evidence of better task decisions or oversight; inferred behavior in examples is participant reporting | Adapt with attribution: use correction and continuity as hypotheses without making the 18 guidelines a mandatory schema or accepting behavior proxies as competence evidence |
| Buçinca, Malaya, Gajos (2021), [To Trust or to Think](https://doi.org/10.1145/3449287), [full text](https://arxiv.org/pdf/2102.09692), 21 pages | Empirical experiment | In a simulated food-choice task with 199 retained participants, forcing interventions improved correct choices on wrong-AI trials; reduced overreliance was significant for ingredient detection, not the complete-choice measure | No significant overall performance gain over simple explanations; greater perceived complexity; one non-critical task and unequal subgroup benefits | Adapt with attribution: test selective decision-linked grounding without universal delays, personality scoring, or a claim of improved human oversight |

These findings motivate a testable direction. They do not establish construct
validity, predictive validity, runtime safety, or authenticated human presence.
References cited by a paper and downloaded but unread leads are not additional
full-text evidence for this revision.

## User-Owned Layers

The layers below identify ownership boundaries. They do not classify human
tasks, concepts, expertise, or cognitive modes.

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
- memory packet candidates accepted for review, without memory promotion
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

The following are non-exhaustive evidence examples for future profile review,
not a closed list of task types. Current task evidence may also include explicit
correction, a demonstrated result, a scoped transfer, an explanation request, or
accepted terminology. They remain uncertain and revisable.

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

These names are non-exhaustive examples, not accepted-value constraints. Describe
an unfamiliar candidate in task-local language rather than force a category.
They are not packet families,
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
