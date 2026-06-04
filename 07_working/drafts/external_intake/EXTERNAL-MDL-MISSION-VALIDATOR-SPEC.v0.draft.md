# EXTERNAL-MDL-MISSION-VALIDATOR-SPEC.v0.draft | inactive validator specification for external MDL mission packet intake
# related: [MDL-MISSION-ISSUE-TEMPLATE, EXTERNAL-MDL-MISSION-PACKET-SCHEMA, MDL-MISSION-GATE-WORKFLOW]
# phase: external_intake_validator_spec_draft

# External MDL Mission Validator Spec v0 Draft

## Status

INACTIVE DRAFT ONLY.

This document is non-canonical. It is not implementation, not executable, not
validator code, not a GitHub Action, not production, and not public intake. It
does not enable public intake, does not scan external repositories, and does not
process live issues.

Do not copy this document into `.github/workflows/`, `.github/ISSUE_TEMPLATE/`,
runtime code, validator code, or production automation without explicit human
authority-boundary review.

## Purpose

This draft specifies a future enforcement contract for external MDL mission
issue submissions. It defines how a future validator would check submitted issue
data against:

- the inactive external MDL mission issue-template draft;
- the external MDL mission packet schema draft;
- the inactive MDL mission gate workflow draft.

This is a specification only. It defines expected validation behavior; it does
not implement that behavior.

## Core Rule

Form collects; validator/gate decides.

The issue form is collection-only. The validator is required before any public
intake decision. Nothing becomes a shadow candidate without `pass` plus
human-gated review.

The validator must not infer authority from prose and must not raise authority
beyond `claim_ceiling <= candidate` plus human-gated review.

## Gate Result Model

Gate results:

- `pass`: packet may enter human-gated candidate review.
- `flag_for_human_review`: fixable issue; not absorbed yet.
- `reject`: denied content, denied request, malformed required field, or unsafe
  parse failure.

Precedence: `reject > flag_for_human_review > pass`.

## Input Model

Expected inputs:

- issue form fields from the inactive issue-template shape;
- parsed packet fields matching ROUTE, EVID, CORE, and CTRL groups;
- issue metadata needed for local validation bookkeeping;
- no external repository content;
- no live external scans;
- no raw artifact ingestion.

The validator must validate submitted issue data only. It must not call external
APIs, clone repositories, inspect external projects, or retrieve linked raw
artifacts.

## Parse And Malformed Defaults

- Missing required field => `reject`.
- Malformed required field => `reject`.
- Duplicated authority field => `reject`.
- Unparseable `requested_shadow_action` => `reject`.
- Unparseable `claim_ceiling` => `reject`.
- Reporter-provided `gate_result` => `reject`.
- Optional malformed field without sensitive content => `flag_for_human_review`.
- Parse failure preventing safe classification => `reject`.
- Never infer missing authority fields from prose.
- Never auto-upgrade authority from prose.
- Never auto-raise `claim_ceiling`.
- Never auto-change `requested_shadow_action` to a higher-authority route.

## Enum Validation

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

`gate_result` is listed only as validator/gate output. It is not reporter input.

## Cross-Field Consistency Validation

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

Validation behavior:

- Higher-than-needed ceilings => `flag_for_human_review`.
- Lower-than-needed ceilings => `flag_for_human_review`.
- Never auto-raise authority.
- Never infer a missing ceiling/action pair from prose.
- Memory, n8n, reproducibility, reporter context, project kind, and boundary
  scope do not raise authority.

## ROUTE Validation

`mission_id`:

- must be system-generated and opaque;
- must not contain external project names, organization names, repo names,
  tracker IDs, domain terms, encoded context, paths, secrets, or authority
  requests.

`external_project_kind`:

- category only;
- if `other`, `other_project_kind_description` is required;
- missing description when `external_project_kind == other` =>
  `flag_for_human_review`.

`other_project_kind_description`:

