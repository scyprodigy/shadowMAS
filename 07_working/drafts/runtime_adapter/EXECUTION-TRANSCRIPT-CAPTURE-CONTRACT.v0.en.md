> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through packet-boundary review
> source basis: future execution transcript capture contract audit and existing runtime-adapter drafts

# EXECUTION-TRANSCRIPT-CAPTURE-CONTRACT.v0

## Status

This file is a non-canonical draft.

It is not an implementation.
It does not create transcript capture.
It does not grant permission to run commands.
It does not grant authority approval.
It does not mark tasks as verified.
It does not prove runtime readiness.
It does not permit product-repo transcript writes.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`, validators, workspace tools, smoke tools, tests, or packet examples.

The contract shape below is planning material only. Contract readability is not implementation, transcript capture is not truth closure, command output is not authority, workspace storage is not product-repo write-back, and evidence existence is not approval.

## Purpose

Define the minimum contract shape for future execution transcript capture.

An execution transcript capture contract describes the boundary a future capture implementation would need to obey before implementation. It is not the capture implementation.

The contract preserves these distinctions:

- command or check execution
- transcript capture
- transcript storage
- transcript representation validation
- transcript authority validation
- approval

The contract also preserves this distinction:

- evidence: bounded recorded output from a scoped command, check, or runtime action
- truth closure: a separately authorized decision that the evidence may be treated as accepted truth

Evidence does not imply truth closure.

## Non-goals

This draft does not define or create:

- transcript capture implementation
- command runner
- runner
- hooks
- adapter registry
- task packet consumer
- review packet emitter
- product-repo writes
- external side effects
- authority approval
- task verification claim
- production readiness claim
- runtime enforcement behavior
- product-repo write-back behavior

## Minimum transcript capture contract fields

A draft execution transcript capture contract record should include at least:

- `transcript_contract_id`: stable identifier for this transcript capture contract record
- `contract_version`: contract schema version, initially `v0`
- `contract_status`: draft status such as `draft`, `blocked`, `workspace_only`, or `retired`
- `runner_contract_ref`: runner contract this transcript capture contract depends on, if any
- `consumption_contract_ref`: task packet consumption contract this transcript capture contract depends on, if any
- `review_emission_contract_ref`: review emission lifecycle contract this transcript capture contract may later support, if any
- `task_packet_ref`: task packet whose scoped work or checks are being evidenced, if any
- `workspace_ref`: external shadowMAS workspace reference, if any
- `command_source_ref`: approved source that defines the command, check, or runtime action eligible for capture
- `allowed_capture_roots`: roots from which transcript content may be captured
- `forbidden_capture_roots`: roots from which transcript content must not be captured
- `transcript_path`: path where transcript evidence may be stored
- `transcript_format`: format for captured transcript evidence
- `capture_scope`: bounded statement of command output, files, streams, and metadata eligible for capture
- `redaction_required`: whether redaction is required before storage or review
- `secret_redaction_policy_ref`: policy reference for detecting and redacting secrets
- `secret_capture_allowed`: whether secret capture is allowed
- `environment_capture_allowed`: whether environment variables or process environment metadata may be captured
- `stdout_capture_allowed`: whether stdout may be captured
- `stderr_capture_allowed`: whether stderr may be captured
- `integrity_hash`: optional hash or integrity record for the stored transcript artifact
- `retention_policy`: retention or discard expectation for the transcript artifact
- `workspace_only_storage_allowed`: whether storage is limited to the external workspace
- `product_repo_write_allowed`: whether product-repo transcript writes are allowed
- `external_side_effects_allowed`: whether network, service, or non-local side effects are allowed
- `capture_state`: current transcript capture lifecycle state
- `representation_validation_state`: representation validation status for the transcript artifact
- `authority_validation_state`: authority validation status for the transcript artifact
- `authority_blocked_reason`: reason authority is blocked or unvalidated
- `non_claim_record`: claims explicitly not made by command output, capture, storage, validation, or transcript existence
- `claim_ceiling`: strongest claim this transcript capture contract may support
- `required_human_approval`: human approval required before command execution, capture, secret capture, storage, review use, or write-back
- `stop_conditions`: conditions that require capture to stop before command execution, capture, storage, validation, review use, or output

## Transcript lifecycle states

Minimum transcript lifecycle states:

- `not_started`: no transcript capture has started
- `capture_blocked`: capture is blocked by missing scope, authority, path, redaction policy, or validation state
- `capture_allowed_for_dry_run`: capture is allowed only for dry-run or check output within the declared scope
- `capture_started`: transcript capture has started
- `capture_completed`: scoped capture completed
- `capture_failed`: capture failed or produced unusable output
- `stored_workspace_only`: transcript was stored only under the external workspace
- `representation_validated`: transcript artifact representation validation passed, if a validator exists
- `authority_unvalidated`: no authority validation path has approved the transcript as truth, task verification, or review approval
- `rejected`: transcript candidate was rejected or cannot be used within this boundary

`capture_completed` is not `verified`, and `stored_workspace_only` is not product-repo write-back.

## Default-deny capabilities

The first execution transcript capture contract must deny by default:

- treating transcript as truth closure
- treating transcript as task verification
- treating transcript as authority approval
- product-repo transcript writes
- external side effects
- capturing secrets
- capturing out-of-scope paths
- transcript-to-review approval promotion
- workspace-to-product artifact promotion
- broad command execution or capture outside declared command/check source
- durable storage outside allowed workspace roots

## Boundary rules

- An execution transcript capture contract is not transcript capture implementation.
- A transcript is evidence only, not truth closure.
- A transcript is not task verification.
- A transcript is not authority approval.
- Capturing command output does not grant permission to run commands.
- `capture_completed` is not verified.
- `stored_workspace_only` is not product-repo write-back.
- Transcript existence does not unblock review packet final emission.
- Local smoke success is not production readiness.
- Product-repo writes remain denied unless a later explicit boundary allows them.
- Secret capture must remain denied unless a later explicit redaction or secret policy allows it.
- Workspace artifacts remain external unless a later approved boundary says otherwise.

## Example draft record

Illustrative and non-authoritative:

```yaml
transcript_contract_id: execution_transcript_capture_contract_v0
contract_version: v0
contract_status: draft
runner_contract_ref: 07_working/drafts/runtime_adapter/RUNTIME-RUNNER-CONTRACT.v0.en.md
consumption_contract_ref: 07_working/drafts/runtime_adapter/TASK-PACKET-CONSUMPTION-CONTRACT.v0.en.md
review_emission_contract_ref: 07_working/drafts/runtime_adapter/REVIEW-PACKET-EMISSION-LIFECYCLE-CONTRACT.v0.en.md
task_packet_ref: null
workspace_ref: null
command_source_ref: null
allowed_capture_roots:
  - external_workspace_runs
