# l1_mutation_coverage_report | fixture-level mutation coverage for authority-boundary invariants
# related: [shadowmas_minimal_validator, demo_signal_governance, demo_signal_governance_violation, AGENTS]
# phase: l1_fixture_evidence

# L1 Mutation Coverage Report

## 1. Status

- Working evidence artifact.
- Public-safe; no private, outreach, or funder content.
- Fixture-level only.
- Not runtime safety evidence.
- Not construct validity evidence.
- Not predictive validity evidence.
- Held under `07_working/drafts/rationale/`; non-canonical working draft.

## 2. Scope

- Validator: `tools/shadowmas_minimal_validator.py` (15 named authority-boundary invariants).
- Positive baseline fixture: `examples/demo_signal_governance.json`.
- Single-flag mutation corpus: `examples/mutations/single_flag/*.json` (15 fixtures).
- Partial-compliance trap corpus: `examples/mutations/partial_compliance/*.json` (15 fixtures).
- Tests: `tests/test_shadowmas_minimal_validator.py`.
- Number of invariants under test: 15.
- Total mutation fixtures: 30.

## 3. Method

### Per-invariant short filename mapping

Filenames use lowercase snake_case with 2–4 segments (consistent with the path-sensitive filename policy memo). The mapping below also serves the tests, where it is reproduced verbatim.

| short filename | full invariant name |
|---|---|
| `truth_status` | `runtime_signal_truth_status_runtime_only` |
| `truth_promotion` | `runtime_signal_cannot_promote_truth_directly` |
| `memory_write` | `runtime_signal_cannot_write_memory_directly` |
| `review_required` | `runtime_signal_requires_human_review_for_promotion` |
| `layer_promotion` | `no_t4_t5_to_t2_t3_direct_promotion` |
| `silent_memory_write` | `no_silent_memory_write` |
| `audit_read_only` | `audit_projection_is_read_only` |
| `audit_approval` | `audit_projection_has_no_approval_authority` |
| `audit_truth` | `audit_projection_has_no_truth_authority` |
| `action_advisory` | `recommended_action_is_advisory_only` |
| `action_runtime_auth` | `recommended_action_cannot_authorize_runtime_action` |
| `action_packet_auth` | `recommended_action_cannot_authorize_packet_change` |
| `action_truth_promotion` | `recommended_action_cannot_promote_truth` |
| `dashboard_authority` | `dashboard_does_not_become_authority` |
| `human_authority` | `human_final_authority_preserved` |

### Single-flag mutation fixtures

Each fixture starts from the positive baseline and flips exactly one field — the field that the target invariant's predicate inspects. The expected outcome is:

- the target invariant FAILS,
- all 14 other invariants PASS,
- the validator exits non-zero.

This isolates each invariant for independent detectability.

### Partial-compliance trap fixtures

Each fixture starts from the positive baseline and mutates the same target field to a value that looks superficially compliant when skimmed but fails the validator's strict-equality / strict-identity predicate. For string-valued invariants the trap uses a case-shifted look-alike (e.g. `"Runtime_Signal_Only"` instead of `"runtime_signal_only"`). For boolean-valued invariants the trap substitutes a string literal (e.g. `"true"` instead of `True`); since the validator uses `is True` / `is False`, the string literal is not the singleton boolean and the predicate fails. The expected outcome is:

- the target invariant FAILS,
- the validator exits non-zero,
- ideally no other invariant is collaterally affected.

### Coverage calculation

```
mutation_detection_rate = caught_mutations / total_mutations
caught_mutations = (single_flag_caught) + (partial_compliance_caught)
partial_compliance_false_pass_rate = (passed_when_should_have_failed) / total_partial_compliance
```

A mutation is `caught` when the validator exits non-zero AND the failing invariant exactly matches the target.

## 4. Results

Measured on the corpus committed in this task.

