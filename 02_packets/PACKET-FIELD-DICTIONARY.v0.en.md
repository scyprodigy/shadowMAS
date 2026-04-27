# PACKET-FIELD-DICTIONARY.v0.en.md

## Purpose
This file defines the shared field dictionary for shadowMAS packet families.

Its goal is to:
- stabilize packet vocabulary
- prevent naming drift
- separate shared vs family-specific fields
- support validation and future packet schemas
- keep human review and machine parsing aligned

## Packet Families
Current minimum packet families:
- `task_packet`
- `memory_packet`
- `review_packet`

## Logical Packet Contract vs Default Codec
This dictionary defines the logical packet contract for shadowMAS packet families:
- shared field names
- field meanings
- packet-family semantics
- machine-stable interpretation rules

It does not itself require one specific serialization format.
For v0, YAML is the default codec used by the current packet files.
Future codecs may serialize the same logical packet contract without changing this dictionary.
Codec-specific transport, framing, or compression concerns belong to runtime handling unless later promoted explicitly into governed truth.

## Naming Rules
- use `snake_case`
- keep names explicit and stable
- prefer semantic clarity over short cryptic names
- MUST NOT invent near-duplicate names for the same concept
- shared fields must keep the same meaning across packet families

## Shared Field Principles
A shared field should exist only if:
- it is needed by more than one packet family
- it keeps the same meaning across packet families
- it improves routing, linking, review, or traceability

If a field is family-specific, keep it family-specific.

## Packet Layer Boundary
The packet layer is for:
- packet schema
- packet states
- source and artifact reference formats
- handoff fields

The packet layer is not for:
- full runtime implementation
- provider-specific adapter logic
- session-only temporary notes

---

## 1. Shared Core Fields

### `packet_id`
Meaning:
Human-readable packet identifier.

Rule:
- stable within the current packet lifecycle
- used for inspection and communication
- not required to be globally unique forever if `packet_uid` exists

Example:
- `task_pkt_001`
- `mem_pkt_014`

### `packet_uid`
Meaning:
Globally unique packet identifier.

Rule:
- machine-stable unique ID
- preferred for linking, registry, and cross-session references

### `packet_type`
Meaning:
The packet family/type.

Allowed current values:
- `task_packet`
- `memory_packet`
- `review_packet`

### `schema_version`
Meaning:
Authoritative in-artifact contract version field for machine-first packet contract surfaces.

Rule:
- required for validation compatibility
- must not be omitted in machine-stable packets
- parsers and validators must use this field, not the filename, as the authoritative contract version when this field exists
- for SemVer-aligned contract versions, prefer `MAJOR.MINOR.PATCH` value form, for example `"0.0.0"`

Example:
- `"0.0.0"`

### Packet contract versioning rules
Filename `.vN` is a major-line mirror for human navigation, grep, and diff convenience only.
It is not parser authority when `schema_version` exists.

Rules:
- filename major and in-artifact major should remain aligned
- mismatch between filename `.vN` and `major(schema_version)` should be treated as a review-blocking condition
- use SemVer-aligned PATCH / MINOR / MAJOR language as governance language only; this dictionary does not formalize full SemVer adoption
- additive optional fields are normally backward-compatible if they do not change existing requiredness, type, meaning, default behavior, or allowed-value semantics
- changes to requiredness, type, semantic meaning, default behavior, or wire-visible identifier names are breaking contract changes
- deprecation must precede removal for visible contract identifiers
- retired identifiers must not be reused

### `task_id`
Meaning:
The higher-level task identifier associated with the packet.

Rule:
- many packets may belong to the same task
- useful for grouping execution, review, and memory outputs

### `run_id`
Meaning:
Identifier for one runtime execution or run context.

Rule:
- used to distinguish multiple runs under the same task

### `session_id`
Meaning:
Identifier for the originating human/agent session context.

Rule:
- useful for session traceability
- does not replace `task_id` or `run_id`

