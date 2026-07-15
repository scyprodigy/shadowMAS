# EXTERNAL-MDL-MISSION-PACKET-SCHEMA.v0.draft | inactive schema draft for external MDL atomic mission packets
# related: [MDL-MISSION-GATE-WORKFLOW, external_intake, mdl_mission_packet, claim_ceiling, requested_shadow_action]
# phase: external_intake_packet_schema_draft

# External MDL Mission Packet Schema v0 Draft

## Status

INACTIVE DRAFT ONLY.

This document is non-canonical. It is not implementation, not a validator,
not an issue template, not a workflow, and not production. It does not enable
external intake by itself.

Form collects; gate decides. Nothing becomes a shadow candidate without gate
pass and human-gated review.

Do not copy this document into `.github/workflows/`, `.github/ISSUE_TEMPLATE/`,
runtime code, validators, or production automation without explicit human
authority-boundary review.

## Purpose

This draft defines the external MDL atomic mission packet schema for receiving
bounded external feedback without absorbing external repositories, external
memory, n8n workflows, raw logs, or project-specific vocabulary.

The packet is a quarantine and review shape. It is not a source of authority.

## Core Invariant

One packet = one bounded observation / failure / seam / verifier case.

- ROUTE routes review only.
- EVID provides bounded evidence pointers only.
- CORE contains bounded human residual only.
- CTRL caps authority and stores routing, quarantine, and acknowledgements.
- No field can raise authority beyond `claim_ceiling <= candidate` plus
  human-gated review.

Best-effort content detection reduces downstream pollution, but it is not the
authority guarantee. The structural authority cap is `claim_ceiling <=
candidate` plus human-gated review.

## Schema Groups

ROUTE describes where the packet should be reviewed and how much scrutiny it
needs. ROUTE fields are not authority fields.

EVID contains bounded evidence summaries and pointers. EVID fields must not
ingest raw external content.

CORE contains the reporter's bounded human-readable mission residual.

CTRL contains requested disposition, authority ceiling, gate result ownership,
external-term quarantine, generalized replacements, and acknowledgements.

## Full Schema Table

