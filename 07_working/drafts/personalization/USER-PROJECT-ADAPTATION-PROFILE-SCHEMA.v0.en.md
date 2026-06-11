# USER-PROJECT-ADAPTATION-PROFILE-SCHEMA.v0.en.md | draft schema for future user/project adaptation profile review surface
# related: [PERSONALIZATION-ADAPTATION-READINESS-CONTRACT, PERSONALIZATION-MEMORY-ADAPTATION-CANDIDATE-LIFECYCLE-NOTE, MEMORY-PLANE-HARNESS, SHADOWMAS-TARGET-TRUTH]
# phase: user_project_adaptation_profile_schema_draft

# User / Project Adaptation Profile Schema v0 Draft

## Status

NON-CANONICAL DRAFT.

This is a schema draft only.
It is not implementation.
It is not a memory backend.
It is not runtime behavior.
It is not an authority validator.
It is not learned personalization.
It is not automatic adaptation.
It is not project truth.
It is not user preference approval.
It does not modify user project truth.
It does not absorb user memory.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, validators,
runtime behavior, tests, packet fixtures, or product repositories.

This draft requires owner review before any promotion, schema implementation,
validator work, memory backend work, runtime work, or downstream update.

## Purpose

This document defines a draft schema for a future user/project adaptation
profile.

The profile is a future review surface for recording how shadowMAS may adapt
around a user or project. It describes reviewable adaptation context without
taking over:

- project truth
- user memory
- tool behavior
- governance / workflow
- repo architecture
- runtime host behavior

The profile exists to make adaptation candidates inspectable, scoped,
invalidatable, resettable, exportable, deletable, and human-gated before any
implementation is considered.

## Core Invariants

- A profile is evidence and review context, not truth.
- A profile cannot raise authority.
- A profile cannot authorize runtime actions.
- A profile cannot authorize write-back.
- A profile cannot import memory.
- A profile cannot infer private preference without approval.
- Repeated signal is evidence, not authority.
- Every promoted adaptation requires human review.
- Profile fields must not collapse candidate status, limited approval, memory
  promotion, canonical truth promotion, or runtime authority.

## Proposed Schema Fields

A future profile record should include at least:

- `profile_id`
- `profile_version`
- `profile_status`
- `owner_scope`
- `project_scope`
- `repo_scope`
- `truth_layer_refs`
- `memory_layer_refs`
- `tool_layer_refs`
- `workflow_layer_refs`
- `runtime_host_refs`
- `allowed_adaptation_domains`
- `forbidden_adaptation_domains`
- `observed_patterns`
- `adaptation_candidates`
- `approved_limited_adaptations`
- `invalidated_adaptations`
- `stale_conditions`
- `reset_policy`
- `export_policy`
- `delete_policy`
- `review_required`
- `promotion_required`
- `claim_ceiling`
- `non_claim_record`

## Field Definitions

All fields have authority effect `none`, except `claim_ceiling`, which caps
what the profile may claim. No field grants truth, memory, runtime, write-back,
or approval authority.

