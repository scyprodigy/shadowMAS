> status: working draft / decision board
> authority: none
> source lane: contract-versioning edge-case decisions
> do not promote without governance review

# FAST-REVIEW-CONTRACT-VERSIONING-EDGE-CASES.v0

## Purpose
Decision board for unresolved contract-versioning edge cases.

This document is a bounded working draft. It is not canonical truth, not packet schema law, not validator implementation, and not CI implementation.

It exists to make the remaining choices inspectable before later human/head selection.

## Scope
- unresolved packet/registry contract-versioning edge cases
- candidate working defaults for later review
- source-supported reasoning from external contract-versioning research
- do-now / do-later boundaries

## Non-Scope
- no edits to canonical packet schemas
- no edits to canonical registry schema
- no validator or CI implementation
- no reservation registry creation
- no `format_version`, `codec_version`, or `serialization_version` fields
- no `schema_version` migration
- no full SemVer adoption

## Current Stable Rule Candidates
- `schema_version` remains the current authoritative in-artifact machine version field unless later changed by formal governance.
- Filename `.vN` is a major-line mirror / human navigation aid only.
- Parsers and validators must not infer authoritative contract version from filename when an in-artifact version exists.
- Additive optional expansion is the normal safe change.
- Requiredness, type, meaning, default behavior, or narrowing allowed values are breaking.
- Deprecation must precede removal.
- Retired identifiers must never be reused.
- Compatibility should eventually be mechanically checked, but no check is implemented here.

## Decision Board Summary
Candidate working defaults are not accepted decisions; they are starting points for later human/head selection.

| Edge case | Risk if unresolved | Candidate working default | Immediate action boundary | Reason |
|---|---|---|---|---|
| Enum unknown-value tolerance | New enum values may break closed consumers. | Treat enum additions as guarded MINOR only when unknown-value tolerance is declared. | Decision board only; no schema change. | Consumer tolerance policy must be explicit first. |
| Reservation registry ownership / location | Retired identifiers may be forgotten or reused. | Keep the non-reuse rule; design registry ownership/location later. | No registry creation. | Scope and owner are not clear enough. |
| Format / codec / dialect version field | Contract version may be confused with representation version. | Reserve the concept; keep dialect/codec version separate from contract version. | No canonical field creation. | Field name and location are unsettled. |
| YAML semantic compatibility diff | Raw text diffs may miss semantic breaks or over-report formatting changes. | Future checks should compare normalized contract shape and meaning. | No validator or CI. | Normalized representation is not designed. |
| Full SemVer adoption or non-adoption | Partial adoption may imply rules not yet accepted. | Keep SemVer-aligned PATCH/MINOR/MAJOR language only. | No migration. | Migration and edge cases remain unresolved. |

## Enum unknown-value tolerance
Problem statement:
Adding an enum value is not automatically safe. It is backward-compatible only when consumers are designed to tolerate unknown values.

Why it matters:
Closed consumers may reject, crash, misroute, or silently mis-handle a new value. Treating all enum additions as MINOR would hide that risk.

Candidate default:
Treat enum additions as guarded MINOR only when the schema or consuming contract declares unknown-value tolerance; otherwise review the change as potentially breaking.

Risks:
- over-classifying enum additions as MINOR breaks strict consumers
- over-classifying all enum additions as MAJOR blocks useful extension
- relying on reviewer memory makes compatibility inconsistent

Decision still needed:
Decide where unknown-value tolerance is declared and what consumers must do with unknown values.

Source basis from the external research:
- Protobuf preserves unknown fields, while newer JSON Schema practice can move toward stricter rejection.
- FlatBuffers treats union-variant evolution carefully: appending can be safe, but positional insertion without explicit discriminant is breaking.
- GraphQL supports additive evolution but uses explicit deprecation for retiring fields and enum values.

## Reservation registry ownership / location
What identifiers may need permanent reservation:
- field names
- explicit IDs
- positional IDs
- enum values
- type or schema IDs
- packet family names
- registry keys

Candidate locations:
- packet layer, for packet-specific contract identifiers
- memory registry, for registry-owned keys and status surfaces
- separate registry, if reservation scope crosses packet and registry families
- `07_working/drafts/` only as temporary design support until formalized

Why retired identifiers must not be reused:
Reuse is the main silent-corruption failure mode. Older producers or consumers may interpret a reused identifier as the old meaning while newer artifacts intend the new meaning.

Candidate default:
Do not create the registry yet. Keep the non-reuse rule in packet governance and track reservation-registry design as future governance/implementation work.

Risks:
- creating a registry too early creates another truth surface
- placing it in the wrong layer confuses ownership
- delaying too long weakens retired-identifier enforcement

Decision still needed:
Choose reservation ownership, location, schema shape, and whether reservation applies per contract family or across all machine-first contract surfaces.

Source basis from the external research:
- Protobuf reserves retired field numbers and names to prevent reuse.
- FlatBuffers warns that changing explicit IDs or positions causes old code to read the wrong bytes.
- Cap'n Proto uses stable type IDs and compatibility loading to avoid rename/reuse ambiguity.