| Group | Field | Type | Required / conditional / gate-assigned | Allowed values or shape | Max length | Denied content | Gate behavior | Authority effect |
|---|---|---|---|---|---:|---|---|---|
| ROUTE | `mission_id` | string | required, machine-derived | opaque intake-system ID | 64 | external project names, organization names, repo names, tracker IDs, domain terms, encoded context, paths, secrets | pass if opaque; flag harmless reporter-provided identity; reject severe identity, path, secret, repo, tracker, or authority request | none |
| ROUTE | `reporter_context_class` | enum | required | `reporter_context_class` enum | n/a | names, orgs, authority claims, private context | pass if enum; reject malformed, duplicated, unparseable, or authority-bearing | none |
| ROUTE | `external_project_kind` | enum | required | `external_project_kind` enum | n/a | project names, product names, repo names | pass if category; flag `other` or harmless identity needing cleanup; reject specific/sensitive identity | none |
| ROUTE | `other_project_kind_description` | string | conditional; required only when `external_project_kind == other` | generalized category description only | 120 | project name, organization name, repo name, domain identity, path, secret, authority request | flag if missing when `external_project_kind == other`; reject identity-bearing or sensitive content | none |
| ROUTE | `boundary_scope` | enum | required | `boundary_scope` enum | n/a | runtime behavior change, product-repo write-back, authority approval, schema edit request, memory import, n8n import | pass if bounded route; reject denied scope or authority request | none |
| ROUTE | `memory_layer_present` | enum | required | `memory_layer_present` enum | n/a | memory content, memory import request | pass as scrutiny signal; reject imported memory content | none |
| ROUTE | `n8n_layer_present` | enum | required | `n8n_layer_present` enum | n/a | workflow graph, node dump, credential dump, trigger dump, n8n import request | pass as scrutiny signal; reject workflow graph or dump | none |
| ROUTE | `reproducibility_level` | enum | required | `reproducibility_level` enum | n/a | contradictory reproducibility used to justify authority | pass as confidence signal; flag harmless contradiction; reject contradiction tied to promotion/approval/higher authority | none |
| EVID | `task_goal` | string | required | short generalized goal | 200 | project identity, secrets, credentials, authority requests | pass if bounded; flag harmless identity; reject sensitive or authority-bearing content | none |
| EVID | `observed_failure` | string | required | generalized symptom | 280 | raw logs, stack traces, full paths, repo dumps, workflow graphs | pass if generalized; reject raw artifacts | none |
| EVID | `expected_behavior` | string | required | generalized expected behavior | 200 | product-specific promises, approval requests, runtime/schema authority requests | pass if bounded; reject authority requests | none |
| EVID | `actual_behavior` | string | required | generalized actual behavior | 280 | raw logs, stack traces, full paths, dumps | pass if bounded; reject raw artifacts | none |
| EVID | `changed_paths_summary` | object | optional | count/type object only | note: 160 | real paths, absolute paths, project names, file contents, diffs, path-like strings | pass if counts only; reject path-like strings or file content | none |
| EVID | `seam_contract` | string or list of strings | optional; required if seam is involved | max 3 abstract signature/shape lines | 240 total | real API names, secrets, credentials, prose body, implementation body, unquarantined project terms | pass if abstract; flag prose without sensitive content; reject secret/API/implementation leakage | none |
| EVID | `evidence_refs` | list of tagged strings | required | allowed tagged forms only | 5 items | raw logs, stack traces, repo dumps, workflow graphs, concrete diffs, patches, schema edits, credentials, imported memory, n8n dumps, full paths, project names | pass if pointer-only; reject denied artifacts | none |
| CORE | `intent` | string | required | bounded intent | 200 | secrets, credentials, raw logs, full paths, repo dumps, workflow graphs, patches, schema edits, authority/promotion requests, unquarantined external project names | pass if bounded; flag fixable identity; reject denied content | none |
| CORE | `restraint` | string | conditional | restraint taken | 200 | same as CORE denied list | optional; required if out-of-scope temptation occurred; reject denied content | none |
| CORE | `boundary_hit` | string | conditional | boundary reached | 200 | same as CORE denied list | optional; required if boundary was reached; reject denied content | none |
| CORE | `seam_gap` | string | conditional | generalized seam gap | 200 | same as CORE denied list, real API names | optional; required if seam was involved; flag missing seam detail; reject denied content | none |
| CORE | `shadow_candidate_lesson` | string | required | one generalized lesson | 280 | promotion request language, authority request language, schema edits, runtime changes, product write-back, unquarantined project names | pass if generalized; reject authority-seeking lesson | none |
| CTRL | `requested_shadow_action` | enum | required | `requested_shadow_action` enum | n/a | invalid, duplicated, unparseable, or prose-inferred value | pass if valid and consistent; flag mismatch; reject malformed | none |
| CTRL | `claim_ceiling` | enum | required | `claim_ceiling` enum | n/a | invalid, duplicated, unparseable, or prose-inferred value | pass if valid and consistent; flag mismatch; reject malformed | cap only |
| CTRL | `gate_result` | enum | gate-assigned | `gate_result` enum | n/a | reporter-submitted value, reporter-provided override, self-declared pass / flag / reject | gate assigns value only; reporter-submitted `gate_result` is malformed input and must hard-reject the packet | none |
| CTRL | `external_terms_quarantine` | list of strings | required | mission-local external terms, or `[]` | 10 terms | empty strings, secrets, credentials, route-field identity | pass if complete; flag missing/fixable terms; reject severe leakage | none |
| CTRL | `generalized_replacement` | list of objects | required | one `{external_term, replacement}` object per quarantined term, or `[]` | 10 mappings | empty strings, project names, paths, secrets, authority request language, glossary promotion | pass if complete; flag missing/empty/extra replacement; reject identity-bearing or sensitive replacement | none |
| CTRL | `acknowledgements` | object of booleans | required | all required acknowledgements true | n/a | missing, false, malformed, duplicated, unparseable values | pass if all true and content clean; reject missing/false/malformed; true values do not override denied content | none |

## Enums