### `created_at`
Meaning:
Packet creation timestamp.

Rule:
- should use a consistent timestamp format
- should be machine-parseable

### `created_by`
Meaning:
Who created the packet.

Rule:
- may refer to human, agent role, or tool identity
- should be explicit, not vague

Examples:
- `human`
- `l2_planner`
- `l3_executor`
- `mergeback_agent`

### `owner`
Meaning:
Stable responsibility holder for this packet.

Rule:
- owner is not the same as current writer
- owner answers "who is responsible for this packet's lifecycle"

### `writable_by`
Meaning:
State-gated writers allowed to modify the packet.

Rule:
- optional in early drafts, but conceptually distinct from `owner`
- should not be confused with responsibility ownership

### `supervision_mode`
Meaning:
Human/agent supervision relationship for this packet's work context.

Allowed direction:
- `human_live_pair`
- `human_available_delegate`
- `human_away_autonomous`

### `risk`
Meaning:
Governance risk tier for this packet's action context.

Allowed direction:
- `r0_trivial`
- `r1_routine`
- `r2_guarded`
- `r3_sensitive`
- `r4_human_only`

### `source_refs`
Meaning:
References to external or internal sources used by this packet.

Rule:
- supports traceability
- source relevance does not imply truth authority

### `artifact_refs`
Meaning:
References to artifacts produced, modified, or touched by this packet.

Rule:
- used for write-back, review, and traceability

### `related_packets`
Meaning:
Links to other related packets.

Rule:
- supports chaining and graph-style packet relationships

### `tags`
Meaning:
Lightweight labels for search, routing, or grouping.

Rule:
- useful but non-authoritative
- should not replace structured fields

### `status`
Meaning:
Current lifecycle state of the packet.

Rule:
- required for packet lifecycle handling
- allowed values depend on packet family

### `handoff`
Meaning:
Structured handoff block for passing responsibility or action.

Rule:
- should remain minimal
- should not turn into a giant unstructured note dump
- should carry only machine-stable resume information, not session-only scratch notes

---

## 2. Structured Reference Fields

### `source_refs` structure
Each source reference should prefer fields like:

- `source_type`
- `source_id`
- `source_path`
- `source_hash`
- `source_version`
- `section`
- `relation`

#### `source_type`
Meaning:
What kind of source this is.

Examples:
- `file`
- `repo_doc`
- `session_handoff`
- `packet`
- `external_reference`

#### `source_id`
Meaning:
Stable source identifier where available.

#### `source_path`
Meaning:
Filesystem or logical path of the source.

#### `source_hash`
Meaning:
Optional integrity or content hash.

#### `source_version`
Meaning:
Version marker where available.

#### `section`
Meaning:
Relevant subsection or range inside the source.

#### `relation`
Meaning:
How this packet used the source.

Examples:
- `read_from`
- `derived_from`
- `compared_against`
- `supports`
- `conflicts_with`

---

### `artifact_refs` structure
Each artifact reference should prefer fields like:

- `artifact_type`
- `artifact_path`
- `exists`
- `change_kind`
- `produced_by`
- `task_role`

#### `artifact_type`
Meaning:
Kind of artifact.

Examples:
- `formal_doc`
- `human_doc`
- `yaml_packet`
- `registry_entry`
- `diagram`
- `patch_plan`

#### `artifact_path`
Meaning:
Filesystem path or logical artifact location.

#### `exists`
Meaning:
Whether the artifact currently exists.

Allowed values:
- `true`
- `false`

#### `change_kind`
Meaning:
How the artifact is affected.

Examples:
- `created`
- `updated`
- `reviewed`
- `proposed`
- `superseded`
- `referenced_only`

#### `produced_by`
Meaning:
Who or what produced the artifact.

#### `task_role`
Meaning:
Which role/layer produced or touched the artifact.

Examples:
- `L1`
- `L2`
- `L3`
- `L4`

---

## 3. Handoff Block Fields