| Field | Purpose | Allowed content | Denied content | Who may assign or update it | Human review required | Authority effect |
|---|---|---|---|---|---|---|
| `profile_id` | Stable identifier for this profile draft or record. | Opaque local ID; no private identity needed. | Secrets, credentials, external project identity, raw paths unless explicitly approved. | Human or scoped profile-drafting process. | Required before active use. | none |
| `profile_version` | Profile schema/draft version marker. | Version token such as `v0`. | Runtime version claims or canonical schema claims. | Human or schema-maintenance process. | Required before promotion. | none |
| `profile_status` | Lifecycle state for the profile. | Values from the `profile_status` enum below. | Ambiguous mixed phrases such as approved candidate. | Human reviewer or owner-approved profile process. | Required to move beyond draft or candidate. | none |
| `owner_scope` | Bounded owner, user, team, or operator scope. | Generalized owner reference, role, or local opaque ID. | Private identity unless explicitly approved; account secrets. | Human owner. | Yes. | none |
| `project_scope` | Project/workspace boundary where profile observations apply. | Project-local scope label, workspace reference, task lane. | Project truth override; broad external repo ingestion. | Human owner or scoped intake process. | Yes. | none |
| `repo_scope` | Repo architecture and read/write boundary. | Allowed read/write scope summaries; no-write default. | Product-repo write-back authorization; raw repo dumps. | Human owner or scoped task packet process. | Yes for any write-related scope. | none |
| `truth_layer_refs` | References to project or shadowMAS truth anchors used for boundary checks. | Source refs to declared truth files or sections. | Replacing truth with profile content; unreviewed domain claims. | Human or scoped review process. | Yes before reuse. | none |
| `memory_layer_refs` | References to declared memory boundaries or approved memory surfaces. | Memory scope refs, memory packet refs, invalidation refs. | Private memory content; memory import; raw memory dumps. | Human owner or memory review process. | Yes. | none |
| `tool_layer_refs` | References to tools or adapters in scope. | Tool names, runtime hosts, adapter notes, capability summaries. | Credentials; tool capability as authority; workflow graph content. | Human owner or scoped runtime review process. | Yes before adaptation. | none |
| `workflow_layer_refs` | References to review, approval, handoff, or governance workflow context. | Review cadence, escalation boundary, handoff pattern refs. | Approval bypass; hidden workflow takeover. | Human owner or review lead. | Yes. | none |
| `runtime_host_refs` | References to host/runtime constraints. | Host name, declared constraint, adapter mismatch evidence. | Runtime authority claims; host-native prompt as truth. | Human owner or runtime review process. | Yes before reuse. | none |
| `allowed_adaptation_domains` | Domains in which adaptation candidates may be considered. | Values listed in this draft. | Any domain not explicitly allowed. | Human owner or future approved profile process. | Yes. | none |
| `forbidden_adaptation_domains` | Domains or signal classes excluded from adaptation. | Values listed in this draft; project-specific additions. | Omitting known forbidden signal classes. | Human owner or authority-boundary review. | Yes. | none |
| `observed_patterns` | Source-linked repeated patterns that may support candidates. | Pattern records defined below. | Raw logs, secrets, private memory, unreviewed runtime output. | Human reviewer or scoped agent as evidence preparation. | Yes before candidate use. | none |
| `adaptation_candidates` | Reviewable candidate adaptations derived from observed patterns. | Candidate objects defined below. | Approval, memory promotion, truth promotion, runtime action. | Human reviewer, owner, or scoped candidate process. | Yes. | none |
| `approved_limited_adaptations` | Human-approved bounded adaptations for a declared scope. | Limited adaptation objects defined below. | Canonical truth claims; runtime authority; write-back permission. | Human owner or authorized reviewer. | Yes. | none |
| `invalidated_adaptations` | Adaptations that are no longer active or safe to use. | Invalidated IDs, reasons, source refs, dates. | Silent deletion without trace when trace is required. | Human reviewer or future approved invalidation process. | Yes for reactivation. | none |
| `stale_conditions` | Conditions that make profile entries stale or require re-review. | Trigger list defined below. | Treating stale material as active. | Human reviewer or future approved checker. | Yes before active reuse. | none |
| `reset_policy` | How profile state can be reset. | Reset scope, requester, retention notes, review requirement. | Hidden persistence; reset blocked by product repo state. | Human owner. | Yes. | none |
| `export_policy` | How profile state can be exported. | Export format, allowed fields, redaction rules. | Secrets, raw memory, raw logs unless separately approved. | Human owner. | Yes. | none |
| `delete_policy` | How profile state can be deleted. | Delete scope, confirmation path, retained audit minimum if any. | Product repo dependency; undeletable hidden state. | Human owner. | Yes. | none |
| `review_required` | Review gates before use or promotion. | Boolean or structured review requirement. | Self-approval by profile. | Human owner or governance review. | Yes. | none |
| `promotion_required` | Promotion path required before reuse, memory, truth, or runtime use. | Explicit target and required review path. | Automatic promotion; target-free promotion wording. | Human owner or authority-boundary review. | Yes. | none |
| `claim_ceiling` | Strongest claim the profile may support. | Values listed in this draft. | Authority expansion beyond allowed values. | Human owner or future approved gate. | Yes. | caps profile claims |
| `non_claim_record` | Explicit claims the profile does not make. | List of non-claims such as not truth, not memory, not runtime authority. | Omission of relevant non-claims when risk is present. | Human or scoped profile author. | Yes before promotion. | none |

## `profile_status` Enum

Allowed draft values:

- `draft_profile`
- `candidate_for_review`
- `accepted_for_review`
- `approved_for_limited_use`
- `stale`
- `invalidated`
- `rejected`

Rules:

- `approved_for_limited_use` is not canonical truth.
- `approved_for_limited_use` is not runtime authority.
- `accepted_for_review` is not memory promotion.
- `candidate_for_review` is not approval.
- `stale` requires re-review before active reuse.
- `invalidated` must not be reused without a new review path.
- `rejected` must not return without new evidence and human review.

## `allowed_adaptation_domains`

Allowed draft values:

- `review_preferences`
- `recurring_boundary_warnings`
- `seam_contract_patterns`
- `verifier_edge_cases`
- `handoff_review_patterns`
- `memory_invalidation_patterns`
- `prompt_layering_notes`
- `tool_adapter_notes`