```yaml
reporter_context_class:
  - external_user
  - integrator
  - maintainer_proxy
  - anonymous_external
  - internal_shadow_reviewer
  - agent_scratch_run
  - ci_run

external_project_kind:
  - api_service
  - web_app
  - workflow_automation
  - data_pipeline
  - ai_agent_system
  - library_framework
  - documentation_site
  - cli
  - other

boundary_scope:
  - shadow_docs_only
  - shadow_verifier_only
  - shadow_contract_only
  - shadow_schema_evidence_only
  - shadow_evidence_only
  - reject_only

memory_layer_present:
  - none
  - light
  - heavy

n8n_layer_present:
  - no
  - yes

reproducibility_level:
  - none
  - once
  - steps
  - deterministic

requested_shadow_action:
  - accept_lesson_candidate
  - accept_verifier_edge_case
  - accept_seam_contract_candidate
  - accept_schema_promotion_evidence
  - accept_doc_clarification_candidate
  - reject_project_specific
  - require_more_reproducible_packet

claim_ceiling:
  - reject_only
  - doc_clarification_candidate
  - evidence_only
  - candidate

gate_result:
  - pass
  - flag_for_human_review
  - reject
```

## Cross-Field Consistency

```yaml
accept_schema_promotion_evidence: evidence_only
accept_lesson_candidate: candidate
accept_verifier_edge_case: candidate
accept_seam_contract_candidate: candidate
accept_doc_clarification_candidate: doc_clarification_candidate
reject_project_specific: reject_only
require_more_reproducible_packet:
  - reject_only
  - evidence_only
```

Higher-than-needed ceilings flag for safe downgrade. Lower-than-needed ceilings
flag for action downgrade. The gate must never auto-raise authority.

`memory_layer_present`, `n8n_layer_present`, `reproducibility_level`,
`reporter_context_class`, `external_project_kind`, and `boundary_scope` route
review only. They cannot change `requested_shadow_action`, cannot raise
`claim_ceiling`, and cannot grant authority.

When `external_project_kind` is `other`, `other_project_kind_description` is
required as a generalized category description only. Missing description flags
for human review. Identity-bearing or sensitive descriptions reject.

## changed_paths_summary Object

```yaml
changed_paths_summary:
  own_scope_changed_count: integer >= 0
  forbidden_scope_changed_count: integer >= 0
  contested_scope_changed_count: integer >= 0
  untracked_count: integer >= 0
  deleted_count: integer >= 0
  renamed_or_moved_count: integer >= 0
  summary_note: short generalized string
```

Rules:

- Counts/types only.
- No real paths.
- No absolute paths.
- No project names.
- No file contents.
- No diffs.
- Path-like strings reject.

## seam_contract Shape

Rules:

- Max 3 lines.
- Concrete abstract signature or shape.
- Generalized types only.
- Not prose.
- No project-specific API names.
- No secrets.
- No implementation body.
- No project-specific domain terms unless quarantined.

Valid examples:

```text
validate(input: GeneralInput) -> ValidationResult
emit(event: AbstractEvent) -> DeliveryStatus
resolve(record_id: OpaqueId, mode: ReviewMode) -> Resolution
```

Invalid examples:

```text
VendorBillingClient.createInvoice(customerSecret, amount)
POST /internal/vendor/orders/{id} with bearer token <credential>
This function should update storage, retry the webhook, and patch the schema.
```

## evidence_refs Tagged Forms

Allowed forms:

```text
hash:<algorithm>:<value>
redacted_snippet_ref:<id>
count:<name>=<number>
repro_note:<short generalized note>
observation:<short generalized observation>
```

Allowed hash algorithms:

- `sha256`
- `sha512`
- `blake3`

`redacted_snippet_ref` ID shape: `rsr_[a-z0-9_]{8,40}`.

Max note / observation length: 180 characters.

Denied artifacts:

- raw logs
- stack traces
- repo dumps
- workflow graphs
- concrete diffs
- patches
- schema edits
- credentials
- secrets
- imported memory content
- n8n node dumps
- n8n credential dumps
- n8n trigger dumps
- full paths
- project names

## CORE Field Limits

- `intent`: max 200 characters, required.
- `restraint`: max 200 characters, optional / required if out-of-scope
  temptation occurred.
