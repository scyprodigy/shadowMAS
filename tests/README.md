# tests/README | overview of what each test file in tests/ covers
# related: [test_shadowmas_minimal_validator, test_l2_trace_fixtures, test_inspect_l2_fixture, test_candidate_registry_validator, test_validator_drift, test_workspace_helper]
# phase: tool_doc

# tests — test plan and coverage overview

## Purpose
Quick reference of what each test file in `tests/` covers, so a
reader can find the right test file without reading every one of
them. The test source remains the authoritative description of
behavior; this README points at the source.

## Files

### tests/test_shadowmas_minimal_validator.py
Three test classes:

- **`ShadowmasMinimalValidatorTests`** — L1 governance demo
  validator behavior on the positive fixture, the coarse-grained
  negative fixture, a non-object JSON root, and a missing-file
  path.

- **`L1MutationCorpusTests`** — confirms the 30-fixture L1
  mutation corpus (15 `single_flag/` + 15 `partial_compliance/`)
  exercises every validator invariant exactly once, and verifies
  the coverage report
  (`07_working/drafts/rationale/l1_mutation_coverage_report.md`)
  exists with the expected counts.

- **`ShadowmasPacketValidatorTests`** — packet validator
  behavior on fixture variants. Coverage groups:
  - `review_packet` `recommendation` enum (positive + negative)
  - `review_packet` `promotion_snapshot` field shape (positive
    plus rejection on `memory_packet`)
  - `review_packet` `reviewers_required` and `consensus_kind`
    (R6)
  - shared invariants enforced by the validator (R10):
    `supervision_mode` enum, `risk` enum, RFC3339 `created_at`
    with Z suffix, non-empty `packet_uid`
  - `memory_packet` `promotion_candidate` YAML 1.1 boolean trap
    regression (R11): quoted `"yes"` passes; unquoted `yes` / `no`
    are rejected with `INVALID_PROMOTION_CANDIDATE`
  - valid `memory_packet` fixture (R14): full validator passes
    end-to-end

### tests/test_l2_trace_fixtures.py
- L2 inspector `REQUIRED_TOP_KEYS` sentinel synced with the test
  file's `REQUIRED_KEYS` set.
- The L2 fixture index lists exactly three handoff fixtures, each
  reachable on disk.
- Every fixture carries the required top keys, `level: L2`, at
  least two trace steps, `expected_boundary_violation` with an
  `unsafe_transition` block.
- `authority_layers_involved` matches the
  `trace_steps[].authority_layer` set.
- `unsafe_transition` carries exactly `source_layer`, `target_layer`,
  `relation`; `relation` is `unsafe_promotion`; source != target.

### tests/test_inspect_l2_fixture.py
- L2 inspector CLI behavior end-to-end via subprocess. Covers
  exit codes (0 pass, 1 fail) and the JSON report envelope shape.
- Detects: malformed fixture missing a key, invalid JSON input,
  missing file path, no argv, wrong relation, same source and
  target layer, non-object JSON root, accumulated violations.

### tests/test_candidate_registry_validator.py
- The currently-tracked `CANDIDATE-REGISTRY` passes the shape
  check (every candidate carries every required field).
- A synthetic candidate entry missing a required field triggers
  exit 1, and the missing field name is reported in stdout.

### tests/test_validator_drift.py
- Validator hardcoded constants and packet yaml schemas agree on
  every checked surface: `PACKET_TYPES`, `SHARED_REQUIRED`,
  per-family `FAMILY_REQUIRED`, per-family `STATUS_VALUES`,
  `SUPERVISION_MODE_VALUES`, `RISK_VALUES`,
  `REVIEW_RECOMMENDATION_VALUES`, `PROMOTION_CANDIDATE_VALUES`.

### tests/test_workspace_helper.py
- Workspace tool `list` and `destroy` subcommands, exercised
  against a tempdir via `XDG_DATA_HOME` override so the real
  workspace root is not touched.
- Cases: list on empty root; list after init shows the workspace;
  destroy without `--yes` is a dry-run (exit 1, workspace
  preserved); destroy with `--yes` removes the workspace; destroy
  on a missing workspace is idempotent (exit 0).

## Running
- All tests: `python3 -m unittest discover tests`
- One file: `python3 -m unittest discover -p test_<name>.py tests`
- Verbose: add `-v`

## Relationship to verification floor
The verification floor in
`07_working/drafts/rationale/negative_audit_cycle_routine.md`
includes `python3 -m unittest discover tests` as one of the checks
that must stay green during an audit cycle. Adding a new test class
or test method should not remove existing coverage; existing
coverage is removed only via the explicit deprecation procedure in
`01_truth/SHADOWMAS-SCHEMA-VERSION-MIGRATION.v0.en.md`.

## Out of scope
This file does not:
- enumerate every individual test method (use `grep '^    def test_' tests/*.py`)
- replace the test source as authority
- specify CI invocation order (see `.github/workflows/checks.yml`)
- enforce coverage thresholds (no coverage tooling is adopted in v0)
