> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through packet-boundary review
> source basis: runtime adapter readiness audit and existing runtime-adapter drafts

# RUNTIME-ADAPTER-MANIFEST.v0

## Status

This file is a non-canonical draft.

It is not an implementation.
It does not grant authority.
It does not prove runtime readiness.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, `04_runtime/`, validators, workspace tools, or packet examples.

The manifest shape below is planning material only. Readability is not truth, and draft existence is not runtime capability.

## Purpose

Define the smallest machine-readable adapter boundary record needed before implementing runtime adapters.

The record should make adapter limits inspectable before any runner, hook, task packet consumer, review packet emitter, or product-repo write-back path exists.

The record preserves this distinction:

- representation validity: a packet or artifact has the required shape for a local validator
- authority validity: a human-approved authority path says the packet or artifact may be acted on

Representation validity does not imply authority validity.

## Non-goals

This draft does not define or create:

- runner
- execution engine
- task packet consumer
- review packet emitter
- product-repo writes
- production safety claim
- authority-validity claim
- adapter registry code
- hook behavior
- runtime enforcement behavior

## Manifest fields

A draft runtime adapter manifest record should include at least:

- `manifest_id`: stable identifier for this adapter manifest record
- `manifest_version`: manifest schema version, initially `v0`
- `adapter_name`: human-readable adapter name
- `adapter_status`: draft status such as `draft`, `blocked`, `experimental`, or `retired`
- `adapter_scope`: bounded statement of the host/runtime and task lane this adapter may describe
- `input_packet_classes`: packet classes the adapter may read as inputs, such as `task_packet`
- `output_packet_classes`: packet classes the adapter may produce as candidates, if separately allowed
- `reads_product_repo`: whether the adapter is allowed to read product-repo files
- `writes_product_repo`: whether the adapter is allowed to write product-repo files
- `writes_external_workspace`: whether the adapter is allowed to write shadowMAS external workspace artifacts
- `execution_allowed`: whether the adapter may execute work, commands, or agent actions
- `review_emission_allowed`: whether the adapter may emit review packet candidates
- `authority_boundary`: explicit authority limits and escalation conditions
- `representation_validator_refs`: validator or checker commands that cover representation form
- `authority_validator_refs`: authority-review surfaces, if any; empty means no authority validator exists
- `claim_ceiling`: strongest claim the manifest may support
- `required_human_approval`: human approval required before execution, review emission, or write-back
- `audit_log_requirement`: expected record of inputs, outputs, checks, scope, and unresolved risks
- `artifact_lifecycle`: where artifacts may be created, reviewed, promoted, retained, or discarded
- `known_non_claims`: claims this adapter manifest explicitly does not make

## Boundary rules

- Schema-valid packets are not authority-valid packets.
- Workspace artifacts are external unless a later approved boundary says otherwise.
- Local smoke success is not production readiness.
- Adapter manifests describe boundaries but do not execute tasks.
- Review emission remains blocked until a separate lifecycle contract exists.
- Runtime or host capability is execution capacity, not authority.
- Draft adapter material must not override canonical shadowMAS truth or project-local truth.
- Product-repo write-back must remain disabled unless a later human-approved boundary explicitly enables it.

## Example draft record

Illustrative and non-authoritative:

```yaml
manifest_id: codex_local_draft_v0
manifest_version: v0
adapter_name: codex_local_draft
adapter_status: draft
adapter_scope:
  runtime_host: codex
  lane: local_controlled_evaluation
  summary: "Boundary record only; no runtime execution."
input_packet_classes:
  - task_packet
output_packet_classes: []
reads_product_repo: false
writes_product_repo: false
writes_external_workspace: false
execution_allowed: false
review_emission_allowed: false
authority_boundary:
  schema_valid_is_authority_valid: false
  may_promote_truth: false
  may_approve_product_repo_write_back: false
  human_final_authority_preserved: true
representation_validator_refs:
  - "python3 05_scripts/validate/shadowmas_validate.py <packet-file>"
  - "python3 tools/first_user_smoke.py"
authority_validator_refs: []
claim_ceiling: boundary_draft_only
required_human_approval:
  before_execution: true
  before_review_emission: true
  before_product_repo_write: true
audit_log_requirement:
  record_inputs: true
  record_outputs: true
  record_checks: true
  record_scope_exceeded_status: true
  record_unresolved_risks: true
artifact_lifecycle:
  allowed_locations: []
  promotion_requires_separate_contract: true
  discard_policy: "undefined_in_this_draft"
known_non_claims:
  - production_safety
  - runtime_authority_enforcement
  - automatic_correctness
  - authority_validity
  - product_repo_write_back_safety
```

## Future unlocks

Before runtime adapter implementation may begin, the repo needs:

- canonical adapter manifest decision
- runner contract
- task packet consumption contract
- review packet emission lifecycle
- execution transcript capture contract
- authority validation boundary
- product-repo write-back approval boundary, if ever needed

## Do Not Promote Yet

This remains draft because adapter manifest ownership, runner behavior, review emission, execution transcript capture, authority validation, and write-back boundaries are unresolved.