- `boundary_hit`: max 200 characters, optional / required if boundary was
  reached.
- `seam_gap`: max 200 characters, optional / required if seam was involved.
- `shadow_candidate_lesson`: max 280 characters, required.

Denied CORE content:

- secrets
- credentials
- raw logs
- full paths
- repo dumps
- workflow graphs
- patches
- schema edits
- authority / promotion request language
- unquarantined external project names

## External Terms Quarantine

`external_terms_quarantine` is a list of mission-local external terms.
`generalized_replacement` is a list of objects pairing each quarantined term
with a generic replacement.

Exact `generalized_replacement` shape:

```yaml
generalized_replacement:
  - external_term: string
    replacement: string
```

Rules:

- Empty string invalid.
- Use `[]` if there are no terms.
- One `generalized_replacement` entry is required per
  `external_terms_quarantine` item.
- `external_term` must exactly match a quarantined term.
- `replacement` must be generalized and non-empty.
- No empty strings.
- No project names.
- No paths.
- No secrets.
- No authority request language.
- Authority request language in `external_term` or `replacement` rejects.
- Missing replacement for a quarantined term flags for human review.
- Empty replacement flags for human review.
- Extra replacement entry with no matching quarantined term flags for human
  review.
- Identity-bearing, sensitive, or authority-bearing replacement rejects.
- Rejected authority-bearing replacements include `canonical rule`, `schema
  update`, `approved behavior`, `runtime change`, and `glossary term`.
- No glossary promotion.
- Repeated terms across missions are evidence only, not authority.
- External terms in `mission_id` or route enums reject rather than quarantine.

## Acknowledgements

Required true acknowledgements:

```yaml
one_bounded_observation_only: true
not_requesting_schema_glossary_memory_n8n_runtime_product_write_back_repo_scan_authority_or_task_verification: true
no_secrets_logs_diffs_repo_dumps_or_workflow_graphs: true
external_terms_quarantined_and_generalized: true
```

Acknowledgements are necessary but not sufficient. True acknowledgements do not
override denied content.

## Gate Behavior

Gate results:

- `pass`: all required fields valid, enums consistent, evidence pointer-only,
  no denied content, acknowledgements complete.
- `flag_for_human_review`: fixable ambiguity, harmless identity leakage,
  `external_project_kind: other` needing generalized description, low
  reproducibility, safely downgradable action/ceiling mismatch, or prose-like
  seam contract without sensitive content.
- `reject`: denied content, malformed authority fields, unparseable required
  fields, raw artifacts, secrets, diffs, repo dumps, workflow graphs, import
  requests, runtime/write-back/approval/schema/task-verification requests, or
  attempted reporter-submitted `gate_result`, including self-declared `pass`,
  `flag_for_human_review`, or `reject`.

Precedence: `reject > flag_for_human_review > pass`.

Fail-closed malformed/default behavior:

- Missing, malformed, duplicated, or unparseable `requested_shadow_action`
  rejects.
- Missing, malformed, duplicated, or unparseable `claim_ceiling` rejects.
- Required form fields that cannot be extracted reject.
- Parsing failures that prevent safe classification reject.
- Missing authority fields must never be inferred from prose.
- `claim_ceiling` or `requested_shadow_action` must never be auto-upgraded from
  prose.

Best-effort detection note:

- Secret detection is best-effort.
- Credential detection is best-effort.
- Raw log / stack trace detection is best-effort.
- Diff / patch / schema-edit detection is best-effort.
- Workflow graph detection is best-effort.
- Semantic authority-ban detection is best-effort.

Best-effort detection is not the authority guarantee. The structural authority
cap is `claim_ceiling <= candidate` plus human-gated review.

Even if content-level pollution is missed, intake cannot become:

- canonical truth
- schema change
- memory ingestion
- runtime behavior change
- glossary promotion
- product-repo write-back
- authority approval
- task verification

## Deny-List

```yaml
deny_list:
  - apply_patch
  - update_schema
  - update_glossary
  - import_memory
  - import_n8n_workflow
  - change_runtime_behavior
  - write_to_product_repo
  - scan_external_repo
  - auto_promote_to_canonical
  - authority_approval
  - task_verification
  - canonical_truth
```

