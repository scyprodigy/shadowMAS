> status: working draft / decision board
> authority: none
> source lane: contract-versioning edge-case decisions
> do not promote without governance review

# FAST-REVIEW-CONTRACT-VERSIONING-EDGE-CASES.v0

## Purpose
Make unresolved contract-versioning edge cases inspectable, comparable, and ready for later human/head selection.

This board is not canonical truth and does not implement validators, CI, migrations, new fields, or registries.

## Scope
- unresolved packet/registry contract-versioning edge cases
- candidate defaults for later review
- do-now / do-later boundaries
- questions that must remain visible before formalization

## Non-Scope
- no edits to canonical packet schemas
- no edits to canonical registry schema
- no validator or CI implementation
- no reservation registry creation
- no `schema_version` migration
- no full SemVer adoption

## Current Settled Baseline
- `schema_version` is the authoritative in-artifact contract version field.
- Filename `.vN` is a major-line mirror only.
- Parser/validator authority must not come from filename when `schema_version` exists.
- Additive optional fields are normally backward-compatible only if existing requiredness, type, meaning, default behavior, and allowed-value semantics are unchanged.
- Requiredness, type, semantic meaning, default behavior, and wire-visible identifier changes are breaking.
- Deprecation must precede removal.
- Retired identifiers must not be reused.
- SemVer-aligned PATCH/MINOR/MAJOR language is currently governance language only.

## Decision Board Summary
Candidate working defaults are not accepted decisions; they are starting points for later human/head selection.

| Edge case | Risk if unresolved | Candidate working default | Immediate action boundary | Reason |
|---|---|---|---|---|
| Format-dialect version field | Contract version may be confused with codec or schema-language version. | Reserve the concept; keep dialect/codec version separate from contract version. | No canonical field creation. | Field naming and location are not settled. |
| Enum addition and unknown values | New enum values may break closed consumers. | Treat as guarded MINOR only when unknown-value tolerance is declared. | Decision board only; no schema change. | Consumer tolerance policy must be explicit first. |
| Reservation registry location | Retired identifiers may be forgotten or duplicated. | Keep non-reuse rule; design registry later. | No registry creation. | Ownership and schema are not clear. |
| YAML compatibility diff | Raw YAML changes may create false positives or miss semantic breaks. | Defer; future diff should compare normalized contract shape and meaning. | No validator or CI. | Tooling design is future work. |
| Full SemVer adoption | Partial adoption may imply rules not yet accepted. | Keep SemVer-aligned language only. | No migration. | Migration and edge cases remain unresolved. |

## Edge Case 1 — Format-Dialect Version Field
Contract version and format/codec/dialect version must not be collapsed.

The contract version answers: what public machine contract does this artifact implement?

The format, codec, or dialect version answers: how should tooling parse or interpret the artifact representation?

Candidate names:
- `format_version`
- `codec_version`
- `serialization_version`

Candidate locations:
- top-level artifact field
- codec metadata block
- registry-side metadata

Risk of adding this too early:
- it may become a second version authority
- it may duplicate `schema_version`
- it may force every artifact into a field before codec variation exists
- it may trigger unnecessary migrations

Candidate default:
Defer field creation. Reserve the concept and require future proposals to keep dialect/codec version separate from contract version.

Do now:
No canonical field creation.

Open questions:
- Should codec metadata live in every artifact or only in registries?
- Is YAML-as-default-codec enough for v0 without a dedicated field?
- Which name avoids confusion with `schema_version`?

## Edge Case 2 — Enum Addition and Unknown Values
Enum additions may be backward-compatible only for unknown-tolerant consumers.

Closed enum consumers may treat new values as breaking.

Need an explicit unknown-value handling signal before classifying all enum additions as MINOR.

Candidate default:
Treat enum additions as guarded MINOR only when the schema or consuming contract declares unknown-value tolerance; otherwise review as potentially breaking.

Do now:
Decision board only; no schema change.

Risk:
- treating all enum additions as MINOR can break strict consumers
- treating all enum additions as MAJOR can block useful extension
- implicit tolerance creates reviewer-memory dependency