### `handoff.from_packet_ref`
Meaning:
Packet reference that this handoff originated from.

### `handoff.to_role`
Meaning:
Target role expected to take the next action.

Rule:
- carries the "next responsible role" semantics
- is the canonical field for what older drafts called `next_owner`
- do not introduce `next_owner` as a parallel canonical field

Examples:
- `L1`
- `L2`
- `L3`
- `L4`

### `handoff.needed_action`
Meaning:
The concrete next action required.

Examples:
- `review`
- `decide`
- `implement`
- `merge`
- `clarify`
- `promote`

### `handoff.reason`
Meaning:
Short explanation for why the handoff exists.

Rule:
- carries the handoff-reason semantics
- is the canonical field for what older drafts called `handoff_reason`
- do not introduce `handoff_reason` as a parallel canonical field

### `handoff.blockers`
Meaning:
List of blockers preventing normal completion.

### `handoff.resume_from`
Meaning:
Minimal resume points that let a zero-memory agent or new session continue without rereading the full prior context.

Rule:
- should be a short ordered list of concrete restart anchors
- should prefer machine-stable or human-inspectable pointers
- should not become a long narrative summary

Examples:
- `read task scope and acceptance criteria`
- `re-open changed files listed in artifact_refs`
- `start from unresolved blocker 2`

---

## 4. task_packet Family Fields

### `goal`
Meaning:
The task objective.

Rule:
- must be explicit
- should describe the intended outcome, not vague activity

### `scope`
Meaning:
What is inside task scope.

Rule:
- required
- should define allowed working boundary

### `out_of_scope`
Meaning:
What is explicitly outside task scope.

Rule:
- strongly recommended
- prevents uncontrolled expansion

### `truth_touchpoints`
Meaning:
Which truth files, truth layers, or authority surfaces this task may affect.

Rule:
- critical for governance safety
- should not be omitted for non-trivial work

### `worker_plan`
Meaning:
Minimal execution plan for task execution control.

Rule:
- should remain actionable
- not a giant essay

Preferred subfields:
- `worker_plan.preferred_worker`
- `worker_plan.fallback_worker`
- `worker_plan.allow_fanout`
- `worker_plan.fanout_limit`
- `worker_plan.retry_limit`

### `why_now`
Meaning:
Why this task should be acted on now instead of later.

Rule:
- optional execution-scoping context
- not governance authority by itself

### `inputs`
Meaning:
Minimal task input block describing what context is needed.

Rule:
- use for execution-scoping context only
- not a replacement for full packet references

Preferred subfields:
- `inputs.required_context`
- `inputs.optional_context`

### `inputs.required_context`
Meaning:
Context that should be read or loaded before normal execution.

### `inputs.optional_context`
Meaning:
Useful but non-blocking context that may improve execution quality.

### `acceptance_criteria`
Meaning:
What must be true for the task to count as done.

Rule:
- required for bounded completion

### `stop_conditions`
Meaning:
When the worker must stop instead of continuing autonomously.

Examples:
- conflict detected
- missing truth
- human decision required
- risk exceeded

### `constraints`
Meaning:
Additional execution constraints.

Examples:
- no schema changes
- no write-back
- read-only audit
- no branch creation

### `expected_outputs`
Meaning:
Artifacts or outcomes expected from this task.

### `on_blocked`
Meaning:
Minimal blocked-state instructions for what to do next if normal progress stops.

Rule:
- should constrain next-step behavior
- not a free-form escape hatch

Preferred subfields:
- `on_blocked.action`
- `on_blocked.next_allowed_work`

### `on_blocked.action`
Meaning:
Preferred next action when the task becomes blocked.

### `on_blocked.next_allowed_work`
Meaning:
Work that is still allowed even while the main path is blocked.

### `deliverables`
Meaning:
Expected outputs to hand back when execution is complete or handed off.

Rule:
- defines expected output surface
- does not imply automatic approval or acceptance

---