These are candidate domains only. They do not create preferences, memory,
runtime behavior, or truth.

## `forbidden_adaptation_domains`

Forbidden draft values and classes:

- `secrets`
- `credentials`
- `raw_logs`
- `raw_repo_content`
- `private_memory_content`
- `n8n_workflow_graphs`
- `external_project_identity`
- `unreviewed_runtime_output`
- `unreviewed_recommendation`
- `model_confidence_score`
- `cache_hit`
- `retrieval_hit`
- `tool_capability_as_authority`
- `user_private_preference_unless_explicitly_approved`
- `project_truth_override`
- `product_repo_write_back`

Forbidden domains must not be normalized into observed patterns or candidates.
If encountered, they should be rejected, redacted, or routed to human review
according to a future approved authority boundary.

## `observed_patterns`

Observed patterns are repeated signals that may support adaptation candidates.

Draft pattern kinds:

- repeated review friction
- repeated `boundary_hit`
- repeated `seam_gap`
- repeated verifier edge case
- repeated packet field ambiguity
- repeated handoff failure
- repeated memory invalidation event
- repeated tool adapter mismatch
- repeated human correction

Rules:

- Observed pattern is evidence only.
- Observed pattern is not adaptation approval.
- Observed pattern must have source references.
- Observed pattern must be invalidatable.
- Observed pattern must not include forbidden adaptation domains.
- Repetition count is not authority.

Preferred object shape:

```yaml
pattern_id: pattern_001
pattern_kind: repeated_seam_gap
source_refs: []
repeat_count: 2
scope_refs: []
summary: "Generalized source-linked pattern summary."
invalidation_triggers: []
claim_ceiling: profile_evidence_only
```

## `adaptation_candidates`

An adaptation candidate is reviewable material derived from observed patterns.

Preferred object shape:

```yaml
candidate_id: adaptation_candidate_001
candidate_type: seam_contract_candidate
source_pattern_refs:
  - pattern_001
proposed_adaptation: "Generalized review suggestion, not a rule."
affected_layers:
  - workflow_layer
  - prompt_layer
denied_inferences:
  - not_project_truth
  - not_memory
  - not_runtime_behavior
review_required: true
claim_ceiling: adaptation_candidate_only
current_lifecycle_state: candidate_for_review
```

Candidate types:

- `review_preference_candidate`
- `recurring_boundary_warning_candidate`
- `seam_contract_candidate`
- `verifier_edge_case_candidate`
- `memory_invalidation_rule_candidate`
- `prompt_layering_note_candidate`
- `tool_adapter_note_candidate`
- `handoff_review_note_candidate`

Rules:

- Candidate is not approval.
- Candidate is not memory.
- Candidate is not truth.
- Candidate is not runtime behavior.
- Candidate must state denied inferences.
- Candidate must carry an explicit claim ceiling.
- Candidate must not enter `approved_limited_adaptations` without human review.

## `approved_limited_adaptations`

An approved limited adaptation is a scoped human-approved use of an adaptation.

Preferred object shape:

```yaml
approved_for_what: "Use this seam-contract review hint in project-scoped reviews."
approved_scope:
  project_scope_ref: project_scope_001
  workflow_scope_ref: review_lane_001
approving_human_ref: human_owner_or_reviewer
expiry_or_recheck_condition: "Recheck when project truth or toolchain changes."
invalidation_triggers:
  - project_truth_changed
  - toolchain_changed
reset_behavior: reset_with_profile
export_behavior: export_summary_only
delete_behavior: delete_with_profile
claim_ceiling: approved_limited_use_only
```

Rules:

- `approved_for_limited_use` is scoped.
- It must state `approved_for_what`.
- It must not imply canonical truth.
- It must not imply runtime authority.
- It must not imply product-repo write-back.
- It must include expiry or recheck conditions.
- It must include reset, export, and delete behavior.

## `invalidated_adaptations` And `stale_conditions`

Stale or invalidation triggers include:

- project truth changed
- memory boundary changed
- toolchain changed
- runtime host changed
- human reversed prior preference
- repo architecture changed
- source signal was invalidated
- approval scope expired

Preferred invalidated adaptation record:

```yaml
adaptation_ref: adaptation_candidate_001
previous_state: approved_for_limited_use
new_state: invalidated
reason: project_truth_changed
source_refs: []
review_required_before_reuse: true
```

Rules:

- Stale profile content must not be presented as active guidance.
- Invalidated adaptations must not be reused without review.
- Source invalidation must propagate to dependent candidates and limited
  adaptations.

## Reset / Export / Delete

