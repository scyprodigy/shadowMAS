> status: working draft / implementation-prep
> authority: none
> source lane: contract-versioning validator and CI prep
> do not implement from this file without governance review

# CONTRACT-VERSIONING-VALIDATOR-CI-PREP.v0

## Purpose
Prepare future contract-versioning validator and CI design without writing code.

This note separates checks that are mature enough to design from checks blocked by unresolved governance decisions.

## Scope
- validator responsibility planning
- candidate check classes
- blocked check classes
- input and output report shape
- failure severity vocabulary
- CI and human review boundaries

## Non-Scope
- no validator scripts
- no CI workflow files
- no tests
- no executable scripts
- no reservation registry
- no new packet fields
- no `schema_version` migration
- no canonical truth promotion

## Current Governance Inputs
- `schema_version` is the authoritative in-artifact contract version field.
- Filename `.vN` is a major-line mirror only.
- Parser/validator authority must not come from filename when `schema_version` exists.
- Filename major and in-artifact major mismatch is review-blocking.
- Additive optional fields are normally backward-compatible only if existing requiredness, type, meaning, default behavior, and allowed-value semantics are unchanged.
- Requiredness, type, semantic meaning, default behavior, and wire-visible identifier changes are breaking.
- Deprecation must precede removal.
- Retired identifiers must not be reused.
- SemVer-aligned PATCH/MINOR/MAJOR language is governance language only.

## Future Validator Responsibilities
- Detect missing or unparseable `schema_version` when required by the artifact type.
- Detect filename major / `schema_version` major mismatch when both are present.
- Report candidate additive optional changes.
- Report candidate breaking changes for human review.
- Detect removal without deprecation only after deprecation metadata policy exists.
- Detect retired identifier reuse only after reservation tracking exists.
- Produce review reports; do not promote artifacts.

## Candidate Check Classes
- `version_presence_check`
- `version_parse_check`
- `filename_major_alignment_check`
- `field_requiredness_change_check`
- `field_type_change_check`
- `field_meaning_change_review_flag`
- `default_behavior_change_review_flag`
- `wire_visible_identifier_rename_check`
- `deprecated_before_removal_check`
- `retired_identifier_reuse_check`
- `packet_surface_registry_alignment_check`

## Blocked Check Classes
- `format_dialect_version_check` is blocked until field naming/location is decided.
- `enum_addition_minor_check` is blocked until unknown-value tolerance policy is decided.
- `reservation_registry_check` is blocked until reservation registry ownership/location is decided.
- `yaml_semantic_diff_check` is blocked until normalized contract representation is designed.
- `full_semver_compliance_check` is blocked until full SemVer adoption/migration policy is decided.

## Input Artifacts
- current artifact under review
- prior canonical version or baseline
- packet field dictionary
- file-status registry
- reservation registry later, if created
- edge-case decision board while unresolved

## Output / Report Shape
A future validator report should include:
- `artifact_path`
- `artifact_kind`
- `current_schema_version`
- `filename_major`
- `baseline_ref`
- `checks_run`
- `checks_blocked`
- `review_blockers`
- `warnings`
- `human_review_required`
- `unresolved_edge_cases`
- `recommended_next_action`

## Failure Severity Draft
- `BLOCKER`: must stop automated acceptance and require human/head review.
- `WARNING`: may continue only with explicit review note.
- `INFO`: recorded for traceability, no stop by itself.
- `UNIMPLEMENTED`: check is known but blocked by unresolved governance decision.

## CI Integration Boundary
Future CI may run validator checks, but CI must not become truth authority.

CI failure can block merge or acceptance only according to approved governance policy.

CI reports are evidence / execution feed until reviewed.

No CI workflow files are created in this task.

## Human Review Boundary
- Human/head review remains required for semantic meaning changes.
- Human/head review remains required when edge cases are blocked or ambiguous.
- Validator output must not bypass promotion gates.

## Do Not Implement Yet
- Do not create validator scripts.
- Do not create CI workflow files.
- Do not create tests.
- Do not add `format_version`, `codec_version`, or `serialization_version` fields.
- Do not create a reservation registry.
- Do not migrate `schema_version` values.
- Do not classify all enum additions as MINOR.
- Do not make raw YAML diff authoritative.

## Open Decisions
- unknown-value tolerance policy for enum additions
- reservation registry ownership and location
- format/codec/dialect version field naming and location
- normalized semantic representation for YAML compatibility diff
- full SemVer adoption or non-adoption
- deprecation metadata shape and storage
- report format stability and owner

## Promotion Requirements
Before implementation begins:
- unresolved edge cases that affect the planned checks must be selected, rejected, or deferred explicitly
- owner files and artifact kinds must be listed
- baseline comparison strategy must be defined
- report severity policy must be reviewed by human/head authority
- CI blocking behavior must be approved separately
- this prep note must be converted into an implementation task without changing canonical truth by implication
