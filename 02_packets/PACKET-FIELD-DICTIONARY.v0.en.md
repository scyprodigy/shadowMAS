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
Packet schema version used by this packet.

Rule:
- required for validation compatibility
- must not be omitted in machine-stable packets

Example:
- `v0`

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

### `handoff.blockers`
Meaning:
List of blockers preventing normal completion.

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
Minimal execution plan for the worker/executor.

Rule:
- should remain actionable
- not a giant essay

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

### `do_not_need_to_read`
Meaning:
What the reviewer can safely skip for this decision.

Rule:
- important for token/human attention discipline

### `change_summary`
Meaning:
Short summary of what changed or is proposed to change.

### `risk_summary`
Meaning:
Short summary of the key risk shape.

### `recommendation`
Meaning:
Best current recommendation from the producing layer.

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
