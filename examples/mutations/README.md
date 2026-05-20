# examples/mutations/README | mutation-fixture explanation for the L1 minimal validator
# related: [shadowmas_minimal_validator, demo_signal_governance, l1_mutation_coverage_report, test_shadowmas_minimal_validator]
# phase: l1_fixture_documentation

# Mutation Fixtures

## Purpose

These JSON fixtures exercise each authority-boundary invariant in `tools/shadowmas_minimal_validator.py` individually. Each fixture flips exactly one field so that exactly one invariant should FAIL while every other invariant continues to PASS.

This lets `tests/test_shadowmas_minimal_validator.py` confirm that each invariant fires only against its own target field and does not over-trigger.

## Mirror-pair convention

For each target invariant there are two fixture variants in mirrored filenames, one under each subdirectory:

| Subdirectory | What the flipped field looks like |
|---|---|
| `single_flag/` | A clearly wrong value the invariant rejects outright (for example, an enum value outside the allowed set). |
| `partial_compliance/` | A value that looks structurally right but is still rejected by exact comparison (for example, wrong casing, wrong type, wrong literal form). |

Both variants should produce the same PASS/FAIL pattern: the target invariant fails, every other invariant passes. The two together verify that each invariant rejects both blatant and near-miss wrong values.

## Filename convention

```
{single_flag,partial_compliance}/<invariant_short_name>.json
```

The short name corresponds to a named invariant in the validator. See the validator source for the canonical list and `07_working/drafts/rationale/l1_mutation_coverage_report.md` for the per-invariant coverage report.

## Positive baseline

The matching positive fixtures live one level up:

- `examples/demo_signal_governance.json` — full-PASS fixture.
- `examples/demo_signal_governance_violation.json` — coarse-grained negative fixture used by the README demo.

The mutations under this folder are the fine-grained per-invariant negatives.

## Boundary

These fixtures are non-canonical illustrative examples. They are not truth files, not packet schemas, and not safety evidence. They are L1 fixture-level coverage only.