forbidden_capture_roots:
  - product_repo
  - 01_truth
  - 02_packets
  - 03_memory
  - 04_runtime
transcript_path: null
transcript_format: text
capture_scope:
  command_output_only: true
  file_content_capture_allowed: false
  process_environment_capture_allowed: false
redaction_required: true
secret_redaction_policy_ref: null
secret_capture_allowed: false
environment_capture_allowed: false
stdout_capture_allowed: true
stderr_capture_allowed: true
integrity_hash: null
retention_policy: "undefined_in_this_draft"
workspace_only_storage_allowed: true
product_repo_write_allowed: false
external_side_effects_allowed: false
capture_state: not_started
representation_validation_state: not_validated
authority_validation_state: not_validated
authority_blocked_reason: no_authority_validator_defined
non_claim_record:
  production_readiness: false
  runtime_enforcement: false
  automatic_correctness: false
  authority_validity: false
  task_verification: false
  truth_closure: false
  final_review_approval: false
  product_repo_write_back_safety: false
claim_ceiling: transcript_capture_contract_draft_only
required_human_approval:
  before_command_execution: true
  before_capture: true
  before_secret_capture: true
  before_workspace_storage: true
  before_review_use: true
  before_product_repo_write: true
stop_conditions:
  - command_source_ref_missing
  - workspace_ref_missing
  - capture_scope_missing
  - redaction_policy_missing
  - requested_secret_capture
  - requested_environment_capture
  - requested_product_repo_write
  - requested_external_side_effect
  - requested_out_of_scope_path_capture
  - requested_review_final_emission
```

## Future unlocks

Before transcript capture implementation may begin, the repo needs:

- canonical transcript capture contract decision
- redaction/secret policy
- authority validation boundary
- runner contract review closure
- task packet consumption contract review closure
- review emission lifecycle contract review closure
- adapter registry decision, if needed
- product-repo write-back approval boundary, if ever needed

## Do Not Promote Yet

This remains draft because transcript capture, redaction and secret handling, authority validation, runner behavior, task packet consumption, review emission, adapter registry ownership, and write-back boundaries are unresolved.