## Minimal Valid Packet Example

This is a post-gate normalized packet example. `gate_result` is gate-assigned
output. Reporter-submitted packets must not include or control `gate_result`;
reporter-submitted `gate_result` is malformed input and must hard-reject the
packet.

```yaml
ROUTE:
  mission_id: "mdl_8f3a2c91d0b4"
  reporter_context_class: external_user
  external_project_kind: api_service
  boundary_scope: shadow_verifier_only
  memory_layer_present: none
  n8n_layer_present: no
  reproducibility_level: steps

EVID:
  task_goal: "Check whether a verifier handles an empty optional input."
  observed_failure: "The generalized check treated missing optional input as a hard failure."
  expected_behavior: "Missing optional input should be classified separately from invalid input."
  actual_behavior: "The generalized verifier path collapsed both cases."
  changed_paths_summary:
    own_scope_changed_count: 0
    forbidden_scope_changed_count: 0
    contested_scope_changed_count: 0
    untracked_count: 0
    deleted_count: 0
    renamed_or_moved_count: 0
    summary_note: "No paths supplied."
  seam_contract: "validate(input: GeneralInput) -> ValidationResult"
  evidence_refs:
    - "count:observed_cases=1"
    - "repro_note:generalized optional input case reproduced with abstract steps"

CORE:
  intent: "Surface a verifier edge case without importing project details."
  restraint: "No logs, paths, diffs, or implementation details included."
  boundary_hit: ""
  seam_gap: "Optional and invalid input states were not separated."
  shadow_candidate_lesson: "Verifier checks should distinguish absent optional input from invalid provided input."

CTRL:
  requested_shadow_action: accept_verifier_edge_case
  claim_ceiling: candidate
  gate_result: pass
  external_terms_quarantine: []
  generalized_replacement: []
  acknowledgements:
    one_bounded_observation_only: true
    not_requesting_schema_glossary_memory_n8n_runtime_product_write_back_repo_scan_authority_or_task_verification: true
    no_secrets_logs_diffs_repo_dumps_or_workflow_graphs: true
    external_terms_quarantined_and_generalized: true
```

## Invalid Packet Examples

### Raw log / secret

```yaml
EVID:
  observed_failure: "A raw trace was pasted with a credential placeholder."
  evidence_refs:
    - "observation:raw log includes <credential>"
```

Expected gate result: `reject`. Raw logs and credentials are denied.

### Schema change disguised as evidence

```yaml
CTRL:
  requested_shadow_action: accept_schema_promotion_evidence
  claim_ceiling: evidence_only
EVID:
  evidence_refs:
    - "observation:add enum value new_runtime_mode and patch validator"
```

Expected gate result: `reject`. A concrete schema edit request is not evidence.

### Project identity leaked in route/evid fields

```yaml
ROUTE:
  mission_id: "vendor-product-INC-124"
  external_project_kind: "VendorProduct"
EVID:
  changed_paths_summary:
    summary_note: "Changed an absolute private project path ending in src/AuthClient.ts"
```

Expected gate result: `reject`. Route identity, tracker IDs, and real paths are
denied.

### Reporter-provided gate result

```yaml
CTRL:
  requested_shadow_action: accept_lesson_candidate
  claim_ceiling: candidate
  gate_result: pass
EVID:
  evidence_refs:
    - "observation:reporter attempted to self-declare pass"
```

Expected gate result: `reject`. Reporter-submitted `gate_result` is malformed
input and must hard-reject the packet. A packet cannot self-declare `pass`,
`flag_for_human_review`, or `reject`.

## Remaining Open Risks

- Public issue secret exposure can happen before gate scan.
- Best-effort detectors can miss content.
- Reporters may misunderstand evidence-pointer rules.
- Issue forms cannot enforce all constraints.
- Full implementation still requires human-gated review.
- `gate_result` ownership must remain gate-assigned.
- Acknowledgements do not override denied content.

## Future Unlocks

- Human review of this inactive schema document.
- Inactive issue-template file draft.
- Inactive validator spec draft.
- Future explicit decision before public intake.
- Future explicit decision before active workflow.
