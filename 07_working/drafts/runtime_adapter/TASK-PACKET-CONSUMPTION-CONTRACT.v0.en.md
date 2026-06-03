> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through packet-boundary review
> source basis: future task packet consumption contract audit and existing runtime-adapter drafts

# TASK-PACKET-CONSUMPTION-CONTRACT.v0

## Status

This file is a non-canonical draft.

It is not an implementation.
It does not grant execution authority.
It does not prove runtime readiness.
It does not make representation-valid packets authority-valid.
It does not unblock review emission.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`, validators, workspace tools, smoke tools, tests, or packet examples.

The contract shape below is planning material only. Contract readability is not implementation, packet loading is not execution, schema validity is not authority, transcript capture is not truth closure, and task packet fields are not authority grants.

## Purpose

Define the minimum contract shape for future task packet consumption.

A task packet consumption contract describes the boundary a future consumer would need to obey before implementation. It is not the consumer implementation.

The contract preserves these distinctions:

- loading a packet
- validating packet representation
- validating packet authority
- allowing dry-run consumption
- capturing transcript evidence
- executing task instructions

The contract also preserves this distinction:

- representation validity: a packet has the required shape for a local validator
- authority validity: a human-approved authority path says the packet may be acted on

Representation validity does not imply authority validity.

## Non-goals

This draft does not define or create:

- task packet consumer
- runner
- hooks
- adapter registry
- review packet emitter
- product-repo writes
- external side effects
- authority approval
- production readiness claim
- runtime enforcement behavior
- product-repo write-back behavior

## Minimum consumption contract fields

A draft task packet consumption contract record should include at least:

- `consumption_contract_id`: stable identifier for this consumption contract record
- `contract_version`: contract schema version, initially `v0`
- `contract_status`: draft status such as `draft`, `blocked`, `dry_run_only`, or `retired`
- `runner_contract_ref`: runner contract this consumption contract depends on, if any
- `adapter_manifest_ref`: runtime adapter manifest this consumption contract depends on, if any
- `task_packet_path`: path to the task packet candidate
- `task_packet_class`: accepted packet class, initially `task_packet`
- `task_packet_id`: task packet identifier, if loaded
- `task_packet_schema_version`: task packet schema version, if loaded
- `task_packet_status`: task packet status value, if loaded
- `representation_validator_ref`: validator or checker command used for representation validation
- `representation_validation_state`: representation validation status for the task packet
- `authority_validation_state`: authority validation status for the task packet
- `authority_blocked_reason`: reason authority is blocked or unvalidated
- `workspace_ref`: external shadowMAS workspace reference, if any
- `allowed_read_roots`: roots a future consumer may read
- `forbidden_read_roots`: roots a future consumer must not read
- `allowed_artifact_roots`: roots where consumption artifacts may be created
- `forbidden_artifact_roots`: roots where consumption artifacts must not be created
- `execution_allowed`: whether task instruction execution is allowed
- `dry_run_allowed`: whether dry-run or transcript-only consumption is allowed
- `review_emission_allowed`: whether review packet emission is allowed
- `external_side_effects_allowed`: whether network, service, or non-local side effects are allowed
- `product_repo_write_allowed`: whether product-repo writes are allowed
- `consumption_state`: current consumption lifecycle state
- `transcript_requirement`: expected transcript capture requirement, if any
- `non_claim_record`: claims explicitly not made by loading, validation, dry-run, or transcript capture
- `claim_ceiling`: strongest claim this consumption contract may support
- `required_human_approval`: human approval required before dry-run, execution, review emission, or write-back
- `stop_conditions`: conditions that require the consumer to stop before loading, dry-run, execution, or output

## Consumption states

Minimum consumption states:

- `not_loaded`: no task packet has been read
- `loaded_unvalidated`: task packet was loaded, but representation validation has not passed
- `representation_validated`: representation validation passed
- `authority_unvalidated`: no authority validation path has approved action
- `authority_blocked`: authority validation is missing, failed, or out of scope
- `consumption_allowed_for_dry_run`: dry-run or transcript-only consumption is allowed
- `consumed_for_transcript_only`: packet was used only to produce bounded transcript evidence
- `rejected`: packet was rejected or cannot be consumed within this boundary

`representation_validated` is not `authority_unvalidated`, and neither state is execution approval.

## Default-deny capabilities

The first task packet consumption contract must deny by default:

- executing task instructions
- product-repo writes
- external side effects
- review packet emission
- authority approval
- task-to-runner promotion
- schema-valid to authority-valid promotion
- workspace-to-product artifact promotion
- broad repo traversal unless explicitly scoped

## Boundary rules

- A task packet consumption contract is not a task packet consumer.
- Loading a task packet is not executing the task.
- Representation-valid is not authority-valid.
- Authority-unvalidated packets must not drive execution.
- Consuming a packet for transcript or dry-run is not approval.
- `worker_plan` is not routing authority.
- `trust_class` is not real-world trust validation.
- `acceptance_criteria` is not completed verification.
- `truth_touchpoints` are not permission to edit truth surfaces.
- Review emission remains blocked until a separate lifecycle contract exists.
- Product-repo writes remain denied unless a later explicit boundary allows them.
- Local smoke success is not production readiness.
- Workspace artifacts remain external unless a later approved boundary says otherwise.
- Product-repo write-back must remain disabled unless a later human-approved boundary explicitly enables it.

## Example draft record

Illustrative and non-authoritative:

```yaml
consumption_contract_id: task_packet_consumption_contract_v0
contract_version: v0
contract_status: draft
runner_contract_ref: 07_working/drafts/runtime_adapter/RUNTIME-RUNNER-CONTRACT.v0.en.md
adapter_manifest_ref: 07_working/drafts/runtime_adapter/RUNTIME-ADAPTER-MANIFEST.v0.en.md
task_packet_path: null
task_packet_class: task_packet
task_packet_id: null
task_packet_schema_version: null
task_packet_status: null
representation_validator_ref: "python3 05_scripts/validate/shadowmas_validate.py <packet-file>"
representation_validation_state: not_validated
authority_validation_state: not_validated
authority_blocked_reason: no_authority_validator_defined
workspace_ref: null
allowed_read_roots: []
forbidden_read_roots:
  - product_repo
  - 01_truth
  - 02_packets
  - 03_memory
  - 04_runtime