- max 120 characters;
- generalized category only;
- identity-bearing, sensitive, path-like, or authority-bearing content =>
  `reject`.

Route authority:

- ROUTE fields route review only.
- ROUTE fields do not raise authority.
- `memory_layer_present` raises scrutiny only.
- `n8n_layer_present` raises scrutiny only.
- `reproducibility_level` raises confidence/review priority only, not authority.

## EVID Validation

`changed_paths_summary`:

- object-like count/type summary only;
- required count keys, if present, must be non-negative integers;
- `summary_note` must be short and generalized;
- no real paths;
- no absolute paths;
- no project names;
- no file contents;
- no diffs.

`seam_contract`:

- max 3 abstract lines;
- concrete generalized signature or shape only;
- no real API names;
- no secrets;
- no credentials;
- no implementation body;
- prose without sensitive content => `flag_for_human_review`;
- secret/API/implementation leakage => `reject`.

`evidence_refs`:

Allowed tagged pointer forms only:

```text
hash:<algorithm>:<value>
redacted_snippet_ref:<id>
count:<name>=<number>
repro_note:<short generalized note>
observation:<short generalized observation>
```

Denied artifacts:

- raw logs;
- stack traces;
- repo dumps;
- workflow graphs;
- concrete diffs;
- patches;
- schema edits;
- credentials;
- secrets;
- imported memory content;
- n8n node dumps;
- n8n credential dumps;
- n8n trigger dumps;
- full paths;
- project names.

Denied artifacts => `reject`.

## CORE Validation

Field limits:

- `intent`: required, max 200 characters.
- `restraint`: conditional, max 200 characters; required if out-of-scope
  temptation occurred.
- `boundary_hit`: conditional, max 200 characters; required if a boundary was
  reached.
- `seam_gap`: conditional, max 200 characters; required if a seam was involved.
- `shadow_candidate_lesson`: required, max 280 characters.

Denied CORE content:

- secrets;
- credentials;
- raw logs;
- full paths;
- repo dumps;
- workflow graphs;
- patches;
- schema edits;
- authority / promotion request language;
- unquarantined external project names.

Denied content => `reject`. Fixable missing conditional detail without denied
content => `flag_for_human_review`.

## CTRL Validation

`requested_shadow_action`:

- must be one accepted enum value;
- missing, malformed, duplicated, or unparseable value => `reject`.

`claim_ceiling`:

- must be one accepted enum value;
- missing, malformed, duplicated, or unparseable value => `reject`.

`gate_result`:

- gate-assigned only;
- reporter-provided `gate_result` => `reject`.

`external_terms_quarantine`:

- list of mission-local external terms;
- use `[]` if none;
- empty string invalid;
- external terms in `mission_id` or route enums reject rather than quarantine.

`generalized_replacement`:

- list of objects;
- object shape: `external_term`, `replacement`;
- one replacement per quarantined term;
- `external_term` must exactly match a quarantined term;
- `replacement` must be generalized, non-empty, and non-authority-bearing;
- missing, empty, or extra unmatched replacement =>
  `flag_for_human_review`;
- identity-bearing, sensitive, path-like, or authority-bearing replacement =>
  `reject`;
- authority request language in `external_term` or `replacement` => `reject`;
- authority-bearing replacement values reject, including `canonical rule`,
  `schema update`, `approved behavior`, `runtime change`, and `glossary term`.

`acknowledgements`:

- all required acknowledgements must be present and true;
- missing, false, malformed, duplicated, or unparseable acknowledgements =>
  `reject`;
- acknowledgements do not override denied content.

## Sensitive-Content Detection

Detection is best-effort defense-in-depth, not the authority guarantee.

- Suspected secret / credential => `reject`.
- Suspected raw log / stack trace => `reject`.
- Suspected workflow graph => `reject`.
- Suspected diff / patch / schema edit => `reject`.
- Do not echo suspected content in labels or comments.
- Do not quote raw rejected content.
- If secret exposure is likely, advise immediate credential rotation.