## Format / codec / dialect version field
Distinction:
The contract version answers which public machine contract an artifact implements.

The format, codec, or dialect version answers how tooling should parse or interpret the artifact representation.

Why these must not collapse into one field:
A contract can be serialized through more than one codec, and a codec or schema dialect can change without changing the public contract. Collapsing both into `schema_version` would make parser behavior and contract compatibility ambiguous.

Candidate field naming options:
- `format_version`
- `codec_version`
- `serialization_version`

Candidate locations:
- top-level artifact field
- codec metadata block
- registry-side metadata

Candidate default:
Defer field creation. Reserve the concept and require future proposals to keep dialect/codec version separate from contract version.

Risks:
- adding the field too early creates churn before codec variation exists
- choosing the wrong location creates a second authority path
- naming may collide conceptually with `schema_version`

Decision still needed:
Decide field name, location, and whether v0 needs an explicit field at all while YAML remains the default codec.

Source basis from the external research:
- JSON Schema separates dialect declaration from public contract meaning.
- The external research's hybrid model separates filename hints, directory/package coexistence, and in-file/in-wire authority.
- Stripe shows that URL/path version can remain a stable outward route while real version behavior lives elsewhere.

## YAML semantic compatibility diff
Why text diff is insufficient:
Raw YAML diffs are affected by formatting, key order, comments, quoting, and examples. They can create false positives while missing semantic changes in requiredness, defaults, meanings, or allowed values.

What semantic changes should count as breaking:
- requiredness changes
- type changes
- meaning changes
- default behavior changes
- narrowing allowed values
- wire-visible identifier rename or reuse
- removal without prior deprecation

Candidate future check categories:
- version presence and parse checks
- filename major / `schema_version` major alignment checks
- requiredness and type comparison
- default behavior review flags
- semantic meaning review flags
- identifier rename/reuse checks
- deprecation-before-removal checks
- packet surface / registry alignment checks

Candidate default:
Defer implementation. Future compatibility diff should compare normalized semantic contract shape before classifying PATCH/MINOR/MAJOR impact.

Risks:
- raw text diffs may harden accidental formatting into governance
- semantic checks may overreach before field meanings are modeled
- implementation may appear to settle unresolved edge cases

Decision still needed:
Design the normalized contract representation and decide which fields are contract shape, annotations, examples, or comments.

No validator is implemented in this task.

Source basis from the external research:
- FlatBuffers `flatc --conform`, Cap'n Proto SchemaLoader, Confluent compatibility checks, and GraphQL schema-diff tools show compatibility can be mechanically checked.
- The research also warns that the useful pattern is mechanical compatibility against contract semantics, not prose-only policy.

## Full SemVer adoption or non-adoption
What is already useful:
PATCH/MINOR/MAJOR language is useful governance vocabulary:
- PATCH: no contract shape or meaning change
- MINOR: backward-compatible growth
- MAJOR: breaking change

What is not yet adopted:
Full SemVer is not formal policy. Prerelease, build metadata, v-prefix handling, `0.y.z` stability posture, and migration from existing `schema_version: v0` remain unresolved.

High-level model comparison:
- SemVer: clear PATCH/MINOR/MAJOR contract language, but full adoption requires migration and edge-case rules.
- Major-only: simple human navigation and stable filenames, but hides minor/patch contract state unless another field carries it.
- CalVer/date-based: useful for release cadence and long-lived external APIs, but does not by itself classify compatibility.
- Additive/deprecation-first: minimizes breaking changes and aligns with GraphQL-style continuous evolution, but still needs an answer for unavoidable breaking changes.

Candidate default:
Do not adopt full SemVer yet. Use SemVer-aligned governance language while keeping migration and edge cases unresolved.

Risks:
- premature full adoption forces churn across existing packet and registry YAML
- partial adoption may mislead future validators
- major-line filename mirrors may be confused with authoritative contract versions

Decision still needed:
Choose whether shadowMAS will formally adopt SemVer, remain major-line plus in-artifact version, allow CalVer/date-based schemes, or prefer additive/deprecation-first governance without full SemVer.

Source basis from the external research:
- SemVer offers explicit PATCH/MINOR/MAJOR semantics.
- Google AIP-style major handling and Stripe's date/named-major model show viable alternatives.
- GraphQL shows a version-refusing, additive/deprecation-first model that works for some domains but cannot express every breaking change.

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
- Should unknown-value tolerance be declared per field, per enum, per artifact, or per consumer contract?
- Which layer owns a retired-identifier reservation registry?
- Does v0 need a codec/dialect field while YAML remains the default codec?
- What is the smallest normalized semantic model needed for YAML compatibility checks?
- Is full SemVer valuable enough for v0, or should shadowMAS keep SemVer-aligned governance language only?

## Promotion Requirements
Before any part of this board is promoted:
- human/head selection must choose, reject, or revise a candidate working default for each promoted edge case
- impacted packet and registry owner files must be identified
- Change Impact Map review must be completed
- migration impact must be checked against existing packet YAML
- validator/CI work must remain separate from governance selection