allowed_artifact_roots: []
forbidden_artifact_roots:
  - product_repo
execution_allowed: false
dry_run_allowed: false
review_emission_allowed: false
external_side_effects_allowed: false
product_repo_write_allowed: false
consumption_state: not_loaded
transcript_requirement:
  required_before_execution: true
  transcript_path: null
non_claim_record:
  production_readiness: false
  runtime_enforcement: false
  automatic_correctness: false
  authority_validity: false
  product_repo_write_back_safety: false
claim_ceiling: consumption_contract_draft_only
required_human_approval:
  before_dry_run: true
  before_execution: true
  before_review_emission: true
  before_product_repo_write: true
stop_conditions:
  - task_packet_not_loaded
  - representation_not_validated
  - authority_not_validated
  - workspace_ref_missing
  - requested_product_repo_write
  - requested_external_side_effect
  - requested_review_emission
  - requested_broad_repo_traversal
```

## Future unlocks

Before task packet consumer implementation may begin, the repo needs:

- canonical task packet consumption contract decision
- authority validation boundary
- runner contract review closure
- review packet emission lifecycle
- execution transcript capture contract
- adapter registry decision, if needed
- product-repo write-back approval boundary, if ever needed

## Do Not Promote Yet

This remains draft because task packet consumption, authority validation, runner behavior, review emission, transcript capture, adapter registry ownership, and write-back boundaries are unresolved.
