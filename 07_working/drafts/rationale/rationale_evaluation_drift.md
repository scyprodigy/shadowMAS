# rationale_evaluation_drift | second-order evaluation drift rationale for shadowMAS
# related: [active_design_log, active_design_ledger, l1_mutation_coverage_report, authority_boundary_evaluation]
# phase: working_rationale

# Rationale: Second-Order Evaluation Drift

## Status

- working rationale; non-canonical; public-safe.
- extracted from historical active design log §36 (R9 — C-II + M-II Three-Layer Evaluation × Static Reward Model Structural Defect).
- does not register a candidate.
- does not modify truth, packet, memory, or runtime surfaces.
- does not modify the registry.

## Problem

Evaluation systems are usually treated as fixed external oracles: a rubric, a reward model, a reviewer, a validation harness, or a dashboard observes a system and emits a score, a label, or a decision. In repeated-optimisation settings, that assumption breaks. The evaluated system adapts to whatever the evaluator measures, and the evaluator's mapping from artifacts to scores may stop preserving the intended distinction.

In multi-agent or agent-assisted settings, the evaluator is not a neutral constant. Reviewers, metrics, prompt rubrics, judge models, retrieval rankings, and dashboard summaries can all become part of the system being optimised against. This is the second-order observation problem familiar from cybernetics: when the observer changes the observed, the observer itself must be observed.

The practical consequence is that a high-impact evaluator's score is not canonical truth. It is a time-indexed observation that can drift, become exploitable, or lose calibration as the surrounding system changes. Without an explicit drift check, an unchanged evaluator can quietly stop measuring the property it was originally designed to measure.

This is a structural concern, not a model-quality concern. It applies regardless of how well-trained any individual evaluator is.

## Construct definition

Second-order evaluation drift is the risk that an evaluation surface — a reviewer, rubric, reward model, dashboard, retrieval ranking, or validation harness — changes meaning, loses calibration, or becomes exploitable as agents, prompts, reviewers, or project artifacts optimise against it.

The construct has three observable shapes:

- **calibration decay**: the same evaluator returns the same labels on outputs whose underlying decision-relevant properties have shifted.
- **proxy exploitation**: the evaluated system learns to maximise the evaluator's signal without preserving the property the signal was a proxy for.
- **boundary erosion**: a drifted evaluator may treat weak signals as stronger evidence than intended, or may admit artifacts past an authority boundary that should have held.

Tied to authority-boundary evaluation:

- a drifted evaluator may treat weak runtime signals as stronger evidence than intended, raising the risk of unjustified promotion.
- a drifted reviewer may admit runtime artifacts into memory or truth more easily over time, eroding the promotion gate.
- a drifted metric may reward compliance-looking artifacts without preserving the actual authority boundary it was originally designed to protect.

## Why this matters for shadowMAS

shadowMAS already publishes an L1 fixture-level evaluation anchor:

- 15 named authority-boundary invariants
- 30 mutation fixtures (15 single-target + 15 partial-compliance)
- `mutation_detection_rate = 30/30`
- `partial_compliance_false_pass_rate = 0/15`
- 6 passing tests in the unittest suite
- fixture-level only; no runtime evidence

The L1 result shows that the validator distinguishes designed compliant fixtures from designed violation fixtures on hand-authored data. The L1 result does not, and cannot, show that the validator's mapping from fixture to PASS/FAIL remains valid as the fixture distribution, the invariant set, the human-rater pool, or the upstream agent population changes. That second-order question is the subject of this memo.

For shadowMAS specifically, second-order drift suggests three kinds of future evaluation discipline:

- **time-indexed evaluator versioning**: the validator and the invariant catalogue should carry an explicit version and a calibration timestamp; every fixture-level result should reference that pair.
- **drift probe fixtures**: a small set of fixtures whose expected behaviour under the validator is held constant on purpose, so any shift in their outcomes signals drift rather than novelty.
- **independent-rater check**: a separate second rater (human or model) should be exposed to the same fixtures occasionally to test whether the validator and the rater still agree on the boundary the validator claims to enforce.

None of these are claims about runtime safety, human-oversight improvement, or empirical construct validity. They are evaluation-hygiene practices that future L2 / L3 / L4 work would need to incorporate if it wishes to defend against second-order drift.

## Practical implications

- **evaluator and rubric versioning**: every evaluation surface used in decisions should carry a version identifier and a calibration timestamp; results should record both.
- **reviewer drift checks**: when the same human rater or model judge is used repeatedly, periodic drift probes should compare current calls against historically labelled reference fixtures.
- **adversarial second-rater labels**: an independent rater outside the validator-author loop should label a subset of fixtures blindly; agreement and disagreement patterns become drift signal.
- **trace fixtures that stress the evaluator, not only the agent**: future trace corpora should include cases that probe whether the evaluator's mapping survives reformulation, paraphrase, refactoring, or distribution shift.
- **false-pass tracking over time**: partial-compliance traps should be tracked across versions of the validator; an increase in false-pass rate is a drift signal.
- **separation between runtime signals and evaluation authority**: a runtime signal — including any signal produced by an evaluator — must not be treated as approval, memory, or truth without an explicit promotion path. The evaluator is one more runtime surface, not an oracle.

## Candidate status

This memo does not register a new candidate. A future candidate review could define one or more bounded primitives drawn from this rationale, for example:

- `evaluator_versioning_record`
- `reviewer_drift_monitor`
- `evaluation_commutativity_check`
- `drift_probe_fixture`
- `false_pass_trend_report`

The first three names already appear in the active design ledger as `representative_primitives` of the `evaluation_and_recalibration_surfaces` family (§0.7 of the historical log; ledger §compact_navigation_preservation). None of them is registered. Any future registration would require a separate candidate review, a change-impact pass, and human approval. Until then this is rationale only.

## Non-claims

- not runtime safety evidence.
- not empirical human-oversight evidence.
- not construct validity.
- not predictive validity.
- not a proof of evaluator robustness under optimisation pressure.
- not a replacement for independent raters or external benchmarks.
- not a runtime safeguard, agent-orchestration component, or policy instrument.
- not a guarantee that any specific drift probe will detect any specific exploitation pattern.

## Source and absorption notes

- Source section: `07_working/archive/shadowmas_cross_domain_active_design_log_v_0_1_doc_optimized_v2_2.md` §36 (R9 C-II + M-II Three-Layer Evaluation × Static Reward Model Structural Defect), lines 8,859–9,478.
- Concept anchors used in the source section (paraphrased, not quoted at length): difference-that-makes-a-difference (Bateson, second-order cybernetics tradition); observing the observer (von Foerster, second-order cybernetics); functor + natural transformation as an audit lens (category theory); reward model overoptimisation literature; Goodhart-style proxy drift comparisons. The historical log captures these as concept analogies and audit framings, not as load-bearing mathematical commitments.
- Current absorption status: not yet registered. `reviewer_drift_monitor` is named in the ledger's family index and P3 batch as a `representative_primitive` and `first_canonical_candidate`, but no candidate registry entry exists. This memo treats it as rationale only.
- Related public evidence: `07_working/drafts/rationale/l1_mutation_coverage_report.md` (30/30 fixture-level result); does not claim drift evidence.
- Mega-log remains as historical provenance at the source path. No portion of the mega-log is modified by this memo.
- This memo is `working_rationale`, non-canonical, public-safe, and held under `07_working/drafts/rationale/` per the path-sensitive filename policy memo.
