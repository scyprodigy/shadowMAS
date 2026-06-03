> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through packet-boundary review
> source basis: future runtime runner contract audit and existing runtime-adapter drafts

# RUNTIME-RUNNER-CONTRACT.v0

## Status

This file is a non-canonical draft.

It is not an implementation.
It does not grant execution authority.
It does not prove runtime readiness.
It does not unblock review emission.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`, validators, workspace tools, smoke tools, tests, or packet examples.

The contract shape below is planning material only. Readability is not runtime readiness, draft existence is not implementation, local execution is not authority, and transcript capture is not truth closure.

## Purpose

Define the minimum contract shape for a future runtime runner.

A runner contract describes the boundary a runner would need to obey before implementation. It is not the runner implementation.

The contract preserves this distinction:

- representation validity: a packet or artifact has the required shape for a local validator
- authority validity: a human-approved authority path says the packet or artifact may be acted on

Representation validity does not imply authority validity.

## Non-goals

This draft does not define or create:

- runner
- hooks
- adapter registry
- task packet consumer
- review packet emitter
- product-repo writes
- external side effects
- production readiness claim
- authority-validity claim
- runtime enforcement behavior
- product-repo write-back behavior

## Minimum runner contract fields

A draft runtime runner contract record should include at least:

- `runner_contract_id`: stable identifier for this runner contract record
- `contract_version`: contract schema version, initially `v0`
- `runner_status`: draft status such as `draft`, `blocked`, `dry_run_only`, or `retired`
- `runner_scope`: bounded statement of the runner lane, host, and allowed task shape
- `adapter_manifest_ref`: runtime adapter manifest this runner contract depends on
- `input_packet_class`: packet class accepted as input, such as `task_packet`
- `input_packet_path`: path to the input packet candidate
- `packet_representation_validation_state`: representation validation status for the packet
- `packet_authority_validation_state`: authority validation status for the packet
- `workspace_path`: external shadowMAS workspace path used for artifacts, if any
- `allowed_artifact_roots`: roots where runner artifacts may be created
- `forbidden_artifact_roots`: roots where runner artifacts must not be created
- `reads_product_repo_allowed`: whether scoped product-repo reads are allowed
- `writes_product_repo_allowed`: whether product-repo writes are allowed
- `external_side_effects_allowed`: whether network, service, or non-local side effects are allowed
- `execution_mode`: allowed execution mode, such as `none`, `dry_run_only`, or `local_bounded`
- `runner_state`: current runner lifecycle state
- `execution_transcript_path`: path to captured transcript or null when absent
- `status_result`: result summary such as `not_started`, `blocked`, `failed`, or `completed`
- `blocked_reason`: reason execution is blocked, if any
- `checks_run`: checks or validators run during the flow
- `non_claim_record`: claims explicitly not made by the runner or transcript
- `review_emission_allowed`: whether review packet emission is allowed
- `review_emission_blocked_reason`: reason review emission remains blocked, if any
- `required_human_approval`: human approval required before execution, review emission, or write-back
- `claim_ceiling`: strongest claim this runner contract may support
- `artifact_lifecycle`: where artifacts may be created, reviewed, promoted, retained, or discarded
- `stop_conditions`: conditions that require the runner to stop before execution or output
- `audit_log_requirement`: expected record of inputs, outputs, checks, scope, and unresolved risks

## Runner states

Minimum runner states:

- `not_started`: no execution attempted
- `blocked`: execution is blocked by missing scope, authority, path, or validation state
- `dry_run_only`: only preview or validation-only behavior is allowed
- `locally_executed`: bounded local execution occurred
- `transcript_captured`: execution transcript was captured as evidence
- `failed`: execution or validation failed
- `verified_by_later_check`: a separate later check verified a bounded result

`locally_executed` is not `verified_by_later_check`.

## Default-deny capabilities

The first runner contract must deny by default:

- product-repo writes
- review packet emission
- authority approval
- external side effects
- production readiness claim
- runtime enforcement claim
- schema-valid to authority-valid promotion
- workspace-to-product artifact promotion
- broad repo traversal unless explicitly scoped

## Boundary rules

- A runner contract is not a runner.
- Local execution is not global authority.
- Captured transcript is evidence only, not approval.
- Schema-valid packets are not authority-valid packets.
- `locally_executed` is not `verified_by_later_check`.
- `review_emission_allowed` must not be inferred from `output_packet_classes`.
- `allowed_artifact_roots` must not imply product-repo write-back.
- Local smoke success is not production readiness.
- Workspace artifacts remain external unless a later approved boundary says otherwise.
- Product-repo write-back must remain disabled unless a later human-approved boundary explicitly enables it.

## Example draft record

Illustrative and non-authoritative:

```yaml
runner_contract_id: local_dry_run_runner_contract_v0
contract_version: v0
runner_status: draft
runner_scope:
  runtime_host: codex
  lane: local_controlled_evaluation
  summary: "Contract boundary only; no runner implementation."
adapter_manifest_ref: 07_working/drafts/runtime_adapter/RUNTIME-ADAPTER-MANIFEST.v0.en.md
input_packet_class: task_packet
input_packet_path: null
packet_representation_validation_state: not_validated
packet_authority_validation_state: not_validated
workspace_path: null
allowed_artifact_roots: []
forbidden_artifact_roots:
  - product_repo
  - 01_truth
  - 02_packets
  - 03_memory
  - 04_runtime
reads_product_repo_allowed: false
writes_product_repo_allowed: false
external_side_effects_allowed: false
execution_mode: dry_run_only
runner_state: not_started
execution_transcript_path: null
status_result: not_started
blocked_reason: "runner implementation and authority boundary do not exist"
checks_run: []
non_claim_record:
  production_readiness: false
  runtime_enforcement: false
  automatic_correctness: false
  authority_validity: false
  product_repo_write_back_safety: false
review_emission_allowed: false
review_emission_blocked_reason: "review packet emission lifecycle does not exist"
required_human_approval:
  before_execution: true
  before_review_emission: true
  before_product_repo_write: true
claim_ceiling: runner_contract_draft_only
artifact_lifecycle:
  promotion_requires_separate_contract: true
  discard_policy: "undefined_in_this_draft"
stop_conditions:
  - packet_representation_not_validated
  - packet_authority_not_validated
  - workspace_path_missing
  - requested_product_repo_write
  - requested_external_side_effect
  - requested_review_emission
audit_log_requirement:
  record_inputs: true
  record_outputs: true
  record_checks: true
  record_scope_exceeded_status: true
  record_unresolved_risks: true
```

## Future unlocks

Before runtime runner implementation may begin, the repo needs:

- canonical runner contract decision
- task packet consumption contract
- review packet emission lifecycle
- execution transcript capture contract
- authority validation boundary
- adapter registry decision
- product-repo write-back approval boundary, if ever needed

## Do Not Promote Yet

This remains draft because runner behavior, task packet consumption, review emission, transcript capture, authority validation, adapter registry ownership, and write-back boundaries are unresolved.
