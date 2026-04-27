# FAST-REVIEW-CONTRACT-VERSIONING-GOVERNANCE.v0.en.md

## Status
Draft.

This file is a working governance draft for shadowMAS machine-first contract versioning.
It is not yet canonical truth.
It is intentionally retained under `07_working/drafts/` as working-only governance input.

## Purpose
This draft defines the minimum version-governance model for machine-first artifacts in shadowMAS.

Its goal is to keep four things true at the same time:
- human navigation stays simple
- machine parsing stays unambiguous
- backward-compatible evolution stays normal
- breaking change handling stays explicit and reviewable

## Scope
This draft applies to machine-first contract surfaces only.

In v0, that means:
- packet schema files
- registry schema files
- compatibility validators
- CI version/compatibility checks
- deprecation / removal handling for machine-first contracts

This draft does **not** govern:
- human-facing prose versioning
- zh-TW companion document versioning
- UI copy revision strategy
- general historical notes or rationale file naming

## Problem
Version signals often drift because different layers are asked to do different jobs.

Typical version signals are:
- filename version
- directory / package version
- in-artifact version field
- format dialect version

If these signals are not separated by responsibility, systems drift into:
- parser ambiguity
- stale filenames that no longer match the actual contract
- human docs that say one version while machine artifacts say another
- compatibility rules that depend on reviewer memory instead of machine checks

## Working conclusion
shadowMAS should use a **hybrid model**:
- the in-artifact contract version is the authoritative machine version source
- filename version mirrors the major version for human navigation only
- directory-level versioning is reserved for future parallel-major coexistence only
- format dialect version, when needed, remains separate from contract version

This keeps one authoritative machine signal without giving up human readability.

## Why this model fits shadowMAS
It aligns with current shadowMAS direction:
- machine-first artifacts are expected to converge toward minimal, parseable, low-ambiguity structure
- zero-memory intake should prefer compiled intake over blind traversal
- formal English truth files stay minimal and stable while richer human-facing explanation stays outside the canonical execution layer

It also matches the current v0 operating style:
- no heavy overbuild before the need is proven
- clear separation between formal truth, working drafts, and human explanation
- hard separation between governance system and product-repo truth

## Version signal responsibilities

### 1. Filename version
Responsibility:
- human navigation
- grep/diff convenience
- visual grouping of major lines

Rule:
- filename version is a mirror only
- it must not be treated as parser authority

Interpretation:
- `.v0` means “major line 0”
- it does **not** carry minor or patch meaning
- it does **not** replace the in-file version field

### 2. Directory / package version
Responsibility:
- side-by-side coexistence of incompatible major lines
- routing or namespace separation when parallel majors are real

Rule:
- do not introduce directory-level versioning in v0 by default
- only introduce it when two incompatible majors must coexist in practice

Interpretation:
- no `/v0/` and `/v1/` tree split is required just to look organized
- directory versioning is an operational coexistence tool, not a default naming ritual

### 3. In-artifact contract version
Responsibility:
- parser / validator authority
- compatibility classification
- machine-readable change discipline

Rule:
- this is the **single authoritative contract version source**

Interpretation:
- parsers read this field, not the filename
- validators compare this field across versions
- CI enforces consistency between this field and the filename mirror

### 4. Format dialect version
Responsibility:
- tells tooling how to interpret the schema language itself
- examples include JSON Schema dialect identifiers such as `$schema`

Rule:
- keep dialect version separate from contract version

Interpretation:
- a schema language version and a public contract version are different things
- they must not be collapsed into a single field

## Authoritative source rule
For machine-first contracts, the authoritative version source is the in-artifact contract version field.

For shadowMAS v0, the practical interpretation is:
- keep `schema_version` as the current authoritative field
- formally define `schema_version` as the public contract version of that artifact
- do not reinterpret it as a prose revision marker, timestamp, or formatting revision