## Semantic Authority-Ban

Denied request classes:

- canonical truth;
- schema change;
- glossary promotion;
- memory ingestion;
- n8n workflow import;
- runtime behavior change;
- product repo write-back;
- external repo scan;
- authority approval;
- task verification.

Requests in these classes => `reject`, even if phrased as evidence or lesson.

## Output Labels

```yaml
labels:
  mdl-gate-pass: "result == pass"
  mdl-gate-flag: "result == flag_for_human_review"
  mdl-gate-reject: "result == reject"
  needs-quarantine-fix: "quarantine flag"
  needs-repro: "low-reproducibility flag"
  contains-denied-request: "semantic-ban reject; do not quote content"
  contains-sensitive-content: "secret/log reject; do not quote content"
  action-ceiling-mismatch: "consistency flag"
  malformed-packet: "structurally malformed packet"
  missing-required-field: "required authority/form field absent"
  unparseable-intake: "issue body could not be parsed into packet fields"
  best-effort-detection: "advisory marker for best-effort detector"
```

## Safe Comment Templates

`pass`:

```text
Gate: pass. This packet may enter candidate review.
Nothing is applied automatically; a maintainer will triage.
```

`flag_for_human_review`:

```text
Gate: flag_for_human_review. Fixable: <generic issue list>.
Not absorbed yet; please edit and resubmit. No rejected content quoted.
```

`reject`:

```text
Gate: reject. This packet contains denied content, a denied request, or unsafe
malformed input and was not accepted. Details are withheld to avoid echoing
sensitive or raw content.
```

`malformed/missing`:

```text
Gate: reject. Required packet fields are missing, malformed, duplicated, or
could not be parsed. Please resubmit using one bounded observation.
```

`suspected sensitive content`:

```text
Gate: reject. Suspected sensitive content was present. If you posted a secret
or credential, rotate it immediately. The rejected content is not quoted.
```

Comment rules:

- Never quote suspected secrets.
- Never echo raw rejected content.
- Never include raw malformed input.
- For suspected secret exposure, advise immediate credential rotation.

## Security And Public Issue Warning

Public issue secret exposure happens before any gate scan. A validator cannot
un-expose already posted secrets. The issue form warning must appear before
submission.

Private intake or a pre-submit proxy may be needed later if public use grows.

## Non-Goals

- no active public intake;
- no executable validator;
- no GitHub Action;
- no production bot;
- no external repo scan;
- no auto-close unless separately approved;
- no candidate promotion without human review;
- no schema / glossary / memory / runtime changes.

## Validation Examples

### Pass Example

```yaml
requested_shadow_action: accept_verifier_edge_case
claim_ceiling: candidate
boundary_scope: shadow_verifier_only
evidence_refs:
  - count:observed_cases=1
  - repro_note:generalized steps reproduced without raw logs
external_terms_quarantine: []
generalized_replacement: []
acknowledgements: all_true
```

Expected result: `pass`.

Reason: enum values valid, action/ceiling consistent, pointer-only evidence, no
denied content, acknowledgements complete.

### Flag Example

```yaml
external_project_kind: other
other_project_kind_description: ""
requested_shadow_action: accept_doc_clarification_candidate
claim_ceiling: candidate
```

Expected result: `flag_for_human_review`.

Reason: `other_project_kind_description` is missing and the action/ceiling pair
can be safely downgraded if no reject finding is present.

### Reject Example

```yaml
requested_shadow_action: accept_schema_promotion_evidence
claim_ceiling: evidence_only
evidence_refs:
  - observation:add enum value and patch validator
generalized_replacement:
  - external_term: "ExternalRule"
    replacement: "canonical rule"
```

Expected result: `reject`.

Reason: schema edit / patch request and authority-bearing replacement are denied.

## Future Unlocks

- human review of this inactive validator spec;
- paper simulation of validator rules;
- inactive implementation draft only after approval;
- explicit human decision before any active GitHub workflow or public intake.
