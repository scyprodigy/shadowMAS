# SHADOWMAS-SCHEMA-VERSION-MIGRATION.v0.en.md

## Purpose
This file describes how shadowMAS evolves machine-stable contracts
(packet schemas, registry entries, validator constants) across version
boundaries without silently breaking existing tools, fixtures, and
downstream consumers.

It is the canonical migration policy. It does not replace
`02_packets/PACKET-FIELD-DICTIONARY.v0.en.md` for field-level semantics;
it adds the temporal dimension.

## Scope
This policy governs:
- packet schema files under `02_packets/`
- packet validator constants in `05_scripts/validate/shadowmas_validate.py`
- registry schemas under `03_memory/registry/`
- runtime baseline files under `04_runtime/`

It does not govern:
- narrative truth documents under `01_truth/` (those use filename `.vN`
  for human navigation but are not parsed by the validator)
- human-facing companion documents under `06_human_docs/`
- working drafts under `07_working/`

## Current State Snapshot
- Every machine-stable contract file is at `.v0` major.
- The packet validator hardcodes `schema_version == "v0"` as the only
  accepted in-artifact value.
- Filename `.vN` and in-artifact `schema_version` are required to align
  at the major level.
- `SemVer`-style `MAJOR.MINOR.PATCH` literals (for example `"0.0.0"`)
  are reserved for a future packet line and are not accepted by current
  validators.

## Change Classification

### Backward-compatible additive changes (no version bump required)
These may ship within the current `.v0` line:
- adding an optional field with a sensible default
- adding a new value to an enum, when validators are extended in the
  same change set
- adding a new optional shared field in `packet_common_shell.v0.yaml`
- adding a new advisory tool that reads existing artifacts
- adding a new test that exercises an existing invariant

A drift checker (`tools/check_validator_drift.py`) must pass after the
change so the validator and schema agree.

### Backward-incompatible changes (require `.v1` migration)
- removing a required field
- changing the type of an existing field
- changing the meaning of an existing field
- removing a value from an enum where existing artifacts use it
- removing a packet family
- renaming a field used in tracked artifacts

### Visible-identifier changes (require deprecation cycle)
- field rename that affects parser surface
- packet-family rename
- enum value rename

Deprecation cycle:
1. Add the new identifier alongside the old one.
2. Mark the old identifier deprecated in the dictionary and validator.
3. Wait at least one full release window for downstream artifacts to
   migrate.
4. Remove the old identifier.
5. The retired identifier must not be reused for a different concept
   (per `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md` §11).

## Version Bump Procedure
When a backward-incompatible change is needed:

1. Open a candidate registry entry naming the proposed `.v1` change set.
2. Land the `.v1` schema files alongside the `.v0` files; do not
   overwrite the `.v0` set.
3. Extend the validator with a `.v1` code path; do not remove the
   `.v0` code path. The validator must accept both lines for one full
   deprecation window.
4. Add a `.v1` valid fixture per packet family under
   `examples/packets/`. Keep the `.v0` fixtures.
5. Update `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
   to track the new files; do not mark the `.v0` files as superseded
   until step 7.
6. Run the full verification floor (packet validators, drift checker,
   registry checker, pollution scanner, unit tests) against both
   lines.
7. After the deprecation window, retire the `.v0` line: mark its
   tracked entries as `superseded`, remove the validator's `.v0` code
   path, and update CI to validate only the `.v1` line.

## Validator Multi-Version Support
The validator should expose distinct code paths per accepted major
schema_version line, not branch on a single accepted value. Sketch:

- `SCHEMA_V0_SHARED_REQUIRED`, `SCHEMA_V1_SHARED_REQUIRED`
- `validate_packet_v0(...)`, `validate_packet_v1(...)`
- `validate_packet(...)` dispatches by reading `schema_version` and
  routing to the matching code path.

Reusing the same constants for both lines is forbidden because it
silently couples the two versions.

## Filename and In-Artifact Version
- Filename `.vN` is a major-line mirror for human navigation, grep,
  and diff convenience only.
- The in-artifact `schema_version` field is the parser authority.
- Mismatch between filename major and `schema_version` major is a
  validator error (`SCHEMA_FILENAME_MAJOR_MISMATCH`).
- This relationship is unchanged across version migrations.

## Compatibility Tests
Each `.vN` line must keep these in CI:
- a positive fixture per packet family that the `.vN` validator
  accepts
- a negative fixture per family-specific invariant that the `.vN`
  validator rejects
- the drift checker, scoped per `.vN` line if the schemas diverge
- the registry checker

A migration that breaks these tests cannot ship.

## Rollback
If a `.vN+1` line is shipped and a serious defect is found before the
deprecation window closes:
- the `.vN` line is still valid (we did not remove it)
- mark the `.vN+1` files as `rejected` in FILE-STATUS-REGISTRY
- remove the `.vN+1` validator code path
- record the rollback in a candidate registry entry
- write a rationale doc explaining what went wrong

Rollback after the deprecation window closes is harder; treat it as a
new migration cycle.

## Relationship to CHANGE-IMPACT-MAP
- Any schema-version migration is at minimum a packet-field change
  per `01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md` §4.
- A major-line bump is also a governance identity change per §1.
- Self-modification of this migration policy itself follows §17.

## Still Open
- exact length of the deprecation window (sessions / commits / time)
- exact CI machinery for running two validator lines side by side
- exact rollback registry format
- whether the validator file should be split per major line or kept
  monolithic with per-line constants and dispatch