## 5. memory_packet Family Fields

### `memory_kind`
Meaning:
The category of memory being captured.

Examples:
- `heuristic`
- `decision_summary`
- `resolved_pattern`
- `tooling_note`
- `governance_note`

### `memory_scope`
Meaning:
Where this memory is valid.

Examples:
- `session_local`
- `repo_local`
- `shadowmas_global`
- `project_specific`

### `summary`
Meaning:
Short human-readable summary of the memory.

### `structured_payload`
Meaning:
Machine-usable payload of the memory content.

Rule:
- may be compact structured data
- should avoid bloated prose

### `invalidation_triggers`
Meaning:
Conditions that would make this memory stale, unsafe, or invalid.

Rule:
- preferred over vague stale naming
- should be explicit and inspectable

Examples:
- source truth updated
- referenced file removed
- policy superseded
- packet schema version changed

### `confidence`
Meaning:
Confidence level for reuse.

Rule:
- must not be mistaken for truth authority
- confidence is not promotion

### `promotion_candidate`
Meaning:
Whether this memory is a candidate for promotion into a higher truth layer.

Allowed direction:
- `yes`
- `no`

### `promotion_notes`
Meaning:
Why promotion may or may not be appropriate.

### `validity`
Meaning:
Minimal structured basis for where and when a memory may still be reused.

Rule:
- validity is reuse-safety metadata, not truth authority
- does not replace `source_refs`
- does not replace promotion review
- exists to make reuse assumptions inspectable

### `validity.applies_to`
Meaning:
Where the memory is intended to be valid.

Preferred subfields:
- `validity.applies_to.modules`
- `validity.applies_to.task_types`

### `validity.applies_to.modules`
Meaning:
Modules or code areas where this memory is expected to apply.

### `validity.applies_to.task_types`
Meaning:
Task categories where this memory is expected to apply.

### `validity.stale_on`
Meaning:
Explicit conditions that should cause the memory to become stale or require revalidation.

Rule:
- should list reuse-relevant change conditions
- should not duplicate all packet lifecycle states

### `validity.review_after`
Meaning:
Optional date, time, or review checkpoint after which reuse should trigger review again.

Rule:
- re-review hint only
- not automatic invalidation by itself

### `invalidation`
Meaning:
Machine-readable invalidation snapshot for the memory's current source condition.

Rule:
- should stay narrower than packet lifecycle status
- should not replace packet `status`

### `invalidation.current_state`
Meaning:
Machine-readable current invalidation state for the memory.

Rule:
- should align with current invalidation semantics such as `valid`, `stale`, `broken_reference`, or `rejected`
- must not conflict with packet status semantics

### `invalidation.source_hashes`
Meaning:
Optional recorded source hashes used to compare whether the cited basis changed.

Rule:
- comparison aid only
- not approval proof
- not truth authority

### `memory_status`
Meaning:
Lifecycle state for memory packet handling.

Preferred direction:
- `captured`
- `draft`
- `candidate`
- `approved_shared`
- `stale`
- `broken_reference`
- `rejected`
- `superseded`
- `archived`

---

## 6. review_packet Family Fields

### `decision_needed`
Meaning:
What explicit decision is required from reviewer/human authority.

### `why_you_are_seeing_this`
Meaning:
Short explanation for why this review packet was raised.

### `minimal_checks.must_read`
Meaning:
The minimum artifacts the reviewer must read.

Rule:
- should stay small and curated
- prevents review overload

### `must_compare`
Meaning:
Artifacts or concepts that must be compared before deciding.

Rule:
- decision-relevant comparison support only
- should make the needed comparison target explicit
- should not turn into render-engine or layout specification

### `do_not_need_to_read`
Meaning:
What the reviewer can safely skip for this decision.

Rule:
- important for token/human attention discipline

### `change_summary`
Meaning:
Short summary of what changed or is proposed to change.