## Recommended v0 naming model
Use this pattern:
- filename: major mirror only
- in-file field: full contract version

Example:
- file name: `SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- in-file field: `schema_version: 0.3.0`

Meaning:
- the registry belongs to major line 0
- the exact current contract state is 0.3.0

This preserves today’s filename convention while making machine interpretation sharper.

## Non-negotiable rules

### R1. Single authoritative machine version
The in-artifact contract version field **MUST** be the sole authoritative version source for parsers and validators.

### R2. Filename major mirrors in-artifact major
If a filename contains `.vN`, then `N` **MUST** equal `major(schema_version)`.
Mismatch is an error, not a warning.

### R3. Parsers do not guess
Parsers and validators **MUST NOT** infer the authoritative version from filename or directory when the in-artifact field exists.
If the authoritative field is absent or ambiguous, processing should fail.

### R4. Additive optional expansion is the normal safe change
Within a stable major line, new fields **MAY** be added only when they are optional and preserve old behavior when absent.

### R5. Requiredness/type/meaning changes are breaking
Changing requiredness, field type, default semantics, or externally observable meaning **MUST** be treated as breaking.

### R6. Wire-visible identifier reuse is forbidden
A retired identifier **MUST NOT** be renamed in place, renumbered, or reused.
If removal occurs, the retired identifier must stay permanently reserved.

### R7. Deprecation must precede removal
A removable component **MUST** first be marked deprecated and must declare its removal window or removal condition at the time of deprecation.

### R8. CI must enforce compatibility
Every machine-first contract change **MUST** pass a mechanical compatibility check before merge.
Compatibility must not depend only on reviewer memory.

## Minimum bump policy

### PATCH
Use PATCH only for changes that do not alter contract shape or meaning.
Examples:
- typo fixes in comments
- clearer descriptions
- documentation-only clarifications
- non-semantic formatting cleanup

### MINOR
Use MINOR for backward-compatible contract growth.
Examples:
- adding an optional field
- adding a new enum value only when the consumer model explicitly allows unknown/future-safe handling
- adding metadata that old consumers can ignore safely

Conditions:
- old consumers still behave correctly
- absent new fields still preserve old behavior
- defaults do not change observable behavior

### MAJOR
Use MAJOR for breaking changes.
Examples:
- removing a field
- renaming a wire-visible identifier in a way that changes machine meaning
- changing type
- changing requiredness/cardinality
- changing default semantics
- changing stable allowed-value meaning
- removing deprecated components after the deprecation window

## Optional field expansion rule
Optional expansion is allowed only when all of the following are true:
- older readers can ignore the new field safely
- new readers still behave correctly when the field is missing
- no hidden new requirement is introduced
- no old default behavior is silently changed

If any of these fail, the change is breaking.

## Breaking change handling rule
If a wire-visible identifier or public machine meaning must change:
1. add the new field / identifier alongside the old one
2. keep a coexistence window
3. mark the old component deprecated
4. migrate producers/consumers
5. remove only in the next major window or other explicitly governed breaking window
6. permanently reserve the retired identifier

The safe pattern is migrate-by-addition, not mutate-in-place.

## Deprecation rule
Deprecation is not removal.

Minimum governance:
- deprecation must be explicit in the artifact or adjacent machine-readable metadata
- the deprecation notice should include either a removal version, removal window, or removal condition
- deprecated components remain valid until the declared removal point
- removal before that point is governance failure

## Multi-version coexistence rule
shadowMAS v0 does not need directory-level multi-major coexistence by default.

However, if future packet or registry families need to support two incompatible majors in parallel, then the system should coordinate:
- parser dispatch by in-artifact major
- validator checks against the supported compatibility floor
- index/registry entries that record active major, deprecated major, and successor line
- human docs that clearly label supported vs deprecated lines

## Parser / validator / docs / index coordination

### Parser
Reads the in-artifact authoritative version field.
Uses that field to select the contract interpretation path.

### Validator
Checks:
- syntax validity
- version-field presence
- filename-major and in-artifact-major consistency
- compatibility against the prior canonical version
- reserved identifier protection
- deprecation/removal governance requirements

### Docs
Do not become a second source of version truth.
Docs should derive visible version information from the machine-readable contract metadata.

### Index / registry
May summarize:
- contract family
- current version
- current major line
- deprecated components
- successor line

But the index is summary state, not the parser’s authority source.

## Drift risks when multiple signals coexist
If multiple version signals exist without hard responsibility separation, expect:
- filename drift: `.v0` file contains `schema_version: 1.x.y`
- documentation drift: human docs reference a version line no longer true in machine artifacts
- parser drift: fallback logic starts reading path names as truth
- validator drift: reviewers assume safety because the filename did not change
- maintenance drift: teams begin updating one signal and forgetting the others

This is why filename and directory should be mirrors, not authorities.

## CI enforcement minimum
The minimum CI gate for machine-first contracts should reject merge when any of the following is true:
- missing authoritative version field
- filename major does not match in-artifact major
- deprecated component lacks removal window/condition
- retired identifier is reused
- compatibility check fails against prior canonical version
- breaking change is introduced without the required version bump

## What v0 should do now
- keep current filename `.v0` pattern
- keep `schema_version` as the authoritative in-artifact contract version field
- explicitly document that `.v0` mirrors major only
- add CI checks for filename/in-file major consistency
- add compatibility validation for packet schema and registry schema changes
- add deprecation/removal discipline before future contract churn appears

## What v0 should reserve for later
- directory-level version trees
- full registry service for version resolution
- transformation pipelines for long-tail compatibility downgrade
- public minor/patch exposure beyond what consumers truly need

These should be earned by actual multi-version pressure, not introduced speculatively.

## What v0 should avoid
- collapsing schema-language version and contract version
- creating duplicate truth files for every minor/patch revision
- hand-maintaining multiple version sources with no automated checks
- treating reviewer intuition as the primary compatibility gate
- overbuilding a protocol platform before packet/registry governance is stable

## Proposed landing path
Recommended path inside shadowMAS:
- keep this file under `07_working/drafts/` first
- use it as the source draft for future CI/version-governance implementation work
- only promote distilled stable rules into canonical truth after one review pass and one implementation-oriented pass

Suggested filename:
- `07_working/drafts/FAST-REVIEW-CONTRACT-VERSIONING-GOVERNANCE.v0.en.md`

## References
Primary and near-primary references that informed this draft:

- Semantic Versioning 2.0.0 — <https://semver.org/>
- Google AIP-180 Backwards Compatibility — <https://google.aip.dev/180>
- Google AIP-181 Stability Levels — <https://google.aip.dev/181>
- Google AIP-185 API Versioning — <https://google.aip.dev/185>
- JSON Schema: Dialect and vocabulary declaration — <https://json-schema.org/understanding-json-schema/reference/schema>
- JSON Schema: Structuring and `$id` — <https://json-schema.org/understanding-json-schema/structuring>
- Protocol Buffers Language Guide (proto2/proto3/editions) — <https://protobuf.dev/programming-guides/proto2/> / <https://protobuf.dev/programming-guides/proto3/> / <https://protobuf.dev/programming-guides/editions/>
- Protocol Buffers Overview — <https://protobuf.dev/overview/>
- Confluent Schema Evolution and Compatibility — <https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html>
- FlatBuffers Evolution — <https://flatbuffers.dev/evolution/>
- Cap’n Proto Schema Language — <https://capnproto.org/language.html>
- RFC 9745 Deprecation Header — <https://www.rfc-editor.org/rfc/rfc9745.html>
- RFC 8594 Sunset Header — <https://www.rfc-editor.org/info/rfc8594>

Supporting memo:
- no separate supporting memo is required for retaining this draft in `07_working/drafts/`