| invariant_name | single_flag_fixture | single_flag_caught | partial_compliance_fixture | partial_compliance_caught |
|---|---|---|---|---|
| `runtime_signal_truth_status_runtime_only` | `single_flag/truth_status.json` | yes | `partial_compliance/truth_status.json` | yes |
| `runtime_signal_cannot_promote_truth_directly` | `single_flag/truth_promotion.json` | yes | `partial_compliance/truth_promotion.json` | yes |
| `runtime_signal_cannot_write_memory_directly` | `single_flag/memory_write.json` | yes | `partial_compliance/memory_write.json` | yes |
| `runtime_signal_requires_human_review_for_promotion` | `single_flag/review_required.json` | yes | `partial_compliance/review_required.json` | yes |
| `no_t4_t5_to_t2_t3_direct_promotion` | `single_flag/layer_promotion.json` | yes | `partial_compliance/layer_promotion.json` | yes |
| `no_silent_memory_write` | `single_flag/silent_memory_write.json` | yes | `partial_compliance/silent_memory_write.json` | yes |
| `audit_projection_is_read_only` | `single_flag/audit_read_only.json` | yes | `partial_compliance/audit_read_only.json` | yes |
| `audit_projection_has_no_approval_authority` | `single_flag/audit_approval.json` | yes | `partial_compliance/audit_approval.json` | yes |
| `audit_projection_has_no_truth_authority` | `single_flag/audit_truth.json` | yes | `partial_compliance/audit_truth.json` | yes |
| `recommended_action_is_advisory_only` | `single_flag/action_advisory.json` | yes | `partial_compliance/action_advisory.json` | yes |
| `recommended_action_cannot_authorize_runtime_action` | `single_flag/action_runtime_auth.json` | yes | `partial_compliance/action_runtime_auth.json` | yes |
| `recommended_action_cannot_authorize_packet_change` | `single_flag/action_packet_auth.json` | yes | `partial_compliance/action_packet_auth.json` | yes |
| `recommended_action_cannot_promote_truth` | `single_flag/action_truth_promotion.json` | yes | `partial_compliance/action_truth_promotion.json` | yes |
| `dashboard_does_not_become_authority` | `single_flag/dashboard_authority.json` | yes | `partial_compliance/dashboard_authority.json` | yes |
| `human_final_authority_preserved` | `single_flag/human_authority.json` | yes | `partial_compliance/human_authority.json` | yes |

### Summary metrics

```
mutation_detection_rate            = 30/30
partial_compliance_false_pass_rate = 0/15
single_flag_independence           = 15/15  (each fixture isolates exactly one invariant; the other 14 still PASS)
```

No predicate coupling was observed. Every fixture isolates exactly one invariant.

## 5. Interpretation

What this supports:

- The 15 invariants are each independently detectable on hand-authored fixtures.
- The validator's predicates are strict enough that a case-shifted string and a non-boolean look-alike both fail; the validator does not silently accept near-misses.
- The corpus exercises the four canonical authority-boundary failure paths (runtime-signal → truth, runtime-signal → memory, audit-projection → approval, recommendation → action authority) plus the related layered-promotion, silent-memory, dashboard, and human-authority boundaries.

What this does not support:

- It does not prove the invariants are necessary or sufficient for any real multi-agent system.
- It does not establish construct validity for authority confusion as a measurement target.
- It does not demonstrate runtime safety, empirical human-oversight improvement, or predictive validity.
- It does not test traces, sequences, or emergent failures across multiple steps.

## 6. Limitations

- Fixtures are hand-authored by the validator author. Inter-rater reliability is not measured.
- Mutations exercise schema/fixture-level predicates only; no runtime traces, no live multi-agent runs.
- No adversarial second-rater corpus exists yet. A blind second rater could construct fixtures that look compliant to the validator but are governance-failing to a human reviewer; this would be future L3 work.
- No evidence of empirical human-oversight improvement is implied. L4 (human-reviewer pilot) is explicitly out of scope here.
- No construct validity, convergent validity, or predictive validity claim is supported by this report.
- The validator's predicate set is a minimum starter set; broader invariant taxonomies (e.g. trace-level, time-series, multi-agent coordination) remain open.

## 7. Next steps

- L2: define a trace fixture schema (`signal → projection → recommendation → review_packet → memory write attempt`) and produce a small pilot corpus with step-attribution labels.
- L3: have a second rater independently author adversarial fixtures with blind labels; report inter-rater reliability and precision/recall against shadowMAS detections.
- L4 (later, contingent on appropriate human-subjects protocol): a small reviewer pilot measuring authority-confusion error rate with vs without shadowMAS scaffolding.
- L5 (later): convergent and predictive validity against an independent operationalisation of authority confusion.
- Any update of working draft material that references this report should cite the figures `30/30` and `0/15` verbatim and link this file by path.