Rule:
- support field only
- should not replace chunked review structure when a more explicit review surface exists
- if `change_units` exists, `change_summary` should not be treated as the primary decision surface by default

### `change_units`
Meaning:
Small review units that split the change into decision-relevant chunks.

Rule:
- should help the reviewer inspect change structure incrementally
- should remain semantic and compact
- not a UI layout contract

### `impact_surface`
Meaning:
Short statement of what areas, behaviors, or truth surfaces may be affected.

### `evidence_at_a_glance`
Meaning:
Compact evidence snapshot that helps a reviewer see the supporting basis quickly.

Rule:
- should stay summary-level
- should point toward evidence, not replace it

### `acceptance_check_result`
Meaning:
Compact result summary of whether the declared acceptance checks appear satisfied.

Rule:
- should report check outcome, not final authority

### `unresolved_questions`
Meaning:
Open questions that still matter to the current review decision.

Rule:
- should stay decision-relevant
- should not become a catch-all note dump

### `safe_to_approve_if`
Meaning:
Explicit conditions under which approval would be considered safe.

Rule:
- should state bounded approval conditions
- should not be used as a hidden substitute for final approval

### `risk_summary`
Meaning:
Short summary of the key risk shape.

### `recommendation`
Meaning:
Best current recommendation from the producing layer.

Rule:
- producer-layer recommendation only
- should stay compact
- should not become essay-style persuasion

Examples:
- approve
- reject
- revise
- defer
- escalate

### `review_status`
Meaning:
Lifecycle state for review handling.

Preferred direction:
- `draft`
- `ready_for_human`
- `under_review`
- `approved`
- `rejected`
- `needs_revision`
- `closed`

---

## 7. Status Rules

### Shared `status`
Meaning:
Generic lifecycle field if one uniform field is used across families.

Rule:
- allowed only if the implementation clearly namespaces family-specific values
- otherwise family-specific status fields may be clearer

### Preferred current approach
Use one visible packet `status` field,
but define allowed value sets per packet family.

This keeps:
- common parsing shape
- family-specific lifecycle control

---

## 8. Forbidden Confusions

Do not confuse:
- `owner` with `writable_by`
- `confidence` with truth authority
- `source_ref` with approval
- `artifact_ref` with promotion
- `summary` with structured payload
- `status` with governance tier
- `status` with `invalidation.current_state`
- `validity` with authority
- `source_hashes` with approval proof
- retrieval hit with approved memory
- approved shared memory with canonical truth

---

## 9. Minimal Required Fields by Family

### task_packet minimum
- `packet_uid`
- `packet_type`
- `schema_version`
- `task_id`
- `created_at`
- `created_by`
- `owner`
- `supervision_mode`
- `risk`
- `status`
- `goal`
- `scope`
- `acceptance_criteria`
- `stop_conditions`

### memory_packet minimum
- `packet_uid`
- `packet_type`
- `schema_version`
- `created_at`
- `created_by`
- `owner`
- `status`
- `memory_kind`
- `memory_scope`
- `summary`
- `structured_payload`
- `source_refs`
- `invalidation_triggers`
- `confidence`
- `promotion_candidate`

### review_packet minimum
- `packet_uid`
- `packet_type`
- `schema_version`
- `created_at`
- `created_by`
- `owner`
- `status`
- `decision_needed`
- `why_you_are_seeing_this`
- `change_summary`
- `risk_summary`
- `recommendation`

---

## 10. Future Schema Files
This field dictionary should later align with:
- `02_packets/packet_common_shell.v0.yaml`
- `02_packets/task_packet.v0.yaml`
- `02_packets/memory_packet.v0.yaml`
- `02_packets/review_packet.v0.yaml`

If a schema conflicts with this dictionary:
- review both
- resolve explicitly
- do not silently let one drift away

## 11. Still Not Final
The following remain open:
- final exact required/optional split for every field
- final timestamp format
- final `status` implementation style
- final `writable_by` encoding style
- final promotion metadata structure
- final handoff block strictness
