> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through packet-boundary review
> source basis: future review packet emission lifecycle audit and existing runtime-adapter drafts

# REVIEW-PACKET-EMISSION-LIFECYCLE-CONTRACT.v0

## Status

This file is a non-canonical draft.

It is not an implementation.
It does not create a review packet emitter.
It does not grant authority approval.
It does not mark tasks as verified.
It does not prove runtime readiness.
It does not permit product-repo write-back.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`, validators, workspace tools, smoke tools, tests, or packet examples.

The lifecycle shape below is planning material only. Contract readability is not implementation, review packet drafting is not approval, schema validity is not authority, transcript capture is not truth closure, and workspace emission is not product-repo write-back.

## Purpose

Define the minimum lifecycle contract shape for future review packet emission.

A review packet emission lifecycle contract describes the boundary a future emitter would need to obey before implementation. It is not the emitter implementation.

The contract preserves these distinctions:

- review packet drafting
- review packet representation validation
- review packet authority validation
- workspace-only storage
- final emission
- rejection

The contract also preserves this distinction:

- representation validity: a review packet has the required shape for a local validator
- authority validity: a human-approved authority path says the review may be acted on

Representation validity does not imply authority validity.

## Non-goals

This draft does not define or create:

- review packet emitter
- runner
- hooks
- adapter registry
- task packet consumer
- product-repo writes
- external side effects
- task verification claim
- authority approval
- production readiness claim
- runtime enforcement behavior
- product-repo write-back behavior

## Minimum emission lifecycle contract fields

A draft review packet emission lifecycle contract record should include at least:

- `emission_contract_id`: stable identifier for this emission lifecycle contract record
- `contract_version`: contract schema version, initially `v0`
- `contract_status`: draft status such as `draft`, `blocked`, `workspace_only`, or `retired`
- `task_packet_ref`: task packet this review concerns
- `runner_contract_ref`: runner contract this emission lifecycle depends on, if any
- `consumption_contract_ref`: task packet consumption contract this emission lifecycle depends on, if any
- `execution_transcript_ref`: transcript evidence this review may cite, if any
- `review_packet_path`: path to the review packet candidate
- `review_packet_class`: accepted packet class, initially `review_packet`
- `review_packet_id`: review packet identifier, if drafted
- `review_packet_schema_version`: review packet schema version, if drafted
- `representation_validator_ref`: validator or checker command used for representation validation
- `representation_validation_state`: representation validation status for the review packet
- `authority_validation_state`: authority validation status for the review packet
- `authority_blocked_reason`: reason authority is blocked or unvalidated
- `workspace_ref`: external shadowMAS workspace reference, if any
- `allowed_output_roots`: roots where review packet artifacts may be created
- `forbidden_output_roots`: roots where review packet artifacts must not be created
- `product_repo_write_allowed`: whether product-repo writes are allowed
- `workspace_only_emission_allowed`: whether workspace-only draft emission is allowed
- `final_emission_allowed`: whether final review emission is allowed
- `external_side_effects_allowed`: whether network, service, or non-local side effects are allowed
- `emission_state`: current emission lifecycle state
- `non_claim_record`: claims explicitly not made by drafting, validation, workspace emission, or transcript citation
- `claim_ceiling`: strongest claim this emission lifecycle contract may support
- `required_human_approval`: human approval required before drafting, workspace emission, final emission, or write-back
- `stop_conditions`: conditions that require the emitter to stop before drafting, validation, workspace emission, final emission, or output

## Emission lifecycle states

Minimum emission lifecycle states:

- `not_started`: no review packet drafting has started
- `blocked`: emission is blocked by missing scope, authority, path, transcript, or validation state
- `draft_allowed`: draft creation is allowed within this lifecycle boundary
- `draft_created`: review packet draft exists
- `representation_validated`: review packet representation validation passed
- `authority_unvalidated`: no authority validation path has approved the review as final
- `emission_blocked`: review packet emission is blocked from final or product-repo destinations
- `emitted_to_workspace_only`: review packet was emitted only to the external workspace
- `rejected`: review packet candidate was rejected or cannot be emitted within this boundary

`representation_validated` is not final review approval, and `emitted_to_workspace_only` is not product-repo write-back.

## Default-deny capabilities

The first review packet emission lifecycle contract must deny by default:

- emitting review packet as authority-approved
- writing review packet into product repo
- marking review as final
- marking task as verified
- upgrading transcript into truth closure
- external side effects
- schema-valid to authority-valid promotion
- workspace-to-product artifact promotion
- product-repo write-back
- review-to-task approval without a separate authority boundary

## Boundary rules

- A review packet emission lifecycle contract is not a review packet emitter.
- Drafting a review packet is not authority-approved emission.
- A review packet is not task verification unless a separate authority boundary says so.
- Transcript capture is not truth closure.
- Representation-valid review packets are not authority-valid review packets.
- Workspace-only emission is not product-repo write-back.
- `status: approved` inside a review packet must not be treated as final verification without a separate authority boundary.
- `recommendation` values are advisory unless a separate authority boundary says otherwise.
- Local smoke success is not production readiness.
- Product-repo writes remain denied unless a later explicit boundary allows them.
- Workspace artifacts remain external unless a later approved boundary says otherwise.

## Example draft record

Illustrative and non-authoritative:

```yaml
emission_contract_id: review_packet_emission_lifecycle_contract_v0
contract_version: v0
contract_status: draft
task_packet_ref: null
runner_contract_ref: 07_working/drafts/runtime_adapter/RUNTIME-RUNNER-CONTRACT.v0.en.md
consumption_contract_ref: 07_working/drafts/runtime_adapter/TASK-PACKET-CONSUMPTION-CONTRACT.v0.en.md
execution_transcript_ref: null
review_packet_path: null
review_packet_class: review_packet
review_packet_id: null
review_packet_schema_version: null
representation_validator_ref: "python3 05_scripts/validate/shadowmas_validate.py <packet-file>"
representation_validation_state: not_validated
authority_validation_state: not_validated
authority_blocked_reason: no_authority_validator_defined
workspace_ref: null
allowed_output_roots:
  - external_workspace_reviews
forbidden_output_roots:
  - product_repo
  - 01_truth
  - 02_packets
  - 03_memory
  - 04_runtime
product_repo_write_allowed: false
workspace_only_emission_allowed: true
final_emission_allowed: false
external_side_effects_allowed: false
emission_state: not_started
non_claim_record:
  production_readiness: false
  runtime_enforcement: false
  automatic_correctness: false
  authority_validity: false
  task_verification: false
  final_review_approval: false
  product_repo_write_back_safety: false
claim_ceiling: emission_lifecycle_contract_draft_only
required_human_approval:
  before_draft: true
  before_workspace_emission: true
  before_final_emission: true
  before_product_repo_write: true
stop_conditions:
  - task_packet_ref_missing
  - execution_transcript_ref_missing
  - representation_not_validated
  - authority_not_validated
  - workspace_ref_missing
  - requested_final_emission
  - requested_product_repo_write
  - requested_external_side_effect
```

## Future unlocks

Before review packet emitter implementation may begin, the repo needs:

- canonical review emission lifecycle contract decision
- authority validation boundary
- execution transcript capture contract
- task packet consumption contract review closure
- runner contract review closure
- adapter registry decision, if needed
- product-repo write-back approval boundary, if ever needed

## Do Not Promote Yet

This remains draft because review emission, authority validation, transcript capture, task packet consumption, runner behavior, adapter registry ownership, and write-back boundaries are unresolved.