Open questions:
- Where should unknown-value tolerance be declared?
- Should tolerance be per field, per enum, or per artifact?
- What should consumers do with unknown values: reject, preserve, ignore, or route to review?

## Edge Case 3 — Reservation Registry Location
Retired identifiers must not be reused.

A reservation registry may eventually be needed for:
- field names
- explicit IDs
- enum values
- packet family names
- registry keys

Possible locations:
- `02_packets/`
- `03_memory/registry/`
- `07_working/drafts/` until formalized

Risk of creating a registry before ownership and schema are clear:
- another truth surface appears too early
- registry semantics may conflict with file-status registry semantics
- reservation scope may be too narrow or too broad
- future migrations may be needed immediately

Candidate default:
Do not create the registry yet. Keep non-reuse rule in packet governance and track reservation-registry design as future implementation/governance work.

Do now:
No registry creation.

Open questions:
- Is reservation ownership packet-specific or cross-contract?
- Should reservations include reason, removal version, and successor?
- Should registry location be canonical or working-only first?

## Edge Case 4 — YAML Compatibility Diff
Raw YAML diffs are not stable enough for contract compatibility.

Formatting, key order, comments, and quoting can create false positives.

Compatibility diff should compare normalized contract shape and meaning, not raw text.

Validator/CI implementation is future work.

Candidate default:
Defer implementation. Future compatibility diff should use normalized semantic extraction before deciding PATCH/MINOR/MAJOR impact.

Do now:
No validator or CI.

Risk:
- raw diffs may over-report harmless changes
- raw diffs may under-report semantic changes hidden in comments or allowed values
- automated checks may harden before the contract model is settled

Open questions:
- What normalized representation should be compared?
- Which fields are contract shape versus annotation?
- How should comments and examples affect compatibility classification?

## Edge Case 5 — Full SemVer Adoption
Current governance uses SemVer-aligned PATCH/MINOR/MAJOR language.

Full SemVer adoption would require rules for:
- prerelease
- build metadata
- v-prefix handling
- `0.y.z` stability posture

Existing packet YAML may still use `schema_version: v0`, so full adoption needs migration policy.

Do not force migration in this decision board.

Candidate default:
Do not adopt full SemVer yet. Use SemVer-aligned language for governance while keeping migration and edge cases unresolved.

Do now:
No migration.

Risk:
- premature full adoption may force churn across packet and registry artifacts
- partial implementation may mislead validators
- `v0` filename mirrors and `schema_version` values may be conflated

Open questions:
- Should `schema_version: v0` be migrated, tolerated, or deprecated later?
- Does shadowMAS need prerelease/build metadata at all?
- How should major-line filename mirrors interact with full SemVer values?

## Recommended Next Decision Order
1. Enum unknown-value tolerance policy.
2. Reservation registry ownership/location.
3. Format/codec/dialect version concept and field naming.
4. YAML semantic diff design.
5. Full SemVer adoption or non-adoption.

## Do Not Implement Yet
- Do not add `format_version`, `codec_version`, or `serialization_version` fields.
- Do not create a reservation registry.
- Do not implement YAML diff tooling.
- Do not implement CI.
- Do not migrate `schema_version` values.
- Do not change packet schema required fields.
- Do not promote this decision board into canonical truth.

Validator and CI implementation-prep is tracked separately in `07_working/drafts/CONTRACT-VERSIONING-VALIDATOR-CI-PREP.v0.en.md`; that prep note must not resolve these edge cases by implication.

## Open Questions
- Which edge cases must be resolved before any validator design begins?
- Should unknown-value tolerance be the first formal addendum to packet governance?
- Can reservation tracking start as a working draft without creating a new truth surface?
- What is the smallest semantic model needed for YAML compatibility checks?
- Is full SemVer valuable enough for v0, or should shadowMAS keep SemVer-aligned governance language only?

## Promotion Requirements
Before any part of this board is promoted:
- human/head selection must choose, reject, or revise a candidate working default for each promoted edge case
- impacted packet and registry owner files must be identified
- Change Impact Map review must be completed
- migration impact must be checked against existing packet YAML
- validator/CI work must remain separate from governance selection