- Profile must be resettable.
- Profile must be exportable.
- Profile must be deletable.
- No hidden persistence.
- Deletion must not require product repo changes.
- Export must not include secrets, raw memory, or raw logs unless separately
  approved.
- Reset must remove active adaptation effect and require re-review before reuse.
- Export should prefer summaries and source refs over raw sensitive content.
- Delete policy must state whether minimal audit tombstones remain and why.

## Claim Ceiling

Allowed draft values:

- `profile_evidence_only`
- `adaptation_candidate_only`
- `approved_limited_use_only`
- `rejected`

Rules:

- Profile evidence is not truth.
- Candidate is not approval.
- Approved limited use is not canonical truth.
- Profile is never runtime authority.
- `approved_limited_use_only` does not authorize product-repo write-back.
- `rejected` means no reuse without new evidence and human review.

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
- project truth override
- authority validator
- active intake behavior
- packet schema change
- validator code

## Examples

### Valid Profile Example

This example records a repeated `seam_gap` and proposes a
`seam_contract_candidate`. It is illustrative only.

```yaml
profile_id: user_project_profile_demo_001
profile_version: v0
profile_status: candidate_for_review
owner_scope: generalized_project_owner
project_scope: project_scope_demo
repo_scope:
  writes_product_repo: false
truth_layer_refs:
  - source_type: repo_doc
    source_id: project_truth_entry
    relation: boundary_anchor
memory_layer_refs: []
tool_layer_refs: []
workflow_layer_refs:
  - review_lane_demo
runtime_host_refs: []
allowed_adaptation_domains:
  - seam_contract_patterns
forbidden_adaptation_domains:
  - secrets
  - credentials
  - raw_logs
  - private_memory_content
observed_patterns:
  - pattern_id: pattern_001
    pattern_kind: repeated_seam_gap
    source_refs:
      - source_type: review_packet
        source_id: review_packet_demo
        relation: derived_from
    repeat_count: 2
    scope_refs:
      - review_lane_demo
    summary: "Repeated seam gap in review handoff wording."
    invalidation_triggers:
      - project_truth_changed
      - workflow_scope_changed
    claim_ceiling: profile_evidence_only
adaptation_candidates:
  - candidate_id: adaptation_candidate_001
    candidate_type: seam_contract_candidate
    source_pattern_refs:
      - pattern_001
    proposed_adaptation: "Suggest a review-only seam contract note."
    affected_layers:
      - workflow_layer
      - prompt_layer
    denied_inferences:
      - not_project_truth
      - not_memory
      - not_runtime_behavior
    review_required: true
    claim_ceiling: adaptation_candidate_only
    current_lifecycle_state: candidate_for_review
approved_limited_adaptations: []
invalidated_adaptations: []
stale_conditions:
  - project_truth_changed
  - repo_architecture_changed
reset_policy:
  resettable: true
export_policy:
  exportable: true
  include_raw_logs: false
delete_policy:
  deletable: true
review_required: true
promotion_required: true
claim_ceiling: adaptation_candidate_only
non_claim_record:
  truth: false
  memory_store: false
  runtime_authority: false
  product_repo_write_back: false
```

### Invalid Example: Private Memory Import

```yaml
memory_layer_refs:
  - raw_private_memory_dump: "full private notes copied here"
claim_ceiling: approved_limited_use_only
```

Invalid because the profile cannot import private memory content.

### Invalid Example: Model Confidence As Authority

```yaml
observed_patterns:
  - pattern_kind: repeated_review_friction
    model_confidence_score: 0.98
    summary: "High confidence means this should be approved."
```

Invalid because model confidence is not authority.

### Invalid Example: Runtime Promotion From Signal

```yaml
observed_patterns:
  - pattern_kind: repeated_tool_adapter_mismatch
adaptation_candidates:
  - candidate_type: tool_adapter_note_candidate
    proposed_adaptation: "Automatically change runtime behavior on next run."
    current_lifecycle_state: promoted_to_runtime_behavior
```

Invalid because a repeated signal cannot promote directly to runtime behavior,
and `promoted_to_runtime_behavior` is not an allowed profile status.

## Future Unlocks

Before implementation or promotion work may begin, the repo needs:

- owner review of this draft
- paper simulation of profile records
- inactive profile packet schema draft
- reset/export/delete policy draft
- authority validation boundary
- memory backend decision
- runtime adapter boundary closure
- explicit storage and lifecycle decision for profiles
- explicit review of whether this belongs in packet, registry, memory, or
  runtime-adapter surfaces

## Do Not Promote Yet

This remains draft because profile storage, lifecycle semantics, authority
validation, memory backend behavior, runtime adapter boundaries, and
reset/export/delete policy are unresolved.
