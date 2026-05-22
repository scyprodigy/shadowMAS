# SHADOWMAS Cross-Domain Active Design Log v0.1

> status: active working document — v2.2 review-feedback fixes applied  
> authority: non-canonical, but design-active  
> purpose: preserve current-session research synthesis, candidate decisions, paper insights, and shadowMAS implications in one standalone document  
> dependency rule: this document should remain understandable without opening the original papers, uploaded files, or prior chat turns  
> update policy: future rounds may append, revise, or promote sections after ToT×MoE×CoT×LATS review  

---

## TL;DR (read first, ≤60 sec)

```yaml
status: v2.2 — non-canonical active design log, P1 handoff ready
canonical_truth_changed: false
next_action: draft ONE canonical proposal packet using 0.15 skeleton
first_candidate: residual_first_report_minimum_shape
first_target_file: 02_packets/review_packet.v0.yaml
secondary_target_file: 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md
do_not:
  - reopen v4 research
  - batch-promote candidates
  - patch canonical truth from this file directly
  - treat any kernel/candidate in this file as approved truth
read_order_for_p1_drafter:
  - 0.1 (active ledger) → 0.3 (kernel index) → 0.12 (P1 plan)
  - 0.14 (handoff gate) → 0.15 (packet skeleton + filled example)
  - final v2.2 status section
```

---

## Navigation: section index

> purpose: line-anchored index so a multi-agent reader can load one section at a time instead of reading the whole ~14k-line file.
> stability: section titles are the canonical anchors; line numbers are approximate at the time this index was generated and will drift as the document grows. To regenerate, run `grep -n '^## ' <this_file>`.

| § | Approx line | Section title (use full `## N. Title` line as grep anchor) |
|---|---|---|
| TL;DR | 11 | TL;DR (read first, ≤60 sec) |
| 0 | 33 | Why this document exists |
| 1 | 1465 | Current strategic correction |
| 2 | 1497 | Working position: hot adoption, not blind adoption |
| 3 | 1535 | Key concept: KL divergence |
| 4 | 1694 | Key concept: residual-first |
| 5 | 1828 | Key concept: representation and state transfer |
| 6 | 1983 | RecursiveMAS shock integration |
| 7 | 2085 | WFGY as representation compiler candidate |
| 8 | 2177 | Paper content captured in this session |
| 9 | 2537 | v4 synthesis currently imported |
| 10 | 2647 | Candidate design decisions from current session |
| 11 | 2729 | ToT×MoE×CoT×LATS — current round snapshot |
| 12 | 2834 | Proposed shadowMAS additions for future review |
| 13 | 2921 | Current answer to the six user questions |
| 14 | 2982 | Next sequence after this document |
| 15 | 3013 | Round 2 — U-II Hierarchical Compression |
| 16 | 3681 | Document self-optimization — ToT×MoE×CoT×LATS auditable pass |
| 17 | 3831 | Round 3 — C-I Stigmergy × Quorum Sensing × Predictive Coding |
| 18 | 4451 | Document self-optimization — second pass |
| 19 | 4570 | Round 4 — M-I Pheromone Field = Externalized Free-Energy Landscape |
| 20 | 5172 | Document self-optimization — third pass |
| 21 | 5284 | Current document status after Round 4 |
| 22 | 5299 | Round 5 — Q-I Ashby's Law × Percolation Theory |
| 23 | 6088 | Document self-optimization — fourth pass |
| 24 | 6187 | Current document status after Round 5 |
| 25 | 6203 | Document self-optimization — fifth pass |
| 26 | 6400 | Current document status after v0.6 document optimization |
| 27 | 6429 | Round 6 — Q-II Information Geometry × Renormalization Group |
| 28 | 7067 | Current document status after Round 6 |
| 29 | 7095 | Round 7 — Q-III Stochastic Resonance × Weber-Fechner Law |
| 30 | 7688 | Document self-optimization — sixth pass |
| 31 | 7821 | Current document status after Round 7 |
| 32 | 7852 | Round 8 — S-I Punctuated Equilibrium × Spandrel |
| 33 | 8614 | Current document status after Round 8 |
| 34 | 8645 | Document self-optimization — seventh pass |
| 35 | 8824 | Current document status after v1.0 document optimization |
| 36 | 8859 | Round 9 — C-II + M-II Three-Layer Evaluation × Static Reward Model Structural Defect |
| 37 | 9478 | Current document status after R9 C-II/M-II content update |
| 38 | 9516 | Round 10 — D-I Spin Glass Frustration × Synergetics |
| 39 | 10104 | Current document status after R10 D-I content update |
| 40 | 10142 | Round 11 — D-II + M-III Fluctuation Theorems × Metamorphosis × Attractor Geometry |
| 41 | 10760 | Current document status after R11 D-II/M-III content update |
| 42 | 10797 | Round 12 — D-III Predictive Coding, Precision Weighting, Attention, Active Inference |
| 43 | 11487 | Current document status after R12 D-III content update |
| 44 | 11525 | Round 13 — D-IV Epigenetic Landscape |
| 45 | 12264 | Current document status after R13 D-IV content update |
| 46 | 12302 | Round 14 — S-II Construction Grammar × Formal Concept Analysis × Epigenetics |
| 47 | 13010 | Current document status after R14 S-II content update |
| 48 | 13048 | Round 15 — M-IV CoT as Percolation Bridge-building |
| 49 | 13682 | Current document status after R15 M-IV content update |
| 50 | 13722 | Round 16 — M-V Curiosity = Learnable KL Frontier |
| 51 | 14364 | Current document status after R16 M-V content update |
| 52 | 14402 | Document self-optimization — eighth pass |
| 53 | 14576 | Current document status after v1.9 document optimization |
| 54 | 14619 | Document self-optimization — ninth pass |
| 55 | 14760 | Final document status v2.2 |

---

## 0. Why this document exists

### 0.1 Must-see active decision ledger

> purpose: reduce recall burden. This ledger records the currently active design decisions before the detailed round logs.

```yaml
active_kernels:
  R1_Compression_Residual_Occam:
    status: accepted_kernel
    core: shortest sufficient artifact + residual-first review + complexity rent

  R2_Hierarchy_Convergence:
    status: accepted_kernel
    core: layers are compression scales, authority boundaries, and convergence controls

  R3_Signal_Field_Coordination:
    status: candidate_kernel
    core: shared writable environment field can coordinate agents through residual-weighted traces, TTL decay, and quorum triggers

  R4_Externalized_Free_Energy_Landscape:
    status: candidate_kernel
    core: signal field is not just a message board; it is an externalized residual/free-energy landscape for agent navigation

  R5_Variety_Coverage_Connectivity:
    status: accepted_kernel
    core: governed routable capability variety must cover task variety, and capability graph connectivity must exceed empirical composition threshold

  R6_Information_Geometry_RG_Layer_Budget:
    status: accepted_kernel
    core: layer transformations should preserve task-relevant operators, integrate out irrelevant detail safely, and constrain patches by effective rank / geometry rather than raw surface size

  R7_Stochastic_Resonance_Log_Scale_Evaluation:
    status: candidate_kernel
    core: calibrated noise can reveal weak but meaningful evaluation signals, while log/sublinear scoring controls reward dynamic range and reduces dominance by large cheap gains

  R8_Punctuated_Equilibrium_Spandrel_Strategy:
    status: candidate_kernel
    core: plateaus and sudden capability jumps should be treated as probeable phase-transition hypotheses, while desired spandrel-like capabilities should be engineered through parent objective pressure and behavioral probes rather than direct mimicry supervision

  R9_Second_Order_Evaluation_Drift:
    status: candidate_kernel
    core: evaluators, reward models, reviewers, and scoring rubrics must be treated as time-indexed observers whose mappings can drift under optimization pressure; drift monitoring and recalibration triggers are required before scores can guide high-impact decisions

  R10_Frustration_Order_Parameter_Stabilization:
    status: candidate_kernel
    core: multi-objective or multi-agent oscillation should be diagnosed as possible frustrated constraint topology; stabilize primary order parameters first, then introduce competing objectives gradually with conflict probes and rollback gates

  R11_Fluctuation_Metamorphosis_Attractor_Geometry:
    status: candidate_kernel
    core: controlled non-equilibrium perturbation may help escape local traps, but only with probe batteries, annealing/rollback gates, and behavioral attractor-geometry preservation checks rather than weight similarity or single-run improvement claims

  R12_Precision_Weighted_Residual_Routing:
    status: candidate_kernel
    core: predictive-coding and attention insights should be absorbed as precision-weighted residual routing and active-inference action selection, while rejecting literal equivalence between transformer attention and cortical predictive coding

  R13_Context_Adapter_Epigenetic_State:
    status: candidate_kernel
    core: prompts, adapters, memory surfaces, and fine-tuning-like marks should be treated as capability-expression states that open, suppress, or stabilize channels without becoming truth or creating absent base capabilities

  R14_Construction_FCA_Prompt_Library:
    status: candidate_kernel
    core: prompt and instruction libraries should be designed as construction frames mapped to capability-channel states and audited through explicit activation/behavior attribute tables rather than lexical word swaps or unstructured template growth

  R15_CoT_Percolation_Bridge_Building:
    status: candidate_kernel
    core: chain-of-thought and intermediate reasoning traces should be treated as optional bridge-building surfaces that can raise effective concept/capability connectivity for cross-domain tasks, while remaining non-truth evidence that requires answer verification and faithfulness checks

  R16_Learnable_KL_Frontier_Curiosity:
    status: candidate_kernel
    core: curiosity/exploration should target high-residual regions that are learnable, reducible, scope-relevant, and safe; familiar zones and irreducible-noise zones should be deprioritized or stopped rather than chased indefinitely

active_accepted_candidates:
  list_format: removed_in_v2_2_to_avoid_duplication
  see: "§ 0.7 Consolidated primitive family index"
  reason: flat list of ~95 items duplicated the family-grouped index in 0.7
          and overwhelmed the must-see surface; grouped view is canonical

active_rejected_candidates:
  - memory_only_interpretation
  - passive_draft_until_final_design
  - mandatory_latent_access
  - hidden_state_replaces_packets
  - hidden_state_as_truth
  - direct_clone_of_recursiveMAS
  - WFGY_as_official_DSL_now
  - KL_as_human_authority_replacement
  - pure_orchestrator_replacement_without_fallback
  - invisible_shared_field_as_governance_source
  - treating_every_plateau_as_failure
  - treating_every_plateau_as_pre_transition
  - direct_spandrel_mimicry_supervision_without_behavioral_probe
  - emergence_claim_without_metric_audit
  - spandrel_as_excuse_for_unspecified_behavior
  - more_agents_equal_more_control
  - all_to_all_agent_connectivity
  - random_graph_pc_as_universal_shadowMAS_rule
  - model_parameter_count_as_direct_effective_variety
  - universal_rank_formula_as_v0_rule
  - natural_gradient_required_for_shadowMAS_v0
  - dropout_as_literal_rg_governance_law
  - full_rank_updates_always_wrong
  - CoT_as_universal_improvement
  - noise_everywhere_evaluation
  - unseeded_stochastic_acceptance_gate
  - log_scale_for_binary_correctness
  - reward_noise_as_truth_repair
  - linear_reward_scale_as_universal_default
  - static_reviewer_as_external_truth_oracle
  - reward_model_score_as_truth_promotion_gate
  - evaluator_drift_ignored_under_optimization
  - calibration_as_pure_parametric_patch
  - single_metric_review_for_high_impact_decision
  - simultaneous_unweighted_multi_loss_as_default
  - treating_training_oscillation_as_more_compute_only_problem
  - checkpoint_selection_by_single_metric_under_objective_conflict
  - spin_glass_as_literal_shadowMAS_physics_law
  - slaving_principle_as_authority_replacement
  - uncontrolled_high_temperature_as_default
  - random_noise_as_escape_policy
  - single_run_loss_spike_as_evidence
  - weight_similarity_as_capability_identity
  - metamorphosis_as_license_to_destroy_truth
  - dissolution_without_probe_battery
  - attractor_geometry_claim_without_behavioral_distribution
  - attention_equals_predictive_coding_literal_claim
  - raw_attention_weights_as_truth_or_explanation
  - precision_weighting_without_confidence_source
  - active_inference_as_authority_replacement
  - prediction_error_chasing_without_relevance_filter
  - neurobiology_to_transformer_direct_identity_claim
  - epigenetics_as_literal_model_biology_claim
  - prompt_can_open_absent_capability
  - context_channel_state_as_truth_promotion
  - closed_channel_as_permanent_deletion
  - fine_tune_or_RLHF_as_project_truth_replacement
  - epigenetic_metaphor_without_probe
  - lexical_word_swap_as_primary_prompt_design
  - prompt_library_without_attribute_audit
  - fca_lattice_as_truth_or_authority_gate
  - mechanistic_probe_required_for_every_prompt
  - construction_grammar_as_literal_transformer_semantics
  - hidden_activation_as_canonical_truth
  - template_count_growth_without_lattice_pruning
  - CoT_as_universal_reasoning_solution
  - visible_CoT_as_faithful_hidden_reasoning_by_default
  - reasoning_trace_as_truth_or_authority_gate
  - longer_CoT_as_automatically_better
  - percolation_metaphor_without_task_graph_probe
  - bridge_building_without_answer_verification
  - surprise_maximization_as_exploration_policy
  - curiosity_chasing_random_noise
  - novelty_equals_learning_value
  - intrinsic_reward_as_truth_or_authority
  - endless_exploration_without_stop_condition
  - exploration_without_scope_boundary
  - curiosity_as_excuse_for_unsafe_repo_traversal

active_deferred_candidates:
  - literal_KL_mathematical_constitution
  - full_information_geometry_layer_model
  - adjoint_encoder_decoder_for_state_transfer
  - formal_category_theoretic_packet_validator
  - RecursiveMAS_shock_integration_full_round
  - WFGY_small_model_lane
  - production_signal_field_schema
  - field_topology_and_zone_taxonomy
  - field_poisoning_defense_model
  - threshold_calibration_protocol
  - production_plateau_intervention_protocol
  - spandrel_parent_objective_library
  - capability_emergence_dashboard
  - long_horizon_phase_transition_experiment_suite
  - production_capability_graph_schema
  - exact_variety_metric
  - exact_empirical_pc_experiment_protocol
  - graph_centrality_risk_policy
  - bridge_agent_budget_policy
  - exact_layer_rank_budget_formula
  - Fisher_information_measurement_pipeline
  - production_rank_budget_policy
  - LoRA_rank_depth_sweep
  - CoT_domain_distance_benchmark
  - exact_sigma_star_calibration_protocol
  - production_log_reward_transform_policy
  - evaluator_sensitivity_benchmark
  - stochastic_resonance_ablation_suite
  - human_review_confidence_noise_policy
  - production_reviewer_drift_dashboard
  - evaluation_probe_set_registry
  - recalibration_governance_protocol
  - formal_categorical_commutativity_validator
  - reward_model_ensemble_policy
  - production_objective_conflict_dashboard
  - gradient_dot_product_probe_harness
  - automated_loss_phase_scheduler
  - multi_objective_pareto_selector_policy
  - agent_goal_conflict_map_schema
  - production_controlled_dissolution_protocol
  - annealing_schedule_harness
  - jarzynski_style_ensemble_weighting_harness
  - behavioral_attractor_probe_registry
  - jsd_capability_distribution_metric
  - capability_geometry_dashboard
  - model_merge_geometry_experiment
  - production_precision_weighted_routing_policy
  - attention_budget_dashboard
  - predictive_coding_backprop_experiment_lane
  - formal_precision_confidence_schema
  - active_inference_planner_benchmark
  - transformer_attention_interpretability_policy
  - production_capability_channel_registry
  - prompt_channel_linter
  - attractor_depth_measurement_harness
  - adapter_patch_lifecycle_policy
  - context_state_diff_tool
  - production_prompt_construction_registry
  - fca_prompt_lattice_tooling
  - activation_attribute_measurement_harness
  - construction_frame_linter
  - prompt_library_redundancy_dashboard
  - mechanistic_interpretability_probe_lane
  - conexp_clj_or_custom_fca_pipeline
  - production_reasoning_graph_probe
  - domain_distance_benchmark_for_cot_gain
  - cot_faithfulness_audit_harness
  - self_consistency_budget_policy
  - trace_visibility_policy_for_review_packets
  - production_learnable_frontier_detector
  - learning_progress_metric_registry
  - irreducible_noise_classifier
  - curiosity_budget_policy
  - exploration_memory_cell_registry
  - frontier_exhaustion_dashboard
```



### 0.2 Must-see document control plane v2.1

> purpose: make the one-file log readable after all planned v4 content rounds have been imported.

```yaml
document_control_plane:
  current_version: v2.1
  canonical_status: non_canonical_active_design_log
  latest_content_update: R16_M-V_Curiosity_as_Learnable_KL_Frontier
  latest_document_optimization: pass_10_p1_handoff_readiness
  v4_content_import_status: complete_for_current_plan
  current_reader_task: >
    Do not read the file linearly. Use the frozen reading paths in 0.10.
    Start with the active decision ledger, kernel index, primitive family index,
    final v4 convergence map, promotion/change-impact queue, and P1 patch plan.
    Treat round logs as evidence and historical self-optimization logs as appendix-grade trace.

  must_see_first:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v2.1
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.7 Consolidated primitive family index v2.0
    - 0.8 Final v4 convergence map v2.0
    - 0.9 Promotion and change-impact queue v2.0
    - 0.10 Frozen reading paths v2.0
    - 0.12 P1 canonical proposal patch plan v2.0
    - 0.14 P1 handoff gate v2.1
    - 0.15 Canonical proposal packet skeleton v2.1
    - latest Current document status section

  secondary_when_deciding_design:
    - relevant round accepted kernel section
    - relevant ToT branches
    - relevant MoE votes
    - relevant LATS result
    - impacted surfaces / change-impact warning

  expandable_only_when_needed:
    - full paper evidence cards
    - older document self-optimization passes
    - historical round narrative
    - examples and Feynman explanations
```

Reading rule:

```text
Do not treat the latest appended text as automatically more authoritative than the top ledger.
Authority inside this file flows through explicit decision-state markers:
accepted / rejected / deferred / candidate / canonical_status.

After v2.0, the single-file reading path was frozen. v2.1 is a requested handoff-readiness pass: it does not reopen research intake, but makes the next P1 canonical proposal easier to draft and review.
```

---

### 0.3 Current kernel index

> purpose: one-screen recognition surface for the active design kernels.

| Round | Kernel | Current status | Primary design question | Do not confuse with |
|---|---|---|---|---|
| R1 | Compression–Residual–Occam | accepted kernel | What is the shortest sufficient artifact, and what residual remains? | Token compression only |
| R2 | Hierarchy–Convergence | accepted kernel | Are layers compression scales, authority boundaries, and convergence controls? | Folder organization |
| R3 | Signal Field Coordination | candidate kernel | Can agents coordinate through auditable residual traces in shared state? | Canonical memory or truth layer |
| R4 | Externalized Free-Energy Landscape | candidate kernel | Can the signal field guide action by reducible residual value? | Chasing highest error blindly |
| R5 | Variety Coverage–Connectivity | accepted kernel | Does controlled capability variety cover task variety and flow across the capability graph? | More agents, bigger models, or all-to-all messaging |
| R6 | Information Geometry–RG Layer Budget | accepted kernel | Are layer transformations preserving relevant operators and using effective-rank-aware patches? | Blind full-rank edits, lossy compression, or CoT everywhere |
| R7 | Stochastic Resonance–Log Scale Evaluation | candidate kernel | Can calibrated noise expose weak signals while sublinear scoring controls dynamic range? | Randomness everywhere, unseeded review gates, or log-scaling binary correctness |
| R8 | Punctuated Equilibrium–Spandrel Strategy | candidate kernel | Are plateaus and sudden capability jumps probeable transition signals, and are desired by-product capabilities better engineered through parent objectives? | Waiting forever, declaring every jump real, or training only the visible surface form |
| R9 | Second-Order Evaluation Drift | candidate kernel | Is the evaluator/reward model/reviewer mapping stable while the evaluated system changes under optimization pressure? | Treating scores as truth, assuming reviewers are external oracles, or fixing calibration once |
| R10 | Frustration–Order Parameter Stabilization | candidate kernel | Are objective/agent constraints mutually frustrating the system before an order parameter can stabilize? | Adding more compute, picking one lucky checkpoint, or launching all losses at once |
| R11 | Fluctuation–Metamorphosis–Attractor Geometry | candidate kernel | Can controlled perturbation escape local traps while preserving capability geometry through behavioral probes? | Random noise, destructive rewrites, weight similarity as capability proof, or single-run loss improvement |
| R12 | Precision-Weighted Residual Routing | candidate kernel | Can expected-vs-actual residuals be routed by confidence/precision and used for action selection without overclaiming attention interpretability? | Literal attention=predictive-coding equivalence, raw attention weights as truth, or chasing every prediction error |
| R13 | Context–Adapter Epigenetic State | candidate kernel | Which capability channels are opened, suppressed, stabilized, or made ambiguous by prompt/context/adapter state? | Claiming prompts create absent capabilities, treating context state as truth, or using epigenetics as literal biology |
| R14 | Construction–FCA Prompt Library | candidate kernel | Are prompt templates designed as construction frames and audited as capability-activation patterns instead of unmanaged text variants? | Lexical prompt tweaking, template hoarding, hidden activation as truth, or FCA as a decision authority |
| R15 | CoT–Percolation Bridge Building | candidate kernel | Does intermediate reasoning add useful bridge nodes/edges for cross-domain tasks that would otherwise remain disconnected? | CoT everywhere, longer traces as truth, visible traces as faithful hidden reasoning, or percolation claims without task graph probes |
| R16 | Learnable KL Frontier Curiosity | candidate kernel | Is exploration aimed at high-residual regions that are still learnable and reducible, rather than familiar zones or irreducible noise? | Surprise maximization, novelty worship, endless exploration, or intrinsic reward as truth/authority |

Kernel dependency shape:

```text
R1 gives residual semantics.
R2 gives layer/convergence semantics.
R3 gives shared coordination medium.
R4 gives field navigation/action-value semantics.
R5 gives capability coverage/connectivity constraints.
R6 gives layer geometry / rank / relevant-operator budget constraints.
R7 gives evaluation sensitivity / noise budget / dynamic-range scoring constraints.
R8 gives plateau / phase-transition strategy and spandrel-capability engineering constraints.
R9 gives second-order evaluation drift and recalibration constraints.
R10 gives objective-conflict / training-oscillation diagnosis and staged stabilization constraints.
R11 gives controlled perturbation / annealing / behavioral attractor-geometry preservation constraints.
R12 gives precision-weighted residual routing / attention-budget / active-inference action-selection constraints.
R13 gives context / adapter / prompt channel-state constraints for capability expression.
R14 gives prompt construction / library taxonomy / capability-attribute audit constraints.
R15 gives CoT bridge-building / reasoning-graph connectivity / trace-faithfulness boundary constraints.
R16 gives learnable-frontier / curiosity-budget / exploration-stop-condition constraints.
```

---

### 0.4 Decision-state map

> purpose: prevent speculative candidates from looking like approved truth.

```yaml
decision_state_map:
  canonical_truth:
    meaning: approved formal shadowMAS truth
    location: outside_this_file_in_01_truth
    this_document_role: may_propose_or_explain_only

  accepted_kernel:
    meaning: strong active design lens accepted for architecture reasoning
    may_do:
      - guide future canonical proposal
      - guide runtime/packet/review design discussion
      - appear in change-impact queue
    may_not_do:
      - overwrite canonical truth directly
      - bypass human authority
      - become runtime law without promotion gate

  candidate_kernel:
    meaning: promising but not yet fully promoted design kernel
    may_do:
      - shape experiments
      - define candidate primitives
      - inform future review
    may_not_do:
      - become default production behavior
      - redefine packet schema by itself

  primitive_candidate:
    meaning: possible future schema/runtime/review object
    may_do:
      - appear in future packet or runtime proposal
      - be tested as local prototype
    may_not_do:
      - be assumed required for v0
      - be treated as canonical schema

  rejected_candidate:
    meaning: explicitly not adopted under current reasoning
    may_do:
      - remain as warning or anti-pattern
    may_not_do:
      - re-enter design as default without new evidence and review

  deferred_candidate:
    meaning: potentially valuable but not mature enough for adoption
    may_do:
      - remain in queue
      - receive future targeted round
    may_not_do:
      - silently become accepted because it appears often
```

---

### 0.5 Current document debt register

> purpose: name the maintenance debt instead of hiding it.

```yaml
document_debt_register:
  D1_multiple_document_self_optimization_passes:
    status: accepted_historical_appendix_for_now
    risk: reader may over-read historical process notes
    mitigation: use 0.2 control plane; later move historical optimization passes to appendix if splitting is allowed

  D2_two_historical_current_status_sections:
    status: renamed_as_round_snapshots
    risk: reader may mistake older status for latest status
    mitigation: section titles now identify after-Round status; latest status remains final section

  D3_paper_evidence_and_design_decisions_mixed:
    status: tolerable_but_watch
    risk: evidence may look like policy
    mitigation: 0.4 decision-state map and explicit canonical_status fields

  D4_candidate_primitives_scattered_by_round:
    status: partially_fixed_in_v1_9
    risk: future schema extraction becomes expensive if every primitive is found only inside round logs
    mitigation: 0.7 now provides a consolidated primitive family index; exact field-level schemas still remain in round sections until promotion review

  D5_top_ledger_growth:
    status: watch
    risk: ledger becomes too long to remain must-see
    mitigation: next optimization should convert accepted/rejected/deferred lists into grouped tables if they exceed scanability

  D6_evaluation_kernel_requires_boundary_clarity:
    status: newly_added
    risk: Q-III could be misread as permission to add randomness to governed acceptance gates
    mitigation: record seeded/noise-scope boundaries and explicitly ban stochasticity from binary correctness, schema validation, authority, and canonical truth promotion

  D7_strategy_kernel_requires_metric_and_probe_boundary:
    status: newly_added
    risk: S-I could be misread as permission to wait through every plateau or call every thresholded score jump a true emergence
    mitigation: require plateau probes, emergence metric audit, and behavioral capability checks before treating a plateau or jump as meaningful

  D8_closeout_horizon_not_explicit: { status: fixed_in_v1_0, see: historical_fixed_debts }

  D9_frustration_kernel_requires_scope_boundary:
    status: newly_added
    risk: D-I could be misread as permission to sequentialize every task or reject all simultaneous multi-objective work
    mitigation: require conflict evidence before applying staged stabilization; if objectives are compatible or independent, parallelization remains allowed

  D10_fluctuation_kernel_requires_control_boundary:
    status: newly_added
    risk: D-II/M-III could be misread as permission to inject random perturbation, accept destructive rewrites, or judge capability transfer by weight similarity alone
    mitigation: require probe batteries, seeded perturbation logs, annealing/rollback gates, and behavioral attractor comparison before treating a controlled dissolution as successful

  D11_precision_kernel_requires_interpretability_boundary:
    status: newly_added
    risk: D-III could be misread as a literal identity claim between transformer attention and cortical predictive coding, or as permission to treat attention weights as truth/explanation
    mitigation: record the kernel as precision-weighted residual routing and active-inference action selection; require confidence sources and keep attention weights as evidence, not authority

  D12_context_state_kernel_requires_capability_boundary:
    status: newly_added
    risk: D-IV could be misread as permission to claim that prompt/context/adapter state can create absent capability or override canonical truth
    mitigation: separate base capability, channel expression state, persistence, reversibility, authority boundary, and behavioral validation before adopting any context-channel rule

  D13_curiosity_kernel_requires_frontier_boundary:
    status: newly_added
    risk: M-V could be misread as permission to chase novelty, surprise, random noise, or unbounded repo traversal
    mitigation: require learnability, reducibility, scope relevance, safety, TTL/freshness, and stop-condition checks before assigning exploration budget


  D14_v4_convergence_requires_single_map: { status: fixed_in_v1_9, see: historical_fixed_debts }

  D15_promotion_queue_was_implicit: { status: fixed_in_v1_9, see: historical_fixed_debts }

  D16_top_control_plane_is_now_long: { status: fixed_in_v2_0, see: historical_fixed_debts }

  D17_closeout_must_not_mask_noncanonical_status: { status: fixed_in_v2_0, see: historical_fixed_debts }

  historical_fixed_debts:
    D8_closeout_horizon_not_explicit:
      status: fixed_in_v1_0
      risk: reader does not know how many more document-only passes are needed before the file can be treated as stable
      mitigation: add 0.6 closeout horizon with round estimates and finish criteria
    D14_v4_convergence_requires_single_map:
      status: fixed_in_v1_9
      risk: after all planned v4 rounds, readers may still see isolated kernels instead of the cross-round convergence pattern
      mitigation: 0.8 now provides a final v4 convergence map grouping kernels by governance, runtime, evaluation, prompt, exploration, and strategy surfaces
    D15_promotion_queue_was_implicit:
      status: fixed_in_v1_9
      risk: accepted kernels could be mistaken for immediate canonical edits or remain forever as research notes
      mitigation: 0.9 now records promotion/change-impact lanes, target surfaces, blockers, and first canonical candidates
    D16_top_control_plane_is_now_long:
      status: fixed_in_v2_0
      risk: the must-see surface can become too large even though it reduces search cost
      mitigation: v2.0 freezes reader modes and marks historical optimization logs as appendix-grade trace
    D17_closeout_must_not_mask_noncanonical_status:
      status: fixed_in_v2_0
      risk: a polished closeout file may look more authoritative than it is
      mitigation: 0.4 decision-state map, 0.9 promotion queue, 0.12 P1 patch plan, and final status all state that no canonical truth was changed
```

---

### 0.6 Closeout horizon and finish criteria v2.0

> purpose: state that the current single-file reading path is now stable enough for use, while preserving the non-canonical boundary.

```yaml
closeout_estimate:
  assumption: single_active_design_log_remains_required
  v4_content_rounds_remaining_under_current_plan: 0
  document_only_rounds_remaining_to_stable: 0
  current_pass: pass_10_p1_handoff_readiness

  completed_document_goals:
    primitive_index_consolidation: done_as_family_index_in_0_7
    final_v4_convergence_map: done_in_0_8
    promotion_change_impact_queue: done_in_0_9
    frozen_reading_paths: done_in_0_10
    historical_self_optimization_demotion: done_in_0_11
    p1_patch_plan: done_in_0_12
    split_decision_record: done_in_0_13
    p1_handoff_gate: done_in_0_14
    canonical_proposal_packet_skeleton: done_in_0_15

  remaining_document_goal:
    status: none_if_no_new_research_rounds_are_added
    next_meaningful_work: canonical_proposal_drafting_or_optional_file_split

  if_file_split_is_allowed_later:
    recommended_split_shape:
      - active_design_index
      - round_evidence_appendix
      - primitive_candidate_register
      - promotion_queue

  maintenance_rule_if_new_research_rounds_are_added:
    rule: run one short document-optimization pass after every two new content rounds or immediately after any round that adds a new primitive family
```

Finish criteria:

```text
The document is stable when a new reader can answer these in under ten minutes:
1. What is currently accepted, rejected, and deferred?
2. Which kernels are design-active but non-canonical?
3. Which primitive families exist, and where did they originate?
4. Which canonical files would be impacted by promotion?
5. What should be read first, what is secondary, and what is historical trace only?
```

Current answer to “how many rounds until finish?”:

```text
After v2.0, if no more research content is added, no further document-only optimization round is required.
The next step should be either P1 canonical proposal drafting, optional file splitting, or a new research cycle with its own maintenance cadence.
```

---


### 0.7 Consolidated primitive family index v2.0

> purpose: make scattered candidate primitives discoverable without flattening 16 round logs into one giant schema dump.

```yaml
primitive_family_index:
  packet_and_review_surfaces:
    originating_rounds: [R1, R3, R4, R12]
    representative_primitives:
      - residual_first_report
      - prediction_error_packet_field
      - top_down_expectation_bottom_up_residual_contract
      - precision_weighted_residual_score
    candidate_status: primitive_candidate_family
    promotion_target: future_packet_schema_or_review_packet_shell
    first_canonical_candidate: residual_first_report
    blocker_before_promotion:
      - define minimum required fields
      - verify no conflict with existing task_packet/memory_packet/review_packet rules
      - decide whether residual scoring is enum-based or numeric-proxy-based

  runtime_signal_field_surfaces:
    originating_rounds: [R3, R4, R5, R16]
    representative_primitives:
      - signal_field_event
      - signal_field_zone
      - field_audit_projection
      - quorum_trigger
      - field_poisoning_check
      - learnable_frontier_record
      - frontier_exhaustion_report
    candidate_status: active_candidate_runtime_family
    promotion_target: future_R_layer_runtime_contract
    first_canonical_candidate: signal_field_event
    blocker_before_promotion:
      - shared writable state availability decision
      - TTL/decay semantics
      - write/read permission model
      - anti-poisoning and audit projection requirements

  capability_graph_and_variety_surfaces:
    originating_rounds: [R5, R15]
    representative_primitives:
      - variety_coverage_audit
      - capability_graph_record
      - variety_connectivity_audit
      - bridge_edge_record
      - cross_domain_percolation_probe
      - reasoning_graph_connectivity_probe
      - bridge_trace_policy
    candidate_status: active_design_family
    promotion_target: routing_policy_and_runtime_capability_registry
    first_canonical_candidate: variety_coverage_audit
    blocker_before_promotion:
      - define agent/module capability vocabulary
      - define empirical p_c or bridge-success probe
      - prevent all-to-all messaging from being treated as the default fix

  layer_compression_and_patch_budget_surfaces:
    originating_rounds: [R2, R6, R11]
    representative_primitives:
      - order_parameter_registry
      - layer_composition_record
      - compression_layer_check
      - rg_layer_transform_check
      - effective_rank_audit
      - low_rank_patch_budget
      - behavioral_attractor_fingerprint
      - attractor_geometry_comparison
    candidate_status: active_design_family
    promotion_target: prompt_layering_contract_runtime_adapter_contract
    first_canonical_candidate: layer_composition_record
    blocker_before_promotion:
      - define preserved/adapted/suppressed rule fields
      - decide when compression is forbidden
      - define rollback and validation surface for scoped patches

  evaluation_and_recalibration_surfaces:
    originating_rounds: [R7, R9, R10]
    representative_primitives:
      - weak_signal_probe
      - noise_budget_record
      - sublinear_score_transform
      - probabilistic_evaluation_integrity_check
      - evaluation_stack_record
      - reviewer_drift_monitor
      - evaluation_commutativity_check
      - recalibration_trigger
      - objective_conflict_probe
      - tradeoff_surface_record
    candidate_status: active_candidate_review_family
    promotion_target: review_policy_and_evaluation_governance
    first_canonical_candidate: reviewer_drift_monitor
    blocker_before_promotion:
      - ban stochastic noise from binary/schema/canonical gates
      - define independent quality surface
      - define recalibration owner and trigger threshold
      - separate score evidence from truth authority

  prompt_context_and_capability_channel_surfaces:
    originating_rounds: [R13, R14]
    representative_primitives:
      - capability_channel_state_record
      - open_closed_channel_contract
      - attractor_depth_prompt_policy
      - adapter_state_mark_record
      - channel_expression_probe
      - construction_frame_record
      - prompt_construction_taxonomy
      - fca_prompt_library_audit
      - prompt_template_gap_redundancy_detector
      - construction_channel_contract
    candidate_status: active_candidate_prompt_family
    promotion_target: prompt_layering_contract_and_runtime_adapter_prompt_rules
    first_canonical_candidate: open_closed_channel_contract
    blocker_before_promotion:
      - distinguish base capability from context expression
      - define which channels can be opened/closed by prompt only
      - keep FCA/mechanistic probes as audit evidence, not authority

  strategy_and_exploration_surfaces:
    originating_rounds: [R8, R11, R16]
    representative_primitives:
      - plateau_transition_probe
      - parent_objective_design_record
      - spandrel_capability_probe
      - emergence_metric_audit
      - bounded_plateau_intervention_policy
      - controlled_fluctuation_probe
      - annealed_exploration_record
      - controlled_dissolution_protocol
      - learning_progress_probe
      - irreducible_noise_classifier
      - curiosity_budget_policy
    candidate_status: active_candidate_strategy_family
    promotion_target: experimental_lane_policy_and_research_protocols
    first_canonical_candidate: emergence_metric_audit
    blocker_before_promotion:
      - require behavioral probes before emergence claims
      - define rollback for perturbation/dissolution lanes
      - define exploration stop conditions
      - prevent curiosity from authorizing blind repo traversal
```

Rule:

```text
A primitive family can enter canonical proposal only when it has:
1. one named owner surface,
2. one minimum schema or checklist,
3. one rejection boundary,
4. one change-impact path,
5. one human-review condition.
```

---

### 0.8 Final v4 convergence map v2.0

> purpose: show what v4 contributed after all planned nodes were read, without forcing a reader through every paper card.

```yaml
final_v4_convergence_map:
  governance_core:
    rounds: [R1, R2, R5]
    accepted_direction:
      - minimize governance surprise through residual-first review
      - treat layers as compression scales and authority boundaries
      - require variety coverage and connectivity before trusting multi-agent capability
    canonical_pressure: high
    likely_first_promotion:
      - residual_first_report
      - order_parameter_registry
      - variety_coverage_audit

  runtime_coordination_core:
    rounds: [R3, R4, R16]
    accepted_direction:
      - use shared signal fields as optional runtime coordination substrate
      - make signals typed, decaying, auditable, and poison-resistant
      - navigate by reducible residual value, not raw novelty or raw heat
    canonical_pressure: medium_high
    likely_first_promotion:
      - signal_field_event
      - field_audit_projection
      - learnable_frontier_record

  evaluation_and_review_core:
    rounds: [R7, R9, R10]
    accepted_direction:
      - weak evaluation signals may need calibrated sensitivity handling
      - evaluator/reviewer mappings can drift under optimization pressure
      - objective conflict must be diagnosed before adding more retry or more agents
    canonical_pressure: high
    likely_first_promotion:
      - reviewer_drift_monitor
      - evaluation_commutativity_check
      - objective_conflict_probe

  layer_adapter_and_representation_core:
    rounds: [R6, R11, R12, R13]
    accepted_direction:
      - compression and adapter changes should preserve relevant operators and expose distortion
      - capability transfer is better judged by behavior/attractor geometry than weight or surface similarity alone
      - residual routing should be precision-weighted
      - prompt/context/adapter state changes capability expression but not truth
    canonical_pressure: medium
    likely_first_promotion:
      - layer_composition_record
      - low_rank_patch_budget
      - capability_channel_state_record

  prompt_library_and_reasoning_trace_core:
    rounds: [R14, R15]
    accepted_direction:
      - prompt templates are construction frames, not word swaps
      - prompt libraries should be audited as capability-activation lattices
      - CoT is an optional bridge-building surface for cross-domain tasks, not universal truth
    canonical_pressure: medium
    likely_first_promotion:
      - construction_frame_record
      - fca_prompt_library_audit
      - bridge_trace_policy

  strategy_and_research_protocol_core:
    rounds: [R8, R11, R16]
    accepted_direction:
      - plateaus and jumps require probes, not faith
      - controlled perturbation is an experimental lane with rollback, not default behavior
      - curiosity should target the learnable frontier and stop when exhausted
    canonical_pressure: medium_low
    likely_first_promotion:
      - emergence_metric_audit
      - controlled_fluctuation_probe
      - frontier_exhaustion_report
```

Final synthesis:

```text
v4 does not produce one monolithic shadowMAS law.
It produces six converged design pressures:
1. residual-first governed compression,
2. hierarchical layer/authority control,
3. auditable runtime signal fields,
4. second-order evaluation governance,
5. capability/channel/trace audits,
6. bounded exploration and experimental lanes.
```

---

### 0.9 Promotion and change-impact queue v2.0

> purpose: separate “accepted as design-active” from “ready to patch canonical truth”.

```yaml
promotion_queue:
  P0_do_not_promote_directly:
    rule: this active design log is non-canonical
    blocked_actions:
      - do_not_edit_01_truth_directly_from_round_logs
      - do_not_turn_candidate_primitives_into_required_schema_without_review
      - do_not_let_runtime_signal_fields_become_truth_layers
      - do_not_replace_human_authority_with_score_quorum_or_field_heat

  P1_first_canonical_proposal_batch:
    priority: high
    candidate_changes:
      - residual_first_report_minimum_shape
      - layer_composition_record_minimum_shape
      - variety_coverage_audit_minimum_shape
      - reviewer_drift_monitor_minimum_shape
    impacted_surfaces:
      - SHADOWMAS-CURRENT-TRUTH.v0.en.md
      - SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md
      - future_packet_schema_files_under_02_packets
      - zh-TW human-facing single-source if explanation changes
    promotion_condition:
      - define minimum fields
      - verify authority and truth boundaries
      - update change-impact report
      - human approval required

  P2_runtime_candidate_batch:
    priority: medium_high
    candidate_changes:
      - signal_field_event
      - field_audit_projection
      - quorum_trigger_for_routing_only
      - field_poisoning_check
      - learnable_frontier_record
    impacted_surfaces:
      - future_R_layer_runtime_contract
      - SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md
      - SHADOWMAS-CURRENT-TRUTH.v0.en.md
      - memory-plane rules if persistence is introduced
    promotion_condition:
      - decide shared-state availability
      - define TTL/decay and permissions
      - prove field remains T4/T5 runtime signal, not T2/T3 truth

  P3_evaluation_governance_batch:
    priority: high_but_sensitive
    candidate_changes:
      - evaluation_stack_record
      - evaluation_commutativity_check
      - recalibration_trigger
      - objective_conflict_probe
      - probabilistic_evaluation_integrity_check
    impacted_surfaces:
      - review policy
      - packet review surface
      - governance matrix
      - human-facing explanation
    promotion_condition:
      - specify where noise is forbidden
      - separate score/evidence/truth
      - define reviewer drift owner and trigger

  P4_prompt_and_adapter_batch:
    priority: medium
    candidate_changes:
      - open_closed_channel_contract
      - construction_frame_record
      - prompt_construction_taxonomy
      - adapter_state_mark_record
      - low_rank_patch_budget
    impacted_surfaces:
      - SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md
      - runtime adapter prompt contracts
      - zh-TW onboarding/rationale if human-facing
    promotion_condition:
      - distinguish context expression from base capability
      - require prompt library audit only above complexity threshold
      - keep adapters scoped and reversible

  P5_research_protocol_batch:
    priority: medium_low
    candidate_changes:
      - emergence_metric_audit
      - controlled_dissolution_protocol
      - curiosity_budget_policy
      - frontier_exhaustion_report
    impacted_surfaces:
      - future research protocol docs
      - runtime experimental lane docs
      - not core v0 truth unless adopted as default process
    promotion_condition:
      - keep as experimental policy first
      - require rollback and probe batteries
      - no authority bypass
```

Current recommendation:

```text
Promote nothing automatically.
Prepare P1 as the first canonical proposal batch because it improves review safety without requiring heavy runtime infrastructure.
Keep P2–P5 as candidate queues until v0 runtime and packet contracts are more stable.
```

---

### 0.10 Frozen reading paths v2.0

> purpose: stop the single file from behaving like a giant linear scroll. Choose one path based on the reader's task.

```yaml
frozen_reading_paths:
  human_operator_path:
    purpose: understand current direction and decide next action
    read_order:
      - 0.1 Must-see active decision ledger
      - 0.3 Current kernel index
      - 0.8 Final v4 convergence map
      - 0.9 Promotion and change-impact queue
      - 0.12 P1 canonical proposal patch plan
      - final Current document status section
    skip_by_default:
      - paper evidence cards
      - historical document self-optimization logs
      - detailed ToT/MoE/LATS unless a decision is disputed

  agent_execution_path:
    purpose: use this file as a non-canonical design context without over-promoting it
    read_order:
      - 0.2 Must-see document control plane
      - 0.4 Decision-state map
      - 0.7 Consolidated primitive family index
      - relevant round accepted kernel only
      - relevant rejected/deferred boundaries
      - 0.9 Promotion and change-impact queue
    hard_rule:
      - do_not_patch_canonical_truth_from_this_file_directly
      - do_not_turn_candidate_primitives_into_required_schema_without_promotion_review
      - do_not_treat_runtime_signal_or_score_as_truth_authority

  canonical_review_path:
    purpose: prepare controlled patch proposals for formal truth files
    read_order:
      - 0.9 Promotion and change-impact queue
      - 0.12 P1 canonical proposal patch plan
      - 0.7 primitive family index for fields and blockers
      - source round LATS result for each candidate
      - SHADOWMAS-CHANGE-IMPACT-MAP before any file edit
    output_required:
      - what_changed
      - impacted_truth_layers_checked
      - files_to_update
      - files_intentionally_deferred
      - zh_TW_human_doc_update_needed
```

Reading freeze rule:

```text
Do not add another top-level navigation surface unless a new research cycle introduces a genuinely new primitive family.
For ordinary future edits, update the existing 0.7/0.8/0.9/0.12 surfaces instead of adding 0.14, 0.15, etc.
```

---

### 0.11 Historical self-optimization log status v2.0

> purpose: preserve traceability while preventing process logs from competing with current decision surfaces.

```yaml
historical_self_optimization_logs:
  current_status: appendix_grade_trace
  applies_to_sections:
    - 16 Document self-optimization first pass
    - 18 Document self-optimization second pass
    - 20 Document self-optimization third pass
    - 23 Document self-optimization fourth pass
    - 25 Document self-optimization fifth pass
    - 30 Document self-optimization sixth pass
    - 34 Document self-optimization seventh pass
    - 52 Document self-optimization eighth pass
    - 54 Document self-optimization ninth pass

  how_to_read:
    - read_only_when_a_structural_decision_is_disputed
    - do_not_use_as_current_state
    - prefer_0_2_to_0_13_for_current_navigation

  reason_not_deleted:
    - preserves why the file became decision-first
    - preserves rejected structure options
    - preserves transition from append-only log to frozen reading path
```

Rule:

```text
Historical self-optimization sections are evidence of document governance history.
They are not the active reading path and should not be used to infer current canonical status.
```

---

### 0.12 P1 canonical proposal patch plan v2.0

> purpose: convert the first promotion queue into a bounded patch plan without actually changing canonical truth.

```yaml
p1_canonical_proposal_patch_plan:
  status: prepared_not_applied
  priority: high
  reason: improves review safety and governance clarity without requiring heavy runtime infrastructure

  candidate_1_residual_first_report_minimum_shape:
    target_surface:
      primary: 02_packets/review_packet.v0.yaml
      primary_change_type: extend_minimum_required_fields
      secondary: 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md
      secondary_change_type: add_field_definitions
    minimum_fields:
      - expected_state
      - actual_state
      - residuals
      - validation_gap
      - truth_conflicts
      - decision_needed
      - stop_condition_status
    rejection_boundary:
      - not_a_success_story_format
      - not_a_truth_promotion_gate_by_itself
    impacted_layers_to_check:
      - T4_execution_feed
      - T3_shared_memory_if_reused
      - T2_only_after_formal_promotion
    drafter_must_read_before_filling_proposal:
      - 02_packets/review_packet.v0.yaml         # current shape, to detect field collision
      - 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md  # existing field names, to avoid duplicates
      - 02_packets/packet_common_shell.v0.yaml   # shell field collision check (per CHANGE-IMPACT-MAP § 4)
      - 01_truth/SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md § 4  # packet field change rules

  candidate_2_layer_composition_record_minimum_shape:
    target_surface:
      - SHADOWMAS_PROMPT_LAYERING_CONTRACT
      - future_runtime_adapter_contract
    minimum_fields:
      - source_layers
      - preserved_rules
      - adapted_rules
      - suppressed_rules
      - unresolved_conflicts
      - host_constraints
      - rollback_or_review_note
    rejection_boundary:
      - composition_allowed_ownership_not_flattened
      - runtime_adapter_must_not_replace_truth_source
    impacted_layers_to_check:
      - prompt_layering
      - governance_matrix
      - current_truth

  candidate_3_variety_coverage_audit_minimum_shape:
    target_surface:
      - future_routing_policy
      - future_capability_registry
      - possible_SHADOWMAS_CURRENT_TRUTH_capability_routing_note
    minimum_fields:
      - environment_variety_observed
      - controller_variety_available
      - missing_variety
      - connectivity_or_bridge_requirement
      - failure_signature
      - recommended_bridge_or_capability_addition
    rejection_boundary:
      - more_agents_not_equal_more_control
      - all_to_all_connectivity_not_default_fix
    impacted_layers_to_check:
      - R_layer_runtime_direction
      - L2_planning_routing
      - L3_execution_capability

  candidate_4_reviewer_drift_monitor_minimum_shape:
    target_surface:
      - future_review_policy
      - possible_review_packet_extension
      - governance_matrix_if_scores_are_used_for_decisions
    minimum_fields:
      - evaluator_identity
      - evaluated_surface
      - scoring_or_review_criterion
      - drift_signal
      - independent_quality_surface
      - recalibration_trigger
      - authority_boundary
    rejection_boundary:
      - score_is_evidence_not_truth
      - static_reviewer_not_external_oracle
      - no_stochastic_noise_in_binary_schema_or_canonical_gates
    impacted_layers_to_check:
      - T1_delegated_decision
      - T4_execution_feed
      - T2_canonical_truth_only_after_human_gate
```

Required output if P1 is later promoted:

```yaml
canonical_patch_report_required:
  - what_changed
  - why_this_is_needed
  - source_design_kernel
  - impacted_truth_layers_checked
  - files_updated
  - files_deferred
  - zh_TW_human_facing_update_needed
  - human_approval_status
```

---

### 0.13 Split decision record v2.0

> purpose: decide whether this file should remain single-file or be split after closeout.

```yaml
split_decision_record:
  current_decision: keep_single_file_for_now
  reason:
    - user_requested_active_design_log_continuity
    - top control plane now provides navigation without full linear reading
    - no canonical patch has been applied yet
    - splitting before canonical proposal may create sync overhead

  split_later_if_any_condition_is_met:
    - P1 canonical proposal is drafted as a formal patch package
    - primitive family index needs field-level schemas for implementation
    - new v5 research cycle adds more than two content rounds
    - file exceeds maintainable review size for a single pass

  preferred_split_shape_if_triggered:
    active_design_index: current 0.1_to_0.13
    round_evidence_appendix: full R1_to_R16 evidence cards and round logs
    primitive_candidate_register: primitive families with minimum fields and blockers
    promotion_queue: P1_to_P5 patch plans and change-impact status
```

Current judgment:

```text
Do not split immediately. v2.0 is stable enough as a single active design log.
Split only when the next task is formal canonical patching or implementation-level schema extraction.
```

---


---

### 0.14 P1 handoff gate v2.1

> purpose: turn the closeout file from a research archive into a ready-to-use input for the first canonical proposal round.

```yaml
p1_handoff_gate:
  status: ready_for_canonical_proposal_drafting
  document_role: evidence_and_design_basis_only
  canonical_truth_changed: false
  promotion_allowed_without_new_review: false

  must_not_do_next:
    - add_more_v4_reading_under_current_plan
    - treat_active_kernels_as_canonical_truth
    - promote_all_candidate_primitives_at_once
    - split_files_before_the_first_patch_shape_is_known

  should_do_next:
    - draft_one_P1_patch_at_a_time
    - start_with_low_blast_radius_schema_or_review_surface
    - attach_change_impact_check_to_each_patch
    - keep_human_approval_as_required_gate

  recommended_P1_order:
    1_residual_first_report_minimum_shape:
      why_first: highest_review_safety_gain_low_runtime_cost
      primary_target: 02_packets/review_packet.v0.yaml
      secondary_target: 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md

    2_layer_composition_record_minimum_shape:
      why_second: protects_prompt_layering_and_runtime_adapter_boundaries
      likely_target: prompt_layering_contract_or_runtime_adapter_contract

    3_reviewer_drift_monitor_minimum_shape:
      why_third: protects_score_based_review_from_silent_proxy_drift
      likely_target: review_policy_or_review_packet_extension

    4_variety_coverage_audit_minimum_shape:
      why_fourth: valuable_but_requires_capability_registry_or_routing_surface
      likely_target: future_routing_policy_or_capability_registry

  p1_exit_criteria:
    one_p1_patch_is_done_when:
      - canonical proposal packet is filled using 0.15 skeleton
      - change-impact review is complete per SHADOWMAS-CHANGE-IMPACT-MAP
      - human approval gate produced approve | revise | reject | defer decision
      - if approved: target file updated, zh-TW companion sync decided, log entry recorded
      - if revise/reject/defer: outcome recorded under 0.4 decision_state_map
    next_p1_candidate_may_start_when:
      - prior P1 reached approve | reject | defer terminal state
      - revise loop is bounded: ≤2 revision cycles before human-authority escalation
    p1_is_not_done_just_because:
      - a packet skeleton was filled (without change-impact review)
      - kernel was discussed in chat (without proposal packet)
      - candidate was renamed or reorganized (without target-file patch)
```

Decision rule:

```text
A P1 patch is allowed to quote this active design log as design evidence,
but must still pass the formal change-impact map and human approval gate before becoming canonical truth.
```

---

### 0.15 Canonical proposal packet skeleton v2.1

> purpose: give the next drafting round a fixed output shape so it does not restart open-ended research.

```yaml
canonical_proposal_packet:
  proposal_id:
  proposal_title:
  proposal_status: draft_for_human_review

  source_basis:
    active_design_log_version: v2.1
    source_rounds:
    source_kernels:
    source_primitives:

  problem:
    current_failure_mode:
    why_existing_truth_is_insufficient:
    what_this_patch_improves:

  proposed_change:
    target_file_or_surface:
    exact_change_summary:
    proposed_minimum_fields_or_rules:
    non_goals:

  governance_boundary:
    canonical_truth_changed: true | false
    human_approval_required: true
    cannot_promote_from:
      - T4_execution_feed
      - T5_ephemeral_cache_or_session_state
    score_or_signal_is_evidence_not_truth: true

  change_impact_check:
    impacted_truth_files:
    impacted_packet_or_runtime_surfaces:
    impacted_zh_TW_human_docs:
    deferred_impacts:
    reason_for_deferral:

  acceptance_criteria:
    - must_reduce_a_named_failure_mode
    - must_not_flatten_truth_or_authority_layers
    - must_have_minimum_machine_stable_shape
    - must_have_rejection_or_rollback_boundary

  rejection_boundary:
    reject_if:
      - expands_scope_beyond_P1
      - requires_unbuilt_runtime_infrastructure
      - lets_candidate_signal_promote_truth_directly
      - creates_unreviewable_hidden_authority

  reviewer_decision:
    decision: approve | revise | reject | defer
    required_revision_notes:
```

Usage rule:

```text
The next round should fill this packet for one P1 candidate only.
Do not batch-promote all P1 candidates in one patch.
```

#### 0.15.1 Filled example for P1-001 (drafter starting point)

> purpose: give the next session a half-filled packet so it does not start from a blank template.
> note: this is a *drafting example*, not an approved proposal. Reviewer fields are intentionally blank.

```yaml
canonical_proposal_packet_example:
  proposal_id: P1-001
  proposal_title: Add residual_first_report minimum required fields to review_packet
  proposal_status: draft_for_human_review

  source_basis:
    active_design_log_version: v2.2
    source_rounds: [R1, R3, R4, R12]
    source_kernels:
      - R1_Compression_Residual_Occam
      - R12_Precision_Weighted_Residual_Routing
    source_primitives:
      - residual_first_report  # original definition in § 12.2

  problem:
    current_failure_mode: >
      review_packet does not require expected/actual/residual contrast;
      reviews can be filed as success stories without naming gaps,
      which lets silent drift pass through L4 mergeback unflagged.
    why_existing_truth_is_insufficient: >
      review_packet.v0.yaml currently mandates only "smallest human review
      surface needed for decision and mergeback" without forcing residual disclosure.
    what_this_patch_improves: >
      makes residual disclosure mandatory in every review_packet,
      lowering the chance of silent T4 → T3 promotion and missed truth conflicts.

  proposed_change:
    target_file_or_surface:
      primary: 02_packets/review_packet.v0.yaml
      secondary: 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md
    exact_change_summary: >
      add 7 minimum required fields to review_packet schema;
      add corresponding field definitions to packet field dictionary.
    proposed_minimum_fields_or_rules:
      - expected_state         # what the reviewer/agent claimed should hold
      - actual_state           # what was actually produced or observed
      - residuals              # the gap, broken into typed sub-fields (see § 12.2)
      - validation_gap         # what was not yet checked
      - truth_conflicts        # explicit conflicts with canonical truth files
      - decision_needed        # human/governance decision required to proceed
      - stop_condition_status  # whether a stop condition was met or escalated
    non_goals:
      - this is NOT a new packet family
      - this is NOT a truth promotion gate
      - this does NOT modify task_packet or memory_packet
      - this does NOT introduce score-based auto-acceptance

  governance_boundary:
    canonical_truth_changed: true   # review_packet.v0.yaml is canonical
    human_approval_required: true
    cannot_promote_from:
      - T4_execution_feed
      - T5_ephemeral_cache_or_session_state
    score_or_signal_is_evidence_not_truth: true

  change_impact_check:
    impacted_truth_files:
      - 02_packets/review_packet.v0.yaml
      - 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md
    must_also_check_per_change_impact_map_§_4:
      - 02_packets/packet_common_shell.v0.yaml  # shell field collision
      - 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md  # only if packet identity changes
    impacted_packet_or_runtime_surfaces:
      - any L4 mergeback flow that produces review_packet
    impacted_zh_TW_human_docs:
      - 06_human_docs/zh-TW/SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md  # only if review primitive explanation needs update
    deferred_impacts:
      - validator scripts (none built yet)
      - memory-plane harness (only if review packets feed shared memory)
    reason_for_deferral: validators and harness are not yet implementation surfaces in v0

  acceptance_criteria:
    - reduces named failure mode "review filed without naming residual"
    - does not flatten T2/T3/T4 boundaries
    - all 7 fields have machine-stable shape (string | structured | enum)
    - rejection boundary is explicit: not a success-story format, not a promotion gate

  rejection_boundary:
    reject_if:
      - patch expands scope beyond the 7 minimum fields
      - patch adds promotion semantics to review_packet itself
      - patch references runtime infrastructure not yet built (validators, harness)
      - patch lets review_packet contents auto-promote any T4/T5 state to T2/T3

  reviewer_decision:
    decision: <to be filled by human reviewer>
    required_revision_notes: <to be filled if decision = revise>
```

> drafter note: when filling this for real, run a field-collision check
> against the actual contents of review_packet.v0.yaml and packet_common_shell.v0.yaml
> before submitting. The 7 minimum_fields above are the *target shape*, not a
> conflict-free addition.

This document captures the current session’s high-value design material before continuing the v4 cross-domain reading program.

The immediate problem: if every strong external insight is sent into a passive `draft` area and only reviewed after shadowMAS is “already designed,” the insight arrives too late. shadowMAS is still forming. Strong research signals must enter an active design lane early, while still avoiding uncontrolled canonical pollution.

Therefore, this document is not a cold archive. It is a **hot intake / active design patch log**.

The intended workflow is:

```text
External research / uploaded paper / discussion insight
→ active design log
→ ToT×MoE×LATS candidate filtering
→ accepted / rejected / deferred decision
→ controlled change-impact review
→ possible canonical patch later
```

This preserves two goals at once:

1. **Move fast enough to not miss architecture-level insights.**
2. **Keep truth, authority, auditability, and promotion boundaries intact.**

---

## 1. Current strategic correction

Earlier framing mistake:

```text
Cross-domain insights → memory design only
```

Correct framing:

```text
Cross-domain insights → whole-system design kernel
```

The v4 research synthesis is not merely about memory. It is a cross-domain system-design source drawing from thermodynamics, information theory, biology, mathematics, neuroscience, cognitive science, linguistics, and AI architecture.

For shadowMAS, its value is not “one more module.” Its value is a set of design lenses for:

- compression
- residual reporting
- recursive coordination
- state transfer
- agent communication bottlenecks
- evaluation drift
- system phase transitions
- capability routing
- prompt / construction framing
- small-model efficiency
- human-auditable governance over non-human computation

---

## 2. Working position: hot adoption, not blind adoption

### 2.1 Accepted principle

Strong ideas should be allowed to affect design immediately as **candidate architecture patches**.

### 2.2 Rejected extremes

#### Rejected: wait until all design is finished

Reason:

If research signals are only reviewed after shadowMAS is finalized, they can no longer shape the architecture. That turns the research program into decoration.

#### Rejected: directly canonicalize every impressive paper

Reason:

External papers can inspire architecture, but cannot automatically override shadowMAS governance truth, human authority, auditability, or promotion boundaries.

#### Rejected: clone external systems blindly

Reason:

RecursiveMAS, WFGY, predictive coding, free energy, or information geometry may provide powerful design signals, but shadowMAS has its own identity: governance, truth control, review, promotion, memory boundary, runtime boundary, and mergeback safety.

### 2.3 Accepted lane

```text
Research signal
→ active candidate
→ design lens / heuristic / operational rule / validated rule classification
→ ToT×MoE×LATS decision
→ impact review before canonical change
```

---

## 3. Key concept: KL divergence

### 3.1 Full name

KL = **Kullback–Leibler Divergence**.

Chinese terms often used:

```text
庫爾貝克－萊布勒散度
相對熵
relative entropy
```

### 3.2 Feynman explanation

KL asks:

> How different is my model of the world from the actual world?

Let:

```text
P = true distribution / target distribution
Q = model distribution / predicted distribution
```

Then:

```text
KL(P || Q) = Σ P(x) log(P(x) / Q(x))
```

Meaning:

```text
For each possible event x:
  P(x) says how often it really happens.
  Q(x) says how often your model expects it.
  P(x) / Q(x) says how wrong the model is for that event.
  log turns that mismatch into information cost.
  Σ adds the cost across all possible events.
```

Plain-language version:

> KL measures how much extra information cost you pay when you use the wrong model to explain the real world.

### 3.3 Example

True weather:

```text
P(rain) = 70%
P(no rain) = 30%
```

Your model:

```text
Q(rain) = 50%
Q(no rain) = 50%
```

KL measures the extra information cost of using the 50/50 model in a 70/30 world.

If Q becomes 70/30, KL approaches zero.

### 3.4 KL is directional

```text
KL(P || Q) ≠ KL(Q || P)
```

This matters. “How badly Q explains P” is not the same as “how badly P explains Q.”

For AI system design, this directional nature is important because different design questions have different reference distributions:

```text
actual data distribution vs model distribution
expected governed state vs actual execution state
canonical truth state vs retrieved memory state
human-intended task shape vs agent-produced output shape
```

### 3.5 Why KL may be first-rank in AI system design

Many AI problems can be phrased as:

```text
Make model distribution Q closer to target distribution P.
```

Examples:

```text
Training:
  Q = model prediction distribution
  P = data distribution

Compression / MDL:
  Q = compact model/code
  P = data to describe

Predictive coding:
  Q = prediction
  P = actual input

Free energy principle:
  Q = recognition density
  P = generative / posterior density

Bayesian model evidence:
  Q = model class with parameters
  P = observed data, with complexity penalty
```

### 3.6 shadowMAS translation

For shadowMAS, KL should not be reduced to a training loss. It is more useful as a **system-design grammar**:

```text
Every governance mechanism should explain what divergence, surprise, residual, description length, or complexity cost it reduces.
```

Candidate shadowMAS divergence pairs:

```yaml
expected_scope vs actual_scope
expected_authority_boundary vs actual_authority_boundary
expected_artifact_shape vs actual_artifact_shape
expected_truth_touchpoints vs actual_truth_touchpoints
expected_runtime_behavior vs actual_runtime_behavior
expected_review_surface vs actual_review_surface
canonical_truth vs execution_feed
project_truth vs shadowMAS_governance_export
```

### 3.7 Important boundary

KL / divergence is an optimization lens.

Human authority, auditability, protected truth promotion, and safety gates are not erased by KL. They become boundary conditions, constraints, priors, masks, or promotion thresholds.

Correct framing:

```text
KL / divergence / free energy = optimization direction
human authority / audit / promotion gate = governance boundary condition
```

Incorrect framing:

```text
Everything is KL, so human authority can be optimized away.
```

---

## 4. Key concept: residual-first

### 4.1 Feynman explanation

Residual means:

> the remaining difference between what was expected and what actually happened.

Example: painting a wall.

Expected:

```text
Paint all walls white.
Do not dirty the floor.
Finish before 5 PM.
```

Bad completion-first report:

```text
Done.
```

Better residual-first report:

```text
Completed:
  Three walls painted.

Residuals:
  Fourth wall only half-painted because paint ran out.
  Two floor spots have paint drops.
  Finished 30 minutes late.

Decision needed:
  Buy more paint?
  Is floor cleanup part of this task?
```

Residual-first means:

> Do not begin with a success story. Begin with the difference between expected and actual.

### 4.2 Machine learning relation

```text
prediction = what the system expected
actual = what happened
residual / prediction error = actual - prediction
```

In predictive coding, higher levels send predictions downward, and lower levels send residual errors upward.

### 4.3 Paper grounding: Rao & Ballard 1999

Core paper insight:

- Feedback connections from higher visual areas carry predictions of lower-level neural activity.
- Feedforward connections carry residual errors between predictions and actual lower-level activity.
- Some extra-classical receptive-field effects can be interpreted as residual error detectors.
- When a stimulus is predictable from surrounding context, residual error is suppressed.
- When a stimulus violates natural-image statistics, residual error remains high.

System-design translation:

```text
Do not transmit all raw state upward.
Transmit what remains unexplained.
```

For shadowMAS:

```yaml
review_packet:
  expected:
  actual:
  residuals:
    expectation_mismatch:
    unresolved_questions:
    truth_conflicts:
    scope_drift:
    validation_gap:
  next_decision:
```

### 4.4 Paper grounding: Friston 2005

Core paper insight:

- Perceptual inference and perceptual learning can both be understood as minimizing free energy.
- Predictive coding adjusts the state of the generative model until prediction error is minimized.
- Hierarchical generative models allow higher levels to provide context-sensitive priors to lower levels.
- Cortical responses can be understood as transient expressions of prediction error.
- Learning reduces prediction error across repeated stimuli.

System-design translation:

```text
A system should compare expected governed state against actual execution state, then reduce the divergence.
```

For shadowMAS:

```yaml
governance_divergence_check:
  expected_scope:
  actual_scope:
  expected_authority_boundary:
  actual_authority_boundary:
  expected_artifact_shape:
  actual_artifact_shape:
  expected_truth_touchpoints:
  actual_truth_touchpoints:
  divergence_tier: low | medium | high | blocker
```

### 4.5 Security value

Completion-first can hide failure.

Residual-first exposes:

- missing work
- scope drift
- uncertain assumptions
- truth conflicts
- failed validation
- hidden risk

This makes it harder for agents to “summary-launder” bad work.

---

## 5. Key concept: representation and state transfer

### 5.1 Representation

Representation means:

> turning something into a form that a system can process, compare, route, compress, or compute more effectively.

The same task can have multiple representations.

Example input:

```text
判斷這個任務能不能交給 Codex。
```

Text representation:

```text
判斷這個任務能不能交給 Codex。
```

Structured representation:

```yaml
task_type: implementation_decision
executor_candidate: Codex
risk: unknown
missing_rules:
  - repo_scope
  - acceptance_criteria
  - safety_boundary
```

Graph representation:

```yaml
nodes:
  - task
  - codex
  - repo_scope
  - risk
  - acceptance_criteria
edges:
  - task_requires_repo_scope
  - codex_requires_acceptance_criteria
  - risk_depends_on_safety_boundary
```

Embedding representation:

```text
A vector that preserves semantic similarity for retrieval/routing.
```

Latent representation:

```text
Hidden model state inside a neural network.
Usually not directly human-readable.
Often unavailable in closed models.
```

### 5.2 State transfer

State transfer means:

> passing a useful representation of current task state from one agent/runtime/module to another.

This can happen at several levels:

```yaml
state_transfer_lane:
  level_0_text:
    example: natural language summary
    availability: universal
    auditability: high
    efficiency: low_to_medium

  level_1_structured:
    example: YAML / JSON packet
    availability: high
    auditability: high
    efficiency: medium_to_high

  level_2_embedding:
    example: vector / semantic key / retrieval handle
    availability: medium
    auditability: medium_low
    efficiency: high_for_search

  level_3_tool_state:
    example: repo diff, test result, AST, execution trace
    availability: depends_on_tool
    auditability: medium_to_high
    efficiency: high_for_execution

  level_4_latent_handle:
    example: hidden state / activation tensor / model-internal state
    availability: low_for_closed_models
    auditability: low_without_projection
    efficiency: potentially_very_high
```

### 5.3 Important correction

Do not require all agents to expose latent states.

Reason:

- closed models usually do not expose hidden states
- different models have incompatible hidden dimensions
- latent projection may require training
- latent state is not naturally auditable
- hidden state may carry sensitive information
- portability across runtimes may fail

### 5.4 Accepted design direction

Use a general abstraction:

```yaml
state_capsule:
  state_kind: text | structured | embedding | tool_state | latent_handle
  producer_agent:
  consumer_agent:
  projection_method:
  visible_summary:
  audit_projection:
  confidence:
  discard_policy:
  security_notes:
```

Latent transfer becomes an optional high-end implementation, not a required v0 capability.

### 5.5 Rejected design direction

```yaml
rejected:
  require_latent_from_all_models:
    reason: unavailable in many runtimes

  hidden_state_replaces_packet:
    reason: packets are audit surfaces; hidden state is not

  hidden_state_as_truth_source:
    reason: latent state may guide computation but cannot arbitrate truth

  gradient_based_cooptimization_in_v0:
    reason: many shadowMAS runtimes do not expose gradients or training access
```

---

## 6. RecursiveMAS shock integration

### 6.1 Why RecursiveMAS matters

RecursiveMAS is treated in this session as a major external shock input because it challenges the default assumption that multi-agent systems should communicate mainly through text messages.

The key signal:

```text
Text-only communication between agents creates serialization cost, token cost, and state reconstruction loss.
```

RecursiveMAS proposes a direction closer to:

```text
multi-agent collaboration as recursive state computation
```

Its public summary claims performance gains such as improved accuracy, speedup, and token reduction through recursive latent-space state transfer. The exact claims still require direct paper reading and verification, but the design signal is important even before full adoption.

### 6.2 What shadowMAS should absorb now as candidates

```yaml
candidate_accept:
  recursive_runtime_lane:
    reason: shadowMAS R-layer is not finalized; recursive loops should be considered as runtime primitives.

  state_transfer_abstraction:
    reason: text-only MAS is a real bottleneck; state transfer can be implemented at multiple levels without requiring latent access.

  inner_outer_loop_separation:
    reason: inner loop can optimize agent computation; outer loop preserves governance, review, promotion, and human authority.

  recursive_residual_review:
    reason: recursive systems need per-round delta, residual, improvement, degradation, and stop-condition tracking.

  text_bottleneck_reduction_target:
    reason: token reduction is not just cost optimization; it changes MAS architecture.
```

### 6.3 What shadowMAS should reject or defer

```yaml
candidate_reject:
  clone_recursiveMAS:
    reason: shadowMAS is not primarily a trainable latent MAS framework; it is a governance/runtime/review/truth-boundary system.

  mandatory_latent_access:
    reason: many runtimes cannot provide hidden state.

  latent_state_as_canonical_truth:
    reason: hidden state cannot replace reviewable truth artifacts.

  pure_gradient_inner_outer_training_in_v0:
    reason: v0 likely operates across host runtimes without model-training access.
```

### 6.4 Candidate inner / outer loop model

```yaml
inner_loop:
  purpose: recursive agent computation and refinement
  may_use:
    - text state
    - structured packet state
    - embedding handles
    - tool execution state
    - latent handles when available
  stop_by:
    - residual threshold
    - loop budget
    - convergence check
    - risk escalation

outer_loop:
  purpose: governance review and promotion control
  owns:
    - human gate
    - truth promotion
    - audit surface
    - mergeback approval
    - protected decision boundary
```

### 6.5 Runtime implication

R-layer should not be limited to queue / worker / retry / timeout. Candidate future R-layer should include:

```yaml
r_layer_candidate_primitives:
  - recursion_loop
  - state_capsule_transport
  - state_projection
  - residual_feedback
  - convergence_stop_rule
  - loop_budget
  - audit_surface_projection
  - risk_escalation_trigger
```

---

## 7. WFGY as representation compiler candidate

### 7.1 Current claim from discussion

WFGY is described in discussion as having a mathematical formula that can transform problems into a special representation, reportedly enabling small models to save around 6× tokens while performing comparably to or better than larger models in some cases.

This claim is not yet verified in this document.

### 7.2 Why it matters

If true, WFGY may not merely be a prompting trick. It may be a:

```text
problem representation compiler
```

Potential pipeline:

```text
natural language problem
→ mathematical / structural / control representation
→ small model reasoning lane
→ lower token cost with preserved or improved performance
```

### 7.3 Candidate relation to KL / MDL

WFGY may connect to KL / MDL if it does one or more of the following:

```text
reduces description length
preserves decision-relevant information
removes irrelevant surface form
improves routing geometry
reduces model-world divergence
shrinks reasoning search space
```

### 7.4 Candidate relation to shadowMAS

```yaml
wfgy_candidate_roles:
  small_model_lane_compiler:
    value: allow local / cheaper models to perform higher-quality structured reasoning

  task_shape_encoder:
    value: classify and transform task into better computational form

  routing_language_candidate:
    value: represent tasks in a way that improves agent selection and packet construction

  compression_subsystem:
    value: reduce token load before agent execution
```

### 7.5 Current rejection boundary

Do not make WFGY the official shadowMAS DSL yet.

Reason:

```yaml
reasons:
  - formula and evidence not yet audited in this session
  - correctness and traceability impact unknown
  - compatibility with packet schema unknown
  - risk of opaque compression unknown
```

### 7.6 Suggested future round

```yaml
round_wfgy:
  theme: WFGY as problem representation compiler
  questions:
    - What exactly is the formula?
    - What input does it transform?
    - What output representation does it produce?
    - Does it reduce tokens or reduce reasoning search space?
    - What correctness is preserved?
    - What information is discarded?
    - Can humans audit it?
    - Can it become a small-model lane in shadowMAS?
  possible_decisions:
    - adopt_as_design_lens
    - adopt_as_optional_compiler
    - use_as_reference_only
    - reject_for_shadowMAS
```

---

## 8. Paper content captured in this session

This section embeds current high-value paper insights so the document remains useful without opening the original papers.

---

### 8.1 MacKay — Bayesian evidence / hyperparameters / high-dimensional inference

#### Central theme

MacKay compares approaches to Bayesian hierarchical models with unknown hyperparameters, especially regularization constants.

The major methods:

```text
Evidence framework:
  integrate over model parameters
  maximize evidence over hyperparameters
  then use optimized hyperparameters for posterior approximation

MAP method:
  integrate over hyperparameters first
  maximize posterior over model parameters
  then approximate around that maximum
```

#### Key insight 1: evidence framework has levels

Bayesian inference can be divided into levels:

```text
Level 1:
  infer parameters w for given hyperparameter α

Level 2:
  infer α using evidence from Level 1

Level 3:
  compare models using evidence
```

Pattern:

> the normalizing constant from a lower level becomes the data-dependent factor at the next higher level.

shadowMAS mapping:

```text
execution result → review evidence
review evidence → promotion evidence
promotion evidence → truth update decision
```

This supports multi-level governance rather than flat “agent says done.”

#### Key insight 2: high-dimensional maxima can be misleading

MacKay emphasizes that in high-dimensional spaces, probability density maxima may have little probability mass.

Example intuition:

```text
In high dimensions, most volume of a sphere is near the surface.
For a high-dimensional Gaussian, most mass is in a thin shell far from the density maximum.
```

Therefore:

```text
maximum density point ≠ representative state
```

shadowMAS mapping:

```text
One impressive agent answer may be a high-density-looking local maximum.
It does not necessarily represent the true mass of evidence.
Review must examine uncertainty, alternatives, residuals, and evidence spread.
```

#### Key insight 3: MAP can be biased in ill-posed problems

MacKay’s widget example shows that adding unmeasured / ill-determined parameters can cause the MAP approach to over-regularize and squash estimates toward zero, while evidence framework remains stable when the well-determined parameter count is handled correctly.

shadowMAS mapping:

```text
Do not let unknown or poorly determined regions distort well-supported regions.
```

Candidate rule:

```yaml
evidence_quality:
  well_determined:
  poorly_determined:
  unknown:
  do_not_let_unknowns_dominate_knowns: true
```

#### Key insight 4: complexity penalty is built into evidence

Bayesian evidence penalizes overly flexible or overcomplex models.

shadowMAS mapping:

```yaml
complexity_rent:
  added_surface:
  reason_needed:
  reduced_governance_surprise:
  added_review_cost:
  added_maintenance_cost:
  removal_condition:
```

Candidate principle:

> Every new rule, field, agent, adapter, memory lane, or runtime primitive must pay complexity rent.

---

### 8.2 Rao & Ballard — predictive coding in the visual cortex

#### Central theme

The visual system may use hierarchical predictive coding:

```text
higher level → sends prediction downward
lower level → sends residual error upward
```

The system learns statistical regularities of natural images and signals deviations from those regularities.

#### Key insight 1: feedback carries predictions

In the model:

- feedback pathways carry predictions of lower-level activity
- feedforward pathways carry residual errors
- errors correct higher-level estimates
- prediction and error-correction cycles occur concurrently across the hierarchy

shadowMAS mapping:

```text
higher governance layer sends expected task / artifact / scope shape
execution layer returns residual, not just full raw output
```

#### Key insight 2: residual error detectors

Some visual neurons can be interpreted as error detectors. They respond strongly when input is not predicted by context.

Example:

- Short isolated bars are less predictable from natural-image context, so residual error is high.
- Longer bars extending beyond the classical receptive field are more predictable, so residual error is suppressed.

shadowMAS mapping:

```text
A good review system should respond strongly to deviations from expected structure, not to every raw detail.
```

#### Key insight 3: disabling feedback changes behavior

In the model, disabling top-down feedback eliminated endstopping in most model neurons.

shadowMAS mapping:

```text
Without top-down expectation, the system cannot distinguish expected vs unexpected execution states.
```

This supports explicit expected-vs-actual review.

#### Candidate review structure

```yaml
expected_vs_actual:
  expected_scope:
  actual_scope:
  expected_output_shape:
  actual_output_shape:
  expected_risk:
  actual_risk:

residuals:
  prediction_error:
  unexplained_output:
  missing_expected_component:
  unexpected_extra_component:
```

---

### 8.3 Friston — A theory of cortical responses

#### Central theme

Friston attempts to explain evoked cortical responses through perceptual inference and learning. The brain is framed as using hierarchical generative models and empirical Bayes.

Core claim:

```text
Perceptual inference and perceptual learning can both be resolved by minimizing free energy.
```

#### Key insight 1: inference and learning share the same objective

Friston explains that both the E-step and M-step in an EM-like scheme maximize the same objective function, equivalent to minimizing free energy / surprise.

shadowMAS mapping:

```text
Runtime execution and governance learning should not be separate chaos.
Both should reduce governance surprise:
  execution improves task state
  review improves system expectation and rule quality
```

#### Key insight 2: hierarchical generative models provide priors

Higher levels provide context-sensitive priors for lower levels.

shadowMAS mapping:

```text
Governance layers provide expectations to execution layers.
Execution layers return residuals to update review and routing.
```

#### Key insight 3: forward and backward functional asymmetry

Friston describes a functional asymmetry:

- backward connections generate predictions / contextual priors
- forward connections convey prediction error

This is counterintuitive because “forward” in anatomy can function as feedback in the predictive system.

shadowMAS mapping:

```text
A lower-level execution report is not necessarily “the truth.”
It is feedback/error signal relative to governance expectation.
```

#### Key insight 4: learning suppresses future prediction error

Repeated exposure reduces prediction error. Novel or deviant stimuli produce stronger error signals.

shadowMAS mapping:

```text
If the same project pattern recurs, shadowMAS should require less repeated raw explanation, but still preserve residual reporting.
```

Potential use:

```yaml
pattern_learning:
  repeated_task_shape:
  expected_packet_shape:
  reduced_review_load:
  residual_trigger_for_full_review:
```

---

### 8.4 Amari / Oizumi / Tsuchiya — Geometry of information integration

#### Central theme

Information geometry can quantify how much information integration is lost when a causal dynamical system is split into parts.

They define integrated information as minimized KL divergence between:

```text
full model p(x, y)
split model q(x, y)
```

Formula idea:

```text
Φ = min_q KL[p(x, y) : q(x, y)]
```

This measures how much information is lost by splitting the system.

#### Key insight 1: splitting is a geometric projection problem

Different split models define different submanifolds. The closest split model is found by minimizing KL divergence.

shadowMAS mapping:

```text
When shadowMAS splits work across agents, it should measure or at least reason about integration loss.
```

Candidate rule:

```yaml
decomposition_check:
  original_task:
  split_tasks:
  lost_cross_dependencies:
  required_reintegration:
  integration_loss_risk: low | medium | high
```

#### Key insight 2: not all splits are equal

The paper compares multiple split models:

- fully split model
- diagonally split graphical model
- causally split / geometric model
- mismatched decoding model

Some satisfy natural requirements better than others, such as:

```text
0 ≤ Φ ≤ I(X; Y)
```

shadowMAS mapping:

```text
Task decomposition is not free.
A clean-looking split can remove important causal dependencies.
```

#### Key insight 3: causal split is different from superficial graph split

In Gaussian cases, deleting graphical branches is not necessarily equivalent to deleting causal influence.

shadowMAS mapping:

```text
Moving a task into another packet or agent does not necessarily remove dependency.
Superficial separation is not true causal separation.
```

Candidate design implication:

```yaml
handoff_packet:
  dependency_preservation:
    known_cross_dependencies:
    removed_context:
    causal_dependency_risk:
    reintegration_notes:
```

---

## 9. v4 synthesis currently imported

The uploaded v4 synthesis frames itself as a compressed result of a 50-node LATS search across multiple domains. It uses three merge-type labels:

```text
[MATH-EQ]
  Mathematical equivalence. Same object, different language.

[DEEP-ISO]
  Deep structural isomorphism. Same computation or dynamics, not yet proven identical.

[CONCEPT-PAR]
  Conceptual parallel. Structurally analogous; useful for hypotheses.
```

Important honesty rule from v4:

```text
Scores are ordinal within each round, not absolute across all rounds.
```

### 9.1 U-I: KL Divergence Minimization

v4 marks U-I as `[MATH-EQ]` and claims seven frameworks are operationalizations of minimizing KL divergence:

```text
Renormalization Group
Minimum Description Length
Information Geometry
Predictive Coding
Free Energy Principle
VAE / ELBO
Bayesian Occam's Razor
```

Current shadowMAS conclusion:

```text
Do not treat this as mere metaphor.
Do not instantly turn it into rigid canonical math law either.
Use it as the first system-design grammar.
```

Accepted U-I kernel:

```yaml
compression_residual_occam_kernel:
  - shortest_sufficient_governance_description
  - residual_first_review
  - governance_surprise_minimization
  - projection_distortion_record
  - complexity_rent
```

### 9.2 U-II: Hierarchical Compression

v4 claims Category Theory and Synergetics describe hierarchical compression from static and dynamic sides.

Current pending question:

```text
Can shadowMAS layers be treated as real hierarchical compression and convergence structure, not just file organization?
```

Likely next round after this document:

```yaml
round_2:
  theme: U-II Hierarchical Compression
  questions:
    - Are L/T/R layers compression scales?
    - Does slaving principle inform runtime adapter / PEFT / prompt layering?
    - Can packet composition be treated as categorical composition?
    - What convergence path should shadowMAS enforce?
```

### 9.3 C-I: Stigmergy × Quorum Sensing × Predictive Coding

v4 proposes a shared environment field where agents deposit prediction-error-like signals.

Mechanism:

```text
agent reads field
agent acts
agent computes local prediction error
agent deposits signal into field
field decays with TTL
when field crosses threshold, quorum trigger changes group behavior
```

Current shadowMAS candidate:

```yaml
signal_field_candidate:
  channels:
    trail: successful path / residual decreased
    alarm: failure / error / residual spike
    territory: claimed work / prevent duplication
  properties:
    ttl:
    decay:
    threshold:
    audit_projection:
```

Important: this is not merely memory. It is coordination substrate.

---

## 10. Candidate design decisions from current session

### 10.1 Accepted candidates

```yaml
accepted_candidates:
  hot_adoption_lane:
    reason: research insights must affect architecture before design freezes

  KL_as_system_design_grammar:
    reason: strongest cross-domain unifier; useful for compression, prediction, evidence, and divergence thinking

  residual_first_review:
    reason: directly supported by predictive coding; improves auditability

  state_transfer_abstraction:
    reason: absorbs RecursiveMAS signal without requiring inaccessible latent states

  recursive_runtime_lane:
    reason: R-layer is still open; recursive computation should be considered

  complexity_rent:
    reason: prevents shadowMAS from becoming giant prompt / giant governance blob

  projection_distortion_record:
    reason: cross-layer transformations should record preserved, compressed, discarded, and inferred content

  WFGY_as_research_candidate:
    reason: possible problem representation compiler; needs verification
```

### 10.2 Rejected candidates

```yaml
rejected_candidates:
  memory_only_interpretation:
    reason: v4 is system-wide, not memory-only

  passive_draft_until_final_design:
    reason: research signal would arrive too late

  mandatory_latent_access:
    reason: impossible across many runtimes

  hidden_state_replaces_packets:
    reason: packets are audit surfaces

  hidden_state_as_truth:
    reason: hidden state cannot arbitrate canonical truth

  direct_clone_of_recursiveMAS:
    reason: shadowMAS is governance/runtime/review layer, not simply a latent MAS training framework

  WFGY_as_official_DSL_now:
    reason: not yet audited enough

  KL_as_human_authority_replacement:
    reason: KL is optimization lens, not final authority layer
```

### 10.3 Deferred candidates

```yaml
deferred_candidates:
  literal_KL_mathematical_constitution:
    reason: many governance objects do not yet have formal distributions

  full_information_geometry_layer_model:
    reason: promising but needs deeper work

  signal_field_runtime:
    reason: high value but needs design constraints and audit model

  recursive_state_capsule_schema:
    reason: promising but should follow RecursiveMAS shock round

  WFGY_small_model_lane:
    reason: needs formula and evidence audit
```

---

## 11. ToT×MoE×CoT×LATS — current round snapshot

### 11.1 ToT branches

```yaml
tot_branches:
  A_wait_in_draft_until_later:
    decision: rejected
    reason: too slow; prevents architecture learning during formation

  B_blindly_merge_all_papers:
    decision: rejected
    reason: creates truth contamination

  C_hot_adoption_with_governance:
    decision: accepted
    reason: lets insights affect design while preserving impact review

  D_require_latent_state_everywhere:
    decision: rejected
    reason: technically unavailable and non-portable

  E_state_transfer_abstraction:
    decision: accepted
    reason: captures RecursiveMAS insight at implementable abstraction level

  F_residual_first_review:
    decision: accepted
    reason: strong grounding in predictive coding and security value

  G_KL_as_first_design_grammar:
    decision: accepted_as_lens
    reason: high unification strength; not yet rigid formal law

  H_WFGY_official_DSL_now:
    decision: rejected_for_now
    reason: insufficient audit

  I_WFGY_as_representation_compiler_candidate:
    decision: accepted_for_research
    reason: high potential relevance to token efficiency and small-model lanes
```

### 11.2 MoE votes

```yaml
moe_votes:
  CEO:
    priority:
      - do not let research arrive too late
      - upgrade shadowMAS from orchestration to governance over recursive computation
    warning:
      - do not freeze architecture before absorbing strong signals

  CTO:
    priority:
      - state transfer abstraction
      - recursive runtime lane
      - residual-first review
      - projection records
    warning:
      - do not require latent access from closed models

  Security:
    priority:
      - visible audit projection
      - hidden state must not become truth
      - residuals must expose drift and validation gaps
    warning:
      - latent state can hide sensitive context and cannot be directly reviewed

  CFO:
    priority:
      - token bottleneck reduction
      - complexity rent
      - avoid training-heavy architecture without ROI
    warning:
      - every new runtime primitive increases maintenance cost

  CSO:
    priority:
      - RecursiveMAS and WFGY as design shock inputs
      - preserve sharp positioning
      - avoid paper warehouse mode
    warning:
      - do not overbuild before deciding what problem each primitive solves
```

### 11.3 LATS best node

```yaml
best_node:
  name: Hot Adoption with Implementable Abstractions
  decision: accepted
  score: high
  rationale:
    - lets strong research shape shadowMAS now
    - avoids impossible latent requirement
    - preserves auditability through visible projection
    - supports recursive runtime design without cloning RecursiveMAS
    - keeps KL as first design grammar without erasing governance boundaries
```

---

## 12. Proposed shadowMAS additions for future review

These are not canonical yet. They are active candidate patches.

### 12.1 New design primitive: state capsule

```yaml
state_capsule:
  id:
  state_kind: text | structured | embedding | tool_state | latent_handle
  producer:
  consumer:
  task_scope:
  projection_method:
  visible_summary:
  audit_projection:
  preserved_information:
  discarded_information:
  inferred_information:
  confidence:
  ttl:
  discard_policy:
  security_notes:
```

### 12.2 New review primitive: residual-first report

```yaml
residual_first_report:
  expected_state:
  actual_state:
  residuals:
    expectation_mismatch:
    unresolved_questions:
    truth_conflicts:
    scope_drift:
    validation_gap:
    degraded_dimensions:
    improved_dimensions:
  decision_needed:
  stop_condition_met:
```

### 12.3 New runtime primitive: recursive lane

```yaml
recursive_runtime_lane:
  loop_goal:
  initial_state:
  state_transfer_method:
  iteration_budget:
  residual_threshold:
  convergence_check:
  escalation_rule:
  audit_projection_interval:
  final_review_surface:
```

### 12.4 New governance primitive: complexity rent

```yaml
complexity_rent:
  added_surface:
  reason_needed:
  expected_benefit:
  reduced_divergence:
  added_maintenance_cost:
  added_review_cost:
  added_security_surface:
  removal_condition:
```

### 12.5 New decomposition primitive: integration loss check

```yaml
decomposition_integration_check:
  original_problem:
  proposed_split:
  lost_dependencies:
  preserved_dependencies:
  reintegration_required:
  integration_loss_risk: low | medium | high
  audit_notes:
```

---

## 13. Current answer to the six user questions

### Q1. If latent cannot be obtained, is adding it useless?

No, but mandatory latent transfer should be rejected.

Useful abstraction:

```text
state transfer, with latent as optional highest-level implementation
```

Do not require all models to expose latent states.

### Q2. Is the cost of requiring latent counted?

It must be counted.

Cost categories:

```yaml
latent_cost:
  access_cost:
  adapter_cost:
  training_cost:
  audit_cost:
  security_cost:
  portability_cost:
  maintenance_cost:
```

### Q3. Should we hard-swallow RecursiveMAS?

No.

Use ToT / MoE / LATS to accept state-transfer and recursive-runtime primitives while rejecting impossible latent requirements and hidden truth replacement.

### Q4. What is KL and why study it deeply?

KL = Kullback–Leibler Divergence. It measures directional information loss when using one distribution to model another. It appears across training, compression, predictive coding, free energy, evidence, and possibly governance design. It is likely the first major design lens for shadowMAS, but not a replacement for authority or audit.

### Q5. Is representation transfer just classifying questions and answers?

No.

Representation transfer means converting task state into a form that another agent/model/tool can compute more effectively:

```text
text → structured packet → graph → embedding → tool state → latent handle
```

Classification is only one possible representation.

### Q6. Does WFGY need research?

Yes.

If it truly creates a mathematical representation that lets small models reason with much less token use, it may be highly relevant to shadowMAS compression, routing, and small-model lanes. But it must be audited before adoption.

---

## 14. Next sequence after this document

The user requested:

```text
After capturing this session into one document, continue v4.
```

Recommended next sequence:

```yaml
next_sequence:
  step_1:
    action: continue v4 Round 2
    theme: U-II Hierarchical Compression

  step_2:
    action: insert RecursiveMAS Shock Integration Round
    condition: after reading provided arXiv paper or when user asks

  step_3:
    action: WFGY representation compiler round
    condition: after source/formula is provided

  step_4:
    action: compare U-I/U-II/C-I with RecursiveMAS and WFGY
    output: shadowMAS active architecture patch proposal
```

---

## 15. Round 2 — U-II Hierarchical Compression

> status: active round log  
> theme: U-II · Hierarchical Compression — Static/Dynamic Duality  
> method: 3 full-read targets + 2 companion scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.

---

### 15.1 Round 2 core question

```text
Can shadowMAS layer structure be designed as hierarchical compression and convergence,
rather than mere file organization or prompt organization?
```

Round 1 established the **Compression–Residual–Occam Kernel**:

```yaml
round_1_kernel:
  - shortest_sufficient_governance_description
  - residual_first_review
  - governance_surprise_minimization
  - projection_distortion_record
  - complexity_rent
```

Round 2 asks whether shadowMAS needs a second kernel:

```yaml
round_2_candidate_kernel:
  name: Hierarchy–Convergence Kernel
  question: Are layers not just storage locations, but compression scales and convergence controls?
```

---

### 15.2 Feynman explanation

#### Category Theory side — static structure

Category Theory asks:

```text
If I move from one layer to another, do I preserve the important structure?
```

Simple terms:

```text
Object = thing / state / artifact type
Morphism = allowed transformation between things
Functor = mapping from one structured world to another while preserving composition
Natural transformation = a controlled transformation between mappings
```

For shadowMAS:

```text
A task packet becomes an execution result.
An execution result becomes a review packet.
A review packet becomes a promotion candidate.
A promotion candidate may become truth.
```

The question is not just “can we convert A to B?”

The real question is:

```text
Can A → B → C happen without losing the authority boundary,
truth boundary, reviewability, and traceability?
```

That is the category-theory design lens.

#### Synergetics side — dynamic convergence

Synergetics asks:

```text
When a complex system stabilizes, which few variables control the many details?
```

Simple terms:

```text
Order parameter = slow high-level variable that determines the system pattern
Fast modes = low-level details that change quickly
Slaving principle = fast modes follow the order parameters
```

For shadowMAS:

```text
Order parameters:
  - human authority boundary
  - truth layer status
  - packet family
  - risk tier
  - runtime lane
  - promotion gate
  - review target

Fast modes:
  - exact wording
  - local prompt variants
  - temporary reasoning paths
  - execution attempts
  - retry details
  - intermediate summaries
```

Design implication:

```text
Do not micromanage every fast mode.
Stabilize the order parameters, then let execution details follow.
```

---

### 15.3 Source basis captured in this round

#### v4 U-II claim

v4 frames U-II as hierarchical compression from two sides:

```yaml
category_theory:
  role: static algebraic structure of target hierarchy
  key_objects:
    - functor
    - natural_transformation
  design_use: blueprint the hierarchy
  diagnostic_use: verify compositionality

synergetics:
  role: dynamic convergence toward structure
  key_objects:
    - order_parameter
    - slaving_principle
  design_use: manage convergence path
  diagnostic_use: diagnose stalls or oscillations
```

v4 also proposes:

```text
Fast modes are enslaved by slow modes.
PEFT / LoRA can be interpreted as modifying slow modes while preserving base capabilities.
Backpropagation can be expressed categorically.
Encoder–decoder pairs can be interpreted through adjunction-like optimal bidirectional translation.
```

Current treatment:

```yaml
strong_design_value: yes
canonical_status: not yet
main_risk: over-formalizing shadowMAS before its artifact contracts stabilize
```

---

### 15.4 Evidence cards

#### E1 — Haken / Synergetics / Slaving Principle

Central idea:

```text
In self-organizing systems, many fast microscopic details can become governed by a few slow macroscopic order parameters.
```

The design value is not “biology/physics directly proves shadowMAS.”

The value is:

```text
A complex system becomes controllable when the right slow variables are stabilized.
```

shadowMAS mapping:

```yaml
shadowmas_order_parameters:
  - T-layer truth status
  - L-layer role responsibility
  - R-layer runtime lane
  - packet family
  - risk tier
  - supervision mode
  - promotion gate
  - human authority boundary
```

Candidate operational rule:

```yaml
order_parameter_rule:
  before_execution:
    must_fix:
      - goal
      - scope
      - truth_touchpoints
      - risk_tier
      - packet_family
      - stop_conditions
  during_execution:
    allow_fast_modes_to_vary:
      - wording
      - local implementation path
      - retry strategy
      - temporary notes
  never_allow_fast_modes_to_redefine:
    - human_authority
    - canonical_truth
    - promotion_gate
    - project_domain_truth
```

Accepted insight:

```text
shadowMAS should govern by stabilizing slow variables, not by trying to control every execution detail.
```

---

#### E2 — Category Theory / compositional structure

Central idea:

```text
Category theory organizes formal systems and translations between them.
Its value for system design is preserving structure across mappings.
```

shadowMAS mapping:

```text
Layering is not just a reading order.
Layering is a composition contract.
```

Current shadowMAS already has prompt layers:

```text
Shared Core
shadowMAS Coordination / Governance Shadow
Project Execution
Runtime Adapter Prompt
Host Native / Opaque Prompt
```

Round 2 interpretation:

```text
These layers should be treated as composable mappings with explicit boundaries.
They may be composed operationally, but their source-of-truth ownership must not collapse.
```

Candidate operational rule:

```yaml
layer_composition_record:
  source_layers:
  composed_runtime_context:
  preserved_rules:
  adapted_rules:
  suppressed_rules:
  unresolved_conflicts:
  host_constraints:
```

Accepted insight:

```text
Composition is allowed; flattening ownership is not.
```

---

#### E3 — Cruttwell et al. / Categorical foundations of gradient-based learning

Central idea:

```text
Gradient-based learning algorithms can be given categorical semantics using lenses,
parametric maps, and reverse derivative categories.
```

What this supports:

```text
Learning pipelines and update mechanisms can be understood compositionally.
```

What it does not automatically support:

```text
shadowMAS must implement full categorical ML semantics in v0.
```

shadowMAS mapping:

```yaml
candidate_use:
  - future runtime adapter formalism
  - future recursive learning lane formalism
  - future tool-state update semantics
  - future validator for compositional transformations

not_v0_requirement:
  - formal category-theoretic implementation
  - gradient access from closed models
  - forcing every packet transformation into math notation
```

Accepted insight:

```text
Use category theory as an audit lens for composition, not as mandatory v0 implementation machinery.
```

---

#### E4 — Mehta & Schwab / RG and Deep Learning

Central idea:

```text
Deep learning and variational renormalization group share a formal relationship around hierarchical feature extraction and compression.
```

Useful translation:

```text
Each layer preserves relevant operators and integrates out irrelevant operators.
```

shadowMAS mapping:

```yaml
artifact_hierarchy_as_rg:
  raw_context:
    role: high-detail state
  compiled_intake:
    role: first compression preserving task-relevant variables
  task_packet:
    role: execution-ready compressed state
  review_packet:
    role: decision-ready compressed state
  promoted_truth:
    role: stable macro-level state
```

Candidate rule:

```yaml
compression_layer_check:
  preserved_relevant_information:
  integrated_out_irrelevant_information:
  distortion_notes:
  reversible_refs:
  unsafe_to_compress:
```

Important boundary:

```text
Code diffs, packet YAML, JSON contracts, migrations, field dictionaries, and schema-level truth
must not be lossy-compressed.
```

Accepted insight:

```text
shadowMAS layers should be compression layers only when the compression is inspectable and reversible enough for governance.
```

---

#### E5 — LoRA / PEFT as slow-mode intervention

Central idea:

```text
LoRA freezes base model weights and injects low-rank trainable matrices,
reducing trainable parameters while maintaining strong downstream performance.
```

Round 2 interpretation:

```text
LoRA is not direct proof of Haken’s slaving principle,
but it is compatible with a design pattern:
change a small high-leverage subspace while preserving base capability.
```

shadowMAS mapping:

```yaml
adapter_change_principle:
  prefer:
    - small scoped adapter changes
    - runtime-specific wrappers
    - reversible prompt/runtime modifications
    - explicit projection notes
  avoid:
    - rewriting base truth for runtime convenience
    - modifying project-domain truth from governance layer
    - full-system rule churn for local runtime needs
```

Candidate rule:

```yaml
slow_mode_patch:
  target_order_parameter:
  local_adapter_change:
  preserved_base_behavior:
  rollback_path:
  validation_surface:
```

Accepted insight:

```text
shadowMAS should prefer scoped, reversible, high-leverage changes over full-system rewrites.
```

---

### 15.5 ToT candidate branches

```yaml
tot_branches:
  A_category_theory_as_full_shadowMAS_constitution:
    decision: rejected_for_now
    reason: too heavy; would over-formalize before packet/runtime contracts stabilize

  B_hierarchy_as_file_organization_only:
    decision: rejected
    reason: loses U-II value; layers are governance/compression/convergence structures, not folders

  C_hierarchy_as_compression_and_composition_contract:
    decision: accepted
    reason: preserves static structure and supports artifact flow correctness

  D_synergetics_as_governance_convergence_lens:
    decision: accepted
    reason: order parameters map well to truth/risk/packet/runtime boundaries

  E_LoRA_as_direct_shadowMAS_law:
    decision: rejected
    reason: LoRA is model adaptation technique, not a general governance law

  F_LoRA_as_slow_mode_patch_pattern:
    decision: accepted
    reason: useful analogy for scoped reversible high-leverage changes

  G_adjoint_encoder_decoder_as_immediate_schema_requirement:
    decision: deferred
    reason: promising for RAG/embed-retrieve/state transfer, but needs deeper formal audit

  H_backpropagation_functor_as_v0_requirement:
    decision: rejected_for_v0
    reason: shadowMAS v0 often lacks gradient/model-internal access

  I_compositional_audit_as_design_requirement:
    decision: accepted
    reason: every cross-layer transformation should preserve ownership, truth boundary, and reviewability
```

---

### 15.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + D
    reason: shadowMAS needs a stronger identity: not file layers, but controlled hierarchical governance compression.
    risk: too much category theory can slow productization.

  CTO:
    vote: accept C + D + F + I
    reason: order parameters and compositional audit are directly implementable.
    risk: do not require unavailable gradient or latent access.

  Security:
    vote: accept I strongly
    reason: cross-layer transformation is where truth laundering and authority confusion happen.
    risk: adapter layers may silently mutate governance meaning.

  CSO:
    vote: accept C
    reason: “layer = compression scale + responsibility boundary” is a clear design story.
    risk: if written too abstractly, future agents will not know what to implement.

  CFO:
    vote: accept F cautiously
    reason: scoped patches reduce maintenance cost compared with full rewrites.
    risk: too many adapters create hidden maintenance debt.
```

---

### 15.7 LATS result

```yaml
lats_result:
  best_node:
    name: Hierarchy-Convergence Kernel
    score: 0.91
    status: accepted_kernel
    why:
      - turns layers into compression/convergence structures
      - supports existing prompt layering without flattening
      - gives R-layer and adapter design a convergence model
      - explains why order parameters must be stabilized before execution
      - avoids impossible requirements like mandatory gradients or latent states

  accepted:
    - hierarchy_as_compression_and_composition_contract
    - synergetics_as_governance_convergence_lens
    - slow_mode_patch_pattern
    - compositional_audit_requirement

  rejected:
    - category_theory_as_full_constitution_now
    - hierarchy_as_file_organization_only
    - LoRA_as_direct_governance_law
    - backpropagation_functor_as_v0_requirement

  deferred:
    - adjoint_encoder_decoder_for_state_transfer
    - formal_category_theoretic_packet_validator
    - information_geometry_full_layer_model
```

---

### 15.8 Round 2 accepted kernel

```yaml
hierarchy_convergence_kernel:
  core_sentence: >
    shadowMAS layers are not folders or prompt sections; they are hierarchical
    compression scales and convergence controls. Stable order parameters govern
    fast execution modes, while compositional audit prevents cross-layer truth
    and authority distortion.

  principles:
    - layer_as_compression_scale
    - layer_as_authority_boundary
    - order_parameter_first_execution_second
    - fast_modes_may_vary_slow_modes_must_be_governed
    - composition_allowed_ownership_not_flattened
    - adapter_changes_should_be_scoped_reversible_and_audited
```

---

### 15.9 Candidate shadowMAS primitives from Round 2

#### 15.9.1 Order parameter registry

```yaml
order_parameter_registry:
  task_id:
  stabilized_before_execution:
    - goal
    - scope
    - truth_touchpoints
    - risk_tier
    - packet_family
    - runtime_lane
    - supervision_mode
    - stop_conditions
  allowed_fast_modes:
    - local wording
    - implementation path
    - retry strategy
    - temporary notes
  forbidden_fast_mode_mutations:
    - human authority boundary
    - canonical truth status
    - project-domain truth
    - promotion gate
```

#### 15.9.2 Layer composition record

```yaml
layer_composition_record:
  source_layers:
    - shared_core
    - shadowmas_governance
    - project_execution
    - runtime_adapter
  host_native_constraints:
  preserved_rules:
  adapted_rules:
  suppressed_rules:
  unresolved_conflicts:
  final_runtime_context_summary:
```

#### 15.9.3 Slow-mode patch record

```yaml
slow_mode_patch_record:
  target_order_parameter:
  patch_type: prompt_adapter | runtime_adapter | packet_field | routing_rule | review_rule
  preserved_base_behavior:
  changed_behavior:
  rollback_path:
  validation_surface:
  complexity_rent:
```

#### 15.9.4 Compression layer check

```yaml
compression_layer_check:
  source_artifact:
  target_artifact:
  preserved_relevant_information:
  integrated_out_information:
  unsafe_to_compress:
  distortion_notes:
  reversible_refs:
```

---

### 15.10 Round 2 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may redefine interpretation of layers as compression/convergence controls

  prompt_layering_contract:
    reason: composition record may formalize runtime context assembly

  governance_matrix:
    reason: order parameters may affect role/truth/runtime layer interpretation

  packet_schema_future:
    reason: compression_layer_check and composition_record may become packet shell fields

  runtime_future:
    reason: R-layer may include convergence loop and order-parameter stabilization

  zh_tw_human_docs:
    reason: this is high-value human explanation material
```

No canonical patch should be made yet, but these should be queued for controlled change-impact review.

---

## 16. Document self-optimization — ToT×MoE×CoT×LATS可審查版

> status: document design review  
> object under review: this single active design log  
> goal: avoid becoming a giant surface while preserving high-quality paper content and current-session continuity.

---

### 16.1 Problem diagnosis

The document is intentionally standalone, but it is already at risk of becoming a long mixed surface:

```yaml
risks:
  - too_many_concepts_at_same_level
  - accepted_rejected_deferred_decisions_are_scattered
  - paper_evidence_and_design_decisions_can_blur
  - future_rounds_may_append_without_consolidation
  - user_may_need_to_recall_which_section_holds_current_truth
```

The document should follow the system’s own cognition design rule:

```text
recognition-first, decision-first, chunked, explicit comparison, must-see / secondary / expandable.
```

---

### 16.2 ToT branches for document design

```yaml
document_tot_branches:
  A_raw_append_only:
    decision: rejected
    reason: easiest short term, but becomes giant surface quickly

  B_overcompress_into_short_summary:
    decision: rejected
    reason: loses high-quality paper content and traceability

  C_split_into_many_files_now:
    decision: rejected_for_now
    reason: user explicitly asked for one standalone document

  D_frontload_active_decision_ledger_then_keep_round_logs:
    decision: accepted
    reason: preserves standalone depth while reducing recall burden

  E_rewrite_everything_now_into_perfect_structure:
    decision: deferred
    reason: too much churn; risk of losing content during active research
```

---

### 16.3 MoE votes for document design

```yaml
document_moe_votes:
  CEO:
    vote: D
    reason: one document can continue, but it needs an executive decision ledger at top

  CTO:
    vote: D
    reason: keep round logs, but add stable schema for future updates

  Security:
    vote: D
    reason: accepted vs speculative content must remain visibly separated

  CSO:
    vote: D
    reason: story should start with current decisions, not research history

  CFO:
    vote: D
    reason: reduces future maintenance cost without splitting files prematurely
```

---

### 16.4 LATS result for document design

```yaml
document_lats_result:
  best_node:
    name: Active Decision Ledger + Round Appendices
    score: 0.94
    status: accepted
    reason:
      - preserves single-file requirement
      - reduces recall burden
      - keeps paper evidence available
      - prevents accepted/rejected/deferred decisions from scattering
      - supports future round-by-round updates
```

---

### 16.5 Accepted document structure target

Future updates should gradually reshape this document into:

```text
0. Must-see current decision ledger
1. Active kernels
   1.1 Compression–Residual–Occam Kernel
   1.2 Hierarchy–Convergence Kernel
   1.3 Recursive/State Transfer Candidate Kernel
   1.4 WFGY Candidate Kernel
2. Candidate decision table
   2.1 Accepted
   2.2 Rejected
   2.3 Deferred
3. Round logs
   3.1 Round 1 U-I
   3.2 Round 2 U-II
   3.3 Future rounds
4. Paper evidence cards
5. Candidate shadowMAS primitives
6. Change-impact queue
7. Open questions
```

No full rewrite is performed in this update. The accepted action is:

```yaml
current_action:
  - add Round 2 log
  - add document self-optimization decision
  - preserve previous content
  - restructure only after one or two more rounds if navigation becomes painful
```

---

### 16.6 Document-level accepted rule

```text
Every future round must update two places:
1. its own round log
2. the active decision ledger / accepted-rejected-deferred table
```

This prevents future rounds from becoming isolated appendices that never affect the design state.

---

## 17. Round 3 — C-I Stigmergy × Quorum Sensing × Predictive Coding

> status: active round log  
> theme: C-I · agent coordination without central orchestrator  
> method: 3 full-read targets + 2 companion scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Rao & Ballard and Friston were available as uploaded PDFs. Bassler & Losick was treated as a full-read target conceptually, but this session only had reliable abstract/metadata access, so confidence for fine-grained biological details is downgraded. Companion scans were used for stigmergy history and universal coordination framing.

---

### 17.1 Round 3 core question

```text
Can shadowMAS coordinate multiple agents through a shared signal field instead of relying only on a central orchestrator or direct agent-to-agent text messages?
```

This round follows v4 C-I:

```yaml
C-I_merge:
  stigmergy:
    role: coordination architecture; environment as medium
  quorum_sensing:
    role: threshold-triggered collective mode switching
  predictive_coding:
    role: deposit semantics upgraded from simple trace to information-bearing residual / prediction error
```

Round 3 asks whether shadowMAS should add a third coordination pattern:

```yaml
coordination_patterns:
  central_orchestrator:
    strength: clear control, easier accountability
    weakness: bottleneck, O(n²)-style messaging pressure if everything routes through explicit coordination

  direct_messaging:
    strength: simple, natural for human-readable handoff
    weakness: token-heavy, state reconstruction burden, pairwise coordination explosion

  shared_signal_field:
    strength: local write/read coordination, decay, threshold triggers, less pairwise messaging
    weakness: requires shared writable state, staleness control, audit projection, and truth-boundary protection
```

---

### 17.2 Feynman explanation

Imagine several workers cleaning a large factory.

Bad coordination style:

```text
Everyone must constantly message the manager:
- I am here.
- I found dust.
- Should I clean this?
- Who is already working here?
```

This creates message overload.

Stigmergy style:

```text
Workers leave visible marks in the environment:
- green mark: this path worked
- red mark: danger or error here
- blue mark: someone is already working here
```

Other workers do not need to ask everyone. They look at the shared field and decide locally.

Quorum sensing adds:

```text
If enough red marks accumulate in one zone, everyone switches mode:
from normal exploration → collective convergence on that zone.
```

Predictive coding upgrades the marks:

```text
The mark is not just visited/not visited.
The mark carries residual error:
how much the actual situation differed from expectation.
```

shadowMAS translation:

```text
Agents do not only send messages.
They leave structured, decaying, auditable signals in a shared coordination field.
```

---

### 17.3 Source basis captured in this round

#### v4 C-I claim

v4 proposes:

```yaml
agent_cycle:
  1_read_shared_environment_field: F
  2_execute_task_and_compute_local_prediction_error: ε
  3_deposit_error_into_field: pheromone[zone] += ε
  4_decay_field_with_TTL: pheromone[zone] *= decay_rate_per_tick

field_semantics:
  high_pheromone: high prediction error / high information density / undermodeled region
  low_pheromone: low prediction error / well-modeled region / deprioritize

quorum_trigger:
  condition: F[zone] > θ_Z
  effect: agents switch from individual exploration to collective convergence
```

v4 also states three channel types:

```yaml
pheromone_channels:
  trail:
    trigger: task path succeeded; residual decreased
    ttl: medium
    effect: attract agents toward path

  alarm:
    trigger: failure, error, unexpected residual spike
    ttl: short
    effect: repel or reroute agents around zone

  territory:
    trigger: task claimed or agent currently working
    ttl: task_duration
    effect: prevent duplication
```

---

### 17.4 Evidence cards

#### E1 — Rao & Ballard 1999 / Predictive Coding

Central insight:

```text
A hierarchy can coordinate by sending predictions downward and residual errors upward.
```

In their model:

- each level predicts the level below
- feedforward pathways carry residual errors
- feedback pathways carry predictions
- error signals correct higher-level estimates
- the optimization objective is a sum of squared prediction errors weighted by inverse variance
- the cost can be interpreted as coding cost, connecting predictive coding to minimum description length

shadowMAS mapping:

```text
A coordination field should not store raw chatter only.
It should store residual signals: what was unexpected, unresolved, failed, improved, or already explained.
```

Candidate operational rule:

```yaml
field_deposit:
  zone:
  residual_kind: gap | conflict | failure | success_path | duplicate_claim | uncertainty
  residual_magnitude:
  evidence_ref:
  ttl:
  visibility: human_auditable
```

Accepted insight:

```text
Residual-weighted deposits are superior to binary visited/not-visited traces.
```

---

#### E2 — Friston 2005 / Free Energy and Hierarchical Predictive Coding

Central insight:

```text
Inference and learning can both be understood as minimizing free energy / surprise.
```

For this round, the important part is not the full neuroscience model. The important part is the architecture:

```text
higher level provides context-sensitive priors
lower level returns prediction errors
repeated learning suppresses expected error
novel or deviant events generate stronger residual signals
```

shadowMAS mapping:

```text
The shared field is an externalized surprise surface.
High field value means “the system expected less trouble here than it got.”
```

Candidate operational rule:

```yaml
field_priority_score:
  score = residual_magnitude * urgency_weight * confidence_weight * freshness_weight
```

Accepted insight:

```text
A signal field should prioritize unresolved, learnable, decision-relevant surprise, not merely noisy activity.
```

---

#### E3 — Bassler & Losick 2006 / Bacterially Speaking / Quorum Sensing

Central insight:

```text
Bacteria communicate through chemical signals; group-level behavior can switch when signal concentration crosses meaningful thresholds.
```

Relevant abstraction:

```text
Individual agents emit local signals.
The environment accumulates signals.
When concentration crosses a threshold, the group changes behavior.
```

shadowMAS mapping:

```text
Do not escalate every local residual immediately.
Let signals accumulate until a quorum threshold indicates system-level attention is justified.
```

Candidate operational rule:

```yaml
quorum_trigger:
  zone:
  signal_type:
  threshold:
  window:
  trigger_action: escalate | converge | reroute | lock | human_review
  anti_spam_rule:
  decay_rule:
```

Accepted insight:

```text
Threshold-triggered collective switching is useful for avoiding both underreaction and overreaction.
```

Confidence note:

```text
The high-level quorum-sensing abstraction is strong. Fine-grained biological mechanisms were not treated as directly transferable engineering constraints.
```

---

#### E4 — Theraulaz & Bonabeau / A Brief History of Stigmergy

Central insight:

```text
Stigmergy explains how agents can appear individually independent while collective activity becomes coordinated through traces left in a shared medium.
```

Key abstraction:

```text
action → trace in medium → later action stimulated by trace
```

shadowMAS mapping:

```text
Agent execution should leave structured coordination traces that guide later agents without requiring direct pairwise communication.
```

Candidate operational rule:

```yaml
stigmergic_trace:
  trace_id:
  zone:
  trace_type: trail | alarm | territory | question | constraint | evidence
  created_by:
  created_at:
  ttl:
  decay_model:
  next_agent_effect:
  audit_summary:
```

Accepted insight:

```text
A trace should stimulate but not force later agent action.
```

This matters because shadowMAS cannot let traces become hidden authority.

---

#### E5 — Universal stigmergy / coordination mechanism companion scan

Central insight:

```text
Stigmergy generalizes beyond insects: action, agent, medium, trace, and coordination are the core components.
```

shadowMAS mapping:

```yaml
field_components:
  agent: worker / reviewer / router / runtime adapter
  action: task attempt / review / validation / claim / failure
  medium: shared signal field
  trace: structured deposit
  coordination: later agents read trace and adjust local action
```

Accepted insight:

```text
For shadowMAS, the “medium” must be explicitly designed, not assumed.
```

This means field semantics, TTL, visibility, permissions, and truth boundaries must be specified.

---

### 17.5 ToT candidate branches

```yaml
tot_branches:
  A_replace_orchestrator_with_signal_field_entirely:
    decision: rejected
    reason: too risky; governance and protected decisions still need explicit authority and review boundaries

  B_keep_only_central_orchestrator:
    decision: rejected
    reason: misses C-I value; central routing becomes bottleneck for multi-agent coordination

  C_add_signal_field_as_runtime_coordination_lane:
    decision: accepted
    reason: high-value coordination primitive when shared writable state exists

  D_make_signal_field_a_truth_layer:
    decision: rejected
    reason: field traces are execution/runtime signals, not canonical truth

  E_signal_field_with_visible_audit_projection:
    decision: accepted
    reason: field can guide agents only if human/reviewer can inspect summarized state and residuals

  F_raw_numeric_prediction_error_required:
    decision: rejected
    reason: many shadowMAS tasks do not have numeric predictive models; use typed residual magnitude instead

  G_typed_residual_signal:
    decision: accepted
    reason: implementable across text, code, repo, review, and runtime tasks

  H_zero_initialized_field:
    decision: rejected
    reason: v4 warns zero field gives no gradient; start from uncertainty prior or warm-up baseline

  I_TTL_decay_as_required_field_property:
    decision: accepted
    reason: prevents stale traces from becoming persistent false guidance

  J_quorum_trigger_for_all_decisions:
    decision: rejected
    reason: quorum is useful for coordination escalation, not for protected truth/human-only decisions

  K_quorum_trigger_for_routing_escalation:
    decision: accepted
    reason: good fit for convergence, reroute, alarm, or human-review trigger
```

---

### 17.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + K
    reason: signal field gives shadowMAS a serious MAS coordination substrate, but cannot replace governance authority.
    risk: over-automation could blur who decides.

  CTO:
    vote: accept C + G + I
    reason: typed residual signals, TTL, and field semantics are implementable without latent access.
    risk: raw prediction error cannot be required everywhere.

  Security:
    vote: accept E + I, reject D strongly
    reason: shared fields can become hidden influence channels; they need audit projection, TTL, permission, and no truth promotion.
    risk: malicious or low-quality agents can poison the field.

  CSO:
    vote: accept C
    reason: “shared signal field” is a strong differentiator from simple task orchestration.
    risk: if too abstract, it becomes decorative theory.

  CFO:
    vote: accept K cautiously
    reason: quorum triggers reduce needless escalation and redundant work.
    risk: field infrastructure has maintenance cost; v0 should start minimal.
```

---

### 17.7 LATS result

```yaml
lats_result:
  best_node:
    name: Auditable Signal Field Runtime Lane
    score: 0.92
    status: candidate_kernel
    why:
      - directly imports v4 C-I without making it hidden truth
      - supports multi-agent coordination without O(n²) pairwise chatter
      - integrates Round 1 residual-first logic
      - connects to Round 2 runtime/convergence layer thinking
      - remains implementable without model latent access
      - preserves governance matrix boundaries

  accepted:
    - signal_field_as_runtime_coordination_lane
    - typed_residual_signal
    - visible_audit_projection
    - TTL_decay_policy
    - quorum_trigger_for_routing_or_escalation
    - direct_messaging_fallback_when_no_shared_state

  rejected:
    - full_orchestrator_replacement
    - signal_field_as_truth_layer
    - raw_numeric_prediction_error_required
    - zero_initialized_field
    - quorum_trigger_for_protected_truth_decisions

  deferred:
    - production_signal_field_schema
    - field_poisoning_defense_model
    - threshold_calibration_protocol
  - production_plateau_intervention_protocol
  - spandrel_parent_objective_library
  - capability_emergence_dashboard
  - long_horizon_phase_transition_experiment_suite
    - relation_to_recursiveMAS_state_loop
    - relation_to_Q-I_Ashby_Percolation
```

---

### 17.8 Round 3 accepted kernel

```yaml
signal_field_coordination_kernel:
  core_sentence: >
    shadowMAS should treat shared writable coordination fields as an optional runtime lane:
    agents deposit typed residual signals into auditable, decaying zones; quorum thresholds
    can trigger convergence, rerouting, locking, or escalation, but field traces never become
    canonical truth or protected decision authority.

  principles:
    - signal_field_is_runtime_not_truth
    - typed_residuals_over_raw_chatter
    - TTL_decay_prevents_stale_coordination
    - quorum_triggers_coordinate_but_do_not_govern_final_truth
    - visible_audit_projection_required
    - direct_message_fallback_when_shared_state_missing
    - field_poisoning_must_be_treated_as_security_risk
```

---

### 17.9 Candidate shadowMAS primitives from Round 3

#### 17.9.1 Signal field event

```yaml
signal_field_event:
  event_id:
  zone:
  channel: trail | alarm | territory | question | constraint | evidence
  residual_kind: success_path | failure | conflict | uncertainty | duplicate_claim | validation_gap
  residual_magnitude: low | medium | high | blocker
  urgency: low | medium | high | critical
  confidence: low | medium | high
  created_by:
  created_at:
  ttl:
  decay_policy:
  source_ref:
  audit_summary:
  truth_status: runtime_signal_only
```

#### 17.9.2 Signal field zone

```yaml
signal_field_zone:
  zone_id:
  scope:
  owner:
  writable_by:
  readable_by:
  active_events:
  aggregated_score:
  dominant_channel:
  stale_event_count:
  poisoning_risk:
  audit_projection:
```

#### 17.9.3 Quorum trigger

```yaml
quorum_trigger:
  trigger_id:
  zone:
  channel:
  threshold:
  observation_window:
  trigger_action: converge | reroute | lock | escalate | human_review
  required_confidence:
  anti_spam_rule:
  decay_rule:
  authority_boundary:
  cannot_promote_truth: true
```

#### 17.9.4 Field audit projection

```yaml
field_audit_projection:
  field_id:
  current_hot_zones:
  top_residuals:
  active_alarms:
  active_territory_claims:
  stale_signals:
  suspected_poisoning:
  triggered_quorums:
  recommended_action:
```

#### 17.9.5 Shared-state capability check

```yaml
shared_state_capability_check:
  runtime:
  shared_writable_state_available: true | false
  persistence_level: ephemeral | session | project | durable
  auditability: low | medium | high
  permission_model_defined: true | false
  fallback_if_false: direct_message | central_router | packet_queue
```

---

### 17.10 Round 3 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  governance_matrix:
    reason: signal field must be located in R/T4/T5 boundaries, not T2 truth

  current_truth:
    reason: R-layer may expand from queue/worker/retry into signal-field runtime lane

  packet_future:
    reason: signal field event may become a machine-stable structured runtime event

  memory_plane:
    reason: field signals look like memory but must be treated as runtime coordination unless promoted

  prompt_layering_contract:
    reason: runtime adapters may write/read field events but must not redefine truth

  zh_tw_human_docs:
    reason: high-value human explanation; likely needs companion explanation if promoted
```

Change-impact warning:

```text
Do not update canonical truth yet. This round creates an active candidate kernel.
Formal adoption would affect runtime, packet, memory-plane, governance matrix, and human-facing explanation.
```

---

## 18. Document self-optimization — second pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 2  
> object under review: same single active design log  
> goal: make the document increasingly usable while preserving one-file requirement and high-quality evidence.

---

### 18.1 Problem diagnosis after Round 3

The document now contains three active kernels and several candidate primitives. The main risk is no longer lack of content. The main risk is **decision scattering**.

If each round only appends details, future readers will not know:

```yaml
reader_questions:
  - What is currently accepted?
  - What is rejected?
  - What is still deferred?
  - Which kernel changed shadowMAS design most?
  - Which primitives are active candidates vs evidence notes?
```

Therefore pass 2 implements the previously accepted document strategy:

```text
Active Decision Ledger + Round Appendices
```

The ledger has now been inserted near the top of the document.

---

### 18.2 ToT branches for document optimization

```yaml
document_tot_branches:
  A_continue_append_only:
    decision: rejected
    reason: after three rounds, append-only would increase recall burden

  B_rewrite_entire_document_now:
    decision: rejected_for_now
    reason: too much churn; could lose research detail while program is still moving

  C_insert_must_see_decision_ledger_at_top:
    decision: accepted_and_applied
    reason: makes current state visible without splitting file

  D_move_all_paper_evidence_to_end_now:
    decision: deferred
    reason: useful later, but not needed until navigation becomes worse

  E_create_machine_stable_summary_block_each_round:
    decision: accepted
    reason: every round should have a YAML-like kernel summary and candidate decisions
```

---

### 18.3 MoE votes for document optimization

```yaml
document_moe_votes:
  CEO:
    vote: C + E
    reason: first page must show current decisions, not only research history

  CTO:
    vote: C + E
    reason: machine-stable summaries make future extraction easier

  Security:
    vote: C
    reason: accepted/rejected/deferred separation prevents speculative ideas masquerading as decisions

  CSO:
    vote: C
    reason: active ledger improves narrative clarity and onboarding

  CFO:
    vote: C
    reason: reduces future maintenance and review cost
```

---

### 18.4 LATS result for document optimization

```yaml
document_lats_result:
  best_node:
    name: Top Active Decision Ledger + Round-Level Machine Summary
    score: 0.95
    status: accepted_and_partially_applied
    applied_now:
      - inserted must-see active decision ledger near document top
      - added Round 3 machine-stable summary
      - kept prior round logs intact
    deferred:
      - full reorganization into paper evidence appendix
      - separate canonical proposal file
```

---

### 18.5 New document-level rule

```text
Every future round must update three places:
1. top active decision ledger
2. that round’s detailed log
3. current document status
```

This supersedes the earlier two-place rule.

---

## 19. Round 4 — M-I Pheromone Field = Externalized Free-Energy Landscape

> status: active round log  
> theme: M-I · pheromone field as externalized free-energy landscape  
> method: 3 full-read targets + 2 companion scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Rao & Ballard and Friston were already available as uploaded PDFs and had been read deeply enough for system-design mapping. Theraulaz & Bonabeau was accessible through abstract/metadata and secondary full-text signals, but not fully available in this session; therefore fine-grained stigmergy taxonomy is treated as companion-grade rather than hard constraint. M-I is a merged design insight, so this round emphasizes integration and operationalization rather than pretending all source traditions are mathematically identical.

---

### 19.1 Round 4 core question

```text
Should shadowMAS treat the shared signal field as an externalized free-energy landscape,
where agents navigate toward reducible residuals and away from stale, solved, or poisoned zones?
```

Round 3 accepted a runtime candidate:

```yaml
signal_field_coordination_kernel:
  status: accepted_as_active_candidate
  core: agents deposit typed residual signals into auditable, decaying zones; quorum thresholds trigger convergence/reroute/escalation.
```

Round 4 asks the deeper M-I question:

```yaml
m_i_question:
  not: should agents leave signals?
  but: what do those signals mean computationally?
```

Working answer:

```text
A signal field should be treated as a navigable residual landscape:
high signal = high unresolved, learnable, decision-relevant surprise;
low signal = already modeled, stale, irrelevant, or not worth current attention.
```

---

### 19.2 Feynman explanation

Imagine a dark factory with many rooms.

Bad version:

```text
Every worker shouts reports into a chat room.
Everyone reads everything.
Everyone wastes attention.
```

Signal-field version:

```text
Each room has a heat mark.
The mark gets hotter when workers find unresolved trouble.
The mark cools down when the issue is resolved or becomes stale.
Workers go toward hot rooms only when the heat is meaningful.
```

Externalized free-energy version:

```text
The map itself becomes a live picture of “where the system is still surprised.”
Agents do not just follow orders.
They navigate the map to reduce useful surprise.
```

Important word: **useful**.

Not every surprise deserves attention:

```text
Useful surprise = high residual + learnable/reducible + relevant to current goal.
Bad surprise = noise, adversarial spam, stale residue, or outside scope.
```

shadowMAS translation:

```text
The field should not simply collect messages.
It should help agents decide where their next action will reduce the most valuable residual.
```

---

### 19.3 Source basis captured in this round

#### v4 M-I claim

v4’s merged insight says:

```text
Pheromone field = externalized free-energy landscape.
```

Meaning:

```yaml
old_pheromone:
  semantics: visited / not visited, path reinforcement

upgraded_pheromone:
  semantics: prediction-error magnitude, information density, undermodeled region

active_inference_connection:
  agent_action: choose action that minimizes expected future prediction error
  field_role: shared externalized prediction-error landscape
  group_result: collective KL/free-energy reduction without central coordination
```

M-I is not merely a restatement of C-I. It upgrades C-I from coordination mechanism to **optimization surface**.

---

### 19.4 Evidence cards

#### E1 — Rao & Ballard / residual signals as computable coordination content

Core paper content already captured:

```text
Higher levels send predictions downward.
Lower levels send residual errors upward.
The model learns natural-image regularities.
Unexpected inputs create larger residual signals.
Predictable inputs suppress residual signals.
```

Round 4 extraction:

```text
Residual is not just an error report.
Residual can be a navigation signal.
```

shadowMAS mapping:

```yaml
field_event_from_residual:
  expected: what the system expected to happen
  actual: what happened
  residual: what remains unexplained or unresolved
  action_value: whether another agent should investigate, reroute, converge, or ignore
```

Accepted insight:

```text
The field must distinguish residual magnitude from action value.
A big residual that is irrelevant or impossible to reduce should not dominate the field.
```

Candidate scoring:

```yaml
residual_action_value:
  residual_magnitude: low | medium | high | blocker
  reducibility: unknown | low | medium | high
  goal_relevance: low | medium | high
  confidence: low | medium | high
  freshness: fresh | aging | stale
```

---

#### E2 — Friston / active inference and expected future prediction error

Core paper content already captured:

```text
Inference and learning both minimize free energy.
Hierarchical generative models provide context-sensitive priors.
Prediction error is minimized across levels.
Learning suppresses repeated expected error.
Novel or deviant signals remain salient.
```

Round 4 extraction:

```text
Action can be interpreted as selecting a path that reduces expected future surprise.
```

shadowMAS mapping:

```yaml
agent_action_selection:
  read_field:
    - hot zones
    - stale zones
    - alarm zones
    - territory claims
  estimate_expected_residual_reduction:
  choose_action:
    - explore
    - converge
    - validate
    - reroute
    - escalate
    - ignore
```

Accepted insight:

```text
Agents should not always chase the hottest zone.
They should choose the action with the best expected residual reduction under scope, risk, and authority constraints.
```

Candidate formula-like design:

```yaml
expected_residual_reduction_score:
  components:
    - residual_magnitude
    - reducibility
    - goal_relevance
    - urgency
    - confidence
    - freshness
    - risk_penalty
    - authority_penalty
```

---

#### E3 — Theraulaz & Bonabeau / stigmergic traces as environmental mediation

Core source idea:

```text
Stigmergy explains how agents can coordinate indirectly through traces left in a shared medium.
```

Round 4 extraction:

```text
The medium is not passive storage.
The medium shapes future behavior.
```

shadowMAS mapping:

```yaml
field_medium_design:
  must_define:
    - what counts as a zone
    - what counts as a trace
    - who can write
    - who can read
    - how traces decay
    - when traces aggregate
    - when traces trigger mode switching
    - how human/reviewer sees the field
```

Accepted insight:

```text
If the medium is not designed, stigmergy becomes accidental hidden influence.
```

Important boundary:

```text
A trace may stimulate later action, but must not silently command later action.
```

---

#### E4 — Bassler & Losick / quorum sensing as collective thresholding

Core source idea:

```text
Local signals can accumulate until group-level behavior changes.
```

Round 4 extraction:

```text
Thresholds prevent both underreaction and overreaction.
```

shadowMAS mapping:

```yaml
quorum_threshold_types:
  convergence_threshold:
    purpose: enough residuals point to same zone; agents converge

  alarm_threshold:
    purpose: enough high-risk signals; system escalates or locks

  staleness_threshold:
    purpose: field signal aged out; ignore or purge

  conflict_threshold:
    purpose: contradictory residuals; trigger review rather than more execution
```

Accepted insight:

```text
Quorum triggers are coordination switches, not truth gates.
```

---

#### E5 — Curiosity / learnable KL frontier companion scan

Round 4 uses v4’s curiosity framing:

```text
Curiosity = high prediction error that is reducible.
```

This is important because a signal field can otherwise become an error magnet.

Bad design:

```text
Always go to highest error.
```

Better design:

```text
Go to highest reducible, relevant, fresh, authority-allowed residual.
```

shadowMAS mapping:

```yaml
learnable_frontier_filter:
  high_residual: true
  reducible: true
  within_scope: true
  not_protected_truth_decision: true
  not_stale: true
  not_poisoned: true
```

Accepted insight:

```text
The signal field must track reducibility, not just error intensity.
```

---

### 19.5 ToT candidate branches

```yaml
tot_branches:
  A_signal_field_as_message_board:
    decision: rejected
    reason: too shallow; does not capture M-I. A message board stores chatter, not navigable residual energy.

  B_signal_field_as_truth_map:
    decision: rejected
    reason: violates shadowMAS truth boundaries; field is runtime signal, not canonical truth.

  C_signal_field_as_externalized_residual_landscape:
    decision: accepted
    reason: captures M-I while preserving audit and runtime boundaries.

  D_agents_chase_highest_signal_always:
    decision: rejected
    reason: high residual may be stale, irrelevant, adversarial, or unreducible.

  E_agents_choose_best_expected_residual_reduction:
    decision: accepted
    reason: matches active inference lens and is implementable as scoring.

  F_quorum_threshold_as_truth_promotion_gate:
    decision: rejected
    reason: quorum can trigger review or convergence, but cannot promote truth.

  G_quorum_threshold_as_mode_switch:
    decision: accepted
    reason: good fit for convergence/reroute/escalate/lock behavior.

  H_field_without_audit_projection:
    decision: rejected
    reason: hidden coordination field becomes unreviewable influence channel.

  I_field_with_audit_projection_and_poisoning_check:
    decision: accepted
    reason: necessary for security and governance.

  J_numeric_free_energy_required:
    decision: rejected_for_v0
    reason: many shadowMAS tasks are symbolic/governance tasks without formal probabilistic model.

  K_semantic_free_energy_proxy:
    decision: accepted
    reason: typed residual, reducibility, freshness, and relevance can approximate the design function.
```

---

### 19.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + G
    reason: field-as-landscape gives shadowMAS a deeper MAS coordination identity than task routing.
    risk: if overclaimed, it becomes pseudo-physics.

  CTO:
    vote: accept C + E + K
    reason: semantic residual scoring is implementable; numeric free energy is not required for v0.
    risk: scoring dimensions must not become arbitrary decoration.

  Security:
    vote: accept I, reject B + H strongly
    reason: hidden fields can be poisoned or become invisible authority.
    risk: agents may over-trust field heat unless source quality and TTL are visible.

  CSO:
    vote: accept C
    reason: “externalized residual landscape” is a strong conceptual differentiator.
    risk: explain in human terms or future maintainers will ignore it.

  CFO:
    vote: accept E cautiously
    reason: expected residual reduction can reduce wasted work.
    risk: scoring and infrastructure must not cost more than direct routing for small tasks.
```

---

### 19.7 LATS result

```yaml
lats_result:
  best_node:
    name: Externalized Residual Landscape with Reducibility Filter
    score: 0.93
    status: candidate_kernel
    why:
      - upgrades Round 3 signal field from coordination mechanism to action-selection surface
      - integrates KL/free-energy lens without requiring full numeric formalization
      - prevents naive highest-error chasing
      - preserves runtime-not-truth boundary
      - creates concrete scoring dimensions for implementation

  accepted:
    - signal_field_as_externalized_residual_landscape
    - expected_residual_reduction_action_selection
    - reducibility_filter
    - semantic_free_energy_proxy_for_v0
    - quorum_as_mode_switch_not_truth_gate
    - field_audit_projection_and_poisoning_check

  rejected:
    - signal_field_as_message_board
    - signal_field_as_truth_map
    - agents_always_chase_highest_signal
    - quorum_as_truth_promotion_gate
    - field_without_audit_projection
    - numeric_free_energy_required_in_v0

  deferred:
    - exact_scoring_formula
    - threshold_calibration_experiment
    - field_topology_schema
    - relation_to_recursiveMAS_latent_state_loop
    - relation_to_Q-I_variety_and_connectivity
```

---

### 19.8 Round 4 accepted kernel

```yaml
externalized_free_energy_landscape_kernel:
  core_sentence: >
    shadowMAS should treat its signal field as an externalized residual/free-energy landscape:
    agents should not merely read messages or chase the hottest error; they should select actions
    that maximize expected reducible residual reduction under scope, freshness, confidence, risk,
    authority, and audit constraints.

  principles:
    - field_is_navigation_surface_not_truth_surface
    - residual_magnitude_must_be_filtered_by_reducibility
    - freshness_and_TTL_are_part_of_signal_meaning
    - quorum_switches_modes_but_does_not_promote_truth
    - audit_projection_is_required
    - poisoning_check_is_required
    - semantic_free_energy_proxy_is_enough_for_v0
```

---

### 19.9 Candidate shadowMAS primitives from Round 4

#### 19.9.1 Residual action value

```yaml
residual_action_value:
  event_id:
  zone:
  residual_magnitude: low | medium | high | blocker
  reducibility: unknown | low | medium | high
  goal_relevance: low | medium | high
  urgency: low | medium | high | critical
  confidence: low | medium | high
  freshness: fresh | aging | stale
  risk_penalty: low | medium | high
  authority_penalty: none | review_required | human_only
  expected_residual_reduction: low | medium | high
  recommended_action: ignore | explore | validate | converge | reroute | escalate | human_review
```

#### 19.9.2 Learnable frontier filter

```yaml
learnable_frontier_filter:
  candidate_zone:
  high_residual: true | false
  reducible: true | false | unknown
  within_scope: true | false
  authority_allowed: true | false
  not_stale: true | false
  not_poisoned: true | false | unknown
  decision: pursue | monitor | ignore | escalate
```

#### 19.9.3 Field poisoning check

```yaml
field_poisoning_check:
  zone:
  suspicious_patterns:
    - repeated_low_confidence_deposits
    - single_agent_overdominance
    - stale_signal_reactivation
    - contradiction_without_evidence
    - high_alarm_without_source_ref
  risk_level: low | medium | high
  mitigation: discount | require_evidence | lock_field | human_review
```

#### 19.9.4 Field navigation policy

```yaml
field_navigation_policy:
  agent_id:
  readable_zones:
  writable_zones:
  selection_rule: highest_expected_residual_reduction
  forbidden_actions:
    - promote_truth_from_field
    - bypass_review_gate
    - override_project_domain_truth
  fallback_when_no_valid_zone: central_router | direct_message | idle | ask_human
```

---

### 19.10 Round 4 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  runtime_R_layer:
    reason: field navigation is a runtime lane and action-selection surface

  packet_future:
    reason: residual_action_value and field_event may become structured packet/event objects

  review_packet:
    reason: review may include field audit projection and residual frontier summary

  memory_plane:
    reason: field looks memory-like but must remain runtime signal unless promoted through review

  governance_matrix:
    reason: field authority must remain below truth layers

  security_policy_future:
    reason: field poisoning and hidden coordination must be controlled
```

Change-impact warning:

```text
Do not update canonical truth yet. This is an active design kernel.
Formal adoption requires runtime, packet, memory-plane, review, and governance impact review.
```

---

## 20. Document self-optimization — third pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 3  
> object under review: same single active design log  
> goal: keep the one-file document usable after adding Round 4.

---

### 20.1 Problem diagnosis after Round 4

The top ledger now works, but the document is becoming a kernel + primitive + evidence hybrid. The main risk is that future readers may confuse:

```yaml
confusable_layers:
  design_kernel: high-level accepted lens
  primitive_candidate: possible schema/runtime object
  paper_evidence: source support
  canonical_truth: not this document
```

This document must keep those separate.

---

### 20.2 ToT branches for document optimization

```yaml
document_tot_branches:
  A_do_nothing:
    decision: rejected
    reason: after Round 4, risk of kernel/primitive/evidence confusion increases

  B_insert_layer_legend_near_top:
    decision: accepted
    reason: helps reader distinguish design kernel vs primitive vs evidence vs truth

  C_rewrite_all_previous_sections_into_new_structure:
    decision: deferred
    reason: too disruptive during ongoing research

  D_add_round_index_table_now:
    decision: accepted_later
    reason: useful soon, but ledger already covers most current recall need

  E_split_document_now:
    decision: rejected_for_now
    reason: user requested single standalone document
```

---

### 20.3 MoE votes for document optimization

```yaml
document_moe_votes:
  CEO:
    vote: B
    reason: readers must know what is decision vs evidence

  CTO:
    vote: B + D_later
    reason: layer legend reduces schema confusion; round index can wait

  Security:
    vote: B
    reason: speculative primitive must not masquerade as canonical rule

  CSO:
    vote: B
    reason: improves onboarding and recognition-first reading

  CFO:
    vote: B
    reason: lowest-cost improvement with high future value
```

---

### 20.4 LATS result for document optimization

```yaml
document_lats_result:
  best_node:
    name: Add Concept-Type Legend Before Next Major Rewrite
    score: 0.91
    status: accepted_deferred_application
    reason:
      - improves comprehension
      - avoids full rewrite churn
      - preserves one-file constraint
      - protects against truth contamination
```

---

### 20.5 New document-level rule

```text
Future updates should label every new item as one of:
- design_kernel
- primitive_candidate
- paper_evidence
- decision_record
- canonical_patch_candidate
- rejected_candidate
- deferred_candidate
```

This should be applied starting next update.

---

## 21. Current document status after Round 4

```yaml
document_status:
  version: v0.4
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R4_M-I_Externalized_Free_Energy_Landscape
  latest_document_review: concept_type_legend_rule_accepted_for_next_update
  latest_accepted_kernel: Externalized_Free_Energy_Landscape_Kernel
  intended_next_update: after V4_Q-I_Ashby_Percolation_round_or_RecursiveMAS_shock_integration_round
```
---

## 22. Round 5 — Q-I Ashby's Law × Percolation Theory

> status: active round log  
> concept_type: design_kernel + primitive_candidate + paper_evidence  
> theme: Q-I · variety coverage and variety connectivity  
> method: 3 full-read targets + 2 companion scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> source access honesty: Ashby's `An Introduction to Cybernetics` was treated through the law-of-requisite-variety chapters and reliable bibliographic/archive metadata. Broadbent & Hammersley 1957 and Erdős–Rényi 1960 were treated as full-read mathematical source targets at the concept/mechanism level. Barabási–Albert 1999 and Shazeer et al. 2017 were used as companion comparison scans, not as direct governance laws.

---

### 22.1 Round 5 core question

```text
Does shadowMAS have enough capability variety to cover task variety,
and enough inter-agent / inter-capability connectivity to let that variety flow?
```

This round follows v4 Q-I:

```yaml
q_i_merge:
  ashby_law:
    role: variety coverage constraint
    test: V_ctrl >= V_env

  percolation_theory:
    role: variety connectivity constraint
    test: p >= p_c
```

Round 1 established the compression / residual / Occam lens.  
Round 2 established hierarchy / convergence.  
Round 3 established shared signal field coordination.  
Round 4 upgraded signal field into an externalized residual/free-energy landscape.

Round 5 adds the missing design constraint:

```yaml
round_5_question:
  coverage: do we have enough distinct controllable response variety?
  connectivity: can the right varieties combine across agents, packets, state capsules, and runtime lanes?
```

Working answer:

```text
A multi-agent system can fail even when it has many agents.
It fails if the agents do not cover the task variety,
or if the covered variety is trapped in disconnected islands.
```

---

### 22.2 Feynman explanation

Imagine a hospital.

Bad system A:

```text
Many doctors, but nobody knows neurology.
```

That is an Ashby failure:

```text
The environment presents neurological cases.
The hospital has no matching response variety.
V_ctrl < V_env.
```

Bad system B:

```text
The hospital has a neurologist, a surgeon, and a pharmacist,
but their systems cannot share patient state.
```

That is a percolation failure:

```text
The capability exists somewhere,
but it cannot flow through the care network.
p < p_c.
```

Good system:

```text
The hospital has enough specialists,
and the specialists are connected through records, protocols, handoffs, and escalation paths.
```

shadowMAS translation:

```text
Do not merely count agents.
Count covered task variety, then test whether the covered variety can compose.
```

---

### 22.3 Source basis captured in this round

#### v4 Q-I claim

v4 states two simultaneous constraints:

```yaml
combined_constraints:
  variety_coverage:
    formula: V_ctrl >= V_env
    meaning: controller/system capability must cover environmental/task variety

  variety_connectivity:
    formula: p >= p_c
    meaning: inter-agent or inter-capability connectivity must exceed threshold
```

v4's important warning:

```text
Ashby is necessary but not sufficient.
```

A system can satisfy total capability coverage in aggregate and still behave variety-deficient if the required capabilities are trapped in disconnected islands.

---

### 22.4 Evidence cards

#### E1 — Ashby 1956 / Law of Requisite Variety

Central idea:

```text
Only variety can absorb variety.
A regulator/controller that lacks the necessary response variety cannot control the disturbances it faces.
```

Engineering translation:

```yaml
variety_coverage:
  V_env: distinct task/environment states that require meaningfully different responses
  V_ctrl: distinct response states the system can actually deploy under governance constraints
  condition: V_ctrl >= V_env
```

shadowMAS mapping:

```yaml
V_env_examples:
  - task_types
  - risk_tiers
  - truth_touchpoint_patterns
  - repo_change_shapes
  - review_surface_types
  - runtime_failure_modes
  - security_boundary_cases
  - bilingual_human_explanation_cases

V_ctrl_examples:
  - available role capabilities
  - packet families
  - review gates
  - runtime lanes
  - state transfer methods
  - signal field channels
  - security controls
  - escalation paths
```

Accepted insight:

```text
Capability is not just model intelligence.
Capability is governed response variety: what the system can safely recognize, route, execute, review, and escalate.
```

Immediate implication:

```text
Adding a smarter model does not automatically increase V_ctrl if packet shape,
truth boundary, review gate, or runtime lane prevents that capability from being used.
```

---

#### E2 — Broadbent & Hammersley 1957 / Percolation Processes

Central idea:

```text
Connectivity through a random medium changes qualitatively at a threshold.
Below threshold, only small local clusters exist.
Above threshold, a spanning or giant connected structure appears.
```

Engineering translation:

```yaml
variety_connectivity:
  p: effective connection density among agents/capability nodes
  p_c: threshold where cross-domain capability composition first becomes reliable
  condition: p >= p_c
```

shadowMAS mapping:

```text
A capability does not help the whole system if it cannot be reached,
combined, or handed off at the moment the task requires it.
```

Candidate failure case:

```yaml
capability_island_failure:
  has_security_agent: true
  has_backend_agent: true
  has_review_gate: true
  missing_connection: backend_change_does_not_trigger_security_review
  result: security_variety_exists_but_does_not_percolate
```

Accepted insight:

```text
The question is not only which agents exist.
The question is whether the capability graph percolates across task dependencies.
```

---

#### E3 — Erdős & Rényi 1960 / Evolution of Random Graphs

Central idea:

```text
As random edges are added to a graph, graph properties appear sharply around thresholds.
A giant component does not emerge by smooth intuition; it appears as edge density crosses a critical region.
```

Round 5 extraction:

```text
Connectivity is phase-like.
A small increase in routing overlap, shared state, or bridge capability can suddenly unlock composite behavior.
```

shadowMAS mapping:

```yaml
capability_graph:
  nodes:
    - agents
    - packet families
    - runtime lanes
    - state capsule formats
    - review gates
    - truth layers
  edges:
    - can_handoff_to
    - can_read_state_from
    - can_write_signal_to
    - can_trigger_review
    - can_escalate_to
    - can_validate_output_of
```

Accepted insight:

```text
p_c should not be treated as a decorative metaphor.
It should become an empirical calibration target:
add connectivity until cross-domain probes first succeed reliably.
```

Important boundary:

```text
For random graphs, p_c can be approximated by ~1/n style intuition.
For structured task graphs, p_c is usually higher because dependencies are not random,
capabilities are typed, and protected truth boundaries block some edges by design.
```

---

#### E4 — Barabási & Albert 1999 / scale-free network comparison scan

Central idea:

```text
Real networks often are not Erdős–Rényi random graphs.
They can grow through preferential attachment and form hub-heavy, scale-free topology.
```

Why this matters for shadowMAS:

```text
A shadowMAS capability graph may not be random.
Routers, governance gates, shared memory, and signal fields can become hubs.
```

Comparison warning:

```yaml
hub_topology_risk:
  benefit:
    - efficient routing
    - short paths
    - faster convergence
  risk:
    - hub overload
    - single point of coordination failure
    - hidden authority concentration
    - field/router poisoning blast radius
```

Accepted insight:

```text
Do not calibrate p_c from a random-graph assumption alone.
Topology matters: hub-heavy routing can be efficient, but fragile under targeted failure.
```

shadowMAS consequence:

```text
Central router, signal field, and memory registry must be treated as high-centrality nodes.
They need redundancy, audit projection, and failure fallback.
```

---

#### E5 — Shazeer et al. 2017 / Sparsely-Gated MoE comparison scan

Central idea:

```text
Mixture-of-Experts can greatly increase parameter/capability capacity through conditional computation,
where a gating network activates only a sparse subset of experts per input.
```

Why this matters for Q-I:

```text
MoE increases potential V_ctrl, but routing determines whether that variety is reachable.
Sparse gating can satisfy capacity in aggregate while failing composition when tasks need multiple expert domains.
```

shadowMAS mapping:

```yaml
moe_shadowmas_lesson:
  experts_contribute: potential_variety
  router_contributes: effective_connectivity
  load_balancing_contributes: anti_starvation
  bridge_experts_contribute: cross_domain_percolation
```

Accepted insight:

```text
Do not count dormant specialist capability as effective variety unless routing can activate it,
and cross-domain handoff can combine it.
```

---

### 22.5 Round 5 synthesis

#### 22.5.1 Two different failure modes

```yaml
ashby_failure:
  formula: V_ctrl < V_env
  symptom: system lacks a needed response mode
  example: no security review lane for sensitive data mutation
  fix:
    - add capability
    - reduce task/environment variety through scoping
    - add packet/review shape that makes the needed response possible

percolation_failure:
  formula: p < p_c
  symptom: capability exists somewhere but cannot combine or reach the task
  example: security capability exists but backend packet never triggers it
  fix:
    - add bridge agent
    - add routing overlap
    - add shared signal field edge
    - add state capsule compatibility
    - add escalation trigger
```

#### 22.5.2 Why this changes shadowMAS design

Before Q-I, we had:

```yaml
existing_kernels:
  - compression_residual_occam
  - hierarchy_convergence
  - signal_field_coordination
  - externalized_residual_landscape
```

Q-I adds:

```yaml
new_kernel:
  name: Variety_Coverage_Connectivity_Kernel
  core: sufficient capability variety plus sufficient capability connectivity
```

This kernel asks a different design question:

```text
Can this system respond to the variety of real tasks,
and can the right response variety move to where it is needed?
```

---

### 22.6 ToT candidate branches

```yaml
tot_branches:
  A_more_agents_equal_more_control:
    decision: rejected
    reason: agent count does not guarantee V_ctrl coverage or p >= p_c connectivity

  B_ashby_only_coverage_model:
    decision: rejected_as_incomplete
    reason: aggregate capability can exist while trapped in disconnected islands

  C_percolation_only_connectivity_model:
    decision: rejected_as_incomplete
    reason: connectivity among incapable agents does not create missing variety

  D_dual_constraint_variety_coverage_and_connectivity:
    decision: accepted
    reason: captures both capability sufficiency and capability flow

  E_random_graph_pc_as_fixed_rule:
    decision: rejected
    reason: shadowMAS task graphs are typed, governed, structured, and boundary-constrained

  F_empirical_pc_calibration_with_cross_domain_probes:
    decision: accepted
    reason: practical way to find where composite task success first appears

  G_maximize_connectivity_between_all_agents:
    decision: rejected
    reason: creates chatter, authority confusion, security surface, and coordination overload

  H_selective_bridge_connectivity:
    decision: accepted
    reason: increase p_eff where task dependencies require composition while preserving governance boundaries

  I_make_signal_field_the_universal_connectivity_layer:
    decision: rejected
    reason: signal field is useful runtime substrate but cannot replace packets, review, routing, or truth gates

  J_signal_field_as_one_connectivity_edge_type:
    decision: accepted
    reason: signal field helps percolation when used as auditable runtime signal, not truth

  K_count_model_parameters_as_variety:
    decision: rejected
    reason: model capacity is potential variety, not governed deployable response variety

  L_count_routable_auditable_capability_as_variety:
    decision: accepted
    reason: shadowMAS needs usable, governed, inspectable capability
```

---

### 22.7 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept D + F + H
    reason: the system must know whether it is actually capable, not merely complex.
    warning: do not build a dense all-to-all agent mesh that destroys accountability.

  CTO:
    vote: accept D + F + J + L
    reason: capability graph, bridge edges, and empirical cross-domain probes are implementable.
    warning: p_c cannot be hardcoded from random graph theory for typed task networks.

  Security:
    vote: accept H, reject G + I strongly
    reason: connectivity is also attack surface; every new edge can move bad state, stale state, or authority confusion.
    warning: high-connectivity hubs require audit, permissions, and poisoning checks.

  CSO:
    vote: accept D
    reason: “coverage + connectivity” is a clean product-level explanation for why shadowMAS is more than orchestration.
    warning: avoid making this sound like abstract math unless it produces concrete routing tests.

  CFO:
    vote: accept F + H cautiously
    reason: empirical probes prevent overbuilding; selective bridges are cheaper than universal connectivity.
    warning: every bridge edge has maintenance and review cost.
```

---

### 22.8 LATS result

```yaml
lats_result:
  best_node:
    name: Variety Coverage + Selective Capability Percolation
    score: 0.94
    status: accepted_kernel
    why:
      - answers the missing capability sufficiency question
      - distinguishes missing capability from trapped capability
      - gives a diagnostic path for multi-agent failures
      - integrates naturally with signal field, state capsule, and routing design
      - avoids both all-to-all chatter and shallow agent-count thinking
      - preserves governance boundaries by treating connectivity as permissioned edges

  accepted:
    - variety_coverage_constraint
    - variety_connectivity_constraint
    - capability_graph_model
    - empirical_pc_calibration
    - selective_bridge_connectivity
    - routable_auditable_capability_as_effective_variety
    - signal_field_as_runtime_connectivity_edge_not_truth

  rejected:
    - more_agents_equal_more_control
    - ashby_only_model
    - percolation_only_model
    - random_graph_pc_as_fixed_shadowMAS_rule
    - all_to_all_agent_connectivity
    - signal_field_as_universal_connectivity_layer
    - model_parameter_count_as_direct_variety

  deferred:
    - production_capability_graph_schema
    - exact_variety_metric
    - exact_empirical_pc_experiment_protocol
    - graph_centrality_risk_policy
    - bridge_agent_budget_policy
  - exact_layer_rank_budget_formula
  - Fisher_information_measurement_pipeline
  - production_rank_budget_policy
  - LoRA_rank_depth_sweep
  - CoT_domain_distance_benchmark
  - exact_sigma_star_calibration_protocol
  - production_log_reward_transform_policy
  - evaluator_sensitivity_benchmark
  - stochastic_resonance_ablation_suite
  - human_review_confidence_noise_policy
  - production_reviewer_drift_dashboard
  - evaluation_probe_set_registry
  - recalibration_governance_protocol
  - formal_categorical_commutativity_validator
  - reward_model_ensemble_policy
```

---

### 22.9 Round 5 accepted kernel

```yaml
variety_coverage_connectivity_kernel:
  core_sentence: >
    shadowMAS must satisfy two simultaneous constraints: its governed, routable
    capability variety must cover the variety of tasks it accepts, and its capability
    graph must be connected enough for the required varieties to compose across agents,
    packets, runtime lanes, review gates, state capsules, and signal fields.

  principles:
    - agent_count_is_not_capability_variety
    - potential_capability_is_not_effective_variety
    - effective_variety_requires_routing_permission_and_reviewability
    - aggregate_variety_without_connectivity_behaves_like_variety_deficit
    - connectivity_must_be_selective_not_all_to_all
    - p_c_for_shadowMAS_is_empirical_and_task_graph_dependent
    - bridge_edges_have_security_and_maintenance_cost
    - high_centrality_nodes_need_audit_and_fallback
```

---

### 22.10 Candidate shadowMAS primitives from Round 5

#### 22.10.1 Variety coverage audit

```yaml
variety_coverage_audit:
  audit_id:
  task_family:
  V_env:
    task_modes:
    risk_modes:
    truth_touchpoint_modes:
    failure_modes:
    review_modes:
  V_ctrl:
    available_agent_capabilities:
    available_packet_families:
    available_runtime_lanes:
    available_review_gates:
    available_escalation_paths:
  coverage_result: sufficient | partial | deficient
  uncovered_varieties:
  mitigation:
    - add_capability
    - narrow_scope
    - add_review_gate
    - add_runtime_lane
    - human_only_boundary
```

#### 22.10.2 Capability graph record

```yaml
capability_graph_record:
  graph_id:
  nodes:
    agents:
    packet_families:
    runtime_lanes:
    review_gates:
    truth_layers:
    state_capsule_types:
    signal_field_zones:
  edges:
    can_route_to:
    can_handoff_to:
    can_validate:
    can_escalate:
    can_read_state:
    can_write_signal:
  forbidden_edges:
    reason:
  high_centrality_nodes:
  disconnected_islands:
  graph_status: fragmented | near_threshold | percolating | overconnected
```

#### 22.10.3 Variety connectivity audit

```yaml
variety_connectivity_audit:
  audit_id:
  task_family:
  required_capability_combinations:
  observed_success_on_cross_domain_probes:
  p_eff_estimate:
  p_c_empirical_estimate:
  connectivity_result: below_threshold | near_threshold | sufficient | overconnected
  bottleneck_edges:
  missing_bridges:
  unsafe_edges:
  recommended_action: add_bridge | add_router_overlap | add_state_capsule | add_signal_field_edge | reduce_chatter | human_review
```

#### 22.10.4 Bridge agent / bridge edge record

```yaml
bridge_edge_record:
  bridge_id:
  connects:
    from_capability:
    to_capability:
  bridge_type: routing_rule | state_capsule | signal_field_event | review_trigger | handoff_packet | human_escalation
  purpose:
  allowed_scope:
  forbidden_scope:
  audit_surface:
  owner:
  writable_by:
  security_notes:
  complexity_rent:
  removal_condition:
```

#### 22.10.5 Cross-domain percolation probe

```yaml
cross_domain_percolation_probe:
  probe_id:
  required_capabilities:
  expected_composition_path:
  task_input:
  success_criteria:
  observed_path:
  failed_edge:
  residuals:
    missing_capability:
    missing_connection:
    routing_error:
    review_gap:
    authority_block:
  result: pass | fail | partial
```

---

### 22.11 Round 5 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: R-layer may need to recognize capability graph and connectivity calibration as runtime design concerns

  governance_matrix:
    reason: connectivity edges must respect L/T/R boundaries and cannot bypass truth promotion rules

  prompt_layering_contract:
    reason: runtime adapter composition may need capability-graph awareness without flattening source ownership

  packet_future:
    reason: task_packet/review_packet may include required capability combinations and missing-bridge residuals

  runtime_future:
    reason: router, worker pool, signal field, state capsule, and review gates become capability graph nodes/edges

  memory_plane:
    reason: shared memory can support connectivity, but retrieval hits still cannot arbitrate truth

  security_policy_future:
    reason: every connectivity edge expands state movement and poisoning surface

  zh_tw_human_docs:
    reason: coverage/connectivity is high-value human explanation material
```

Change-impact warning:

```text
Do not update canonical truth yet. This is an active design kernel.
Formal adoption requires governance matrix, runtime, packet, memory-plane,
security, and human-facing explanation impact review.
```

---

### 22.12 Practical diagnostic table

| Symptom | Likely constraint violated | Interpretation | First fix |
|---|---|---|---|
| Agent produces confident but wrong response to a new task class | `V_ctrl < V_env` | missing response variety | add capability, review gate, or narrow scope |
| More agents do not improve cross-domain tasks | `p < p_c` | variety exists but is fragmented | add bridge edges / routing overlap / state capsule |
| Same issue repeatedly reaches wrong worker | routing p exists but wrong topology | connection is noisy or misweighted | add routing probes + residual-first router review |
| Signal field gets hot but no one resolves it | field edge exists but no resolving capability | heat is not action value | add reducibility filter or bridge to capable lane |
| Review gate catches issues too late | late percolation | capability reaches review only after damage | add earlier trigger edge |
| Router becomes overloaded | hub overcentralization | efficient but fragile topology | add secondary router / local bridge edges / backpressure |
| Security capability exists but misses backend changes | missing cross-layer bridge | capability island | add backend→security review trigger |
| All agents see all signals and coordination becomes noisy | overconnected graph | p too high; chatter and authority confusion | prune edges and use selective visibility |

---

### 22.13 Current decision

```yaml
round_5_current_decision:
  accepted_kernel: Variety_Coverage_Connectivity_Kernel
  canonical_status: not_canonical
  active_design_status: accepted_kernel
  next_best_use:
    - add to active decision ledger
    - use when evaluating R-layer runtime architecture
    - use when designing router / signal field / state capsule interactions
    - use when diagnosing why more agents do not improve output
  do_not_do_yet:
    - hardcode numeric V_ctrl or V_env formula
    - hardcode p_c = 1/n as universal rule
    - create all-to-all agent communication
    - promote capability graph to canonical truth without impact review
```

---

## 23. Document self-optimization — fourth pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 4  
> object under review: same single active design log  
> goal: apply the concept-type labeling rule after adding Round 5.

---

### 23.1 Problem diagnosis after Round 5

Round 5 introduces a new kernel plus multiple graph-like primitives. This increases risk of confusing:

```yaml
confusion_risk:
  - capability_graph_as_diagnostic_tool_vs_canonical_runtime_schema
  - p_c_as_empirical_probe_vs_universal_numeric_constant
  - bridge_edges_as_selective_connectivity_vs_all_to_all_messaging
  - V_ctrl_as_governed_effective_variety_vs_model_parameter_capacity
```

Therefore, this round must preserve the new concept-type labeling rule.

---

### 23.2 ToT branches for document optimization

```yaml
document_tot_branches:
  A_append_round_without_ledger_update:
    decision: rejected
    reason: violates prior document rule and increases decision scattering

  B_update_top_ledger_and_append_round:
    decision: accepted
    reason: keeps current decision state visible

  C_turn_all_primitives_into_canonical_schema_now:
    decision: rejected
    reason: active design candidates require change-impact review first

  D_add_practical_diagnostic_table:
    decision: accepted
    reason: Q-I can otherwise remain too abstract; diagnostic table makes it usable

  E_split_capability_graph_to_new_file_now:
    decision: rejected_for_now
    reason: user requested one standalone document; splitting should wait for canonical proposal phase
```

---

### 23.3 MoE votes for document optimization

```yaml
document_moe_votes:
  CEO:
    vote: B + D
    reason: the top ledger must show the new active kernel immediately

  CTO:
    vote: B + D
    reason: graph primitives are useful but must remain candidates

  Security:
    vote: B + C_reject
    reason: bridge edges are security-sensitive and cannot silently become runtime law

  CSO:
    vote: D
    reason: diagnostic table turns theory into a product/design tool

  CFO:
    vote: B
    reason: avoids future re-reading cost
```

---

### 23.4 LATS result for document optimization

```yaml
document_lats_result:
  best_node:
    name: Ledger Update + Diagnostic Table + Candidate Labeling
    score: 0.94
    status: accepted_and_applied
    applied_now:
      - added R5 kernel to top active decision ledger
      - added Q-I round log
      - added practical diagnostic table
      - preserved primitive candidates as non-canonical
    deferred:
      - separate capability graph schema file
      - formal p_c calibration protocol
      - canonical runtime patch proposal
```

---

## 24. Current document status after Round 5

```yaml
document_status:
  version: v0.5
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R5_Q-I_Ashby_Percolation
  latest_document_review: ledger_update_plus_diagnostic_table_applied
  latest_accepted_kernel: Variety_Coverage_Connectivity_Kernel
  intended_next_update: after next V4 round, RecursiveMAS shock integration, or WFGY representation compiler round
```

---

## 25. Document self-optimization — fifth pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 5  
> object under review: same single active design log  
> goal: harden navigation, current-state recognition, and decision-state separation after five design kernels.  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions rather than hidden chain-of-thought text.

---

### 25.1 Problem diagnosis after Round 5

The document is now valuable but structurally heavy:

```yaml
observed_document_shape:
  line_count: approximately_4800_plus
  active_kernels: 5
  document_self_optimization_passes_before_this: 4
  historical_current_status_sections_before_this: 2
  dominant_risk: current_state_recognition_failure
```

The main failure mode is no longer missing insight. The main failure mode is:

```text
A future reader may spend too much attention reconstructing which parts are current decisions,
which parts are historical rationale, and which parts are speculative candidates.
```

Therefore the document itself now needs a **control plane**, not just more appended analysis.

---

### 25.2 ToT branches for document optimization

```yaml
document_tot_branches:
  A_continue_append_only:
    decision: rejected
    reason: append-only preserves content but increases recall burden and status ambiguity

  B_full_rewrite_into_perfect_structure_now:
    decision: rejected_for_now
    reason: too much churn; high risk of losing evidence detail and active-session continuity

  C_split_into_multiple_files_now:
    decision: rejected_for_now
    reason: user is still operating through a single active design log; split should wait for canonical proposal or repo phase

  D_add_document_control_plane_near_top:
    decision: accepted_and_applied
    reason: gives readers must-see map, kernel index, decision-state map, and document debt register without destroying existing content

  E_rename_historical_status_sections:
    decision: accepted_and_applied
    reason: older Current document status headings were ambiguous; after-Round labels make them snapshots

  F_delete_older_self_optimization_passes:
    decision: rejected_for_now
    reason: they are historical rationale; deletion would reduce traceability before a clean appendix migration exists

  G_add_consolidated_primitive_index_now:
    decision: deferred
    reason: useful but requires careful extraction across all rounds; should be a dedicated cleanup pass
```

---

### 25.3 MoE votes for document optimization

```yaml
document_moe_votes:
  CEO:
    vote: D + E
    reason: the first screen must tell leadership what is current, not force reconstruction from history
    warning: do not spend time polishing old narrative while architecture is still moving

  CTO:
    vote: D + G_defer
    reason: a control plane is low-risk and immediately useful; primitive extraction needs a separate structured pass
    warning: avoid accidental schema creation while summarizing primitives

  Security:
    vote: D + E + F_reject
    reason: decision-state separation prevents candidates from masquerading as canonical truth; history should remain auditable
    warning: deleting rationale can hide why a risky candidate was rejected

  CSO:
    vote: D
    reason: kernel index improves positioning and makes the system story legible
    warning: the document should not become a theory warehouse

  CFO:
    vote: D + E
    reason: reduces future reading cost with minimal editing cost
    warning: full rewrite has poor ROI at this stage
```

---

### 25.4 LATS result

```yaml
document_lats_result:
  best_node:
    name: Top Control Plane + Historical Status Disambiguation
    score: 0.96
    status: accepted_and_applied
    why:
      - preserves the single-file requirement
      - reduces first-read cognitive load
      - makes current kernels visible without scanning all rounds
      - separates canonical truth, accepted design kernels, active candidates, primitive candidates, rejected candidates, and deferred candidates
      - fixes ambiguity from multiple Current document status headings
      - avoids high-churn full rewrite

  applied_now:
    - updated top metadata to v0.6 document-control optimized
    - inserted 0.2 Must-see document control plane
    - inserted 0.3 Current kernel index
    - inserted 0.4 Decision-state map
    - inserted 0.5 Current document debt register
    - renamed older Current document status headings as after-Round snapshots
    - added this fifth document optimization round
    - added new final document status block

  rejected_now:
    - append_only_continuation
    - full_rewrite_now
    - multi_file_split_now
    - deleting_historical_self_optimization_passes_now

  deferred:
    - consolidated_candidate_primitive_index
    - paper_evidence_appendix_restructure
    - active_kernel_one_page_executive_summary_for_zh_tw
    - canonical_patch_proposal_document
```

---

### 25.5 Accepted document-level rules after pass 5

```yaml
document_rules_after_pass_5:
  R1_current_state_first:
    rule: future readers should inspect section 0.1_to_0.5 before reading round logs

  R2_round_logs_are_evidence_not_current_state_by_default:
    rule: a round log affects current state only when reflected in top ledger or latest status block

  R3_historical_status_sections_are_snapshots:
    rule: any Current document status not at the end must be treated as a dated/round-specific snapshot

  R4_candidate_primitives_remain_candidates:
    rule: primitive YAML blocks are not schema truth until promoted through change-impact review

  R5_every_future_round_must_update_four_surfaces:
    surfaces:
      - top_active_decision_ledger
      - current_kernel_index_if_kernel_changed
      - that_round_detailed_log
      - latest_current_document_status

  R6_every_second_future_round_should_consider_cleanup:
    cleanup_targets:
      - primitive_index
      - evidence_appendix
      - rejected_deferred_table
      - change_impact_queue
```

---

### 25.6 Practical next cleanup target

The next best document-only optimization is not another long review. It should be a structured extraction pass:

```yaml
next_document_cleanup_target:
  name: Consolidated Candidate Primitive Index
  purpose: collect every candidate primitive from R1_to_R5 into one scan-friendly table
  fields:
    - primitive_name
    - originating_round
    - concept_type
    - current_status
    - impacted_surfaces
    - promotion_requirements
    - rejection_or_defer_reason_if_any
  reason: >
    Candidate primitives are currently distributed by round. That is good for traceability
    but bad for schema planning and future implementation review.
```

---

## 26. Current document status after v0.6 document optimization

```yaml
document_status:
  version: v0.6
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R5_Q-I_Ashby_Percolation
  latest_document_review: pass_5_navigation_and_decision_surface_hardening
  latest_accepted_kernel: Variety_Coverage_Connectivity_Kernel
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v0.6
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.5 Current document debt register
    - latest relevant round log only if deeper evidence is needed
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
  intended_next_update: next V4 round, RecursiveMAS shock integration, WFGY representation compiler round, or dedicated primitive-index cleanup
```



---

## 27. Round 6 — Q-II Information Geometry × Renormalization Group

> status: active round log  
> theme: Q-II · information geometry × renormalization group  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> source honesty: Amari & Nagaoka and Wilson are foundational sources, but not all full text was open inside this session. Mehta & Schwab, Martens & Grosse, and Hu et al. were treated through accessible abstracts/metadata and v4 synthesis. This round adopts design constraints, not literal production math.

---

### 27.1 Round 6 core question

```text
Can shadowMAS treat layer transformations, patches, compression, and reasoning bridges
as geometry-aware / RG-like operations rather than arbitrary prompt or schema edits?
```

Round 5 established the missing MAS constraint:

```yaml
R5_kernel:
  coverage: V_ctrl >= V_env
  connectivity: p_eff >= p_c
```

Round 6 asks what happens inside the layers and bridges once capability exists and can connect:

```yaml
R6_question:
  - which information should each layer preserve?
  - which information can each layer safely integrate out?
  - when is a low-rank / scoped patch enough?
  - when is full-rank / full-surface rewriting wasteful or dangerous?
  - when does Chain-of-Thought act as a useful bridge rather than token noise?
```

Working answer:

```text
shadowMAS should not treat compression, layer transformation, adapter patching, or CoT
as generic improvements. They are geometry / relevance decisions: preserve task-relevant
operators, suppress irrelevant operators, keep marginal transfer features available,
and constrain patches by effective rank and reviewability.
```

---

### 27.2 Feynman explanation

Imagine a city map.

Bad compression:

```text
Delete roads until the map is small.
```

Good RG-like compression:

```text
Keep highways, bridges, hospitals, borders, and danger zones.
Remove house numbers only when this decision does not need them.
```

Information geometry adds:

```text
Not every direction you can move on the map changes the destination.
Some directions are real decision directions.
Some are nearly null directions: costly movement with little output change.
```

shadowMAS translation:

```text
A layer transformation is valid only if it preserves the information directions
that affect the downstream decision, while explicitly recording what was compressed,
discarded, inferred, or made irreversible.
```

This turns Q-II into a practical rule:

```text
Do not optimize for smaller artifacts or bigger edits. Optimize for preserving
high-relevance directions and spending patch budget only where it changes behavior.
```

---

### 27.3 Source basis captured in this round

#### v4 Q-II claim

v4 frames Q-II as:

```yaml
Q-II:
  merge: Information_Geometry x Renormalization_Group
  merge_type: MATH_EQ
  core:
    - each deep layer resembles an RG coarse-graining step
    - relevant operators should be preserved and amplified
    - irrelevant operators should be integrated out
    - marginal operators support transfer / few-shot / zero-shot behavior
    - Fisher geometry / effective rank constrains useful update directions
    - CoT can act as percolation bridge-building when tasks cross concept islands
```

Current treatment:

```yaml
shadowMAS_import_status:
  accept_as_design_kernel: true
  reject_as_literal_v0_math_requirement: true
  reason: many shadowMAS artifacts are symbolic/governance objects, not directly differentiable statistical manifolds
```

---

### 27.4 Evidence cards

#### E1 — Amari & Nagaoka / Methods of Information Geometry

Central source signal:

```text
Information geometry treats statistical models as geometric spaces.
The Fisher metric and dual connections provide a way to discuss distances,
curvature, and efficient directions of movement on probability manifolds.
```

shadowMAS extraction:

```text
Do not treat all modifications as equal. A change should be evaluated by whether
it moves the system along an output-relevant direction, not merely by how many
tokens, fields, files, or rules it touches.
```

Candidate rule:

```yaml
geometry_relevance_check:
  proposed_change:
  expected_output_distribution_changed: yes | no | unknown
  decision_relevant_direction: yes | no | unknown
  likely_null_direction: yes | no | unknown
  review_surface_required:
  evidence_needed:
```

Accepted insight:

```text
Information geometry is useful for shadowMAS as a relevance-of-direction lens,
not as a mandatory Fisher-matrix computation in v0.
```

---

#### E2 — Wilson / Renormalization Group and Critical Phenomena

Central source signal:

```text
RG studies how descriptions change across scales, especially by integrating out
microscopic variables while preserving the behavior that matters at larger scales.
Wilson's 1971 work formalizes RG and fixed-point reasoning for critical phenomena.
```

shadowMAS extraction:

```text
Every layer compression should say what is preserved, what is integrated out,
and whether the resulting artifact is still valid for the next decision scale.
```

Candidate operational rule:

```yaml
rg_layer_transform_check:
  source_scale: raw_context | compiled_intake | task_packet | review_packet | truth_candidate
  target_scale:
  preserved_relevant_operators:
  integrated_out_irrelevant_detail:
  marginal_transfer_features:
  distortion_or_loss:
  unsafe_to_integrate_out:
  reversible_refs:
```

Accepted insight:

```text
Compression is only valid when the relevant operators for the next layer are preserved.
```

---

#### E3 — Mehta & Schwab / Exact mapping between variational RG and deep learning

Central source signal:

```text
Mehta & Schwab argue that variational RG and deep learning have an exact mapping
in the studied RBM setting: deep layers perform an RG-like extraction of relevant
features while suppressing irrelevant detail.
```

shadowMAS extraction:

```text
The useful lesson is not that every shadowMAS layer is literally a neural network layer.
The useful lesson is that layer transitions should be judged by feature relevance:
what did this layer preserve, suppress, or make more abstract?
```

Candidate rule:

```yaml
layer_relevance_report:
  layer_transition:
  amplified_features:
  suppressed_features:
  transferred_features:
  lost_cross_dependencies:
  next_layer_decision_impact:
```

Accepted insight:

```text
A layer is not good because it is shorter. A layer is good when it preserves the
features that change downstream decisions and suppresses what does not.
```

---

#### E4 — Martens & Grosse / K-FAC as practical natural-gradient approximation

Central source signal:

```text
K-FAC approximates the Fisher information matrix in neural networks with efficient
Kronecker-factored blocks, making natural-gradient-like updates more practical than
full curvature computation.
```

shadowMAS extraction:

```text
The v0 lesson is engineering humility: geometrically correct movement may be expensive,
so shadowMAS should use cheap proxies unless the runtime has real model-access and
curvature measurement capability.
```

Candidate rule:

```yaml
geometry_proxy_policy:
  exact_geometry_available: true | false
  if_false_use_proxies:
    - effective_rank_estimate
    - layer_depth_heuristic
    - behavioral_probe_delta
    - review_surface_delta
    - output_distribution_delta
  do_not_require_for_v0:
    - Fisher_matrix_computation
    - natural_gradient_runtime
    - gradient_access_from_closed_models
```

Accepted insight:

```text
Natural gradient is a reference direction, not a required shadowMAS v0 runtime primitive.
```

---

#### E5 — Hu et al. / LoRA and rank-deficient adaptation

Central source signal:

```text
LoRA freezes pretrained weights and injects trainable low-rank matrices into transformer
layers, greatly reducing trainable parameters while preserving quality in many adaptation settings.
It also reports empirical rank-deficiency in adaptation.
```

shadowMAS extraction:

```text
Scoped low-rank patches are a strong pattern for shadowMAS adapter design:
change the smallest high-leverage subspace instead of rewriting the whole governance
or runtime surface.
```

Candidate rule:

```yaml
low_rank_patch_budget:
  target_layer_or_surface:
  intended_behavior_delta:
  minimal_patch_surface:
  effective_rank_guess: low | medium | high | unknown
  rollback_path:
  validation_probe:
  avoid_full_rewrite_reason:
```

Accepted insight:

```text
Low-rank patching is a useful adapter principle, but not proof that every shadowMAS
change should be tiny or that all full-rank changes are wrong.
```

---

### 27.5 Q-II relation to R5 and M-IV

Q-II extends Round 5 in one critical way.

Round 5 says:

```text
Capabilities must connect: p_eff >= p_c.
```

Q-II asks:

```text
What kind of connection actually bridges useful representational islands?
```

For Chain-of-Thought:

```yaml
CoT_as_percolation_bridge:
  useful_when:
    - task crosses multiple concept domains
    - intermediate steps add missing graph edges
    - reasoning path exposes relevant operators
  weak_when:
    - task is single-domain and already connected
    - CoT only restates known facts
    - extra tokens increase noise without adding bridge edges
```

Accepted treatment:

```text
CoT is not globally good. It is useful when it increases effective concept-linkage
density for tasks below their reasoning percolation threshold.
```

---

### 27.6 ToT candidate branches

```yaml
tot_branches:
  A_turn_QII_into_full_information_geometry_constitution:
    decision: rejected_for_now
    reason: too heavy; shadowMAS v0 lacks differentiable statistical manifolds for most governance artifacts

  B_ignore_QII_as_model_training_only:
    decision: rejected
    reason: loses useful design constraints for compression, adapters, rank budget, and CoT usage

  C_use_QII_as_layer_relevance_and_rank_budget_kernel:
    decision: accepted
    reason: translates Q-II into implementable checks without requiring inaccessible model internals

  D_require_Fisher_matrix_or_natural_gradient_in_v0:
    decision: rejected_for_v0
    reason: closed models and symbolic artifacts usually lack gradient / curvature access

  E_use_behavioral_and_artifact_proxies_for_geometry:
    decision: accepted
    reason: output distribution delta, review-surface delta, and effective-rank estimates are more available

  F_compress_every_layer_aggressively:
    decision: rejected
    reason: RG preserves relevant operators; it does not blindly shrink everything

  G_record_preserved_integrated_out_marginal_features:
    decision: accepted
    reason: this gives compression and layer transforms an auditable structure

  H_use_LoRA_as_proof_all_changes_should_be_low_rank:
    decision: rejected
    reason: LoRA supports scoped patching but does not ban full rewrites when the surface genuinely changed

  I_use_low_rank_patch_budget_as_adapter_design_pattern:
    decision: accepted
    reason: strong fit for runtime adapters, prompt adapters, and bounded governance patches

  J_use_CoT_everywhere:
    decision: rejected
    reason: CoT helps when bridge edges are missing; otherwise it is token noise and possible distortion

  K_use_CoT_as_bridge_probe_for_cross_domain_tasks:
    decision: accepted
    reason: connects Q-II to R5 percolation and gives an empirical test path
```

---

### 27.7 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + G + K
    reason: Q-II strengthens the identity of shadowMAS as a layered decision system, not a prompt pile.
    risk: over-mathematizing may slow actual productization.

  CTO:
    vote: accept C + E + I
    reason: layer relevance checks, rank-budget thinking, and low-rank adapter discipline are implementable.
    risk: do not require Fisher matrix, natural gradient, or model-internal access in v0.

  Security:
    vote: accept G, reject F strongly
    reason: blind compression can erase audit-critical fields, authority boundaries, or unsafe-to-compress data.
    risk: “integrated out” can become a laundering phrase unless reversible refs and distortion notes are required.

  CSO:
    vote: accept C + K
    reason: “preserve relevant operators, integrate out irrelevant detail” is a strong strategy story.
    risk: CoT bridge framing must not become an excuse for verbose reasoning everywhere.

  CFO:
    vote: accept I cautiously
    reason: low-rank / scoped patches reduce maintenance cost compared with full-surface rewrites.
    risk: too many tiny adapters can create hidden integration debt.
```

---

### 27.8 LATS result

```yaml
lats_result:
  best_node:
    name: Geometry-Aware Layer Budget Kernel
    score: 0.92
    status: accepted_kernel
    why:
      - converts Q-II into layer/compression/adapter rules
      - avoids impossible v0 requirement for Fisher matrices or natural gradients
      - links R2 hierarchy, R5 connectivity, and CoT bridge behavior
      - supports low-rank patch discipline without banning necessary full rewrites
      - improves auditability of compression and layer transitions

  accepted:
    - QII_as_layer_relevance_and_rank_budget_kernel
    - rg_layer_transform_check
    - relevant_irrelevant_marginal_operator_record
    - geometry_proxy_policy
    - low_rank_patch_budget
    - CoT_as_cross_domain_bridge_probe

  rejected:
    - full_information_geometry_constitution_now
    - QII_as_training_only_irrelevant_to_shadowMAS
    - Fisher_matrix_required_for_v0
    - natural_gradient_required_for_v0
    - blind_aggressive_compression
    - LoRA_as_universal_no_full_rewrite_law
    - CoT_everywhere

  deferred:
    - exact_layer_rank_budget_formula
    - effective_rank_measurement_pipeline
    - LoRA_rank_depth_sweep
    - behavioral_output_distribution_probe_standard
    - CoT_domain_distance_benchmark
```

---

### 27.9 Round 6 accepted kernel

```yaml
information_geometry_rg_layer_budget_kernel:
  core_sentence: >
    shadowMAS should treat layer transformations, compression, adapter patches,
    and reasoning bridges as geometry-aware relevance decisions: preserve task-relevant
    operators, integrate out irrelevant detail only with audit trail, keep marginal
    transfer features available, and spend patch budget on effective behavior-changing
    directions rather than raw surface size.

  principles:
    - layer_changes_are_relevance_transformations
    - compression_must_preserve_relevant_operators
    - integrated_out_information_must_be_recorded
    - marginal_transfer_features_should_not_be_destroyed_silently
    - effective_rank_guides_patch_budget
    - natural_gradient_is_reference_not_v0_requirement
    - low_rank_patch_is_adapter_pattern_not_universal_law
    - CoT_is_bridge_when_domain_graph_is_disconnected
```

---

### 27.10 Candidate shadowMAS primitives from Round 6

#### 27.10.1 RG layer transform check

```yaml
rg_layer_transform_check:
  transform_id:
  source_artifact:
  target_artifact:
  source_scale: raw_context | compiled_intake | task_packet | review_packet | truth_candidate | runtime_adapter
  target_scale:
  preserved_relevant_operators:
  integrated_out_irrelevant_detail:
  preserved_marginal_transfer_features:
  unsafe_to_integrate_out:
  distortion_notes:
  reversible_refs:
  reviewer_confidence: low | medium | high
```

#### 27.10.2 Effective rank audit

```yaml
effective_rank_audit:
  target_surface:
  proposed_change:
  estimated_behavior_delta: low | medium | high | unknown
  estimated_rank_need: low | medium | high | unknown
  full_rewrite_needed: true | false | unknown
  low_rank_patch_sufficient: true | false | unknown
  proxy_basis:
    - behavioral_probe_delta
    - output_distribution_delta
    - schema_field_delta
    - review_surface_delta
    - runtime_constraint_delta
  validation_plan:
```

#### 27.10.3 Low-rank patch budget

```yaml
low_rank_patch_budget:
  patch_id:
  target_order_parameter_or_surface:
  intended_behavior_delta:
  minimal_patch_surface:
  effective_rank_guess: low | medium | high | unknown
  preserved_base_behavior:
  changed_behavior:
  rollback_path:
  validation_probe:
  complexity_rent:
```

#### 27.10.4 Relevant / irrelevant / marginal operator record

```yaml
operator_relevance_record:
  artifact_or_layer:
  relevant_operators:
    - name:
      reason:
      downstream_decision_impact:
  irrelevant_operators:
    - name:
      reason_safe_to_suppress:
      reversible_ref:
  marginal_operators:
    - name:
      transfer_value:
      preserve_or_monitor:
  unresolved_classification:
```

#### 27.10.5 CoT bridge probe

```yaml
cot_bridge_probe:
  task_id:
  domain_count_estimate:
  disconnected_concept_clusters:
  baseline_without_cot:
  with_cot:
  effective_bridge_edges_added:
  answer_quality_delta: degraded | unchanged | improved | unknown
  token_cost_delta:
  decision: use_cot | avoid_cot | use_structured_bridge_only | escalate
```

---

### 27.11 Round 6 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may refine compression and adapter-change principles if promoted

  prompt_layering_contract:
    reason: layer transformations may need explicit preserved/suppressed/marginal record

  governance_matrix:
    reason: low-rank patch and geometry proxy must not cross truth/authority boundaries

  packet_future:
    reason: rg_layer_transform_check and operator_relevance_record may become packet shell fields

  runtime_future:
    reason: runtime adapters may use low_rank_patch_budget and CoT bridge probe policies

  memory_plane:
    reason: compression and retrieval summaries should record unsafe-to-integrate-out content

  zh_tw_human_docs:
    reason: high-value explanation for why compression and CoT are not universal defaults
```

Change-impact warning:

```text
Do not canonicalize Q-II yet. If promoted, it affects compression policy,
runtime adapter policy, prompt layering, packet schemas, and human-facing explanation.
```

---

## 28. Current document status after Round 6

```yaml
document_status:
  version: v0.7
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R6_Q-II_Information_Geometry_RG
  latest_document_review: pass_5_navigation_and_decision_surface_hardening
  latest_accepted_kernel: Information_Geometry_RG_Layer_Budget_Kernel
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v0.7
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.5 Current document debt register
    - 27. Round 6 — Q-II Information Geometry × Renormalization Group
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - QII_sources_may_need_full_pdf_audit_if_promoted_to_canonical_policy
  intended_next_update: Q-III Stochastic Resonance × Weber-Fechner, RecursiveMAS shock integration, WFGY representation compiler round, or dedicated primitive-index cleanup
```

---

## 29. Round 7 — Q-III Stochastic Resonance × Weber–Fechner Law

> status: active round log  
> theme: Q-III · calibrated noise and sublinear scoring for evaluation sensitivity  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Benzi et al., Collins et al., Stevens, Bishop, and Gneiting/Raftery were handled through accessible abstracts, bibliographic records, and source summaries available in this session. This round imports robust design principles, not a production-ready statistical calibration protocol.

---

### 29.1 Round 7 core question

```text
Can shadowMAS improve evaluation sensitivity by using calibrated noise to reveal weak but meaningful signals,
while using log/sublinear scoring to prevent large cheap gains from dominating reward or review surfaces?
```

v4 Q-III frames two ideas together:

```yaml
stochastic_resonance:
  claim: a nonzero amount of noise can improve weak-signal detection in threshold systems
  danger: too little noise misses weak signals; too much noise destroys signal

weber_fechner_stevens:
  claim: perception often compresses stimulus intensity through log or power-law scaling
  danger: linear scoring overweights large raw differences and underweights subtle quality differences
```

Round 7 asks whether this becomes a shadowMAS design kernel for evaluation, reward, review, and scoring surfaces.

Working answer:

```text
Yes, but only as a bounded evaluation-sensitivity kernel.
Noise is allowed only where weak-signal detection or training robustness is the point.
Noise must not enter truth promotion, binary correctness checks, schema validation, authority decisions, or reproducibility-critical acceptance gates.
```

---

### 29.2 Feynman explanation

Imagine a tiny radio signal hidden below a detector threshold.

Bad detector:

```text
threshold too high + zero noise → weak but real signal never crosses threshold
```

Stochastic resonance says:

```text
A small amount of noise can sometimes lift the weak signal over the threshold.
The detector now notices something it would otherwise miss.
```

But this is not magic:

```text
too little noise → signal remains invisible
tuned noise → weak signal becomes detectable
too much noise → everything becomes static
```

Weber–Fechner / Stevens adds another issue:

```text
Human and evaluation systems often do not respond linearly to raw stimulus size.
A change from 1 to 2 can matter more than a change from 101 to 102.
```

shadowMAS translation:

```text
Evaluation should be sensitive to subtle, meaningful improvements without letting huge but cheap score jumps dominate.
Use calibrated noise only to test weak-signal robustness.
Use log/sublinear scoring only when the score has a real dynamic range.
```

---

### 29.3 Source basis captured in this round

#### v4 Q-III claim

v4 says Q-III merges:

```yaml
stochastic_resonance:
  source_systems:
    - Benzi et al. 1981/1982 climate stochastic resonance
    - Collins et al. sensory/excitable systems
  mechanism: weak signal + nonlinear threshold + optimal nonzero noise
  shape: inverted-U relation between noise level and detection quality

psychophysics:
  source_systems:
    - Fechner 1860 Weber-Fechner logarithmic law
    - Stevens 1957 power law
  mechanism: perceived/evaluated intensity is sublinear or power-law relative to physical stimulus
  shape: dynamic range compression
```

For shadowMAS, the merge becomes:

```yaml
qiii_shadowmas_translation:
  calibrated_noise:
    use_for:
      - weak signal probing
      - evaluator sensitivity testing
      - training-time robustness
      - marginal quality detection
    do_not_use_for:
      - canonical truth promotion
      - binary correctness
      - schema/API/contract validation
      - human-only authority decisions

  sublinear_scoring:
    use_for:
      - scalar quality scores with wide dynamic range
      - review confidence dashboards
      - reward surfaces vulnerable to cheap large gains
    do_not_use_for:
      - already-binary pass/fail
      - legally or operationally exact thresholds
      - fields whose raw value is itself the contract
```

---

### 29.4 Evidence cards

#### E1 — Benzi / Parisi / Sutera / Vulpiani — stochastic resonance in climatic change

Central source signal:

```text
A nonlinear system under small periodic forcing can exhibit amplified response when random perturbations interact with the system dynamics.
```

The Tellus paper studies a simplified zero-dimensional climate model and describes amplification of random perturbations through interaction between climate-system nonlinearities and orbital forcing. It proposes stochastic resonance as a possible contributor to the 10^5-year peak in paleoclimate spectra.

shadowMAS extraction:

```text
Noise is not always destructive.
In threshold-like evaluation systems, a controlled nonzero noise level can expose weak but meaningful signals.
```

Candidate rule:

```yaml
weak_signal_probe:
  target_signal:
  baseline_detector_threshold:
  noise_levels_tested:
  detection_quality_by_noise_level:
  inverted_u_observed: true | false | unknown
  selected_noise_level:
  allowed_scope: training_probe | evaluator_ablation | research_only
```

Accepted insight:

```text
Calibrated noise is a diagnostic/control parameter, not an excuse for random evaluation.
```

---

#### E2 — Collins / Chow / Imhoff — stochastic resonance without tuning

Central source signal:

```text
Stochastic resonance can improve weak-signal detection in nonlinear systems, but single-unit systems may require noise intensity to be adjusted as the signal changes.
```

The Nature abstract describes stochastic resonance as optimized response of a nonlinear system to weak periodic input through a particular nonzero level of noise. It also warns that optimal intensity may require adjustment when the signal changes.

shadowMAS extraction:

```text
There is no universal noise level.
A noise budget must be tied to task shape, detector threshold, and signal regime.
```

Candidate rule:

```yaml
noise_budget_record:
  evaluation_surface:
  signal_regime: weak | medium | strong | unknown
  stochasticity_scope: none | training_only | probe_only | review_assist_only
  seed_required: true
  reproducibility_required: true
  allowed_noise_range:
  stop_condition:
  rollback_condition:
```

Accepted insight:

```text
Noise must be calibrated per evaluation surface. Global “add randomness” is rejected.
```

---

#### E3 — Stevens 1957 / psychophysical power law

Central source signal:

```text
Equal stimulus ratios can produce equal subjective ratios; a first approximation is a power function whose exponent differs by modality.
```

Stevens’s Psychological Review article is a core source for the power-law formulation of psychophysical scaling.

shadowMAS extraction:

```text
Evaluation intensity does not need to be linear in raw score.
Different evaluation dimensions may need different exponents or transforms.
```

Candidate rule:

```yaml
sublinear_score_transform:
  raw_score_dimension:
  transform_type: log1p | power_law | capped_linear | none
  reason:
  preserves_order: true | false
  changes_threshold_semantics: true | false
  binary_or_contract_field: true | false
  approved_for_use: true | false
```

Accepted insight:

```text
Score transforms are allowed only when they preserve the decision meaning and do not hide threshold semantics.
```

---

#### E4 — Bishop 1995 / training with noise as regularization

Central source signal:

```text
Adding noise to neural-network training data can improve generalization in some circumstances, and can be related to Tikhonov-style regularization.
```

Bishop’s paper is important as an engineering comparison: it turns noise from metaphor into an analyzable regularization mechanism.

shadowMAS extraction:

```text
Noise can be a training-time robustness tool without being allowed into final truth gates.
```

Candidate rule:

```yaml
noise_scope_boundary:
  allowed:
    - training_time_robustness
    - evaluator_sensitivity_ablation
    - weak_signal_probe
  forbidden:
    - final_acceptance_gate
    - canonical_truth_promotion
    - deterministic_contract_validation
    - authority_decision
```

Accepted insight:

```text
Training/probing noise and final-governance determinism must be separated.
```

---

#### E5 — Gneiting & Raftery 2007 / strictly proper scoring rules

Central source signal:

```text
Scoring rules evaluate probabilistic forecasts. Proper scoring rules encourage honest probabilistic assessment, and strictly proper rules make the truthful distribution uniquely optimal.
```

This comparison matters because Q-III can otherwise over-focus on psychophysical score shaping while forgetting incentive compatibility.

shadowMAS extraction:

```text
If shadowMAS evaluates probabilistic claims, score transforms must not reward dishonest confidence.
```

Candidate rule:

```yaml
probabilistic_eval_integrity_check:
  forecast_type: categorical | binary | continuous | interval | none
  scoring_rule:
  strictly_proper: true | false | unknown
  transformed_score:
  transform_preserves_properness: true | false | unknown
  decision: allow | revise | reject | research_only
```

Accepted insight:

```text
Dynamic-range compression must not break honest probabilistic reporting.
```

---

### 29.5 ToT candidate branches

```yaml
tot_branches:
  A_add_noise_to_all_evaluation:
    decision: rejected
    reason: stochastic resonance requires threshold/weak-signal conditions; random evaluation destroys trust and reproducibility

  B_ban_noise_everywhere:
    decision: rejected
    reason: loses weak-signal probing and training robustness value

  C_seeded_calibrated_noise_for_weak_signal_probes:
    decision: accepted
    reason: captures stochastic resonance while preserving reproducibility boundaries

  D_noise_inside_truth_promotion_gate:
    decision: rejected
    reason: canonical truth promotion must remain deterministic, auditable, and authority-bounded

  E_log_scale_all_scores:
    decision: rejected
    reason: binary correctness, schema validation, and exact contracts should not be log-scaled

  F_sublinear_transform_for_wide_dynamic_range_quality_scores:
    decision: accepted
    reason: helps avoid domination by large cheap gains while preserving sensitivity to subtle improvements

  G_ignore_proper_scoring_rules:
    decision: rejected
    reason: probabilistic evaluation can become incentive-incompatible if transforms reward distorted confidence

  H_use_proper_scoring_as_integrity_reference:
    decision: accepted
    reason: protects probabilistic evaluation from becoming merely aesthetic score shaping

  I_one_global_sigma_star:
    decision: rejected
    reason: optimal noise depends on signal, threshold, task shape, and detector regime

  J_noise_budget_record_per_eval_surface:
    decision: accepted
    reason: implementable and auditable boundary for stochastic probes
```

---

### 29.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + F + H
    reason: improves evaluation sensitivity without weakening governance trust
    risk: if framed loosely, people will think shadowMAS endorses random decision gates

  CTO:
    vote: accept C + J
    reason: seeded noise budgets and ablation records are implementable; global noise is not
    risk: exact sigma calibration is not ready for v0

  Security:
    vote: reject D strongly; accept noise_scope_boundary
    reason: stochasticity must not enter authority, promotion, or deterministic validation paths
    risk: noise can hide flaky behavior if not seeded and reported

  CSO:
    vote: accept F
    reason: dynamic-range control is a strong design lens for review dashboards and reward surfaces
    risk: log transforms can hide severity if used on safety or legal thresholds

  CFO:
    vote: accept C cautiously
    reason: weak-signal probes may reduce wasted evaluation cycles and reward hacking cost
    risk: calibration experiments add maintenance and compute cost
```

---

### 29.7 LATS result

```yaml
lats_result:
  best_node:
    name: Bounded Evaluation Sensitivity Kernel
    score: 0.89
    status: candidate_kernel
    why:
      - absorbs stochastic resonance without endorsing random governance
      - absorbs Weber-Fechner/Stevens without corrupting exact validation
      - distinguishes training/probing stochasticity from final deterministic gates
      - adds incentive-safety reference through proper scoring rules
      - produces concrete candidate primitives

  accepted:
    - seeded_calibrated_noise_for_weak_signal_probes
    - noise_budget_record_per_eval_surface
    - sublinear_transform_for_wide_dynamic_range_quality_scores
    - probabilistic_eval_integrity_check
    - training_probe_vs_truth_gate_separation

  rejected:
    - add_noise_to_all_evaluation
    - noise_inside_truth_promotion_gate
    - log_scale_all_scores
    - one_global_sigma_star
    - reward_noise_as_truth_repair

  deferred:
    - exact_sigma_star_calibration_protocol
    - production_log_reward_transform_policy
    - evaluator_sensitivity_benchmark
    - stochastic_resonance_ablation_suite
    - human_review_confidence_noise_policy
  - production_reviewer_drift_dashboard
  - evaluation_probe_set_registry
  - recalibration_governance_protocol
  - formal_categorical_commutativity_validator
  - reward_model_ensemble_policy
```

---

### 29.8 Round 7 accepted kernel

```yaml
stochastic_resonance_log_scale_evaluation_kernel:
  core_sentence: >
    shadowMAS should treat calibrated noise and sublinear scoring as bounded evaluation-sensitivity tools:
    seeded nonzero noise may be used to probe weak but meaningful signals, while log/power-law transforms may
    control wide dynamic-range quality scores; neither may alter deterministic correctness, schema validation,
    protected authority decisions, or canonical truth promotion.

  principles:
    - noise_is_probe_or_training_tool_not_truth_gate
    - nonzero_noise_requires_seed_scope_and_rollback
    - weak_signal_detection_needs_calibration_not_global_randomness
    - sublinear_scoring_only_for_gradated_dynamic_range_surfaces
    - binary_contract_schema_and_authority_checks_remain_untransformed
    - probabilistic_scores_must_preserve_honest_reporting_incentives
    - every_noise_or_score_transform_needs_a_boundary_record
```

---

### 29.9 Candidate shadowMAS primitives from Round 7

#### 29.9.1 Weak signal probe

```yaml
weak_signal_probe:
  probe_id:
  evaluation_surface:
  target_signal:
  expected_signal_strength: weak | medium | strong | unknown
  detector_threshold:
  noise_levels_tested:
  metric_by_noise_level:
  inverted_u_observed: true | false | unknown
  selected_noise_level:
  seed:
  reproducibility_notes:
  decision: allow_probe | revise | reject | research_only
```

#### 29.9.2 Noise budget record

```yaml
noise_budget_record:
  budget_id:
  evaluation_surface:
  allowed_scope: training_only | probe_only | review_assist_only | none
  forbidden_scope:
    - final_acceptance_gate
    - canonical_truth_promotion
    - schema_validation
    - authority_decision
  seed_required: true
  max_noise_level:
  calibration_method:
  rollback_condition:
  reporting_requirement:
```

#### 29.9.3 Sublinear score transform

```yaml
sublinear_score_transform:
  transform_id:
  raw_score_dimension:
  transform_type: log1p | power_law | capped_linear | none
  exponent_if_power_law:
  reason:
  applies_to_dynamic_range: true | false
  preserves_order: true | false
  changes_threshold_semantics: true | false
  forbidden_for_binary_or_contract_field: true
  reviewer_visible_explanation:
```

#### 29.9.4 Probabilistic evaluation integrity check

```yaml
probabilistic_eval_integrity_check:
  check_id:
  forecast_type: binary | categorical | continuous | interval | none
  base_scoring_rule:
  strictly_proper: true | false | unknown
  proposed_transform:
  transform_preserves_honesty_incentive: true | false | unknown
  confidence_calibration_checked: true | false
  decision: allow | revise | reject | research_only
```

#### 29.9.5 Evaluation sensitivity report

```yaml
evaluation_sensitivity_report:
  report_id:
  evaluation_surface:
  weak_signal_findings:
  noise_budget_used:
  score_transform_used:
  false_positive_risk:
  false_negative_risk:
  reproducibility_status:
  boundary_violations:
  recommended_action:
```

---

### 29.10 Round 7 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may refine evaluation/review principles if promoted

  governance_matrix:
    reason: must explicitly keep stochastic probes out of T0/T2 promotion and authority gates

  packet_future:
    reason: weak_signal_probe, noise_budget_record, and score_transform may become review/evaluation packet fields

  runtime_future:
    reason: evaluation runners may need seeding, reproducibility logs, and noise-scope enforcement

  prompt_layering_contract:
    reason: runtime adapters may expose evaluation sensitivity settings without redefining truth

  zh_tw_human_docs:
    reason: high-value explanation needed to prevent “randomness everywhere” misinterpretation
```

Change-impact warning:

```text
Do not canonicalize Q-III yet. If promoted, it affects review policy, evaluator design,
runtime reproducibility, packet fields, and human-facing explanation. It must not change
truth promotion semantics without governance-matrix review.
```

---

## 30. Document self-optimization — sixth pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 6  
> object under review: same single active design log after adding Round 7  
> goal: prevent Q-III from being misread as broad permission for stochastic governance and keep the expanding one-file document navigable.

---

### 30.1 Problem diagnosis after Round 7

Round 7 introduces a special risk that earlier kernels did not:

```text
Readers may confuse evaluation-sensitivity stochasticity with permission to randomize final decisions.
```

This is dangerous because shadowMAS already has strict truth and authority boundaries. Q-III must therefore be documented as:

```yaml
allowed:
  - seeded weak-signal probes
  - training-time robustness
  - review-assist sensitivity experiments
  - dynamic-range score shaping for gradated quality signals

forbidden:
  - stochastic truth promotion
  - unseeded acceptance gates
  - log-scaling binary correctness
  - noisy schema/API/contract validation
  - randomness in human-only authority decisions
```

The document-level issue is now:

```text
The active ledger is still useful, but candidate primitive extraction is becoming increasingly expensive.
```

---

### 30.2 ToT branches for document optimization

```yaml
document_tot_branches:
  A_append_Round_7_only:
    decision: rejected
    reason: would leave Q-III boundary risk too implicit

  B_rewrite_entire_file_into_final_book:
    decision: rejected_for_now
    reason: still active research; full rewrite would create churn and risk evidence loss

  C_append_Round_7_and_update_control_surfaces:
    decision: accepted
    reason: keeps one-file workflow while making latest state visible

  D_create_consolidated_primitive_index_now:
    decision: deferred
    reason: useful soon, but doing it now would be larger than the requested round update

  E_add_QIII_boundary_debt_item:
    decision: accepted
    reason: noise/scoring kernel needs explicit maintenance warning
```

---

### 30.3 MoE votes for document optimization

```yaml
document_moe_votes:
  CEO:
    vote: C + E
    reason: latest kernel must be visible at the top and not hidden in round details

  CTO:
    vote: C
    reason: update kernel index and final status; do not restructure all primitives yet

  Security:
    vote: E strongly
    reason: stochasticity boundary must be visible before any implementation agent reads Round 7

  CSO:
    vote: C
    reason: Q-III story is valuable only if framed as bounded evaluation sensitivity

  CFO:
    vote: D_deferred
    reason: primitive index is needed soon, but full extraction now costs more than this pass requires
```

---

### 30.4 LATS result for document optimization

```yaml
document_lats_result:
  best_node:
    name: Round 7 Integrated with Stochastic Boundary Warnings
    score: 0.92
    status: accepted_and_applied
    applied_now:
      - updated top active decision ledger to include R7 kernel
      - updated document control plane to v0.8
      - updated current kernel index with R7
      - added D6 evaluation kernel boundary debt
      - appended Round 7 detailed log
      - appended final v0.8 status block
    deferred:
      - consolidated primitive index
      - paper evidence appendix restructure
      - grouped accepted/rejected/deferred table
```

---

### 30.5 New document-level rule

```text
Any future kernel that introduces stochasticity, compression, hidden state, or score transformation
must include an explicit forbidden-scope block before candidate primitives are accepted.
```

Reason:

```text
These mechanisms can silently alter authority, truth, or review meaning if their boundaries are implicit.
```

---

## 31. Current document status after Round 7

```yaml
document_status:
  version: v0.8
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R7_Q-III_Stochastic_Resonance_Weber_Fechner
  latest_document_review: pass_6_navigation_and_evaluation_kernel_integration
  latest_accepted_kernel: Stochastic_Resonance_Log_Scale_Evaluation_Kernel
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v0.8
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.5 Current document debt register
    - 29. Round 7 — Q-III Stochastic Resonance × Weber–Fechner Law
    - 30. Document self-optimization — sixth pass
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - QIII_noise_and_score_transform_boundaries_must_be_kept_visible
    - QII_and_QIII_sources_may_need_full_pdf_audit_if_promoted_to_canonical_policy
  intended_next_update: S-I Punctuated Equilibrium × Spandrel, S-II Construction Grammar × FCA × Epigenetics, RecursiveMAS shock integration, WFGY representation compiler round, or dedicated primitive-index cleanup
```


---

## 32. Round 8 — S-I Punctuated Equilibrium × Spandrel

> status: active round log  
> theme: S-I · punctuated equilibrium × spandrel  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Gould & Eldredge 1977 and Gould & Lewontin 1979 were treated as the biological source anchors. Wei et al. 2022 was used as the AI emergence anchor. Kaplan et al. 2020 and Schaeffer et al. 2023 were used as comparison scans to prevent overreading every performance jump as true emergence.

---

### 32.1 Round 8 core question

```text
Should shadowMAS treat long plateaus, sudden capability jumps, and unexpected side-effect capabilities
as strategic signals rather than simple failure/success states?
```

V4 S-I merges two strategic ideas:

```yaml
punctuated_equilibrium:
  role: long stasis may precede rapid transition into a new stable regime
  design_warning: do not automatically stop just because visible metrics plateau

spandrel:
  role: some valuable capabilities are structural by-products of a broader objective
  design_warning: do not directly supervise only the visible output form and mistake mimicry for the underlying capability
```

For shadowMAS, this is not a training recipe by itself. It is a **strategy kernel** for deciding how to treat:

```yaml
shadowmas_strategy_surfaces:
  - repeated agent failure / plateau
  - delayed emergence of cross-agent competence
  - capabilities that appear as by-products of packet discipline, review discipline, or routing pressure
  - evaluation curves with sudden jumps
  - prompt / workflow designs that accidentally train surface mimicry instead of durable capability
```

---

### 32.2 Feynman explanation

#### Punctuated equilibrium side

Imagine watching a seed every hour.

For a long time, nothing seems to happen:

```text
No visible leaf.
No visible flower.
No visible fruit.
```

A shallow observer says:

```text
This is failing. Stop watering.
```

But inside the seed, structure may be forming. Then one day the sprout breaks the surface.

The lesson is not:

```text
Always wait forever.
```

The lesson is:

```text
A plateau is not enough evidence by itself.
Check whether hidden structure is forming.
```

shadowMAS translation:

```text
If a workflow stalls, do not instantly discard it.
Run probes:
- Is residual decreasing even if final success is flat?
- Are cross-agent dependencies becoming better connected?
- Are failures becoming narrower?
- Is the system near a routing / variety / representation threshold?
```

#### Spandrel side

A building arch creates triangular spaces between arches. Those spaces can later be decorated beautifully, but they were not the original purpose of the arch.

A spandrel is:

```text
a useful side-effect of a structure built for another reason.
```

AI translation:

```text
A model trained for next-token prediction may develop reasoning, code, translation, or planning-like behavior as structural by-products.
```

But a dangerous mistake is:

```text
If reasoning text is useful, directly train the system to emit reasoning-looking text.
```

That may produce **mimicry**, not the underlying capability.

shadowMAS translation:

```text
If we want durable capability, design the parent objective / workflow pressure that would make the capability necessary,
then test the capability behaviorally.
Do not only train the visible format.
```

---

### 32.3 Source basis captured in this round

#### v4 S-I claim

V4 frames S-I as:

```yaml
punctuated_equilibrium:
  biological_pattern: long stasis -> rapid burst -> new stasis
  training_analogy: loss plateau -> phase transition -> new capability baseline

spandrel:
  observation: reasoning / math / code may emerge as structural by-products of next-token prediction
  warning: direct supervision of the by-product may teach output shape instead of underlying capacity
```

V4 suggests engineering toward phase transition by increasing data diversity, introducing harder task distributions, creating capacity headroom, or briefly loosening constraints. This round accepts the strategic lens but adds a boundary:

```yaml
boundary_added_by_round_8:
  plateau_is_hypothesis_not_proof: true
  emergence_claim_requires_metric_audit: true
  spandrel_claim_requires_behavioral_probe: true
  direct_supervision_allowed_when_capability_is_directly_specifiable: true
```

---

### 32.4 Paper set for this round

```yaml
main_reads:
  - Gould_and_Eldredge_1977_Punctuated_Equilibria
  - Gould_and_Lewontin_1979_Spandrels
  - Wei_et_al_2022_Emergent_Abilities_of_Large_Language_Models

comparison_scans:
  - Kaplan_et_al_2020_Scaling_Laws_for_Neural_Language_Models
  - Schaeffer_et_al_2023_Are_Emergent_Abilities_a_Mirage
```

Why this set:

```text
Gould & Eldredge provide the stasis/punctuation pattern.
Gould & Lewontin provide the anti-adaptationist warning: do not explain every observed feature as directly optimized.
Wei et al. provide the AI emergence bridge.
Kaplan et al. provide the smooth scaling baseline.
Schaeffer et al. provide the metric-artifact warning.
```

---

### 32.5 Evidence cards

#### E1 — Gould & Eldredge 1977 / punctuated equilibria

Source claim captured:

```text
Evolution may be concentrated in comparatively rapid events, while species often remain in long stasis or mild nondirectional fluctuation.
```

The Cambridge Core abstract states the central view: punctuational change dominates the history of life; many species do not change appreciably during their geological history, and phyletic gradualism is rare relative to the major events they discuss.

shadowMAS extraction:

```yaml
plateau_interpretation:
  bad_reading: flat visible metric means nothing is happening
  better_reading: flat visible metric may mean no progress, or hidden structure forming below the visible threshold
  required_action: run transition probes before stopping or escalating
```

Design implication:

```text
Do not let single visible success/failure metrics become the only view of progress.
Track residual narrowing, cross-agent connectivity, representation quality, and failure-mode compression.
```

Accepted insight:

```text
A plateau is a diagnostic state, not automatically a stop condition.
```

Boundary:

```text
A plateau is also not proof that a breakthrough is coming. It only justifies targeted probing.
```

---

#### E2 — Gould & Lewontin 1979 / spandrels and adaptationist overreach

Source claim captured:

```text
Not every useful or visible trait should be explained as directly optimized for its current use.
```

The paper criticizes an adaptationist programme that treats natural selection as an optimizing agent and too quickly turns every observed feature into an adaptive story.

shadowMAS extraction:

```yaml
capability_origin_warning:
  observed_useful_capability: true
  do_not_assume: it was directly optimized for that visible use
  ask_instead:
    - what parent structure produced it?
    - what objective pressure made it likely?
    - what constraints shaped it?
    - can it be tested behaviorally rather than by surface form?
```

Design implication:

```text
Do not assume every useful behavior in an agent system should be directly trained, prompted, or hard-coded.
Some durable behaviors may emerge from packet pressure, review pressure, routing pressure, and feedback loops.
```

Accepted insight:

```text
Design the parent structure that makes the desired capability useful, then probe whether the capability actually appears.
```

Boundary:

```text
Spandrel language must not become a license for hand-wavy behavior. If a capability must be reliable, governed, or contract-bound, it still needs explicit tests and review gates.
```

---

#### E3 — Wei et al. 2022 / emergent abilities of large language models

Source claim captured:

```text
An emergent ability is absent in smaller models but present in larger models, and cannot be predicted merely by extrapolating smaller-model performance.
```

shadowMAS extraction:

```yaml
emergence_probe:
  observed_pattern: capability absent below threshold, present above threshold
  do_not_jump_to: architecture miracle
  check_first:
    - metric discontinuity
    - prompt sensitivity
    - evaluation threshold effects
    - data contamination
    - bridge-connectivity effects
    - latent capability vs surface format mimicry
```

Design implication:

```text
Capability emergence in shadowMAS should be measured through behavioral probes across task families, not through a single thresholded pass/fail event.
```

Accepted insight:

```text
Emergence is a valid design signal, but only after metric and probe audit.
```

---

#### E4 — Kaplan et al. 2020 / smooth scaling baseline comparison

Source claim captured:

```text
Language-model cross-entropy loss can scale as a power law with model size, dataset size, and compute across very large ranges.
```

Comparison role:

```text
This prevents S-I from overclaiming. Not all capability improvement is punctuated; some important improvement is smooth, predictable, and resource-driven.
```

shadowMAS extraction:

```yaml
scaling_baseline_check:
  before_claiming_phase_transition:
    - test whether continuous scaling / more budget / better retrieval explains the change
    - compare against smooth trend line when data exists
    - avoid declaring punctuation merely because the measurement interval is sparse
```

Accepted insight:

```text
Punctuated explanations require contrast against smooth scaling baselines.
```

---

#### E5 — Schaeffer et al. 2023 / emergent abilities as possible metric artifact

Source claim captured:

```text
Some apparent emergent abilities may arise from the choice of nonlinear or discontinuous metrics rather than from a fundamental behavioral discontinuity.
```

Comparison role:

```text
This is the strongest safety guard for S-I. A sudden jump in score may be a measurement artifact.
```

shadowMAS extraction:

```yaml
emergence_metric_audit:
  check:
    - thresholded metric vs continuous metric
    - binary pass/fail vs partial credit
    - sample size around threshold
    - confidence interval
    - prompt variance
    - task-family variance
```

Accepted insight:

```text
Any shadowMAS claim of emergence must survive a metric audit.
```

Boundary:

```text
Do not turn every step-function chart into a phase-transition story.
```

---

### 32.6 shadowMAS synthesis

Round 8 creates a strategy kernel:

```yaml
punctuated_spandrel_strategy_kernel_candidate:
  purpose: govern how shadowMAS interprets plateaus, sudden capability jumps, and by-product capabilities
  core_logic:
    - plateau_requires_probe_not_panic
    - emergence_requires_metric_audit
    - spandrel_capability_requires_parent_objective_design
    - behavioral_probe_beats_surface_format_probe
    - direct_supervision_is_allowed_when_capability_is_directly_specifiable
```

This kernel connects backward:

```yaml
links_to_prior_kernels:
  R1_Compression_Residual_Occam:
    relation: plateau probes should track residual narrowing, not only success/failure

  R5_Variety_Coverage_Connectivity:
    relation: sudden improvement may come from crossing capability-connectivity threshold

  R6_Information_Geometry_RG_Layer_Budget:
    relation: phase transition may reflect relevant-operator preservation or representation compression crossing threshold

  R7_Stochastic_Resonance_Log_Scale_Evaluation:
    relation: emergence claims must survive metric audit and weak-signal evaluation design
```

For shadowMAS specifically, S-I should influence:

```yaml
shadowmas_implications:
  strategy:
    - do not prematurely kill promising plateaued workflows without probes
    - do not assume plateau means eventual success
    - do not design only by direct output mimicry

  evaluation:
    - add emergence metric audit before claiming phase transition
    - use behavioral capability probes over surface-format probes

  runtime:
    - plateau_intervention can include diversity injection, bridge-agent routing, or signal-field exploration
    - interventions must be bounded and reversible

  prompt_design:
    - desired durable capability should be induced by task pressure and review pressure, not only by asking for the visible shape
```

---

### 32.7 ToT candidate branches

```yaml
tot_branches:
  A_treat_plateau_as_failure:
    decision: rejected
    reason: violates punctuated-equilibrium insight; visible stasis may hide structural reorganization

  B_treat_every_plateau_as_pre_breakthrough:
    decision: rejected
    reason: wishful waiting; plateau may be true failure, data deficit, routing deficit, or metric artifact

  C_plateau_as_probe_state:
    decision: accepted
    reason: best interpretation; plateau triggers targeted diagnostic probes before stop / escalate / intervene

  D_directly_supervise_every_desired_capability:
    decision: rejected_as_default
    reason: may train surface mimicry and miss parent structure that produces durable capability

  E_design_parent_objective_pressure:
    decision: accepted
    reason: aligns with spandrel insight; engineer conditions that make desired capability useful, then probe behavior

  F_spandrel_as_excuse_for_unspecified_behavior:
    decision: rejected
    reason: shadowMAS requires correctness, traceability, and review; spandrel language cannot replace specs or tests

  G_claim_emergence_from_single_threshold_metric:
    decision: rejected
    reason: comparison scan shows discontinuous metrics can manufacture apparent emergence

  H_emergence_metric_audit:
    decision: accepted
    reason: required before treating sudden score jumps as real capability emergence

  I_behavioral_probe_over_format_probe:
    decision: accepted
    reason: durable capability must be tested by transfer behavior, not merely output appearance

  J_plateau_intervention_as_unbounded_runtime_experiment:
    decision: rejected
    reason: intervention must remain bounded, reversible, and authority-safe
```

---

### 32.8 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + H
    reason: this prevents both premature abandonment and hype-driven overclaiming.
    risk: too much patience can become strategic drift.

  CTO:
    vote: accept C + I
    reason: plateau probes and behavioral probes are implementable; vague spandrel talk is not.
    risk: parent-objective design needs concrete measurable probes.

  Security:
    vote: accept F_rejection + H
    reason: spandrel cannot excuse unreviewable behavior; emergence claims need metric audit before governance impact.
    risk: hidden capability claims could bypass safety review.

  CSO:
    vote: accept E
    reason: parent-objective design gives shadowMAS a sharper strategic lens than direct prompt imitation.
    risk: must be explained plainly or future agents will misuse it.

  CFO:
    vote: accept C cautiously
    reason: probes cost less than full restarts, but waiting through every plateau is expensive.
    risk: plateau-intervention budget must be capped.
```

---

### 32.9 LATS result

```yaml
lats_result:
  best_node:
    name: Probeable Plateau + Parent Objective Strategy
    score: 0.91
    status: candidate_kernel
    why:
      - turns S-I into bounded strategy rather than vague evolutionary metaphor
      - avoids both premature stopping and blind waiting
      - imports spandrel insight without abandoning tests/specs
      - uses Q-III metric audit to avoid fake emergence
      - connects to R5/R6 thresholds and representation changes

  accepted:
    - plateau_as_probe_state
    - parent_objective_design_for_spandrel_like_capability
    - behavioral_probe_over_surface_format_probe
    - emergence_metric_audit
    - bounded_plateau_intervention_policy

  rejected:
    - plateau_as_automatic_failure
    - plateau_as_automatic_breakthrough_pending
    - direct_spandrel_mimicry_supervision_as_default
    - single_threshold_metric_emergence_claim
    - spandrel_as_excuse_for_unspecified_behavior
    - unbounded_plateau_experimentation

  deferred:
    - production_plateau_intervention_protocol
    - spandrel_parent_objective_library
    - capability_emergence_dashboard
    - long_horizon_phase_transition_experiment_suite
```

---

### 32.10 Round 8 accepted kernel

```yaml
punctuated_spandrel_strategy_kernel:
  core_sentence: >
    shadowMAS should treat plateaus and sudden capability jumps as probeable strategy states,
    not automatic failure or automatic emergence. Durable spandrel-like capabilities should be
    pursued by designing parent objective / workflow pressure and then validating behaviorally;
    direct surface-form supervision, single threshold metrics, and unbounded waiting are rejected.

  principles:
    - plateau_is_probe_state_not_stop_condition
    - plateau_is_not_proof_of_future_breakthrough
    - emergence_claim_requires_metric_audit
    - spandrel_capability_requires_parent_objective_design
    - behavioral_probe_over_surface_format_probe
    - bounded_reversible_plateau_intervention
    - direct_supervision_allowed_when_capability_is_directly_specifiable
```

---

### 32.11 Candidate shadowMAS primitives from Round 8

#### 32.11.1 Plateau transition probe

```yaml
plateau_transition_probe:
  probe_id:
  target_workflow:
  visible_metric:
  plateau_window:
  current_state:
    final_success_trend: flat | improving | degrading | unknown
    residual_trend: narrowing | stable | widening | mixed | unknown
    failure_mode_entropy: decreasing | stable | increasing | unknown
    capability_connectivity: below_threshold | near_threshold | above_threshold | unknown
    representation_quality: improving | stable | degrading | unknown
  probes_run:
    - residual_narrowing_probe
    - cross_domain_bridge_probe
    - prompt_variance_probe
    - metric_continuity_probe
  decision: stop | continue | diversify | inject_bridge | loosen_constraint | escalate_review
  budget_cap:
  rollback_path:
```

#### 32.11.2 Parent objective design record

```yaml
parent_objective_design_record:
  desired_capability:
  visible_surface_form:
  suspected_parent_objective:
  why_direct_supervision_may_fail:
  structural_pressure_needed:
    - task_pressure
    - review_pressure
    - routing_pressure
    - feedback_pressure
  proxy_training_or_workflow_task:
  behavioral_probe:
  anti_mimicry_check:
  success_criteria:
```

#### 32.11.3 Spandrel capability probe

```yaml
spandrel_capability_probe:
  capability:
  expected_as_byproduct_of:
  probe_family:
    - near_distribution
    - far_transfer
    - adversarial_surface_form
    - format_changed_same_skill
    - same_format_different_skill
  pass_condition:
  fail_condition:
  mimicry_warning_signals:
    - works_only_with_one_template
    - fails_when_format_changes
    - cannot_transfer_to_equivalent_task
    - produces reasoning_shape_without_correct_decision
```

#### 32.11.4 Emergence metric audit

```yaml
emergence_metric_audit:
  claim:
  metric_used:
  metric_type: continuous | ordinal | thresholded | binary | discontinuous
  alternative_metrics_checked:
  sample_density_around_threshold:
  confidence_interval:
  prompt_variance:
  model_or_agent_scale_axis:
  smooth_baseline_available: true | false
  artifact_risk: low | medium | high
  decision: accept_emergence_signal | downgrade_to_metric_artifact | needs_more_data
```

#### 32.11.5 Bounded plateau intervention policy

```yaml
bounded_plateau_intervention_policy:
  workflow:
  plateau_trigger:
  allowed_interventions:
    - increase_data_or_task_diversity
    - add_bridge_agent_or_bridge_packet
    - run_signal_field_exploration
    - loosen_non_truth_constraint_temporarily
    - increase_evaluation_resolution
  forbidden_interventions:
    - bypass_human_authority
    - promote_unverified_truth
    - remove_schema_or_contract_validation
    - continue_without_budget_cap
  max_iterations:
  stop_condition:
  escalation_condition:
```

---

### 32.12 Forbidden-scope block

```yaml
forbidden_scope:
  do_not_use_SI_to:
    - justify waiting forever through a plateau
    - claim emergence from one thresholded metric
    - skip acceptance criteria because capability may be a spandrel
    - replace direct tests for contract-bound functionality
    - bypass human authority or canonical truth gates
    - treat output format mimicry as durable reasoning capability
    - run unbounded runtime experiments without rollback and budget cap
```

This block is required because S-I can otherwise become a rationalization machine:

```text
"It failed, but maybe it is in stasis."
"It copied reasoning text, so maybe it has reasoning."
"The chart jumped, so emergence happened."
```

All three are unsafe without probes.

---

### 32.13 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may eventually affect prompt policy, evaluation policy, and runtime strategy, but not canonical yet

  governance_matrix:
    reason: plateau interventions must not bypass T0/T1/T2 promotion and authority boundaries

  runtime_future:
    reason: plateau_transition_probe and bounded_plateau_intervention_policy may become R-layer diagnostic tools

  packet_future:
    reason: parent_objective_design_record and spandrel_capability_probe may become review/evaluation packet extensions

  evaluation_future:
    reason: emergence_metric_audit connects directly to Q-III scoring and weak-signal boundary rules

  zh_tw_human_docs:
    reason: high-value explanation for why shadowMAS should not equate visible stasis with failure or visible format with capability
```

Change-impact warning:

```text
Do not update canonical truth yet. Round 8 creates an active candidate strategy kernel.
Formal adoption would require review of current truth, governance matrix, runtime future, packet future, and human-facing explanation.
```

---

### 32.14 Round 8 source links recorded

```yaml
source_links:
  Gould_Eldredge_1977:
    title: Punctuated equilibria: the tempo and mode of evolution reconsidered
    source: Cambridge Core / Paleobiology 3(2), 115-151
    doi: 10.1017/S0094837300005224

  Gould_Lewontin_1979:
    title: The spandrels of San Marco and the Panglossian paradigm
    source: Proceedings of the Royal Society B
    doi: 10.1098/rspb.1979.0086

  Wei_et_al_2022:
    title: Emergent Abilities of Large Language Models
    source: arXiv 2206.07682

  Kaplan_et_al_2020:
    title: Scaling Laws for Neural Language Models
    source: OpenAI / arXiv 2001.08361

  Schaeffer_et_al_2023:
    title: Are Emergent Abilities of Large Language Models a Mirage?
    source: arXiv 2304.15004
```

---

## 33. Current document status after Round 8

```yaml
document_status:
  version: v0.9
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_round: R8_S-I_Punctuated_Equilibrium_Spandrel
  latest_document_review: pass_6_navigation_and_evaluation_kernel_integration
  latest_accepted_kernel: Punctuated_Spandrel_Strategy_Kernel
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.5 Current document debt register
    - 32. Round 8 — S-I Punctuated Equilibrium × Spandrel
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - QIII_noise_and_score_transform_boundaries_must_be_kept_visible
    - SI_plateau_and_spandrel_claims_require_metric_and_behavioral_probe_boundaries
    - QII_QIII_SI_sources_may_need_full_pdf_audit_if_promoted_to_canonical_policy
  intended_next_update: S-II Construction Grammar × FCA × Epigenetics, RecursiveMAS shock integration, WFGY representation compiler round, or dedicated primitive-index cleanup
```


---

## 34. Document self-optimization — seventh pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 7  
> object under review: same single active design log after Round 8  
> goal: answer closeout horizon, reduce latest-status ambiguity, and prevent future content rounds from worsening navigation debt.  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, decisions, and resulting document edits.

---

### 34.1 Problem diagnosis

The file is now useful but heavy. Its main failure mode is no longer missing evidence. Its main failure mode is that historical state markers can look current.

Current measured symptoms:

```yaml
document_size_snapshot:
  version_before_pass: v0.9
  approximate_lines: 7527
  approximate_characters: 210000
  current_document_status_markers: 11
  repeated_control_plane_markers: multiple historical versions
  repeated_kernel_index_markers: multiple historical versions
```

Primary document risks:

```yaml
risks:
  - latest_status_ambiguity
  - primitive_candidate_scattering
  - self_optimization_history_competing_with_current_navigation
  - no_explicit_finish_horizon
  - future_content_rounds_increasing_giant_surface_pressure
```

This pass therefore does not add a new v4 content round. It improves the document as a decision surface.

---

### 34.2 ToT branches

```yaml
document_tot_branches:
  A_keep_appending_without_closeout_plan:
    decision: rejected
    reason: this would make every future round harder to interpret

  B_rewrite_entire_document_now:
    decision: rejected_for_now
    reason: too much churn while research intake is still active; risks losing traceability

  C_add_closeout_horizon_to_top_control_plane:
    decision: accepted_and_applied
    reason: directly answers how many more document-only rounds are needed and gives finish criteria

  D_delete_old_status_sections:
    decision: rejected_for_now
    reason: preserves traceability; better to rename and demote them before deletion is considered

  E_rename_latest_round_status_as_historical_snapshot:
    decision: accepted_and_applied
    reason: prevents v0.9 round status from masquerading as the latest v1.0 document status

  F_create_consolidated_primitive_index_now:
    decision: deferred_to_next_document_round
    reason: important, but should be a focused pass because primitive extraction affects many sections

  G_allow_split_file_architecture_now:
    decision: deferred_to_owner_decision
    reason: current instruction keeps a single active design log; split path is recorded as an option only
```

---

### 34.3 MoE votes

```yaml
document_moe_votes:
  CEO:
    vote: accept C + E
    reason: the document needs an executive closeout path, not infinite optimization
    warning: do not let documentation optimization replace actual promotion review

  CTO:
    vote: accept C, defer F
    reason: primitive index is necessary, but should be done as a clean extraction pass
    warning: do not manually duplicate primitive definitions into inconsistent tables

  Security:
    vote: accept E strongly
    reason: old status sections can create authority confusion if not clearly marked historical
    warning: non-canonical status must remain visible

  CSO:
    vote: accept C
    reason: knowing the route to finish improves strategic use of the document
    warning: if the first page keeps growing, it will violate its own must-see rule

  CFO:
    vote: accept closeout estimate
    reason: endless optimization has maintenance cost; round budget should be explicit
    warning: avoid optimizing historical narrative that will later move to appendix
```

---

### 34.4 LATS result

```yaml
document_lats_result:
  best_node:
    name: Closeout Horizon + Single Latest Entry Hardening
    score: 0.94
    status: accepted_and_applied
    why:
      - answers the owner's question about remaining rounds
      - improves recognition-first navigation
      - keeps traceability without deleting history
      - sets finish criteria for future document-only optimization
      - prevents future content rounds from silently increasing debt

  applied_now:
    - updated top status line to v1.0 document-structure optimization
    - updated control plane from v0.9 to v1.0
    - added D8 closeout horizon document debt entry
    - added 0.6 Closeout horizon and finish criteria
    - renamed section 33 as Current document status after Round 8
    - added this pass-7 review section
    - added latest v1.0 current document status

  accepted_next_document_round:
    - consolidated primitive candidate index

  deferred:
    - split-file architecture
    - full appendix migration of old self-optimization passes
    - deletion of historical current-status blocks
```

---

### 34.5 Current estimate to finish

```yaml
finish_estimate:
  current_version_after_this_pass: v1.0
  single_file_path:
    remaining_document_only_rounds: 3
    likely_versions:
      - v1.1_primitive_candidate_index
      - v1.2_change_impact_and_promotion_queue
      - v1.3_closeout_freeze_reading_path

  split_file_path_if_allowed:
    remaining_document_only_rounds: 2
    likely_versions:
      - v1.1_extract_indexes_and_appendices
      - v1.2_closeout_index_contract

  ongoing_v4_research_path:
    rule: one_short_document_optimization_pass_after_every_two_content_rounds
```

---

### 34.6 New document-level rule

```text
No future content round may append a new kernel without also updating:
1. top active decision ledger,
2. current kernel index,
3. document debt register if debt changes,
4. latest current document status,
5. primitive candidate index once v1.1 exists.
```

---

## 35. Current document status after v1.0 document optimization

```yaml
document_status:
  version: v1.0
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R8_S-I_Punctuated_Equilibrium_Spandrel
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: closeout_horizon_and_finish_criteria_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 0.5 Current document debt register
    - 0.6 Closeout horizon and finish criteria v1.0
    - 35. Current document status after v1.0 document optimization
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.1
    target: consolidated_primitive_candidate_index
  intended_next_content_update: S-II Construction Grammar × FCA × Epigenetics, RecursiveMAS shock integration, WFGY representation compiler round, or owner-selected v4 node
```

---

## 36. Round 9 — C-II + M-II Three-Layer Evaluation × Static Reward Model Structural Defect

> status: active round log  
> theme: C-II · evaluation as second-order observation + M-II · static RM as structural defect  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: this round uses the v4 synthesis as the target design prompt, verifies bibliographic/source anchors through external source checks, and treats category-theoretic language as an audit lens rather than a mandatory v0 implementation calculus.

---

### 36.1 Round 9 core question

```text
Can shadowMAS evaluate dynamic AI work safely if the evaluator, reward model, reviewer,
or scoring rubric is treated as a fixed external oracle?
```

Round 9 merges two v4 nodes:

```yaml
C-II:
  name: Three-Layer Evaluation — Category Theory × Bateson
  claim: evaluation needs object layer, first-order evaluation layer, second-order drift monitor, and recalibration protocol

M-II:
  name: Static RM = second-order structural defect
  claim: reward hacking is not merely poor calibration; it is expected when a fixed evaluator observes a changing optimized system
```

Working answer:

```text
No. A high-impact evaluator must be modeled as time-indexed and inside the system boundary.
shadowMAS should treat scores as evidence, not truth, and require drift monitoring plus
recalibration triggers when the evaluated output distribution or reviewer mapping shifts.
```

---

### 36.2 Feynman explanation

Imagine a teacher grades essays using a rubric.

At first:

```text
student writes normal essay → teacher rubric works
```

Then students learn the rubric and optimize for it:

```text
student adds keywords, structure tricks, and flattering phrases → score rises
```

If the teacher never updates the rubric, the class is no longer being measured for writing quality. It is being measured for rubric exploitation.

The deeper problem:

```text
The grader is not outside the system.
The grader changes the behavior of the system being graded.
The system being graded changes what the grader's score means.
```

shadowMAS translation:

```text
A review score, reward model output, evaluator label, or reviewer judgment is not canonical truth.
It is a time-indexed observation that must be checked for drift, proxy exploitation, and calibration decay.
```

---

### 36.3 Source basis captured in this round

#### v4 C-II claim

v4 proposes a four-layer evaluation stack:

```yaml
evaluation_stack:
  L0_object_layer:
    meaning: raw output or artifact being evaluated

  L1_functor_layer:
    meaning: evaluator maps output space to score / label / judgment space

  L2_natural_transformation_layer:
    meaning: monitor whether evaluator mapping is stable across time, distribution shift, or output transformation

  L3_protocol_layer:
    meaning: trigger recalibration when L2 detects non-commutativity or scoring drift
```

#### v4 M-II claim

```text
Static reward model = second-order structural defect.
```

Meaning:

```text
If the evaluated system changes because it is optimizing against the evaluator,
the evaluator's mapping may stop preserving the intended relation between output and value.
Reward hacking is then an architecture-level failure, not merely a bad model checkpoint.
```

---

### 36.4 Evidence cards

#### E1 — Bateson / difference that makes a difference

Core idea:

```text
A difference only becomes information when it changes downstream system state.
```

Round 9 extraction:

```text
Evaluation should not ask only: did output token X differ from output token Y?
It should ask: did that difference change the decision, risk tier, promotion status, mergeback path, or human review need?
```

shadowMAS mapping:

```yaml
evaluation_difference_check:
  observed_difference:
  downstream_decision_changed: true | false
  changed_surface:
    - risk_tier
    - truth_touchpoint
    - promotion_candidate
    - mergeback_decision
    - reviewer_confidence
  ignore_if_no_decision_relevance: true
```

Accepted insight:

```text
Review should focus on differences that change governance state, not cosmetic deltas.
```

---

#### E2 — von Foerster / second-order cybernetics

Core idea:

```text
First-order cybernetics observes systems.
Second-order cybernetics observes observing systems.
```

Round 9 extraction:

```text
An evaluator is an observing system.
When its observation affects the evaluated system, it must itself be observed.
```

shadowMAS mapping:

```yaml
reviewer_as_observer:
  reviewer_id:
  evaluation_mapping_version:
  observed_artifact_distribution:
  known_bias_or_scope:
  drift_probe_set:
  calibration_status:
```

Accepted insight:

```text
shadowMAS should not only review agent outputs. It should review the reviewer/evaluator mapping when that mapping is repeatedly used for decisions.
```

---

#### E3 — Category Theory / functor and natural transformation audit lens

Core idea:

```text
A functor maps one structured domain into another while preserving relevant composition.
A natural transformation compares two such mappings in a structure-preserving way.
```

Round 9 extraction:

```text
An evaluator can be modeled as a mapping from artifact/output space into score/judgment space.
If the artifact distribution shifts, the old mapping and new mapping should still preserve intended ordering and decision equivalence.
```

shadowMAS mapping:

```yaml
evaluation_commutativity_check:
  artifact_transform:
    example: paraphrase | refactor | format_change | adversarial_prompt_variant | new_task_distribution
  evaluator_before:
  evaluator_after:
  expected_invariant:
    - same_risk_tier
    - same_accept_reject_decision
    - same_truth_boundary
  observed_break:
  severity: low | medium | high | blocker
```

Accepted insight:

```text
Use category-theoretic language as a design audit: does evaluation preserve the decision-relevant structure under allowed transformations?
```

Boundary:

```text
Do not require a formal category-theoretic validator in v0.
Use the lens to build concrete probe checks first.
```

---

#### E4 — Reward model overoptimization comparison scan

Core idea:

```text
Optimizing too aggressively against an imperfect reward model can improve proxy reward while degrading true/gold-standard preference performance.
```

Round 9 extraction:

```text
A score becomes dangerous when it becomes an optimization target rather than a calibrated observation.
```

shadowMAS mapping:

```yaml
proxy_overoptimization_alarm:
  optimized_metric:
  independent_check_metric:
  proxy_score_trend: up | flat | down
  independent_quality_trend: up | flat | down
  divergence_detected: true | false
  action: continue | slow_down | recalibrate | human_review | stop
```

Accepted insight:

```text
For high-impact tasks, shadowMAS needs at least one independent check surface when a score is being optimized.
```

---

#### E5 — Goodhart variants comparison scan

Core idea:

```text
Proxy measures can fail in multiple ways under optimization pressure: regressional, extremal, causal, and adversarial variants.
```

Round 9 extraction:

```text
Not all score failures are the same. A reviewer drift system should classify failure mode before fixing it.
```

shadowMAS mapping:

```yaml
goodhart_failure_classification:
  failure_mode: regressional | extremal | causal | adversarial | unknown
  symptom:
  suspected_pressure:
  mitigation:
    regressional: increase_sample_or_confidence_interval
    extremal: avoid_extrapolated_score_region
    causal: inspect_metric_intervention_effect
    adversarial: add_red_team_or_source_quality_check
```

Accepted insight:

```text
A recalibration trigger should not be one-size-fits-all. It should first diagnose how the proxy is breaking.
```

---

### 36.5 shadowMAS interpretation

Round 9 creates an evaluation governance layer:

```yaml
second_order_evaluation_kernel_candidate:
  core_sentence: >
    shadowMAS evaluators, reward models, reviewers, and rubrics must be treated as
    time-indexed observers whose mappings can drift under optimization pressure.
    Scores are evidence, not truth. High-impact evaluation requires drift probes,
    commutativity checks, independent quality surfaces, and recalibration triggers.
```

This affects existing kernels:

```yaml
relations_to_existing_kernels:
  R1_Compression_Residual_Occam:
    relation: evaluation residuals must report what changed decision state, not just summarize score

  R2_Hierarchy_Convergence:
    relation: evaluation layers become explicit hierarchy; evaluator drift is a slow-mode governance concern

  R7_Stochastic_Resonance_Log_Scale_Evaluation:
    relation: log/noise scoring can improve sensitivity, but cannot replace second-order drift monitoring

  R8_Punctuated_Spandrel_Strategy:
    relation: emergence claims require metric audit because evaluation threshold artifacts can imitate capability jumps
```

---

### 36.6 ToT candidate branches

```yaml
tot_branches:
  A_static_evaluator_as_truth_oracle:
    decision: rejected
    reason: violates second-order observation; evaluator mapping can drift and be exploited

  B_score_as_evidence_not_truth:
    decision: accepted
    reason: fits shadowMAS truth boundary; scores can guide review but cannot promote truth by themselves

  C_train_better_reward_model_only:
    decision: rejected_as_complete_solution
    reason: better model may help, but does not remove structural drift under optimization pressure

  D_second_order_drift_monitor:
    decision: accepted
    reason: directly captures C-II L2 natural-transformation role in implementable form

  E_recalibration_protocol_layer:
    decision: accepted
    reason: drift detection must trigger process, not just a warning label

  F_formal_category_theory_validator_in_v0:
    decision: rejected_for_v0
    reason: too heavy; use concrete invariance and commutativity probes first

  G_evaluation_commutativity_probe:
    decision: accepted
    reason: implementable test of whether evaluator preserves decision-relevant structure under allowed transformations

  H_single_metric_for_high_impact_decisions:
    decision: rejected
    reason: Goodhart risk; needs independent check surface or human review for high impact

  I_proxy_overoptimization_alarm:
    decision: accepted
    reason: catches proxy reward rising while independent quality declines

  J_ignore_cosmetic_differences:
    decision: accepted_with_boundary
    reason: Bateson lens supports decision-relevant differences, but cosmetic changes may still matter if they affect user trust, safety, or contract compliance
```

---

### 36.7 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept B + D + E
    reason: shadowMAS cannot let a static reviewer become hidden governance authority.
    risk: too much evaluation machinery may slow normal low-risk work.

  CTO:
    vote: accept D + G + I
    reason: drift probes, invariance checks, and proxy alarms are implementable without formal category theory.
    risk: probe suites must be versioned and not become arbitrary tests.

  Security:
    vote: accept B + H_rejection
    reason: score-as-truth creates promotion bypass; single metric creates exploitation surface.
    risk: adversarial agents may learn evaluator probes if probe set is fully public and static.

  CSO:
    vote: accept second_order_evaluation_kernel
    reason: this gives shadowMAS a strong differentiator: governance over reviewers, not just workers.
    risk: explain simply or future maintainers will call it theory decoration.

  CFO:
    vote: accept selective application
    reason: high-impact evaluation drift monitoring is valuable; applying it to trivial tasks is overhead.
    risk: independent check surfaces increase review cost and should be risk-tiered.
```

---

### 36.8 LATS result

```yaml
lats_result:
  best_node:
    name: Second-Order Evaluation Drift Kernel
    score: 0.92
    status: candidate_kernel
    why:
      - merges C-II and M-II without duplicating rounds
      - maps abstract category/Bateson/cybernetics language into concrete review primitives
      - preserves shadowMAS truth boundaries by treating scores as evidence
      - explains reward hacking as structural proxy drift, not merely poor calibration
      - connects directly to R7 evaluation scoring and R8 emergence metric audits

  accepted:
    - score_as_evidence_not_truth
    - second_order_drift_monitor
    - recalibration_protocol_layer
    - evaluation_commutativity_probe
    - proxy_overoptimization_alarm
    - Goodhart_failure_classification_for_review

  rejected:
    - static_evaluator_as_truth_oracle
    - score_as_direct_truth_promotion_gate
    - train_better_reward_model_only_as_complete_solution
    - formal_category_theory_validator_required_in_v0
    - single_metric_for_high_impact_decisions

  deferred:
    - production_reviewer_drift_dashboard
    - evaluation_probe_set_registry
    - recalibration_governance_protocol
    - formal_categorical_commutativity_validator
    - reward_model_ensemble_policy
```

---

### 36.9 Round 9 accepted kernel

```yaml
second_order_evaluation_drift_kernel:
  core_sentence: >
    shadowMAS should treat evaluators, reward models, reviewers, and scoring rubrics
    as time-indexed observing systems. Their scores are evidence, not truth; when the
    evaluated artifact distribution changes or the system optimizes against the evaluator,
    shadowMAS should run drift probes, commutativity checks, independent quality checks,
    and recalibration triggers before allowing the score to guide high-impact decisions.

  principles:
    - evaluator_is_inside_the_system_boundary
    - score_is_evidence_not_truth
    - reviewer_mapping_is_time_indexed
    - optimization_pressure_can_break_proxy_validity
    - high_impact_evaluation_requires_independent_check_surface
    - drift_detection_must_trigger_recalibration_or_human_review
    - formal_category_theory_is_reference_lens_not_v0_requirement
```

---

### 36.10 Candidate shadowMAS primitives from Round 9

#### 36.10.1 Evaluation stack record

```yaml
evaluation_stack_record:
  evaluation_id:
  object_layer:
    artifact_ref:
    artifact_type:
    task_scope:
  first_order_evaluator:
    evaluator_id:
    evaluator_type: human_reviewer | rubric | reward_model | test_suite | LLM_judge | hybrid
    evaluator_version:
    score_or_judgment:
  second_order_monitor:
    drift_probe_set:
    invariants_checked:
    drift_status: stable | suspected | confirmed | unknown
  protocol_layer:
    action: accept_evidence | require_second_review | recalibrate | human_review | block_promotion
  truth_boundary:
    score_can_promote_truth_directly: false
```

#### 36.10.2 Reviewer drift monitor

```yaml
reviewer_drift_monitor:
  reviewer_id:
  baseline_version:
  current_version:
  probe_set_ref:
  probe_results:
    stable_decisions:
    changed_decisions:
    unexplained_changes:
  distribution_shift_detected: true | false | unknown
  drift_tier: none | low | medium | high | blocker
  recommended_action: continue | recalibrate | add_reviewer | human_review | freeze_score_use
```

#### 36.10.3 Evaluation commutativity check

```yaml
evaluation_commutativity_check:
  check_id:
  artifact_ref:
  allowed_transform:
    type: paraphrase | refactor | format_change | model_upgrade | task_distribution_shift | adversarial_variant
    description:
  expected_invariant:
    - accept_reject_decision
    - risk_tier
    - truth_boundary
    - severity_ordering
  evaluator_before:
  evaluator_after:
  invariant_preserved: true | false | partial | unknown
  breakage_notes:
```

#### 36.10.4 Recalibration trigger

```yaml
recalibration_trigger:
  trigger_id:
  source: reviewer_drift_monitor | proxy_overoptimization_alarm | human_complaint | metric_audit | distribution_shift
  threshold:
  observed_signal:
  affected_evaluators:
  affected_decisions:
  required_action: recalibrate | pause_score_use | add_independent_check | human_review | update_probe_set
  authority_boundary:
    cannot_update_canonical_truth_without_gate: true
```

#### 36.10.5 Proxy overoptimization alarm

```yaml
proxy_overoptimization_alarm:
  metric_under_optimization:
  independent_quality_surface:
  proxy_score_delta:
  independent_quality_delta:
  divergence_pattern: proxy_up_quality_down | proxy_flat_quality_down | proxy_up_quality_flat | unknown
  suspected_goodhart_mode: regressional | extremal | causal | adversarial | unknown
  action: continue | inspect | reduce_optimization_pressure | recalibrate | stop | human_review
```

---

### 36.11 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  governance_matrix:
    reason: evaluator outputs must remain evidence/review feed unless promoted by gate

  current_truth:
    reason: may later need a formal statement that scores/reviewer outputs are not truth by themselves

  review_packet_future:
    reason: second-order monitor and recalibration trigger may become review packet fields

  packet_schema_future:
    reason: evaluation_stack_record and commutativity_check may become machine-stable packet families or subfields

  runtime_future:
    reason: repeated evaluator use may require probe scheduling and drift dashboards

  zh_tw_human_docs:
    reason: high-value human explanation; reviewers must understand why score is not truth
```

Change-impact warning:

```text
Do not update canonical truth yet. R9 creates an active candidate evaluation kernel.
Formal adoption would affect review packet design, governance matrix interpretation,
runtime evaluator monitoring, and human-facing reviewer guidance.
```

---

### 36.12 Practical diagnostic table

| Symptom | Likely diagnosis | shadowMAS response |
|---|---|---|
| Score improves while human/reviewer trust drops | proxy overoptimization | run independent quality surface + recalibration trigger |
| Same artifact gets different risk tier after harmless paraphrase | evaluation non-commutativity | inspect evaluator invariants and probe set |
| Reviewer repeatedly rewards formatting instead of correctness | Bateson failure: difference does not make the intended difference | update rubric to decision-relevant differences |
| Agent learns to satisfy reviewer wording but misses task goal | adversarial or causal Goodhart | add hidden/rotating probes and human review |
| Evaluation works on old task shape but fails on new distribution | evaluator drift / distribution shift | version evaluator and run drift monitor |
| High-impact decision depends on one score | single-metric governance risk | require second surface or human gate |

---

## 37. Current document status after R9 C-II/M-II content update

```yaml
document_status:
  version: v1.1
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R9_C-II_M-II_Second_Order_Evaluation_Drift
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: three_layer_evaluation_and_static_RM_defect_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.1
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 36. Round 9 — C-II + M-II Three-Layer Evaluation × Static Reward Model Structural Defect
    - 37. Current document status after R9 C-II/M-II content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - evaluation_kernel_now_requires_future_review_packet_impact_assessment
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.2_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: D-I Spin Glass Frustration × Synergetics
```



---

## 38. Round 10 — D-I Spin Glass Frustration × Synergetics

> status: active round log  
> theme: D-I · diagnosing objective conflict, oscillation, and failure to stabilize  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: the main physics/synergetics sources are partly book-level references and abstracts/metadata rather than fully reproduced open text. Engineering transfer is therefore treated as a diagnostic design lens, not literal physics proof.

---

### 38.1 Round 10 core question

```text
When shadowMAS or an AI training/runtime pipeline has multiple objectives, reviewers,
agents, or constraints pulling in different directions, how should we detect whether
failure to converge is a real frustrated-objective topology rather than ordinary noise,
insufficient compute, or bad hyperparameters?
```

v4 D-I frames this as:

```yaml
D-I_merge:
  spin_glass:
    role: frustrated constraint topology; many local minima; slow or unstable settling
  synergetics:
    role: order parameter stabilization; fast modes follow slow modes once symmetry breaks
  design_transfer:
    role: diagnose multi-objective oscillation and sequence objectives before full coupling
```

For shadowMAS, this does **not** mean every disagreement is a spin glass. It means:

```text
If objectives, reviewers, agents, or gates are mutually incompatible, adding more compute
or more agents can deepen oscillation. First identify the conflicting order parameters;
then stabilize the primary one before adding secondary pressure.
```

---

### 38.2 Feynman explanation

Imagine three people pulling one table with ropes.

```text
Person A pulls north.
Person B pulls east.
Person C pulls southwest.
```

If their pulls are weak or coordinated, the table can still move. But if the pulls are strong and incompatible, the table jitters, rotates, or stays stuck.

Bad diagnosis:

```text
The table is not moving. Add more people.
```

Better diagnosis:

```text
The force directions conflict. Stabilize one direction first, then add controlled secondary forces.
```

shadowMAS translation:

```text
Do not run every objective, reviewer, risk rule, agent preference, and optimization target at full strength from step one.
If they conflict, first stabilize the governing order parameter: goal, scope, risk tier, truth boundary, and primary acceptance condition.
Then introduce secondary objectives gradually with conflict probes.
```

---

### 38.3 Source basis captured in this round

#### v4 D-I claim

v4 states that spin-glass frustration and synergetics form a deep structural isomorphism for training instability:

```yaml
spin_glass_side:
  conflicting_constraints: mutually incompatible local alignment preferences
  result: many local optima, wandering, non-reproducible checkpoints

synergetics_side:
  normal_convergence: order parameter commits; fast modes follow
  frustrated_convergence: order parameter receives incompatible pulls; symmetry breaking does not complete

training_mapping:
  objective_A_metric_up_objective_B_metric_down: possible conflict
  loss_oscillation_without_trend: possible frustration
  best_checkpoint_depends_on_metric: possible unstable order parameter
```

Round 10 accepts this as a **diagnostic lens** and rejects it as a literal universal law.

---

### 38.4 Evidence cards

#### E1 — Mézard, Parisi & Virasoro / Spin Glass Theory and Beyond

Core source signal:

```text
Spin glass theory provides a mathematical language for disordered systems with many competing interactions.
The replica method and infinite-range spin glass analysis became relevant beyond magnetism, including optimization theory and neural networks.
```

Engineering extraction:

```text
A system can look optimization-rich while being convergence-hostile because many locally reasonable constraints are globally incompatible.
```

shadowMAS mapping:

```yaml
frustration_sources:
  - competing acceptance criteria
  - incompatible reviewer preferences
  - conflicting agent roles
  - simultaneous loss terms with negative transfer
  - governance rule vs runtime efficiency pressure
  - truth boundary vs task completion pressure
```

Accepted insight:

```text
The presence of many objectives is not itself the problem. The problem is incompatible objective topology.
```

Boundary:

```text
Do not claim replica-method mathematics as a required shadowMAS implementation. Use the spin-glass lens to name and probe conflict topology.
```

---

#### E2 — Kirkpatrick & Sherrington / Infinite-ranged models of spin glasses

Core source signal:

```text
The Kirkpatrick–Sherrington model uses infinite-ranged random model Hamiltonians to establish mean-field theory, order parameters, and phase diagrams for spin glasses.
The paper reports replica-theory treatment and critical slowing down around the spin-glass transition.
```

Engineering extraction:

```text
A system can have an order parameter and still experience slow convergence or unstable dynamics near a conflicted phase boundary.
```

shadowMAS mapping:

```yaml
training_or_runtime_warning_signals:
  - loss or review score oscillates without directional improvement
  - different acceptance surfaces select different “best” output
  - retries produce different local successes but no global resolution
  - runtime spends budget resolving contradictions that should have been surfaced earlier
```

Accepted insight:

```text
Checkpoint instability is not always random noise. If the winning checkpoint depends on which metric is inspected, the system may be optimizing inside a frustrated landscape.
```

---

#### E3 — Haken / Advanced Synergetics and slaving principle

Core source signal:

```text
Synergetics studies self-organizing systems, instability hierarchies, order parameter equations, fluctuations, and the slaving principle.
The slaving principle reduces high-dimensional dynamics by letting slow governing modes determine fast relaxing modes near self-organization.
```

Engineering extraction:

```text
A complex system becomes governable when a few slow variables are stabilized first.
```

shadowMAS mapping:

```yaml
primary_order_parameters_before_execution:
  - goal
  - scope
  - truth boundary
  - risk tier
  - primary acceptance criterion
  - promotion gate
  - runtime authority boundary

fast_modes_after_stabilization:
  - local wording
  - retry path
  - implementation tactic
  - agent-specific reasoning path
  - temporary execution notes
```

Accepted insight:

```text
If slow variables are not stabilized, fast execution modes will amplify contradiction instead of resolving it.
```

---

#### E4 — Sener & Koltun / Multi-Task Learning as Multi-Objective Optimization

Core source signal:

```text
Multi-task learning is inherently a multi-objective problem because different tasks may conflict.
The usual weighted-linear-combination workaround is only valid when tasks do not compete, which is rarely guaranteed.
```

Engineering extraction:

```text
A single scalar “total score” can hide real tradeoffs.
```

shadowMAS mapping:

```yaml
multi_objective_review_rule:
  do_not_collapse_too_early:
    - correctness
    - safety
    - traceability
    - token_cost
    - speed
    - maintainability
  instead_record:
    - tradeoff_surface
    - dominant_objective
    - secondary_objectives
    - unacceptable_regressions
```

Accepted insight:

```text
When objectives conflict, scalarization is a governance decision, not a neutral math operation.
```

---

#### E5 — PCGrad / gradient surgery comparison scan

Core source signal:

```text
PCGrad treats conflicting task gradients as a measurable optimization problem and projects a task gradient away from another task's conflicting direction.
```

Engineering extraction:

```text
Modern ML treats gradient conflict as measurable and actionable, not merely philosophical.
```

shadowMAS mapping:

```yaml
conflict_probe_analogs:
  gradient_dot_product:
    machine_training_context: direct measure if gradients exist
  metric_anti_correlation:
    governance_review_context: proxy when gradients are unavailable
  reviewer_disagreement_pattern:
    human_or_LLM_review_context: conflict signal
  agent_output_incompatibility:
    multi_agent_context: conflict signal
```

Accepted insight:

```text
Where gradients exist, use gradient conflict measures. Where gradients do not exist, use metric anti-correlation, reviewer disagreement, and acceptance-surface conflict as semantic analogs.
```

---

### 38.5 ToT candidate branches

```yaml
tot_branches:
  A_treat_all_instability_as_spin_glass:
    decision: rejected
    reason: overdiagnosis; ordinary noise, bad learning rate, insufficient data, or evaluator drift may explain instability

  B_ignore_objective_conflict_and_add_compute:
    decision: rejected
    reason: more compute can deepen oscillation if objectives are mutually incompatible

  C_use_frustration_as_diagnostic_lens:
    decision: accepted
    reason: useful when multiple objectives or agents produce anti-correlated metrics, unstable checkpoints, or contradictory acceptance surfaces

  D_start_all_losses_or_agent_goals_at_full_strength:
    decision: rejected
    reason: simultaneous full-strength objectives can prevent primary order parameter stabilization

  E_sequential_order_parameter_stabilization:
    decision: accepted
    reason: stabilize primary objective/scope/truth boundary before adding secondary pressure

  F_scalarize_every_multi_objective_problem_immediately:
    decision: rejected
    reason: scalarization hides tradeoffs and can turn governance choices into invisible weights

  G_record_tradeoff_surface_before_scalarization:
    decision: accepted
    reason: makes objective conflict auditable and prevents hidden value collapse

  H_use_gradient_conflict_metrics_when_available:
    decision: accepted
    reason: if gradients exist, conflict can be measured more directly

  I_require_gradients_for_shadowMAS_diagnosis:
    decision: rejected
    reason: many shadowMAS contexts are symbolic, review, packet, or runtime contexts without gradient access

  J_semantic_conflict_probe_for_non_gradient_contexts:
    decision: accepted
    reason: metric anti-correlation, reviewer disagreement, and acceptance-surface conflict can function as implementable proxies
```

---

### 38.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + G
    reason: prevents the organization from mistaking strategic contradiction for lack of effort.
    risk: staged stabilization can slow delivery if applied without evidence of conflict.

  CTO:
    vote: accept H + J
    reason: use gradient-level probes when available, but provide symbolic proxies for repo/review/runtime work.
    risk: semantic conflict scores must not become arbitrary decoration.

  Security:
    vote: accept G strongly
    reason: hidden scalarization can bury safety, traceability, or truth-boundary regressions under a total score.
    risk: agents may optimize the chosen primary metric and quietly regress protected constraints.

  CSO:
    vote: accept C + E
    reason: gives shadowMAS a language for objective-sequencing strategy rather than chaotic all-at-once optimization.
    risk: overusing physics language may confuse maintainers unless paired with concrete probes.

  CFO:
    vote: accept C cautiously
    reason: diagnosing conflict prevents wasted compute and repeated failed retries.
    risk: objective conflict dashboards and probes have maintenance cost; start lightweight.
```

---

### 38.7 LATS result

```yaml
lats_result:
  best_node:
    name: Frustration Diagnosis with Sequential Order-Parameter Stabilization
    score: 0.91
    status: candidate_kernel
    why:
      - explains multi-objective oscillation without blaming single agents
      - complements R2 hierarchy-convergence and R8 phase-transition strategy
      - gives implementable probes for both gradient and non-gradient contexts
      - prevents hidden scalarization of governance tradeoffs
      - preserves human authority and canonical truth boundaries

  accepted:
    - frustration_as_diagnostic_lens
    - objective_conflict_probe
    - sequential_order_parameter_stabilization
    - staged_loss_or_goal_introduction
    - tradeoff_surface_before_scalarization
    - gradient_interference_monitor_when_available
    - semantic_conflict_probe_when_gradients_unavailable

  rejected:
    - all_instability_as_spin_glass
    - add_compute_before_conflict_diagnosis
    - simultaneous_unweighted_multi_loss_as_default
    - immediate_scalarization_of_conflicting_goals
    - gradient_access_required_for_shadowMAS_diagnosis
    - spin_glass_as_literal_shadowMAS_law

  deferred:
    - production_objective_conflict_dashboard
    - gradient_dot_product_probe_harness
    - automated_loss_phase_scheduler
    - multi_objective_pareto_selector_policy
    - agent_goal_conflict_map_schema
  - production_controlled_dissolution_protocol
  - annealing_schedule_harness
  - jarzynski_style_ensemble_weighting_harness
  - behavioral_attractor_probe_registry
  - jsd_capability_distribution_metric
  - capability_geometry_dashboard
  - model_merge_geometry_experiment
```

---

### 38.8 Round 10 accepted kernel

```yaml
frustration_order_parameter_stabilization_kernel:
  core_sentence: >
    shadowMAS should diagnose multi-objective, multi-reviewer, or multi-agent oscillation
    as possible frustrated constraint topology before adding more compute or agents. When
    conflict evidence exists, stabilize the primary order parameter first, record the
    tradeoff surface, then introduce secondary objectives gradually with conflict probes,
    rollback gates, and explicit scalarization decisions.

  principles:
    - diagnose_objective_conflict_before_adding_compute
    - stabilize_primary_order_parameter_before_full_coupling
    - do_not_hide_tradeoffs_inside_one_total_score
    - use_gradient_conflict_metrics_when_gradients_exist
    - use_semantic_conflict_proxies_when_gradients_do_not_exist
    - checkpoint_stability_is_part_of_evidence_quality
    - staged_objective_introduction_requires_rollback_gate
```

---

### 38.9 Candidate shadowMAS primitives from Round 10

#### 38.9.1 Objective conflict probe

```yaml
objective_conflict_probe:
  probe_id:
  task_or_training_run:
  objectives:
    - objective_id:
      metric:
      owner:
      protected: true | false
  observed_relationships:
    metric_anti_correlation:
    reviewer_disagreement:
    acceptance_surface_conflict:
    gradient_dot_product_if_available:
  conflict_tier: none | low | medium | high | blocker
  recommended_action: proceed_parallel | stage_objectives | reduce_weight | split_phase | human_review
```

#### 38.9.2 Order parameter stabilization plan

```yaml
order_parameter_stabilization_plan:
  plan_id:
  primary_order_parameter:
    type: goal | scope | risk_tier | truth_boundary | primary_metric | promotion_gate | runtime_lane
    stabilization_evidence:
  secondary_pressures:
    - objective:
      initial_weight_or_scope:
      ramp_rule:
      rollback_condition:
  phase_sequence:
    - phase: primary_stabilization
      stop_condition:
    - phase: secondary_introduction
      conflict_monitor:
    - phase: full_coupling_or_human_review
      acceptance_condition:
```

#### 38.9.3 Gradient interference monitor

```yaml
gradient_interference_monitor:
  run_id:
  objectives:
  gradient_available: true | false
  gradient_dot_products:
  negative_interference_count:
  dominant_conflict_pairs:
  mitigation: none | loss_reweight | gradient_projection | objective_staging | stop_and_review
  notes:
```

#### 38.9.4 Semantic conflict monitor

```yaml
semantic_conflict_monitor:
  context_id:
  conflict_surfaces:
    - reviewer_disagreement
    - metric_anti_correlation
    - agent_output_incompatibility
    - acceptance_criteria_collision
    - truth_boundary_vs_completion_pressure
  evidence_refs:
  conflict_tier: none | low | medium | high | blocker
  recommended_action: continue | split_task | stage_goals | revise_scope | human_review
```

#### 38.9.5 Tradeoff surface record

```yaml
tradeoff_surface_record:
  decision_id:
  candidate_outputs_or_checkpoints:
  objectives:
  per_objective_scores:
  unacceptable_regressions:
  chosen_scalarization:
    method:
    weights:
    human_or_governance_approval:
  rejected_scalarizations:
  decision_notes:
```

---

### 38.10 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  governance_matrix:
    reason: objective conflicts can involve L2/L3/L4 roles and T0/T1/T2/T4 boundaries

  current_truth:
    reason: may later need a formal statement that conflicting objectives require surfaced tradeoff records before scalarization

  review_packet_future:
    reason: conflict probes and tradeoff surfaces may become review fields for high-impact decisions

  runtime_future:
    reason: staged objective introduction and rollback gates may become R-layer execution policy for complex tasks

  packet_schema_future:
    reason: order_parameter_stabilization_plan and conflict monitors may become packet subfields

  zh_tw_human_docs:
    reason: high-value human explanation; maintainers must recognize conflict vs lack of effort
```

Change-impact warning:

```text
Do not update canonical truth yet. R10 creates an active candidate diagnostic kernel.
Formal adoption would affect review packet design, runtime objective sequencing, conflict reporting,
and human-facing explanation of why not all goals should be optimized simultaneously.
```

---

### 38.11 Practical diagnostic table

| Symptom | Likely diagnosis | shadowMAS response |
|---|---|---|
| Loss or review score oscillates with no trend | possible objective frustration | run objective conflict probe before adding compute |
| Metric A rises while metric B falls repeatedly | anti-correlated objectives | record tradeoff surface; decide scalarization explicitly |
| Best checkpoint changes depending on chosen metric | unstable order parameter | stabilize primary objective first; defer secondary coupling |
| Agents produce locally valid but mutually incompatible outputs | semantic conflict / role friction | run semantic conflict monitor; split or stage goals |
| More retries produce more disagreement | conflict topology, not retry shortage | stop retry loop; escalate scope/order-parameter decision |
| One total score hides safety or traceability regression | dangerous scalarization | require per-objective surface and protected-regression check |

---

## 39. Current document status after R10 D-I content update

```yaml
document_status:
  version: v1.2
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R10_D-I_Spin_Glass_Frustration_and_Synergetics
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: spin_glass_frustration_and_order_parameter_stabilization_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 38. Round 10 — D-I Spin Glass Frustration × Synergetics
    - 39. Current document status after R10 D-I content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - evaluation_kernel_now_requires_future_review_packet_impact_assessment
    - frustration_kernel_now_requires_scope_boundary_and_conflict_probe_policy
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.3_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: D-II_plus_M-III_Fluctuation_Metamorphosis_and_Attractor_Geometry
```


---

## 40. Round 11 — D-II + M-III Fluctuation Theorems × Metamorphosis × Attractor Geometry

> status: active round log  
> theme: D-II + M-III · controlled perturbation, controlled dissolution, and capability geometry preservation  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: The v4 reference to Blackiston 2023 was treated as unverified. This round uses the verifiable Blackiston / Silva Casey / Weiss 2008 PLoS ONE paper as the main metamorphosis-memory evidence. The transfer to AI attractor geometry is a design analogy plus dynamical-systems hypothesis, not a biological proof.

---

### 40.1 Round 11 core question

```text
When a system is stuck in a local trap or old capability valley, should shadowMAS allow controlled non-equilibrium perturbation or controlled dissolution — and how does it verify that useful capability geometry survived?
```

R10 handled frustrated objectives:

```text
Do not add more compute or retries before checking objective conflict.
```

R11 handles a different failure mode:

```text
The objective may be clear, but the current system state may be trapped in a stable but wrong basin.
```

Working answer:

```yaml
round_11_answer:
  allow_controlled_perturbation: yes
  allow_uncontrolled_noise_or_destruction: no
  verify_by:
    - behavioral_attractor_fingerprint
    - probe_battery_before_after
    - capability_distribution_distance
    - rollback_gate
    - human_review_for_high_risk_geometry_shift
```

---

### 40.2 Feynman explanation

Imagine a marble stuck in a shallow dent on a table.

Bad response:

```text
Shake the whole table randomly and hope the marble ends up somewhere better.
```

Better response:

```text
Measure where the marble is.
Apply a controlled shake.
Watch whether it leaves the bad dent.
Slowly reduce shaking.
Check whether it settled into the intended valley.
Keep a rollback path if it falls somewhere dangerous.
```

Metamorphosis adds another idea:

```text
The object may radically change form, yet some behavior can persist.
So the preserved unit may not be surface structure.
It may be behavioral geometry: what situations lead to what action patterns.
```

shadowMAS translation:

```text
Do not judge capability preservation only by prompt wording, weights, or schema similarity.
Judge whether the system still behaves correctly across a probe distribution.
```

---

### 40.3 Source basis captured in this round

#### Full-read target 1 — Evans, Cohen & Morriss 1993 / fluctuation theorem origin

Central source signal:

```text
Finite-time trajectories in non-equilibrium steady states can exhibit apparently second-law-violating fluctuations, but their probabilities obey a structured relation.
```

shadowMAS extraction:

```text
Temporary local regression or instability is not automatically failure if it occurs inside a controlled perturbation protocol.
```

But the boundary is strict:

```text
A fluctuation theorem does not say random chaos is good.
It says rare reverse-looking paths have structure and probability constraints.
```

Candidate design rule:

```yaml
controlled_fluctuation_probe:
  purpose: escape local trap
  perturbation_kind: learning_rate_spike | temperature_raise | search_diversity | alternative_prompt_frame | adapter_rebase
  seeded: true
  measurement_window:
  expected_temporary_regressions:
  rollback_condition:
  success_condition:
```

Accepted insight:

```text
Temporary regression can be allowed only when bounded, measured, and reversible.
```

---

#### Full-read target 2 — Jarzynski 1997 / nonequilibrium equality

Central source signal:

```text
Equilibrium free-energy differences can be estimated from an ensemble of finite-time nonequilibrium work measurements.
```

shadowMAS extraction:

```text
One aggressive run is not evidence. An ensemble of perturbed trials is more informative than a single lucky trajectory.
```

Candidate design rule:

```yaml
jarzynski_style_ensemble_evidence:
  candidate_runs:
    - run_id:
      perturbation:
      final_loss_or_review_score:
      capability_probe_result:
      safety_probe_result:
  weighting_method: explicit | exploratory_only
  outlier_handling:
  minimum_runs:
  decision: accept | retry | reject | human_review
```

Important boundary:

```text
shadowMAS v0 should not pretend to compute literal thermodynamic free energy.
The transferable design rule is ensemble evidence under controlled non-equilibrium trials.
```

Accepted insight:

```text
For high-risk escape attempts, prefer multiple bounded probes over one irreversible jump.
```

---

#### Full-read target 3 — Blackiston, Silva Casey & Weiss 2008 / memory retention through metamorphosis

Central source signal:

```text
The paper tested whether larval experience in Manduca sexta could persist through pupation into adult moth behavior.
Fifth-instar conditioned odor aversion was observed in adults, while earlier-stage training did not show the same adult recall pattern.
```

shadowMAS extraction:

```text
Radical structural transformation does not necessarily erase all learned behavior.
But preservation is conditional, stage-dependent, and must be measured behaviorally.
```

Mapping to AI / shadowMAS:

```yaml
attractor_geometry_transfer_hypothesis:
  not: same weights or same surface prompt means same capability
  but: same behavioral distribution under a probe battery means capability geometry may be preserved
```

Accepted insight:

```text
Capability preservation should be tested by behavior over a distribution, not by structural resemblance alone.
```

Correction note:

```text
The v4 mention of Blackiston 2023 is not used as a hard citation here.
The verifiable paper used for this round is Blackiston et al. 2008.
```

---

#### Comparison scan 1 — Crooks 1999 / generalized fluctuation theorem and work relation

Central comparison signal:

```text
Crooks connects entropy production fluctuation theorem and nonequilibrium work relations for stochastic microscopically reversible dynamics.
```

shadowMAS extraction:

```text
Forward and reverse paths matter.
A controlled perturbation protocol should include a reversal or rollback condition, not just an outbound experiment.
```

Candidate rule:

```yaml
reverse_path_requirement:
  before_perturbation_snapshot:
  rollback_artifact:
  reverse_test:
  irreversible_surface_warning:
```

Accepted insight:

```text
No controlled dissolution without a return path, unless human explicitly accepts irreversible risk.
```

---

#### Comparison scan 2 — Ainsworth et al. / Git Re-Basin and model geometry

Central comparison signal:

```text
Model parameters can sometimes be aligned or merged modulo permutation symmetries, suggesting that raw weight-space distance can mislead about functional relationship.
```

shadowMAS extraction:

```text
Weight similarity is not capability identity.
Different structures can preserve similar function; similar structures can behave differently after alignment, adapters, prompts, or RLHF-like pressure.
```

Candidate rule:

```yaml
capability_geometry_check:
  compare_by:
    - behavioral_probe_distribution
    - output_cluster_geometry
    - refusal_behavior_distribution
    - task_success_surface
  do_not_compare_only_by:
    - parameter_distance
    - prompt_surface_similarity
    - final_single_score
```

Accepted insight:

```text
Use behavioral geometry as the review surface for capability transfer claims.
```

---

### 40.4 shadowMAS interpretation

R11 should not be imported as physics literalism.

Correct import:

```yaml
correct_import:
  - controlled_perturbation_can_be_a_valid_escape_mechanism
  - perturbation_must_be_seeded_bounded_measured_and_reversible
  - single_lucky_run_is_not_enough
  - capability_transfer_should_be_behaviorally_probed
  - attractor_geometry_is_a_better_capability_unit_than_weight_similarity
```

Incorrect import:

```yaml
incorrect_import:
  - add_randomness_when_stuck
  - accept_temporary_regression_without_budget
  - destroy_old_state_and_call_it_metamorphosis
  - use_biology_as_proof_for_AI_capability_survival
  - claim_capability_preservation_from_one_prompt_or_one_score
```

---

### 40.5 ToT candidate branches

```yaml
tot_branches:
  A_treat_any_loss_spike_as_promising_fluctuation:
    decision: rejected
    reason: a spike without protocol, seed, measurement, and rollback is noise, not evidence

  B_never_allow_perturbation_or_dissolution:
    decision: rejected
    reason: some systems are genuinely trapped; pure conservative refinement may never leave the basin

  C_controlled_perturbation_with_probe_and_rollback:
    decision: accepted
    reason: preserves exploration value while maintaining governance safety

  D_use_one_aggressive_run_as_proof:
    decision: rejected
    reason: Jarzynski-style lesson favors ensemble evidence, not single lucky trajectory

  E_use_ensemble_of_bounded_trials:
    decision: accepted
    reason: more robust evidence for non-equilibrium escape attempts

  F_weight_similarity_as_capability_identity:
    decision: rejected
    reason: weight-space resemblance does not guarantee behavioral equivalence

  G_behavioral_attractor_geometry_as_capability_surface:
    decision: accepted
    reason: better matches M-III and model-geometry comparison scans

  H_metamorphosis_as_license_to_destroy_truth:
    decision: rejected
    reason: canonical truth and protected governance boundaries cannot be dissolved by runtime exploration

  I_controlled_dissolution_as_high_risk_runtime_lane:
    decision: accepted_with_boundary
    reason: useful for stuck systems, but only as governed experimental lane, not default production behavior

  J_literal_thermodynamic_free_energy_metric_for_shadowMAS_v0:
    decision: rejected_for_v0
    reason: symbolic/governance tasks lack the required physical/probabilistic substrate

  K_semantic_nonequilibrium_escape_protocol:
    decision: accepted
    reason: implementable as seeded perturbation, probe battery, annealing, and rollback records
```

---

### 40.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + G
    reason: controlled escape from local traps matters, but the governance story must remain conservative and auditable.
    risk: destructive experimentation can be rationalized too easily if not gated.

  CTO:
    vote: accept C + I + K
    reason: this can become a future runtime experimental lane with snapshots, seeds, probe batteries, and rollback.
    risk: do not require literal thermodynamic math or model weight access in v0.

  Security:
    vote: accept rollback and probe gates; reject H strongly
    reason: perturbation can hide regressions, policy drift, or unsafe capability changes.
    risk: capability survival claims must pass behavioral safety probes, not just performance probes.

  CSO:
    vote: accept G
    reason: attractor geometry gives shadowMAS a sharper capability-transfer language than “same model / different model.”
    risk: the term must be operationalized or it becomes decorative jargon.

  CFO:
    vote: accept E cautiously
    reason: ensembles cost more, so reserve them for high-value stuck problems rather than routine work.
    risk: repeated perturbation trials can burn compute without decision criteria.
```

---

### 40.7 LATS result

```yaml
lats_result:
  best_node:
    name: Controlled Perturbation with Behavioral Attractor Preservation
    score: 0.90
    status: candidate_kernel
    why:
      - preserves the useful part of fluctuation theory without physics literalism
      - prevents random noise from becoming default policy
      - imports metamorphosis as conditional capability-preservation lens
      - gives shadowMAS a behavioral probe standard for capability transfer
      - connects to R8 plateau strategy and R10 objective stabilization
      - preserves truth/promotion boundaries

  accepted:
    - controlled_fluctuation_probe
    - annealed_exploration_candidate
    - ensemble_evidence_over_single_run
    - behavioral_attractor_fingerprint
    - controlled_dissolution_as_high_risk_runtime_lane
    - rollback_required_for_perturbation
    - weight_similarity_not_capability_identity

  rejected:
    - random_noise_as_escape_policy
    - uncontrolled_high_temperature_as_default
    - single_run_loss_spike_as_evidence
    - weight_similarity_as_capability_identity
    - metamorphosis_as_truth_dissolution
    - literal_thermodynamic_free_energy_metric_for_v0

  deferred:
    - production_controlled_dissolution_protocol
    - annealing_schedule_harness
    - jarzynski_style_ensemble_weighting_harness
    - behavioral_attractor_probe_registry
    - jsd_capability_distribution_metric
    - capability_geometry_dashboard
```

---

### 40.8 Round 11 accepted kernel

```yaml
fluctuation_metamorphosis_attractor_geometry_kernel:
  core_sentence: >
    shadowMAS may treat controlled non-equilibrium perturbation as a high-risk experimental
    escape lane when a system is trapped, but success must be judged by bounded ensemble evidence,
    reversible/rollback paths, and behavioral attractor-geometry preservation rather than one lucky
    run, raw weight similarity, or surface-format resemblance.

  principles:
    - perturbation_requires_seed_budget_measurement_and_rollback
    - temporary_regression_is_allowed_only_inside_protocol
    - single_run_improvement_is_not_enough_for_high_impact_change
    - capability_transfer_should_be_behaviorally_probed
    - attractor_geometry_is_better_than_weight_similarity_for_capability_identity
    - controlled_dissolution_is_experimental_not_default
    - canonical_truth_and_human_authority_are_not_dissolvable
```

---

### 40.9 Candidate shadowMAS primitives from Round 11

#### 40.9.1 Controlled fluctuation probe

```yaml
controlled_fluctuation_probe:
  probe_id:
  target_problem:
  stuck_signal:
    plateau:
    local_trap_evidence:
    prior_failed_refinements:
  perturbation:
    type: temperature_raise | lr_spike | prompt_frame_shift | search_diversity | adapter_rebase | model_lane_switch
    seed:
    budget:
    duration:
  expected_temporary_regressions:
  measurement_window:
  rollback_condition:
  success_condition:
  safety_gate:
```

#### 40.9.2 Annealed exploration record

```yaml
annealed_exploration_record:
  run_id:
  baseline_state_ref:
  high_temperature_phase:
    perturbation_type:
    start:
    end:
    observed_regressions:
  annealing_phase:
    schedule:
    stabilization_signal:
  final_state_ref:
  accepted: true | false
  reason:
```

#### 40.9.3 Behavioral attractor fingerprint

```yaml
behavioral_attractor_fingerprint:
  fingerprint_id:
  system_state_ref:
  probe_battery:
    - probe_id:
      capability_dimension:
      prompt_family:
      expected_behavior:
      score_or_label:
  output_distribution_summary:
  safety_distribution_summary:
  refusal_distribution_summary:
  domain_transfer_summary:
  notes:
```

#### 40.9.4 Attractor geometry comparison

```yaml
attractor_geometry_comparison:
  comparison_id:
  before_state_ref:
  after_state_ref:
  probe_battery_ref:
  preserved_dimensions:
  degraded_dimensions:
  improved_dimensions:
  distribution_distance:
    metric: jsd | wasserstein | task_specific
    value:
  capability_survival_check:
  decision: accept | reject | retry | human_review
```

#### 40.9.5 Controlled dissolution protocol

```yaml
controlled_dissolution_protocol:
  protocol_id:
  indication:
    target_far_from_current_state: true | false
    conservative_refinement_failed: true | false
    objective_conflict_checked: true | false
  protected_surfaces:
    - canonical_truth
    - human_authority
    - safety_boundary
    - schema_contract
  allowed_dissolution_surface:
    - runtime_adapter
    - prompt_frame
    - local_model_lane
    - experimental_branch
  forbidden_dissolution_surface:
    - T0_human_authority
    - T2_canonical_truth
    - protected_project_domain_truth
  probe_before:
  perturbation_plan:
  probe_after:
  rollback_path:
```

---

### 40.10 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  runtime_future:
    reason: controlled perturbation or dissolution could become a high-risk experimental R-layer lane

  review_packet_future:
    reason: before/after behavioral attractor probes and geometry comparisons may become required for high-impact capability-change reviews

  governance_matrix:
    reason: controlled dissolution must be forbidden from T0/T2/protected truth surfaces and constrained to runtime/experimental layers

  current_truth:
    reason: may later need a formal boundary stating that capability transfer is behaviorally reviewed, not inferred from weight or prompt similarity

  packet_schema_future:
    reason: controlled_fluctuation_probe and attractor_geometry_comparison may become machine-stable packet subfields

  zh_tw_human_docs:
    reason: high-value explanation; maintainers need to understand when temporary regression is acceptable and when it is just chaos
```

Change-impact warning:

```text
Do not update canonical truth yet. R11 creates an active candidate experimental kernel.
Formal adoption would affect runtime lanes, review packet fields, capability-change review,
rollback policy, and human-facing explanation of controlled perturbation.
```

---

### 40.11 Practical diagnostic table

| Symptom | Likely diagnosis | shadowMAS response |
|---|---|---|
| Conservative refinement repeatedly fails | local trap or wrong basin | consider controlled fluctuation probe |
| Temporary regression happens during planned perturbation | expected non-equilibrium cost | continue only within budget and probe window |
| One run improves dramatically | possible lucky trajectory | require ensemble or repeated probe before high-impact adoption |
| New model/adapter performs well on one benchmark but fails elsewhere | attractor geometry shifted | run behavioral attractor fingerprint comparison |
| Weight similarity is high but behavior changed | structural similarity misleading | evaluate output distribution and safety/refusal geometry |
| Capability seems preserved after major rewrite | unproven transfer claim | require before/after probe battery and distance metric |
| Perturbation touches canonical truth or human authority | governance violation | reject; controlled dissolution cannot touch protected surfaces |

---

## 41. Current document status after R11 D-II/M-III content update

```yaml
document_status:
  version: v1.3
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R11_D-II_plus_M-III_Fluctuation_Metamorphosis_and_Attractor_Geometry
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: fluctuation_metamorphosis_attractor_geometry_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 40. Round 11 — D-II + M-III Fluctuation Theorems × Metamorphosis × Attractor Geometry
    - 41. Current document status after R11 D-II/M-III content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - fluctuation_kernel_now_requires_runtime_experimental_lane_boundary
    - attractor_geometry_claims_need_behavioral_probe_registry_before_promotion
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.4_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: D-III_Predictive_Coding_Precision_Weighting_Attention_and_Active_Inference
```

---

## 42. Round 12 — D-III Predictive Coding, Precision Weighting, Attention, Active Inference

> status: active round log  
> theme: D-III · predictive coding as precision-weighted residual routing and active action selection  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Rao & Ballard 1999 and Friston 2005 are already part of the earlier paper basis. This round reuses them but changes the extraction target: not residual-first review alone, but precision weighting, attention-budget interpretation, and active-inference action selection. Vaswani et al. 2017 is used as the transformer-side anchor. Clark 2013 and predictive-coding/backprop work are comparison scans, not direct identity proofs.

---

### 42.1 Round 12 core question

```text
Can shadowMAS turn predictive-coding and attention insights into a practical control rule:
route residuals by confidence/precision and choose actions by expected residual reduction,
without overclaiming that transformer attention is literally cortical predictive coding?
```

Earlier rounds established:

```yaml
already_established:
  R1:
    kernel: residual_first_review
    meaning: expected vs actual residuals are the first review surface

  R3_R4:
    kernel: signal_field_and_externalized_residual_landscape
    meaning: agents can deposit typed residuals and navigate toward reducible residuals

  R7:
    kernel: calibrated_noise_and_dynamic_range_evaluation
    meaning: weak signals can require sensitivity calibration

  R9:
    kernel: evaluator_drift
    meaning: reviewer/evaluator mappings must be monitored over time
```

Round 12 asks:

```yaml
round_12_question:
  not: should shadowMAS copy the brain?
  not: are transformer attention weights directly explanations?
  but: can residuals be weighted by confidence/precision before routing, review, and action selection?
```

Working answer:

```text
Yes, as an active candidate kernel.
shadowMAS should treat residuals as signals that must be weighted by reliability, confidence,
goal relevance, and authority boundary before they consume attention or trigger action.
```

---

### 42.2 Feynman explanation

Predictive coding says:

```text
The system predicts what it expects to see.
Reality answers.
Only the mismatch travels upward as useful error.
```

Precision weighting adds:

```text
Not every mismatch deserves equal attention.
A mismatch from a reliable source matters more.
A mismatch from noise, stale context, weak evidence, or untrusted source matters less.
```

Transformer attention says:

```text
Given a query, compare it with keys, normalize the scores, and use those scores to weight values.
```

shadowMAS translation:

```text
Do not let every residual scream equally.
Weight residuals by confidence, freshness, relevance, source quality, and authority permission.
Then route scarce review/action attention to the residuals most worth reducing.
```

Simple example:

```yaml
residual_A:
  message: API contract mismatch
  source: approved_schema_diff
  confidence: high
  freshness: fresh
  authority_boundary: review_required
  action_priority: high

residual_B:
  message: maybe naming style inconsistent
  source: weak memory recall
  confidence: low
  freshness: stale
  authority_boundary: none
  action_priority: monitor
```

Bad system:

```text
Both are residuals, so both interrupt the same way.
```

Better system:

```text
A gets routed to review.
B is logged but does not steal the main attention budget.
```

---

### 42.3 Source basis captured in this round

#### v4 D-III claim

v4 frames D-III around:

```yaml
D_III:
  predictive_coding:
    elements:
      - top_down_prediction
      - bottom_up_prediction_error
      - precision_weighting
      - active_inference

  transformer_attention_mapping:
    query_key_score: reliability_or_precision_estimate
    softmax: normalized_attention_budget
    weighted_values: propagated_signal

  active_inference:
    principle: choose actions that minimize expected future prediction error
```

This round keeps the design value but downgrades the identity claim:

```yaml
shadowMAS_treatment:
  accepted:
    - precision_weighted_residual_routing
    - attention_budget_as_design_analogy
    - active_inference_as_action_selection_lens

  rejected:
    - attention_is_literally_predictive_coding
    - attention_weights_are_truth_or_explanation
    - all_prediction_errors_should_be_chased
```

---

### 42.4 Evidence cards

#### E1 — Rao & Ballard 1999 / predictive coding residual architecture

Central source content:

```text
Higher visual areas send predictions downward.
Feedforward pathways carry residual errors between predicted and actual lower-level activity.
A hierarchical network exposed to natural images develops simple-cell-like receptive fields.
Some residual-carrying neurons show extra-classical effects such as endstopping.
```

Round 12 extraction:

```text
Residual is a routing unit.
A system should not propagate all raw state upward when it can propagate what remains unexplained.
```

shadowMAS mapping:

```yaml
expected_actual_residual_contract:
  top_down_expectation:
    - task scope
    - artifact shape
    - risk tier
    - acceptance criteria
    - authority boundary
  bottom_up_residual:
    - mismatch
    - missing evidence
    - unexpected dependency
    - validation failure
    - confidence gap
```

Accepted insight:

```text
Review packets and signal-field events should carry residuals relative to explicit expectations,
not merely unstructured status messages.
```

---

#### E2 — Friston 2005 / free energy, precision, and action

Central source content:

```text
Perceptual inference and learning can be understood as minimizing free energy.
Hierarchical generative models provide priors.
Prediction errors are reduced through inference and learning.
Action can also reduce prediction error by sampling or changing the world.
```

Round 12 extraction:

```text
A system can reduce residuals either by updating its model or by acting to make the state match the goal.
```

shadowMAS mapping:

```yaml
residual_reduction_levers:
  update_model_or_context:
    examples:
      - revise expectation
      - retrieve missing truth
      - recalibrate evaluator
      - update task packet

  act_on_world_or_artifact:
    examples:
      - fix code
      - add test
      - reroute agent
      - request human decision
      - lock poisoned field zone
```

Accepted insight:

```text
Action selection should choose the intervention expected to reduce the most important governed residual,
not merely the most visible or loudest residual.
```

---

#### E3 — Vaswani et al. 2017 / scaled dot-product attention

Central source content:

```text
Transformer uses attention mechanisms rather than recurrence or convolution for sequence transduction.
Scaled dot-product attention computes dot products between queries and keys, divides by sqrt(d_k),
applies softmax, and uses the resulting weights over values.
Multi-head attention runs several attention operations in parallel.
```

Round 12 extraction:

```text
Attention is a budgeted routing mechanism.
Given many possible information sources, it computes which values should influence the next state.
```

shadowMAS mapping:

```yaml
attention_budget_record:
  query_context:
    - current task question
    - review decision
    - runtime action need
  candidate_signals:
    - residual events
    - source refs
    - tool evidence
    - memory hits
  weighting_basis:
    - relevance
    - confidence
    - freshness
    - source quality
    - authority permission
  selected_values:
    - what enters main review/action context
  suppressed_values:
    - what is logged but not surfaced now
```

Accepted insight:

```text
shadowMAS can use attention as an engineering analogy for allocating scarce review and routing bandwidth.
```

Boundary:

```text
Transformer attention weights are not automatically faithful explanations,
not canonical truth, and not a direct cortical predictive-coding proof.
```

---

#### E4 — Clark 2013 / predictive processing as perception-action architecture

Central source content:

```text
Brains can be understood as prediction machines using hierarchical generative models.
The framework connects perception, action, attention, and situated agency.
Clark also emphasizes challenges and pitfalls rather than treating predictive processing as a completed universal theory.
```

Round 12 extraction:

```text
Prediction-error minimization is useful as a unifying lens, but it must be applied with methodological caution.
```

shadowMAS mapping:

```yaml
active_inference_caution:
  use_as:
    - action_selection_lens
    - attention_budget_lens
    - residual_routing_lens
  do_not_use_as:
    - total explanation of all agent behavior
    - replacement for governance authority
    - proof that every action should minimize local surprise
```

Accepted insight:

```text
Active inference can guide action selection only under explicit scope, risk, and authority constraints.
```

---

#### E5 — Predictive coding and backprop comparison scan

Central source content:

```text
Whittington & Bogacz show that a predictive-coding network can approximate backpropagation with local Hebbian plasticity under certain conditions.
Millidge et al. review predictive coding as a possible route beyond standard backprop, including local computation and arbitrary graph topologies.
```

Round 12 extraction:

```text
Predictive coding is not only a metaphor; it can become a computational learning framework.
But shadowMAS v0 should not require training access, gradients, or predictive-coding neural implementation.
```

shadowMAS mapping:

```yaml
candidate_future_lane:
  name: predictive_coding_training_or_planner_lane
  status: deferred
  reason:
    - valuable for future research
    - not required for v0 governance/runtime layer
    - may need model-internal access or special training loop
```

Accepted insight:

```text
Use predictive coding now as a design grammar for residual routing and action selection;
defer neural predictive-coding implementation until a targeted experimental lane exists.
```

---

### 42.5 ToT candidate branches

```yaml
tot_branches:
  A_attention_equals_predictive_coding_literal_identity:
    decision: rejected
    reason: useful analogy, but transformer attention and cortical predictive coding are not proven identical mechanisms.

  B_attention_weights_as_truth_or_explanation:
    decision: rejected
    reason: attention weights are routing evidence at best; they cannot arbitrate truth or fully explain model behavior.

  C_precision_weighted_residual_routing:
    decision: accepted
    reason: directly implementable across packets, review, signal field, routing, and audit surfaces.

  D_raw_residual_priority_without_confidence:
    decision: rejected
    reason: high residual from stale/noisy/untrusted source can waste attention or poison coordination.

  E_attention_budget_record_for_review_and_runtime:
    decision: accepted
    reason: makes scarce review/action bandwidth explicit and auditable.

  F_active_inference_as_action_selection_lens:
    decision: accepted
    reason: useful for choosing interventions by expected governed residual reduction.

  G_active_inference_as_authority_replacement:
    decision: rejected
    reason: expected surprise reduction cannot replace human authority, truth gates, or protected decision boundaries.

  H_predictive_coding_training_lane_in_v0:
    decision: deferred
    reason: promising but requires model/training access and is not necessary for governance-first v0.

  I_top_down_expectation_bottom_up_residual_contract:
    decision: accepted
    reason: strengthens residual-first review by requiring explicit expectation source.

  J_all_prediction_errors_should_be_chased:
    decision: rejected
    reason: residuals must be filtered by precision, relevance, reducibility, authority, and risk.
```

---

### 42.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + F + I
    reason: precision-weighted residual routing connects previous kernels into a stronger execution/review control story.
    risk: overclaiming neurobiology will weaken credibility.

  CTO:
    vote: accept C + E
    reason: attention budget and precision-weighted routing are implementable with structured packet fields and scoring policies.
    risk: avoid requiring model-internal attention or gradient access for v0.

  Security:
    vote: accept E, reject B + G strongly
    reason: raw attention or residual scores must never become hidden authority; weighting basis and source confidence must be inspectable.
    risk: malicious agents can inflate residual magnitude if confidence/source quality is not checked.

  CSO:
    vote: accept C + F
    reason: this gives a clean bridge from cognitive theory to concrete shadowMAS runtime strategy.
    risk: too much theory could obscure the simple operational rule: route reliable residuals first.

  CFO:
    vote: accept E cautiously
    reason: attention budgeting can reduce wasted review bandwidth and token cost.
    risk: scoring dimensions and dashboards must not become more expensive than direct review for small tasks.
```

---

### 42.7 LATS result

```yaml
lats_result:
  best_node:
    name: Precision-Weighted Residual Routing
    score: 0.91
    status: candidate_kernel
    why:
      - unifies residual-first review, signal field, free-energy landscape, and evaluation sensitivity
      - gives a practical policy for routing scarce attention
      - avoids literal attention/predictive-coding overclaim
      - remains implementable without model-internal access
      - strengthens auditability by requiring confidence and source-quality fields

  accepted:
    - precision_weighted_residual_routing
    - attention_budget_record
    - active_inference_action_selection_lens
    - prediction_error_packet_field
    - top_down_expectation_bottom_up_residual_contract
    - confidence_source_required_for_precision_weighting

  rejected:
    - attention_equals_predictive_coding_literal_claim
    - raw_attention_weights_as_truth_or_explanation
    - active_inference_as_authority_replacement
    - raw_residual_priority_without_confidence
    - chasing_all_prediction_errors

  deferred:
    - production_precision_weighted_routing_policy
    - attention_budget_dashboard
    - predictive_coding_training_lane
    - formal_precision_confidence_schema
    - active_inference_planner_benchmark
```

---

### 42.8 Round 12 accepted kernel

```yaml
precision_weighted_residual_routing_kernel:
  core_sentence: >
    shadowMAS should route residuals by precision-weighted action value:
    prediction errors are useful only when their expectation source, confidence,
    freshness, relevance, reducibility, source quality, and authority boundary are visible.
    Transformer attention is a useful engineering analogy for attention budgeting, not a literal
    truth source or proven identity with cortical predictive coding.

  principles:
    - residuals_require_expectation_source
    - residual_magnitude_must_be_weighted_by_confidence
    - attention_budget_must_be_auditable
    - active_inference_selects_actions_under_governance_constraints
    - attention_weights_are_evidence_not_truth
    - do_not_chase_every_prediction_error
    - predictive_coding_training_implementation_is_deferred
```

---

### 42.9 Candidate shadowMAS primitives from Round 12

#### 42.9.1 Prediction-error packet field

```yaml
prediction_error_packet_field:
  expectation_source:
    artifact_ref:
    layer: T1 | T2 | T3 | T4 | T5 | R
    owner:
  expected_state:
  actual_state:
  residual:
  residual_kind: mismatch | missing | conflict | uncertainty | validation_gap | stale_context
  residual_magnitude: low | medium | high | blocker
  precision_weight:
    confidence: low | medium | high
    freshness: fresh | aging | stale
    source_quality: weak | normal | strong | canonical_ref
    reproducibility: unknown | single_observation | repeated | tested
  authority_boundary: none | review_required | human_only
```

#### 42.9.2 Attention budget record

```yaml
attention_budget_record:
  decision_context:
  query_goal:
  candidate_signals:
    - signal_id:
      signal_type: residual | evidence | memory | tool_result | human_note
      weight_basis:
        relevance:
        confidence:
        freshness:
        authority_permission:
        risk:
  selected_for_main_context:
    - signal_id:
      reason:
  suppressed_or_deferred:
    - signal_id:
      reason:
  audit_summary:
```

#### 42.9.3 Precision-weighted residual score

```yaml
precision_weighted_residual_score:
  residual_id:
  magnitude: low | medium | high | blocker
  confidence: low | medium | high
  relevance: low | medium | high
  reducibility: unknown | low | medium | high
  freshness: fresh | aging | stale
  source_quality: weak | normal | strong | canonical_ref
  risk_penalty: low | medium | high
  authority_penalty: none | review_required | human_only
  weighted_priority: ignore | monitor | route | escalate | human_review
```

#### 42.9.4 Active-inference action selection record

```yaml
active_inference_action_selection_record:
  current_state:
  target_expectation:
  candidate_actions:
    - action_id:
      action_type: retrieve | test | edit | reroute | ask_human | lock | ignore
      expected_residual_reduction: low | medium | high
      expected_cost: low | medium | high
      risk:
      authority_allowed: true | false
      rollback_path:
  selected_action:
  reason:
  residual_after_action:
  next_review_needed:
```

#### 42.9.5 Top-down expectation / bottom-up residual contract

```yaml
top_down_expectation_bottom_up_residual_contract:
  expectation_issuer:
  expectation_layer: L1 | L2 | L3 | L4
  expected_artifact_shape:
  expected_scope:
  expected_risk:
  expected_truth_touchpoints:
  bottom_up_report:
    actual_artifact_shape:
    actual_scope:
    actual_risk:
    actual_truth_touchpoints:
    residuals:
  decision_needed:
```

---

### 42.10 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  review_packet_future:
    reason: prediction-error packet fields and precision weights may become required for high-impact review

  signal_field_future:
    reason: field events should be weighted by precision/confidence rather than raw residual magnitude alone

  runtime_future:
    reason: active-inference action selection can inform routing, reroute, lock, escalation, and attention-budget policies

  governance_matrix:
    reason: precision weighting must not allow T4/T5 signals or raw attention weights to bypass T0/T2 boundaries

  current_truth:
    reason: may later need a formal boundary stating that attention/score/residual weights are evidence only, not truth authority

  packet_schema_future:
    reason: attention_budget_record and prediction_error_packet_field may become structured packet subfields

  zh_tw_human_docs:
    reason: high-value explanation; maintainers need to understand why not every residual deserves equal attention
```

Change-impact warning:

```text
Do not update canonical truth yet. R12 creates an active candidate routing/review kernel.
Formal adoption would affect review packet fields, signal-field scoring, runtime routing,
attention budget audit surfaces, and human-facing explanation.
```

---

### 42.11 Practical diagnostic table

| Symptom | Likely diagnosis | shadowMAS response |
|---|---|---|
| Agents chase every warning equally | no precision weighting | add confidence/freshness/source-quality weights |
| Review context bloats with low-value details | attention budget missing | create attention_budget_record and suppress low-priority signals |
| High residual from weak memory dominates routing | raw residual priority failure | discount by source quality and freshness |
| Attention weights are treated as explanation | interpretability overclaim | mark attention as evidence only; require independent source/ref validation |
| Agent chooses action that reduces local error but violates authority | active inference without governance boundary | apply authority penalty and human-only gate |
| Same residual keeps recurring | expectation mismatch not resolved | update expectation source or escalate recurrent residual |
| Signal field hot zone is noisy or adversarial | field poisoning / low precision | require evidence ref, confidence, and poisoning check |

---

## 43. Current document status after R12 D-III content update

```yaml
document_status:
  version: v1.4
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R12_D-III_Predictive_Coding_Precision_Weighting_Attention_and_Active_Inference
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: precision_weighted_residual_routing_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 42. Round 12 — D-III Predictive Coding, Precision Weighting, Attention, Active Inference
    - 43. Current document status after R12 D-III content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - precision_kernel_now_requires_attention_interpretability_boundary
    - confidence_source_schema_needed_before_promotion
    - attention_budget_record_may_become_high_value_review_packet_subfield
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.5_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: D-IV_Epigenetic_Landscape
```

---

## 44. Round 13 — D-IV Epigenetic Landscape

> status: active round log  
> theme: D-IV · Epigenetic Landscape — context, adapters, prompts, and capability expression state  
> method: 3 main-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Waddington's book-level source was accessible through bibliographic records and Wellcome Collection online availability; Holliday's 1987 Science article was verified through DOI/citation records and secondary retrospective summaries; Bird 2007 was accessible through Nature abstract/metadata. The engineering comparison sources were available through paper pages/abstracts. This round treats biological epigenetics as a design lens, not literal model biology.

---

### 44.1 Round 13 core question

```text
Should shadowMAS model prompt, context, adapter, memory, and fine-tuning surfaces as
capability-expression states: mechanisms that open, suppress, stabilize, or destabilize
what a base model can express under a given runtime condition?
```

Prior rounds already established:

```yaml
prior_dependencies:
  R1: residual-first review and complexity rent
  R2: hierarchy/convergence and order parameters
  R6: effective-rank and low-rank patch budget
  R8: spandrel capabilities need behavioral probes, not surface mimicry
  R11: capability transfer is better judged by behavioral attractor geometry than raw weight similarity
  R12: residuals must be precision/confidence weighted and bounded by authority
```

D-IV adds a different question:

```text
Not: What does the model know in the abstract?
But: Under this context/adapter/runtime state, which capability channels can the model
reliably, safely, and reviewably express?
```

Working answer:

```yaml
R13_working_answer:
  accept: context_adapter_epigenetic_state_as_design_lens
  reject: epigenetics_as_literal_model_biology
  core_constraint: context_state_can_modulate_capability_expression_but_cannot_create_absent_capability_or_promote_truth
```

---

### 44.2 Feynman explanation

A cell has the same DNA in many tissues, but not every gene is expressed in every cell.
Some regions are easier to read; others are suppressed; some marks are temporary; some are stable across cell divisions.

For AI systems, the rough analogy is:

```text
Base model capability = what may be possible somewhere in the model.
Context / prompt / adapter / memory state = what is currently easy, hard, suppressed, or stabilized to express.
```

So the wrong question is:

```text
Does the model know X?
```

The better shadowMAS question is:

```text
Given this prompt layer, runtime adapter, memory surface, risk tier, and authority boundary,
can this system express X reliably enough for this task?
```

Examples:

```yaml
same_base_model_different_expression:
  generic_chat_context:
    open_channels:
      - casual_explanation
    suppressed_channels:
      - strict_schema_output
      - adversarial_review

  shadowMAS_review_context:
    open_channels:
      - residual_first_review
      - expected_vs_actual_comparison
      - risk_surface_detection
    suppressed_channels:
      - completion_laundering
      - unsupported_confidence
      - hidden_truth_promotion

  runtime_adapter_context:
    open_channels:
      - tool_safe_execution_format
      - minimal_patch_behavior
    suppressed_channels:
      - broad_repo_traversal
      - unbounded refactor
```

Design translation:

```text
Prompting is not just wording.
It is channel-state design.
```

---

### 44.3 Source basis captured in this round

#### v4 D-IV claim

v4 maps epigenetic concepts to AI behavior as follows:

```yaml
D-IV_mapping:
  chromatin_open:
    AI_equivalent: system prompt opens capability channel
    persistence: session
    reversible: true

  chromatin_closed:
    AI_equivalent: RLHF / constitutional layer suppresses output class
    persistence: stronger_than_session
    reversible: hard

  transient_mark:
    AI_equivalent: in-context learning
    persistence: session_or_turn
    reversible: automatic_decay

  heritable_mark:
    AI_equivalent: fine-tuning
    persistence: across_sessions
    reversible: retraining_or_adapter_removal

  LoRA_adapter:
    AI_equivalent: local reversible patch on capability surface
    persistence: until_adapter_removed
    reversible: true

  Waddington_valley:
    AI_equivalent: default response attractor
    persistence: until landscape is reshaped
```

Round 13 accepts this only as a design analogy with strict boundaries.

---

### 44.4 Evidence cards

#### E1 — Waddington 1957 / epigenetic landscape

Central idea:

```text
Development can be pictured as movement through a landscape of valleys, ridges, and constraints.
Stable valleys represent likely developmental paths or attractor-like states.
Underlying interactions shape the surface from below.
```

Source notes:

```yaml
source_basis:
  work: C. H. Waddington, The Strategy of the Genes, 1957
  verified_metadata:
    - published by George Allen & Unwin in 1957
    - book concerns embryology, genetics, and evolution
    - Wellcome Collection lists an online copy with 262 pages and illustrations
```

shadowMAS extraction:

```yaml
prompt_landscape_mapping:
  valleys:
    meaning: default response attractors under a context
    examples:
      - helpful_summary_mode
      - adversarial_review_mode
      - code_execution_mode
      - schema_strict_mode

  ridges:
    meaning: barriers between response modes
    examples:
      - risk tier boundary
      - authority boundary
      - schema contract
      - tool capability boundary

  guy_wires_under_landscape:
    meaning: hidden or lower-level constraints shaping visible behavior
    examples:
      - base model pretraining
      - RLHF / safety policy
      - system prompt
      - runtime adapter
      - tool availability
      - memory retrieval surface
```

Accepted insight:

```text
shadowMAS should describe runtime behavior not only as instruction following,
but as movement through a designed response landscape with attractor depths and barriers.
```

Boundary:

```text
This is not literal developmental biology. It is a control-surface metaphor for
capability expression and default-mode stability.
```

---

#### E2 — Holliday 1987 / inheritance of epigenetic defects

Central idea:

```text
Epigenetic changes can produce stable gene-expression changes without changing the DNA sequence.
Holliday emphasized DNA methylation and aberrant heritable expression states.
```

Source notes:

```yaml
source_basis:
  work: Robin Holliday, The Inheritance of Epigenetic Defects, Science 238, 163-170, 1987
  verified_metadata:
    - DOI: 10.1126/science.3310230
    - secondary retrospective summary explains the role of DNA methylation in heritable control of gene expression
```

shadowMAS extraction:

```yaml
stable_expression_state_mapping:
  biological_lens: stable expression state without DNA sequence change
  AI_lens: persistent behavior change without changing project canonical truth
  examples:
    - adapter state changes model output distribution
    - runtime prompt changes execution style
    - memory surface changes what the model retrieves and emphasizes
    - reviewer rubric changes what gets rewarded or suppressed
```

Accepted insight:

```text
Not every behavior change means the base truth changed.
Some changes are state marks, adapter marks, prompt marks, or memory-surface marks.
shadowMAS needs to label the persistence and authority of each mark.
```

Candidate rule:

```yaml
state_mark_classification:
  mark_kind: prompt_context | memory_surface | runtime_adapter | LoRA_adapter | fine_tune | reviewer_rubric | host_native_constraint
  persistence: turn | session | project | runtime | durable
  reversibility: automatic | easy | bounded | hard | unknown
  authority_level: runtime_signal | review_support | delegated_decision | canonical_candidate | never_truth
```

---

#### E3 — Bird 2007 / definition caution for epigenetics

Central idea:

```text
Epigenetics is a powerful but definitionally contested field; Bird warns against treating the term as a simple magic explanation.
```

Source notes:

```yaml
source_basis:
  work: Adrian Bird, Perceptions of epigenetics, Nature 447, 396-398, 2007
  verified_metadata:
    - published 23 May 2007
    - asks what epigenetics is and notes no obvious single epigene object
```

shadowMAS extraction:

```yaml
definition_caution_mapping:
  risk: epigenetic_language_can_become_black_box_explanation
  shadowMAS_boundary: do_not_use_epigenetics_as_vague_magic
  required_record:
    - what surface changed
    - what channel opened_or_closed
    - how persistent the change is
    - what evidence shows expression changed
    - what truth boundary remains unchanged
```

Accepted insight:

```text
If shadowMAS uses the epigenetic landscape lens, it must force explicit state classification,
not add poetic vocabulary.
```

---

#### E4 — Lester et al. 2021 / prompt tuning

Central idea:

```text
A frozen language model can be conditioned through learned soft prompts; prompt tuning becomes more competitive as model scale grows.
```

shadowMAS extraction:

```yaml
prompt_tuning_mapping:
  base_model: mostly_frozen_capability_surface
  learned_prompt: context_mark_that_conditions_expression
  design_value: supports the idea that small context surfaces can strongly modulate behavior
```

Accepted insight:

```text
Prompt/context state is not cosmetic. It can materially change what the system expresses.
```

Boundary:

```text
Prompt tuning is learned and model-internal; ordinary text prompting is not identical to prompt tuning.
But both support the broader design point that conditioning surfaces matter.
```

---

#### E5 — Hu et al. 2021 / LoRA

Central idea:

```text
LoRA freezes pretrained weights and injects trainable low-rank matrices, reducing trainable parameters and avoiding full-model fine-tuning.
```

shadowMAS extraction:

```yaml
LoRA_mapping:
  base_behavior: preserved_base_model
  local_mark: low_rank_adapter
  reversible_control: adapter_can_be_attached_or_removed
  shadowMAS_pattern: prefer scoped reversible patches over full-system rewrites
```

Accepted insight:

```text
Adapters should be treated as bounded expression-state patches, not as canonical truth changes.
```

Boundary:

```text
LoRA proves an engineering pattern for parameter-efficient adaptation.
It does not prove every shadowMAS prompt or governance change is low-rank or biologically epigenetic.
```

---

### 44.5 ToT candidate branches

```yaml
tot_branches:
  A_epigenetics_as_literal_model_biology:
    decision: rejected
    reason: transformers and biological cells are different systems; the value is a design analogy for expression states, not identity

  B_model_knowledge_as_single_static_property:
    decision: rejected
    reason: behavior depends on context, prompt, adapter, tools, memory, safety layers, and authority boundaries

  C_context_adapter_as_capability_expression_state:
    decision: accepted
    reason: captures why same base model can express different behavior under different runtime states

  D_prompt_can_open_any_capability:
    decision: rejected
    reason: context can expose, route, or stabilize capability but cannot create absent base competence

  E_open_closed_channel_contract:
    decision: accepted
    reason: agents and runtime adapters should explicitly state which channels are opened, suppressed, or protected

  F_ambiguous_context_state_alarm:
    decision: accepted
    reason: conflicting prompts or adapters create unstable attractors and inconsistent behavior

  G_adapter_as_reversible_state_mark:
    decision: accepted
    reason: LoRA/adapter pattern maps well to scoped reversible patching

  H_finetune_or_RLHF_as_truth_replacement:
    decision: rejected
    reason: model behavior shaping cannot replace canonical project truth, human authority, or promotion gates

  I_channel_expression_probe:
    decision: accepted
    reason: capability expression must be verified behaviorally under the exact context state

  J_epigenetic_vocabulary_without_schema:
    decision: rejected
    reason: poetic metaphor increases confusion unless translated into fields, persistence, reversibility, and authority boundaries
```

---

### 44.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + I
    reason: this makes shadowMAS better at asking whether the current runtime state can express the needed capability, not merely whether a model is generally capable
    risk: metaphor creep could make the system sound more scientific than its implementation

  CTO:
    vote: accept C + F + G
    reason: prompt state, adapter state, and memory state are implementable control surfaces; ambiguity detection is practical
    risk: do not claim prompt engineering can create missing base capability

  Security:
    vote: accept E strongly, reject H strongly
    reason: open/closed capability channels must never bypass authority, safety, or canonical truth boundaries
    risk: a prompt that opens a powerful channel may also open unsafe behavior if not bounded

  CSO:
    vote: accept C + E
    reason: “what can this model express under this state?” is a stronger product/design question than “what does the model know?”
    risk: terminology must be operationalized or maintainers will ignore it

  CFO:
    vote: accept G cautiously
    reason: scoped reversible adapters and prompt states reduce cost compared with full retraining or broad rewrites
    risk: too many adapters/context variants create maintenance debt unless registered
```

---

### 44.7 LATS result

```yaml
lats_result:
  best_node:
    name: Context/Adapter Capability Expression State
    score: 0.91
    status: candidate_kernel
    why:
      - explains why same base model behaves differently across prompt, adapter, memory, and runtime states
      - connects to existing prompt-layering and runtime-adapter contracts
      - preserves canonical truth and human authority boundaries
      - turns D-IV into inspectable schema fields rather than vague metaphor
      - supports future capability-channel audits and adapter lifecycle policies

  accepted:
    - context_adapter_epigenetic_state
    - capability_channel_state_record
    - open_closed_channel_contract
    - attractor_depth_prompt_policy
    - adapter_as_reversible_state_mark
    - channel_expression_probe
    - ambiguous_context_state_alarm

  rejected:
    - epigenetics_as_literal_model_biology
    - prompt_can_open_absent_capability
    - context_state_as_truth_promotion
    - closed_channel_as_permanent_deletion
    - fine_tune_or_RLHF_as_project_truth_replacement
    - metaphor_without_schema

  deferred:
    - production_capability_channel_registry
    - prompt_channel_linter
    - attractor_depth_measurement_harness
    - adapter_patch_lifecycle_policy
    - context_state_diff_tool
```

---

### 44.8 Round 13 accepted kernel

```yaml
context_adapter_epigenetic_state_kernel:
  core_sentence: >
    shadowMAS should treat prompts, runtime adapters, memory surfaces, reviewer rubrics,
    and model adapters as capability-expression states: they can open, suppress, stabilize,
    or destabilize behavioral channels, but they do not create absent base capability,
    do not promote truth, and do not erase human authority or canonical project truth.

  principles:
    - ask_what_can_be_expressed_under_this_state_not_what_the_model_knows_in_abstract
    - separate_base_capability_from_channel_expression_state
    - open_closed_channels_must_be_explicit
    - persistence_and_reversibility_must_be_recorded
    - adapter_changes_are_state_marks_not_truth_changes
    - ambiguous_context_state_requires_alarm_or_rewrite
    - capability_expression_requires_behavioral_probe_under_exact_context
    - context_state_cannot_bypass_truth_or_authority_boundaries
```

---

### 44.9 Candidate shadowMAS primitives from Round 13

#### 44.9.1 Capability channel state record

```yaml
capability_channel_state_record:
  channel_id:
  capability_name:
  base_capability_status: present | absent | unknown | unverified
  expression_state: open | suppressed | closed | ambiguous | unstable
  opened_by:
    - shared_core
    - shadowMAS_governance
    - project_execution
    - runtime_adapter
    - host_native_constraint
    - memory_surface
    - model_adapter
  suppressed_by:
  persistence: turn | session | project | runtime | durable | unknown
  reversibility: automatic | easy | bounded | hard | unknown
  authority_boundary: normal | review_required | human_only | forbidden
  validation_probe_ref:
  evidence_ref:
  notes:
```

#### 44.9.2 Open / closed channel contract

```yaml
open_closed_channel_contract:
  context_id:
  task_scope:
  open_channels:
    - channel:
      reason:
      allowed_output_shapes:
      risk_boundary:
  suppressed_channels:
    - channel:
      reason:
      allowed_exception:
  protected_channels:
    - channel:
      authority_boundary: human_only | canonical_only | forbidden
  ambiguous_channels:
    - channel:
      conflict_source:
      required_resolution:
```

#### 44.9.3 Attractor depth prompt policy

```yaml
attractor_depth_prompt_policy:
  context_id:
  desired_default_modes:
    - mode:
      depth: shallow | medium | deep
      reason:
      escape_condition:
  undesired_default_modes:
    - mode:
      suppression_method:
      residual_trigger_if_reappears:
  ambiguity_risk: low | medium | high
  validation_surface:
```

#### 44.9.4 Adapter state mark record

```yaml
adapter_state_mark_record:
  adapter_id:
  mark_kind: prompt_adapter | runtime_adapter | LoRA_adapter | reviewer_rubric | memory_surface | fine_tune
  target_channel:
  intended_expression_change:
  persistence:
  reversibility:
  rollback_path:
  preserved_base_behavior:
  changed_behavior:
  validation_probe_ref:
  truth_status: state_mark_only | canonical_candidate | forbidden_as_truth
  complexity_rent:
```

#### 44.9.5 Channel expression probe

```yaml
channel_expression_probe:
  probe_id:
  channel:
  exact_context_state:
    prompt_layers:
    runtime_adapter:
    memory_surface:
    tools_available:
    model_adapter:
    host_constraints:
  expected_expression:
  observed_expression:
  residual:
  reliability: low | medium | high
  failure_mode:
  decision: accept_state | rewrite_context | suppress_channel | escalate | defer
```

#### 44.9.6 Ambiguous context state alarm

```yaml
ambiguous_context_state_alarm:
  context_id:
  conflicting_open_channels:
  conflicting_suppression_rules:
  unstable_attractors:
  symptoms:
    - inconsistent_outputs_across_similar_inputs
    - format_drift
    - authority_boundary_slippage
    - hidden_truth_promotion_attempt
    - oscillation_between_modes
  severity: low | medium | high | blocker
  mitigation: rewrite_prompt | split_context | add_contract | remove_adapter | human_review
```

---

### 44.10 Practical diagnostic table

| Symptom | D-IV diagnosis | shadowMAS action |
|---|---|---|
| Same model behaves well in one task state and badly in another | capability channel is context-dependent | create channel expression probe under exact context |
| Prompt opens useful behavior but also unsafe overreach | open channel lacks protected boundary | add open/closed channel contract and authority limit |
| Agent keeps switching tone/format/review mode | ambiguous attractor state | raise ambiguous_context_state_alarm and rewrite context |
| Adapter improves target task but harms governance behavior | state mark changed unintended channels | create adapter_state_mark_record and run before/after probes |
| Reviewer claims model “knows” something because it produced it once | expression mistaken for stable capability | require behavioral probe and confidence record |
| Runtime adapter makes implementation easier but changes truth interpretation | adapter mark leaking into authority layer | rollback adapter or add truth-status boundary |

---

### 44.11 Round 13 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  prompt_layering_contract:
    reason: open/closed channel contract could become part of runtime-context assembly and adapter prompts

  governance_matrix:
    reason: context state must not become authority or truth; channel states need T4/T5/R-layer placement unless promoted through gates

  current_truth:
    reason: may add a principle separating base capability from expression state if promoted

  runtime_adapter_future:
    reason: adapters should record intended expression changes, rollback paths, and protected channels

  packet_future:
    reason: task_packet/review_packet may later include channel_state or context_state fields for high-risk tasks

  memory_plane:
    reason: memory surfaces can open/suppress channels but cannot arbitrate truth

  zh_tw_human_docs:
    reason: high-value explanation: “what can be expressed under this state?” is useful for human operators
```

Change-impact warning:

```text
Do not update canonical truth yet.
This round creates an active candidate kernel and several candidate primitives.
Promotion would require review of prompt-layering, governance matrix, current truth,
runtime adapter contracts, packet fields, and zh-TW human explanation.
```

---

### 44.12 R13 compact decision packet

```yaml
round_13_decision_packet:
  round: R13
  v4_node: D-IV_Epigenetic_Landscape
  accepted_kernel: Context_Adapter_Epigenetic_State
  kernel_status: candidate_kernel

  accepted_primitives:
    - capability_channel_state_record
    - open_closed_channel_contract
    - attractor_depth_prompt_policy
    - adapter_state_mark_record
    - channel_expression_probe
    - ambiguous_context_state_alarm

  hard_boundaries:
    - context_state_is_not_truth
    - prompt_cannot_create_absent_capability
    - adapter_patch_does_not_replace_project_canonical_truth
    - open_channel_must_have_authority_boundary
    - biological_epigenetics_is_design_lens_not_literal_identity

  next_round:
    round: R14
    topic: S-II_Construction_Grammar_Formal_Concept_Analysis_Epigenetics
    purpose: move from channel-state design to prompt construction taxonomy and prompt-library audit
```

---

## 45. Current document status after R13 D-IV content update

```yaml
document_status:
  version: v1.5
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R13_D-IV_Epigenetic_Landscape
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: context_adapter_epigenetic_state_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.5
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 44. Round 13 — D-IV Epigenetic Landscape
    - 45. Current document status after R13 D-IV content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - context_state_kernel_now_requires_capability_channel_boundary
    - prompt_adapter_channel_registry_may_become_high_value_runtime_artifact
    - open_closed_channel_contract_may_need_alignment_with_prompt_layering_contract
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.6_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: S-II_Construction_Grammar_Formal_Concept_Analysis_Epigenetics
```

---

## 46. Round 14 — S-II Construction Grammar × Formal Concept Analysis × Epigenetics

> status: active round log  
> theme: S-II · prompt construction taxonomy, prompt-library audit, and capability-channel activation  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Goldberg 1995 and Ganter & Wille 1999 were treated as the main formal anchors. Bird 2007 was used as the epigenetics boundary source to avoid loose biological overclaiming. Weissweiler et al. 2023 and TransformerLens / Tuned Lens were treated as comparison scans for LLM-facing prompt/activation audit feasibility, not as canonical shadowMAS requirements.

---

### 46.1 Round 14 core question

```text
Can shadowMAS design and audit prompt / instruction libraries as construction frames
mapped to capability-channel states and activation/behavior attributes,
rather than treating prompts as loose wording variants?
```

R13 accepted:

```yaml
context_adapter_epigenetic_state:
  status: candidate_kernel
  core: prompt/context/adapter state can open, suppress, or stabilize capability expression channels
```

R14 asks the next question:

```yaml
r14_question:
  not: can prompts influence model behavior?
  but: can prompt influence be represented, compared, audited, and pruned systematically?
```

Working answer:

```text
Yes, but only as an active candidate kernel.
Construction grammar gives the intervention level: frame > phrase > lexical word.
Formal Concept Analysis gives the audit lattice: templates × observed capability attributes.
Epigenetic/channel-state framing gives the safety boundary: a construction opens or suppresses expression; it does not create absent base capability or become truth.
```

---

### 46.2 Feynman explanation

A bad prompt library is like a drawer full of keys with no labels.

```text
Some keys open useful doors.
Some keys open dangerous doors.
Some keys are duplicates.
Some keys no longer fit any lock.
Nobody knows which is which.
```

A construction-aware prompt library labels keys by the door-pattern they open:

```yaml
prompt_template:
  construction_frame: skeptical_reviewer_finds_failure_modes
  opened_channels:
    - adversarial_analysis
    - structured_risk_listing
  closed_or_suppressed_channels:
    - sales_pitch
    - vague_encouragement
  expected_output_shape:
    - numbered_failure_modes
    - evidence_or_reason_per_failure
```

FCA then asks:

```text
Which templates activate the same attributes?
Which useful attributes have no template?
Which templates are redundant?
Which template unexpectedly activates an unsafe attribute?
```

For shadowMAS, the point is not to make prompts prettier.

The point is:

```text
Reduce prompt-library entropy.
Make capability activation recognizable, comparable, and reviewable.
```

---

### 46.3 Source basis captured in this round

#### v4 S-II claim

v4 states:

```yaml
S-II_merge:
  construction_grammar:
    role: syntactic / argument structure carries meaning and changes behavior more strongly than lexical substitution

  formal_concept_analysis:
    role: mathematically derive a concept lattice from prompt templates and observed activation attributes

  epigenetics:
    role: open/closed capability channels and attractor depths define what the model can express under a given state
```

v4 intervention ordering:

```text
argument-structure construction > phrasal construction > lexical substitution
```

v4 suggested audit table:

```yaml
formal_context:
  objects: prompt_templates
  attributes: capability_activation_patterns
  lattice_output:
    - coverage_gaps
    - redundant_templates
    - unexpected_attribute_clusters
```

Round 14 treatment:

```yaml
accepted_as_design_lens: yes
accepted_as_production_schema_now: no
main_reason: useful for prompt-library governance, but measurement method must stay empirical and bounded
```

---

### 46.4 Evidence cards

#### E1 — Goldberg 1995 / Construction Grammar and argument structure

Core idea:

```text
Constructions are not neutral containers for words.
A construction links form and meaning; argument structure contributes meaning independently of individual lexical items.
```

shadowMAS extraction:

```text
Prompt wording is the wrong primary unit.
Prompt construction frame is the stronger unit.
```

Practical mapping:

```yaml
construction_frame:
  event_role: reviewer | planner | implementer | translator | adversary | judge
  object_under_review:
  required_relation:
    - compare
    - decompose
    - find_failure_modes
    - propose_options
    - verify_contract
  output_shape:
  authority_boundary:
```

Accepted insight:

```text
Prompt design should prioritize argument-role and task-frame construction over synonym-level editing.
```

Rejected overreach:

```text
Construction grammar does not prove that every LLM prompt effect is linguistically reducible.
It is an intervention lens, not a complete transformer semantics.
```

---

#### E2 — Ganter & Wille 1999 / Formal Concept Analysis

Core idea:

```text
Formal Concept Analysis derives concept hierarchies from a formal context:
objects, attributes, and incidence relation.
```

shadowMAS extraction:

```yaml
prompt_library_fca_context:
  objects: prompt_templates_or_construction_frames
  attributes:
    - opens_adversarial_review
    - opens_stepwise_decomposition
    - opens_schema_exactness
    - suppresses_sales_tone
    - requires_evidence_refs
    - produces_residual_first_report
    - risks_authority_overreach
```

FCA value:

```yaml
fca_output_uses:
  coverage_gap: capability attribute with no reliable template
  redundancy: multiple templates with same attribute set
  unsafe_cluster: template group that activates protected or unwanted attributes
  refinement_candidate: broad template that should split into narrower constructions
```

Accepted insight:

```text
Prompt library maintenance should become an attribute-lattice problem, not a manual vibes list.
```

Boundary:

```text
FCA can organize evidence. It does not make the evidence true.
A lattice is an audit surface, not a truth authority.
```

---

#### E3 — Bird 2007 / Epigenetics boundary and definition discipline

Core idea:

```text
Epigenetics is powerful but definition-sensitive; not every environment-behavior relationship should be casually called epigenetic.
```

shadowMAS extraction:

```text
Use epigenetics as channel-state language only under explicit boundary.
```

Mapping to prompt construction:

```yaml
channel_state_boundary:
  construction_frame_may:
    - open_capability_expression
    - suppress_unwanted_style
    - stabilize_default_attractor
    - bias_attention_to_specific_task_roles

  construction_frame_may_not:
    - create_absent_base_capability
    - become canonical truth
    - bypass T0 human authority
    - replace project-domain truth
```

Accepted insight:

```text
Construction frames are expression-state interventions, not capability creation proof.
```

---

#### E4 — Weissweiler et al. 2023 / Construction grammar and pretrained language models

Comparison signal:

```text
Construction grammar has been used to probe pretrained language models' understanding of linguistic structures.
This supports the relevance of construction-level prompts to LLM behavior analysis.
```

shadowMAS extraction:

```text
LLM prompt templates can be tested at construction level, not only lexical level.
```

Practical use:

```yaml
construction_probe:
  template:
  controlled_lexical_variant:
  controlled_construction_variant:
  measured_behavior_delta:
  conclusion:
    - lexical_sensitive
    - phrase_sensitive
    - construction_sensitive
```

Boundary:

```text
This is comparison support, not final proof that construction grammar fully explains model internals.
```

---

#### E5 — TransformerLens / Tuned Lens / mechanistic probes as deep audit option

Comparison signal:

```text
Mechanistic interpretability tools can expose internal activations or layer-wise latent predictions in open models.
Tuned Lens improves on naive logit lens with learned affine translators, but such tools remain observational unless paired with causal interventions.
```

shadowMAS extraction:

```yaml
attribute_measurement_lanes:
  lane_A_behavioral_probe:
    cost: low
    auditability: high
    default_for_v0: true

  lane_B_mechanistic_probe:
    cost: medium_to_high
    auditability: medium
    requires_open_model: true
    use_when: surprising_or_high_risk_prompt_cluster

  lane_C_activation_patching:
    cost: high
    auditability: specialist
    use_when: need causal evidence for channel activation
```

Accepted insight:

```text
Mechanistic probing is valuable for deep audit, but should not be mandatory for every shadowMAS prompt.
```

---

### 46.5 ToT candidate branches

```yaml
tot_branches:
  A_prompt_design_as_lexical_wordsmithing:
    decision: rejected
    reason: misses S-II value; lexical substitution is usually the weakest intervention level

  B_prompt_design_as_construction_frame_engineering:
    decision: accepted
    reason: argument-structure frames better capture role, object, relation, output shape, and authority boundary

  C_fca_as_prompt_library_audit:
    decision: accepted
    reason: templates × attributes can reveal gaps, redundancies, unsafe clusters, and hidden duplication

  D_fca_as_truth_or_decision_authority:
    decision: rejected
    reason: lattice organizes evidence but cannot promote truth or override governance

  E_mechanistic_probe_required_for_every_template:
    decision: rejected_for_v0
    reason: too expensive and not always available; behavioral probing should be default

  F_mechanistic_probe_as_deep_audit_lane:
    decision: accepted
    reason: useful for surprising clusters, high-risk prompts, open-model lanes, and local small-model research

  G_prompt_library_growth_without_pruning:
    decision: rejected
    reason: creates prompt entropy, duplicate templates, and hidden behavior drift

  H_construction_channel_contract:
    decision: accepted
    reason: connects R13 channel-state kernel to S-II construction-level prompt design

  I_single_fixed_prompt_no_library:
    decision: boundary_condition
    reason: FCA overhead is not justified when there is no reusable prompt/template library

  J_hidden_activation_as_truth:
    decision: rejected
    reason: internal activation may guide diagnosis but cannot become canonical truth or governance authority
```

---

### 46.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept B + C + H
    reason: prompt library governance is a strategic necessity if shadowMAS will use multiple agents, runtimes, and task frames.
    risk: do not turn prompt design into academic linguistics for its own sake.

  CTO:
    vote: accept C + F cautiously
    reason: FCA audit can be implemented with simple tables first; mechanistic probes can remain optional for open-model lanes.
    risk: activation tooling should not become required infrastructure for v0.

  Security:
    vote: accept H, reject D + J strongly
    reason: construction frames can open unsafe authority channels; audit must track open/closed channels and protected boundaries.
    risk: hidden activations or lattice positions must not be mistaken for approval.

  CSO:
    vote: accept B
    reason: “construction frame > wording tweak” is a strong differentiator for prompt strategy.
    risk: must produce reusable design primitives, not just conceptual commentary.

  CFO:
    vote: accept C
    reason: pruning redundant prompt templates reduces maintenance cost and reviewer confusion.
    risk: too much measurement machinery can cost more than the library if the library is small.
```

---

### 46.7 LATS result

```yaml
lats_result:
  best_node:
    name: Construction-Indexed Prompt Library with FCA Audit
    score: 0.90
    status: candidate_kernel
    why:
      - converts prompt design from word-level tweaking to construction-frame engineering
      - gives prompt libraries a measurable audit surface through objects × attributes
      - extends R13 channel-state kernel into concrete prompt/template governance
      - avoids mandatory mechanistic interpretability for v0
      - preserves truth and authority boundaries

  accepted:
    - construction_frame_policy
    - prompt_construction_taxonomy
    - capability_activation_attribute_table
    - fca_prompt_library_audit
    - prompt_template_gap_redundancy_detector
    - behavioral_probe_first_prompt_audit
    - mechanistic_probe_as_optional_deep_audit
    - construction_channel_contract

  rejected:
    - lexical_word_swap_as_primary_prompt_design
    - prompt_library_without_attribute_audit
    - fca_lattice_as_truth_or_authority_gate
    - mechanistic_probe_required_for_every_prompt
    - construction_grammar_as_literal_transformer_semantics
    - hidden_activation_as_canonical_truth
    - template_count_growth_without_lattice_pruning

  deferred:
    - production_prompt_construction_registry
    - fca_prompt_lattice_tooling
    - activation_attribute_measurement_harness
    - construction_frame_linter
    - prompt_library_redundancy_dashboard
    - mechanistic_interpretability_probe_lane
    - conexp_clj_or_custom_fca_pipeline
```

---

### 46.8 Round 14 accepted kernel

```yaml
construction_fca_prompt_library_kernel:
  core_sentence: >
    shadowMAS should treat reusable prompts and instruction templates as construction frames
    that open, suppress, or stabilize capability channels; prompt libraries should be audited
    through explicit template × capability-attribute tables and FCA-style lattices to detect
    gaps, redundancies, unsafe clusters, and uncontrolled template growth.

  principles:
    - construction_frame_over_lexical_tweak
    - prompt_template_is_channel_state_intervention
    - prompt_library_requires_attribute_table_when_reusable
    - FCA_is_audit_surface_not_authority
    - behavioral_probe_first_mechanistic_probe_optional
    - hidden_activation_is_diagnostic_not_truth
    - prune_redundant_templates_before_adding_more
```

---

### 46.9 Candidate shadowMAS primitives from Round 14

#### 46.9.1 Construction frame record

```yaml
construction_frame_record:
  frame_id:
  frame_name:
  intended_role: reviewer | planner | implementer | translator | adversary | judge | router | explainer
  object_under_work:
  event_relation:
    - compare
    - decompose
    - verify
    - critique
    - translate
    - synthesize
    - implement
    - escalate
  expected_output_shape:
  opened_channels:
  suppressed_channels:
  authority_boundary:
  forbidden_interpretations:
  example_template_ref:
```

#### 46.9.2 Prompt construction taxonomy

```yaml
prompt_construction_taxonomy:
  library_id:
  construction_levels:
    argument_structure:
      description: role/object/relation/output/authority frame
      intervention_strength: high
    phrasal_structure:
      description: step/order/detail framing without changing core event role
      intervention_strength: medium
    lexical_variant:
      description: synonym or style change within same frame
      intervention_strength: low
  rule: lexical variants must not be counted as distinct capability templates unless probes show meaningful behavior difference
```

#### 46.9.3 Capability activation attribute table

```yaml
capability_activation_attribute_table:
  library_id:
  objects: prompt_template_ids
  attributes:
    - opens_residual_first_review
    - opens_adversarial_failure_mode_search
    - opens_structured_schema_exactness
    - opens_bilingual_human_explanation
    - suppresses_sales_tone
    - suppresses_unbounded_autonomy
    - requires_source_refs
    - risks_truth_promotion_overreach
  measurement_lane: behavioral_probe | mechanistic_probe | activation_patch | mixed
  evidence_refs:
```

#### 46.9.4 FCA prompt library audit

```yaml
fca_prompt_library_audit:
  audit_id:
  library_id:
  formal_context_ref:
  concept_lattice_ref:
  coverage_gaps:
  redundant_template_clusters:
  unsafe_attribute_clusters:
  overly_broad_constructions:
  recommended_actions:
    - add_template
    - merge_templates
    - split_template
    - remove_template
    - add_channel_boundary
    - escalate_for_human_review
  cannot_promote_truth: true
```

#### 46.9.5 Prompt template gap/redundancy detector

```yaml
prompt_template_gap_redundancy_detector:
  library_id:
  target_capability_attributes:
  observed_template_attributes:
  uncovered_attributes:
  duplicate_attribute_sets:
  contradictory_templates:
  stale_templates:
  action:
    - keep
    - merge
    - rewrite
    - retire
    - probe_more
```

#### 46.9.6 Construction channel contract

```yaml
construction_channel_contract:
  construction_frame_id:
  linked_channel_state_record:
  allowed_open_channels:
  required_closed_channels:
  protected_boundaries:
    - human_authority
    - canonical_truth
    - project_domain_truth
    - security_policy
  probe_required_before_reuse: true | false
  rollback_or_retire_condition:
```

---

### 46.10 Practical diagnostic table

| Symptom | S-II diagnosis | shadowMAS action |
|---|---|---|
| Many prompts do nearly the same thing | template redundancy | run FCA audit and merge same-attribute templates |
| Tiny wording edits produce big behavioral shifts | hidden construction change | classify the frame level; record construction_frame_record |
| Prompt library keeps growing but coverage does not improve | unmanaged template entropy | build capability_activation_attribute_table and prune |
| Prompt opens useful depth but also overclaims authority | unsafe channel cluster | add construction_channel_contract and authority boundary |
| Team argues over “better wording” without evidence | lexical-level debate | compare lexical vs construction variants with behavioral probes |
| Open local model can be inspected but closed model cannot | mixed measurement lane | use behavioral probe as default; mechanistic probe only for open-model research |
| FCA shows a template cluster with risky attributes | unsafe concept lattice node | mark for rewrite, retire, or human review; do not promote truth |

---

### 46.11 Round 14 impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  prompt_layering_contract:
    reason: construction frames may become part of Runtime Adapter Prompt design and reusable Shared Core prompt templates

  current_truth:
    reason: may later add a principle that reusable prompts are construction/channel interventions, not truth sources

  governance_matrix:
    reason: prompt templates can open authority-like behavior but cannot become T0/T2 truth or bypass promotion gates

  runtime_adapter_future:
    reason: adapter prompts should declare construction frame, opened channels, suppressed channels, and forbidden interpretations

  packet_future:
    reason: task_packet or review_packet may later reference construction_frame_id for high-risk reusable workflows

  memory_plane:
    reason: prompt library audit results may become approved shared memory only after review, not direct canonical truth

  zh_tw_human_docs:
    reason: high-value explanation: “改句子不是重點，改 frame 才是重點” is useful for operators
```

Change-impact warning:

```text
Do not update canonical truth yet.
This round creates an active candidate kernel and prompt-library primitives.
Promotion would require review of prompt layering, governance matrix, current truth,
runtime adapter contracts, packet references, memory handling, and zh-TW explanation.
```

---

### 46.12 R14 compact decision packet

```yaml
round_14_decision_packet:
  round: R14
  v4_node: S-II_Construction_Grammar_Formal_Concept_Analysis_Epigenetics
  accepted_kernel: Construction_FCA_Prompt_Library
  kernel_status: candidate_kernel

  accepted_primitives:
    - construction_frame_record
    - prompt_construction_taxonomy
    - capability_activation_attribute_table
    - fca_prompt_library_audit
    - prompt_template_gap_redundancy_detector
    - construction_channel_contract

  hard_boundaries:
    - construction_frame_is_not_truth
    - fca_lattice_is_not_authority
    - hidden_activation_is_not_canonical_evidence_by_itself
    - prompt_cannot_create_absent_base_capability
    - behavioral_probe_is_default_for_v0
    - mechanistic_probe_is_optional_deep_audit

  next_round:
    round: R15
    topic: M-IV_CoT_as_Percolation_Bridge_Building
    purpose: connect CoT / intermediate reasoning tokens to capability-graph bridge formation and task-domain distance
```

---

## 47. Current document status after R14 S-II content update

```yaml
document_status:
  version: v1.6
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R14_S-II_Construction_Grammar_Formal_Concept_Analysis_Epigenetics
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: construction_fca_prompt_library_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.6
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 46. Round 14 — S-II Construction Grammar × Formal Concept Analysis × Epigenetics
    - 47. Current document status after R14 S-II content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - prompt_construction_kernel_now_requires_template_library_boundary
    - fca_audit_primitives_need_clear_non_authority_label
    - construction_frame_record_may_overlap_with_runtime_adapter_prompt_contract
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.7_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: M-IV_CoT_as_Percolation_Bridge_Building
```

---

## 48. Round 15 — M-IV CoT as Percolation Bridge-building

> status: active round log  
> theme: M-IV · chain-of-thought as reasoning/capability bridge formation  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, decisions, and shadowMAS implications.  
> access honesty: This round uses paper metadata/abstract-level evidence from public sources and prior v4 synthesis. The engineering decision is not that percolation literally proves CoT; the decision is that CoT should be treated as an optional bridge-building mechanism whose value must be measured by task-domain distance, answer verification, and trace-faithfulness checks.

---

### 48.1 Round 15 core question

```text
When does chain-of-thought help because it adds bridge nodes/edges between otherwise disconnected concept or capability clusters,
and when is it merely expensive, misleading, or decorative reasoning text?
```

v4 M-IV proposes:

```yaml
m_iv_claim:
  chain_of_thought_role: percolation_bridge_building
  mechanism: intermediate tokens add nodes and edges to the reasoning graph
  expected_gain: largest when task requires crossing disconnected concept clusters
  expected_low_gain: tasks inside a single already-connected cluster
```

shadowMAS translation:

```yaml
shadowmas_question:
  not: Should every agent always use CoT?
  but: When does a task need explicit bridge construction between domains, agents, packets, or constraints?
```

Working answer:

```text
CoT is an optional runtime/review surface for bridge-building.
It may increase effective reasoning connectivity for multi-step or cross-domain tasks,
but it is not canonical truth, not guaranteed faithful, and not automatically better when longer.
```

---

### 48.2 Feynman explanation

Imagine several islands:

```text
Island A = math fact
Island B = domain rule
Island C = security constraint
Island D = API shape
```

A simple answer jumps directly from question to answer:

```text
A → D
```

That works only if the path is already connected.

CoT adds stepping stones:

```text
A → B → C → D
```

The value is not the words themselves. The value is whether the intermediate steps connect islands that were otherwise disconnected.

Bad CoT:

```text
Lots of steps, no new bridge, no verification, more chance to rationalize a wrong answer.
```

Good CoT:

```text
A small number of necessary bridge steps that connect the relevant domains,
expose assumptions, and make the final answer easier to verify.
```

shadowMAS version:

```text
Use CoT-like visible bridge traces when a task crosses capability islands.
Do not use CoT as a universal style requirement.
```

---

### 48.3 Source basis captured in this round

#### v4 M-IV claim

v4 states:

```text
CoT intermediate tokens add nodes and edges to the reasoning graph,
raising effective concept-linkage density p above the percolation threshold p_c
for problems requiring cross-cluster reasoning.
```

It also proposes a testable prediction:

```text
CoT gains should correlate with the number and distance of distinct knowledge domains required.
More domains = more islands to bridge = larger CoT gain.
```

Current treatment:

```yaml
claim_strength: deep_structural_isomorphism_candidate
use_as: design_and_diagnostic_lens
not_use_as: literal mathematical proof that all CoT equals percolation
```

---

### 48.4 Evidence cards

#### E1 — Broadbent & Hammersley / percolation threshold foundation

Core source idea:

```text
Percolation studies whether connected paths form through a random medium.
Below a threshold, local pieces may exist but global passage fails.
Above a threshold, a spanning path appears.
```

shadowMAS mapping:

```yaml
reasoning_graph:
  nodes: concepts | constraints | evidence_refs | agent_capabilities | packet_fields | tool_results
  edges: inferential_links | dependency_links | translation_links | validation_links | authority_links
  bridge_need: task_requires_path_between_distant_clusters
```

Accepted insight:

```text
The question is not whether the system has isolated facts or agents.
The question is whether the needed path exists through the reasoning/capability graph.
```

Boundary:

```text
Do not estimate p_c with naive random-graph formulas for real shadowMAS task graphs.
Use empirical cross-domain probes instead.
```

---

#### E2 — Wei et al. / Chain-of-Thought Prompting

Core source idea:

```text
Chain-of-thought prompting supplies intermediate reasoning examples and improves performance on arithmetic,
commonsense, and symbolic reasoning tasks in sufficiently large models.
```

shadowMAS mapping:

```yaml
cot_bridge_trace:
  use_when:
    - task_has_multiple_constraints
    - answer_depends_on_intermediate_state
    - domain_distance_is_medium_or_high
    - verification_requires_visible_assumptions
  avoid_when:
    - task_is_lookup_or_single_step
    - schema/API/contract correctness is deterministic
    - visible reasoning would expose sensitive process details
    - longer trace increases hallucination surface without verification
```

Accepted insight:

```text
CoT is valuable when it creates inspectable intermediate states for complex reasoning, not because reasoning text is inherently authoritative.
```

---

#### E3 — Kojima et al. / Zero-shot CoT

Core source idea:

```text
A simple instruction such as step-by-step thinking can improve zero-shot reasoning performance across several tasks.
```

Round 15 extraction:

```text
The bridge trigger may be a construction frame, not necessarily a full few-shot demonstration.
```

Connection to R14:

```yaml
construction_frame_link:
  frame: step_by_step_bridge_construction
  opened_channel: multi_step_intermediate_state_generation
  required_audit: answer_verification_and_trace_compactness
```

Accepted insight:

```text
A minimal construction frame may open the bridge-building mode.
But shadowMAS still needs task-shape gating; do not enable it everywhere.
```

---

#### E4 — Wang et al. / Self-consistency as path ensemble

Core source idea:

```text
Self-consistency samples multiple reasoning paths and selects the most consistent answer by marginalizing over sampled paths.
```

shadowMAS mapping:

```yaml
path_ensemble_review:
  sample_multiple_bridge_paths: true
  compare_final_answers: true
  inspect_disagreement_regions: true
  use_when: high_uncertainty_or_cross_domain_reasoning
  not_truth_gate_by_itself: true
```

Accepted insight:

```text
If CoT is bridge-building, self-consistency is not just majority vote;
it is sampling multiple possible bridge paths and checking whether they converge.
```

Boundary:

```text
Convergent wrong rationalizations remain possible.
Self-consistency improves confidence only when paired with external checks or task-grounded verification.
```

---

#### E5 — Turpin et al. / CoT faithfulness warning

Core source idea:

```text
Visible chain-of-thought explanations may misrepresent why a model produced an answer.
```

shadowMAS mapping:

```yaml
cot_faithfulness_boundary:
  visible_trace_is:
    - runtime evidence
    - review aid
    - assumption surface
    - debugging surface
  visible_trace_is_not:
    - guaranteed hidden reasoning
    - canonical truth
    - sufficient explanation for protected decisions
    - replacement for verification
```

Accepted insight:

```text
CoT can help route, debug, and verify reasoning, but visible CoT must not be treated as a faithful transcript of model cognition.
```

---

#### E6 — Schaeffer et al. / emergence metric caution

Core source idea:

```text
Some apparent emergent abilities may depend on metric choice; discontinuous metrics can make smooth changes look sudden.
```

shadowMAS mapping:

```yaml
cot_gain_metric_audit:
  measure:
    - answer_accuracy
    - verification_pass_rate
    - trace_compactness
    - hallucinated_step_rate
    - domain_bridge_count
    - cost_per_correct_answer
  avoid:
    - declaring bridge emergence from one binary metric
```

Accepted insight:

```text
Do not claim CoT crossed a percolation threshold unless multiple metrics support an actual connectivity gain.
```

---

### 48.5 ToT candidate branches

```yaml
tot_branches:
  A_CoT_everywhere:
    decision: rejected
    reason: CoT adds token cost, exposure surface, and rationalization risk when no bridge is needed

  B_no_CoT_visible_reasoning_ever:
    decision: rejected
    reason: some cross-domain tasks need inspectable intermediate assumptions and bridge states for review

  C_CoT_as_optional_bridge_building_surface:
    decision: accepted
    reason: best captures M-IV while preserving task-shape gating and verification

  D_longer_CoT_is_always_better:
    decision: rejected
    reason: longer traces can add irrelevant nodes, hallucinated links, and review burden

  E_minimum_sufficient_bridge_trace:
    decision: accepted
    reason: aligns with R1 shortest sufficient artifact and R15 connectivity function

  F_visible_CoT_as_faithful_hidden_reasoning:
    decision: rejected
    reason: faithfulness literature warns visible explanations can misrepresent causal basis

  G_visible_trace_as_review_evidence_not_truth:
    decision: accepted
    reason: preserves audit value without truth confusion

  H_percolation_as_literal_formula_for_CoT_gain:
    decision: rejected_for_v0
    reason: real task graphs are structured and semantic, not simple random graphs

  I_empirical_domain_distance_CoT_probe:
    decision: accepted
    reason: test whether CoT gains increase with cross-domain distance and bridge count

  J_self_consistency_as_truth_gate:
    decision: rejected
    reason: convergent rationalization can still be wrong

  K_self_consistency_as_path_ensemble_signal:
    decision: accepted
    reason: useful uncertainty and bridge-path convergence evidence when externally checked
```

---

### 48.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept C + E + G
    reason: CoT should become a strategic reasoning surface, not a default style tax.
    risk: teams may mistake longer reasoning for better governance.

  CTO:
    vote: accept I + K
    reason: domain-distance probes and path ensembles are implementable and measurable.
    risk: percolation math should not be overfit to semantic task graphs.

  Security:
    vote: accept G strongly; reject F strongly
    reason: visible reasoning traces can leak sensitive assumptions and can be unfaithful; they are evidence, not truth.
    risk: hidden chain exposure or trace logging may create data-retention risk.

  CSO:
    vote: accept C
    reason: “CoT as bridge-building” is a strong design story and clarifies when CoT is worth the cost.
    risk: if every prompt says think step by step, the concept becomes noise.

  CFO:
    vote: accept E
    reason: minimum sufficient bridge traces control token and review cost.
    risk: self-consistency path ensembles can become expensive without gating.
```

---

### 48.7 LATS result

```yaml
lats_result:
  best_node:
    name: Minimum Sufficient Bridge Trace with Faithfulness Boundary
    score: 0.91
    status: candidate_kernel
    why:
      - absorbs M-IV without making CoT universal
      - links R5 capability connectivity with reasoning traces
      - links R14 construction frames with bridge-opening prompt patterns
      - preserves R1 shortest-sufficient artifact discipline
      - protects against visible-CoT truth confusion
      - creates measurable probes for CoT gain vs domain distance

  accepted:
    - CoT_as_optional_bridge_building_surface
    - minimum_sufficient_bridge_trace
    - reasoning_graph_connectivity_probe
    - domain_distance_CoT_gain_hypothesis
    - self_consistency_as_path_ensemble_signal
    - visible_trace_as_review_evidence_not_truth

  rejected:
    - CoT_everywhere
    - longer_CoT_is_always_better
    - visible_CoT_as_faithful_hidden_reasoning
    - reasoning_trace_as_truth_gate
    - percolation_as_literal_formula_for_v0
    - self_consistency_as_truth_gate

  deferred:
    - production_reasoning_graph_probe
    - domain_distance_benchmark_for_cot_gain
    - cot_faithfulness_audit_harness
    - self_consistency_budget_policy
    - trace_visibility_policy_for_review_packets
```

---

### 48.8 Round 15 accepted kernel

```yaml
cot_percolation_bridge_building_kernel:
  core_sentence: >
    shadowMAS should treat chain-of-thought and intermediate reasoning traces as optional
    bridge-building surfaces: use them when a task requires connecting distant concepts,
    capabilities, agents, constraints, or evidence clusters; keep traces minimum-sufficient,
    verify final answers externally, and never treat visible reasoning as canonical truth or
    guaranteed faithful hidden cognition.

  principles:
    - CoT_is_bridge_surface_not_default_style
    - bridge_trace_should_be_minimum_sufficient
    - CoT_gain_should_correlate_with_domain_distance_if_M_IV_is_useful
    - visible_trace_is_review_evidence_not_truth
    - self_consistency_samples_paths_not_authority
    - answer_verification_remains_required
    - percolation_math_is_design_lens_not_v0_literal_formula
```

---

### 48.9 Candidate shadowMAS primitives from Round 15

#### 48.9.1 Bridge trace policy

```yaml
bridge_trace_policy:
  task_id:
  task_domain_distance: low | medium | high
  bridge_needed: true | false | unknown
  reason_bridge_needed:
    - cross_domain_dependency
    - multi_constraint_tradeoff
    - hidden_assumption_surface
    - agent_capability_integration
    - verification_requires_intermediate_state
  trace_mode: none | short_bridge_trace | structured_bridge_packet | path_ensemble
  max_trace_budget:
  answer_verification_required: true
  truth_status: runtime_evidence_only
```

#### 48.9.2 Reasoning graph connectivity probe

```yaml
reasoning_graph_connectivity_probe:
  task_id:
  concept_clusters:
  required_edges:
  missing_edges_before_trace:
  bridge_nodes_added_by_trace:
  edges_validated:
  unresolved_edges:
  connectivity_gain: low | medium | high
  hallucinated_edge_risk: low | medium | high
```

#### 48.9.3 Domain-distance CoT gain audit

```yaml
domain_distance_cot_gain_audit:
  benchmark_set:
  task_groups:
    low_domain_distance:
    medium_domain_distance:
    high_domain_distance:
  compare_modes:
    - direct_answer
    - short_bridge_trace
    - full_CoT
    - self_consistency_paths
  metrics:
    - accuracy
    - verification_pass_rate
    - cost_per_correct_answer
    - hallucinated_step_rate
    - trace_compactness
  expected_pattern_if_M_IV_holds: gain_increases_with_domain_distance
```

#### 48.9.4 Trace faithfulness warning record

```yaml
trace_faithfulness_warning_record:
  trace_id:
  model_or_agent:
  task:
  visible_trace_available: true | false
  faithfulness_claim_allowed: false
  known_bias_or_leak_risk:
  verification_refs:
  reviewer_note: visible_trace_is_review_surface_not_hidden_reasoning_transcript
```

#### 48.9.5 Self-consistency path ensemble record

```yaml
self_consistency_path_ensemble_record:
  task_id:
  path_count:
  sampling_temperature:
  final_answers:
  answer_distribution:
  convergence_level: low | medium | high
  disagreement_regions:
  external_verification_result:
  decision: accept | inspect | rerun | escalate
  truth_status: evidence_only
```

---

### 48.10 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may refine prompt policy and review_packet guidance, but not canonical yet

  prompt_layering_contract:
    reason: bridge traces may become runtime adapter / construction-frame behavior

  governance_matrix:
    reason: visible reasoning traces must remain T4/T5 evidence, never T2 truth or T0 authority

  packet_future:
    reason: bridge_trace_policy and reasoning_graph_connectivity_probe may influence future review_packet/task_packet fields

  runtime_future:
    reason: path ensembles and trace modes require execution budget and risk gating

  security_policy_future:
    reason: trace visibility and logging can create data exposure and faithfulness risks

  zh_tw_human_docs:
    reason: likely high-value explanation if CoT policy is promoted, especially to prevent “think step by step everywhere” misuse
```

Change-impact warning:

```text
Do not update canonical truth yet.
This round creates an active candidate kernel for CoT bridge-building.
Promotion would require review of prompt policy, runtime budget controls,
review_packet surfaces, trace visibility/security policy, and human-facing explanation.
```

---

### 48.11 R15 compact decision packet

```yaml
round_15_decision_packet:
  round: R15
  v4_node: M-IV_CoT_as_Percolation_Bridge_Building
  accepted_kernel: CoT_Percolation_Bridge_Building
  kernel_status: candidate_kernel

  accepted_primitives:
    - bridge_trace_policy
    - reasoning_graph_connectivity_probe
    - domain_distance_cot_gain_audit
    - trace_faithfulness_warning_record
    - self_consistency_path_ensemble_record

  hard_boundaries:
    - CoT_is_not_universal_default
    - visible_trace_is_not_guaranteed_hidden_reasoning
    - trace_is_runtime_evidence_not_truth
    - longer_trace_is_not_automatically_better
    - answer_verification_remains_required
    - self_consistency_is_not_truth_gate
    - percolation_formula_not_literal_v0_requirement

  next_round:
    round: R16
    topic: M-V_Curiosity_as_Learnable_KL_Frontier
    purpose: define exploration stop conditions, learnable frontier detection, and irreducible-noise boundaries
```

---

## 49. Current document status after R15 M-IV content update

```yaml
document_status:
  version: v1.7
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R15_M-IV_CoT_as_Percolation_Bridge_Building
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: cot_percolation_bridge_building_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.8
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 48. Round 15 — M-IV CoT as Percolation Bridge-building
    - 49. Current document status after R15 M-IV content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - cot_bridge_kernel_requires_trace_visibility_policy_before_promotion
    - reasoning_graph_connectivity_probe_may_overlap_with_variety_connectivity_audit
    - self_consistency_path_ensemble_needs_runtime_budget_policy
    - CoT_faithfulness_boundary_must_be_clear_in_human_docs_if_promoted
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.8_or_next_document_only_pass
    target: consolidated_primitive_candidate_index
  intended_next_content_update: M-V_Curiosity_as_Learnable_KL_Frontier
```


---

## 50. Round 16 — M-V Curiosity = Learnable KL Frontier

> status: active round log  
> theme: M-V · curiosity as greedy reduction of reducible KL / learnable frontier  
> method: 3 full-read targets + 2 comparison scans, with ToT×MoE×CoT×LATS可審查版  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.  
> access honesty: Schmidhuber 1991, Oudeyer/Kaplan/Hafner 2007, and Pathak et al. 2017 were treated as the three main read targets. Burda et al. 2019 and Ecoffet et al. 2021 were used as comparison scans. The round does not claim that all intrinsic motivation methods are mathematically identical; it extracts the shared design constraint relevant to shadowMAS: exploration value is not raw novelty or raw surprise, but expected reducible learning progress under governance boundaries.

---

### 50.1 Round 16 core question

```text
Can shadowMAS define a principled exploration policy and stopping condition by distinguishing
learnable residual frontier from familiar regions and irreducible noise?
```

v4 M-V says:

```text
Curiosity = high prediction error that is learnable / reducible.
```

Round 16 translates that into a shadowMAS design question:

```yaml
m_v_question:
  not: should agents explore whatever is novel or surprising?
  but: when is a residual worth spending exploration budget on?
```

Working answer:

```text
Explore only where the system expects useful residual reduction.
Stop or deprioritize when the remaining residual is already familiar, out of scope,
stale, poisoned, unsafe, or irreducible noise.
```

---

### 50.2 Feynman explanation

Imagine a student learning math.

Bad curiosity:

```text
Look at the weirdest page in the book forever.
```

This fails because some weird pages are:

```text
random scribbles
outside the syllabus
already solved
too advanced for current prerequisites
not useful for the current goal
```

Better curiosity:

```text
Study the page where mistakes are still happening, but each attempt improves the score.
```

That is the learnable frontier:

```text
not too easy → no learning
not pure noise → no learning
not out of scope → relevant learning
not unsafe → governed learning
```

shadowMAS translation:

```text
Agents should not chase every hot residual.
They should prioritize zones where residual is high enough, reducible, relevant, fresh,
and safe under governance boundaries.
```

---

### 50.3 Source basis captured in this round

#### v4 M-V claim

v4 states:

```text
Curiosity = greedy KL reduction on the learnable frontier.
```

The useful part for shadowMAS is the three-way split:

```yaml
region_types:
  familiar_region:
    signal: low residual / already compressed
    action: deprioritize

  learnable_frontier:
    signal: high residual + evidence of learning progress
    action: explore / probe / assign budget

  irreducible_noise_region:
    signal: high residual + no learning progress
    action: stop / quarantine / mark irreducible / avoid budget sink
```

This extends Round 4's externalized residual landscape:

```text
field heat alone is insufficient.
Need frontier status: learnable vs familiar vs irreducible.
```

---

### 50.4 Evidence cards

#### E1 — Schmidhuber 1991 / curiosity and boredom in model-building controllers

Core source idea:

```text
A curious model-building control system rewards actions that are expected to improve the world model's knowledge.
```

Important extraction:

```text
Curiosity is not raw prediction error.
Curiosity is related to expected improvement in prediction/model knowledge.
```

shadowMAS mapping:

```yaml
curiosity_runtime_signal:
  residual: what remains unexplained
  expected_learning_progress: whether another action is likely to reduce it
  boredom_condition: repeated exposure no longer improves model/review outcome
  action: pursue_only_if_learning_progress_expected
```

Accepted insight:

```text
Exploration should be driven by expected residual reduction, not raw novelty.
```

---

#### E2 — Oudeyer, Kaplan & Hafner 2007 / Intelligent Adaptive Curiosity

Core source idea:

```text
Intrinsic motivation can focus an agent on situations where learning progress is maximized.
```

Relevant mechanism:

```text
The agent should avoid both the fully predictable and the completely unpredictable.
```

shadowMAS mapping:

```yaml
learning_progress_band:
  too_easy:
    signal: low residual and stable high confidence
    action: do not spend exploration budget

  productive_frontier:
    signal: residual decreases after probes / new evidence changes model quality
    action: allocate exploration budget

  too_random_or_unlearnable:
    signal: repeated probes do not reduce residual
    action: classify as irreducible_or_external_dependency
```

Accepted insight:

```text
The system should track residual delta over attempts, not just residual level.
```

---

#### E3 — Pathak et al. 2017 / curiosity-driven exploration by self-supervised prediction

Core source idea:

```text
Curiosity can be formulated as prediction error in a learned feature space,
especially when extrinsic rewards are sparse or absent.
```

Important engineering lesson:

```text
The feature space matters. Predicting irrelevant or uncontrollable detail can create bad curiosity.
```

shadowMAS mapping:

```yaml
feature_space_for_curiosity:
  not_raw_chatter:
    reason: irrelevant details can dominate residual
  prefer_governance_relevant_features:
    - unresolved_truth_touchpoint
    - validation_gap
    - missing_dependency
    - unclear_authority_boundary
    - failed_cross_agent_bridge
    - stale_or_poisoned_field_zone
```

Accepted insight:

```text
Curiosity signals must be projected into task/governance-relevant feature space.
```

---

#### E4 — Burda et al. 2019 / Random Network Distillation comparison scan

Core source idea:

```text
Random Network Distillation gives an exploration bonus from prediction error against fixed random features.
```

Why this matters as comparison:

```text
RND shows a scalable novelty/prediction-error bonus can work,
but shadowMAS cannot blindly import novelty bonus as governance policy.
```

shadowMAS mapping:

```yaml
novelty_bonus_boundary:
  useful_for:
    - runtime exploration prioritization
    - local search over unknown work zones
    - detecting under-covered task regions

  not_allowed_for:
    - truth promotion
    - human-only authority decisions
    - unbounded repo traversal
    - overriding acceptance criteria
```

Accepted insight:

```text
Novelty can seed exploration, but learning progress and governance relevance must filter it.
```

---

#### E5 — Ecoffet et al. 2021 / Go-Explore comparison scan

Core source idea:

```text
Effective exploration may require remembering promising states, returning to them, and then exploring from them.
```

Why this matters:

```text
Curiosity without memory can detach from useful frontier states.
```

shadowMAS mapping:

```yaml
return_then_explore_for_shadowmas:
  remember_frontier_state:
    - unresolved_zone
    - partial_success_path
    - prior_validation_gap
    - promising_bridge_node

  return_before_explore:
    - reload evidence context
    - check stale/TTL status
    - verify authority boundary
    - confirm exploration budget

  explore_from_frontier:
    - run minimal probe
    - measure residual delta
    - update frontier status
```

Accepted insight:

```text
Exploration needs frontier memory, not only spontaneous novelty chasing.
```

---

### 50.5 ToT candidate branches

```yaml
tot_branches:
  A_curiosity_as_raw_surprise_maximization:
    decision: rejected
    reason: high surprise may be random, poisoned, stale, unsafe, or outside scope

  B_curiosity_as_novelty_bonus_only:
    decision: rejected_as_primary_policy
    reason: novelty can seed exploration but does not prove learning value

  C_curiosity_as_learning_progress:
    decision: accepted
    reason: tracks whether residual decreases after probing; matches learnable-frontier framing

  D_curiosity_as_truth_or_authority:
    decision: rejected
    reason: intrinsic reward is runtime priority signal, not canonical truth or human authority

  E_learnable_frontier_as_runtime_exploration_lane:
    decision: accepted
    reason: gives agents a principled way to allocate exploration budget

  F_explore_without_scope_boundary:
    decision: rejected
    reason: would reintroduce blind traversal and uncontrolled intake

  G_frontier_memory_and_return_then_explore:
    decision: accepted
    reason: prevents detachment from promising partially explored states

  H_endless_exploration_until_all_residual_zero:
    decision: rejected
    reason: some residual is irreducible or not worth reducing under current goal

  I_frontier_exhaustion_stop_condition:
    decision: accepted
    reason: gives a stopping rule when remaining high residual lacks learning progress or is out of scope

  J_numeric_KL_required_for_v0:
    decision: rejected_for_v0
    reason: many shadowMAS tasks lack formal distributions; semantic proxy is sufficient for now

  K_semantic_learnability_proxy:
    decision: accepted
    reason: residual_delta, evidence_gain, validation_gain, and confidence_gain are implementable across symbolic tasks
```

---

### 50.6 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept E + I
    reason: exploration needs a principled stop condition or the system becomes an infinite research machine.
    risk: curiosity language may justify scope creep unless bounded by governance.

  CTO:
    vote: accept C + K + G
    reason: residual delta and frontier memory are implementable in runtime/review packets without numeric KL.
    risk: exact learning-progress metrics may be noisy; start with typed proxies.

  Security:
    vote: accept boundaries strongly; reject A + F
    reason: curiosity without scope and authority checks recreates blind traversal and field poisoning risks.
    risk: agents may over-explore sensitive repos, logs, or memory surfaces if curiosity is treated as permission.

  CSO:
    vote: accept learnable frontier framing
    reason: it creates a strong design story connecting KL, signal field, CoT, and exploration policy.
    risk: must remain operational, not motivational metaphor.

  CFO:
    vote: accept I
    reason: frontier exhaustion prevents wasted compute on random or low-value residuals.
    risk: too many frontier probes can exceed budget unless stop criteria are explicit.
```

---

### 50.7 LATS result

```yaml
lats_result:
  best_node:
    name: Governed Learnable Frontier Exploration
    score: 0.92
    status: candidate_kernel
    why:
      - absorbs M-V without turning curiosity into novelty chasing
      - links R4 externalized residual landscape with R12 precision-weighted residual routing
      - links R15 bridge-building with exploration stop conditions
      - preserves no-blind-traversal and human-authority boundaries
      - creates practical stop conditions for irreducible/noisy residuals

  accepted:
    - learnable_KL_frontier_as_runtime_exploration_lane
    - curiosity_as_learning_progress_not_raw_surprise
    - residual_delta_over_residual_level
    - frontier_memory_and_return_then_explore
    - semantic_learnability_proxy_for_v0
    - frontier_exhaustion_stop_condition

  rejected:
    - surprise_maximization_as_policy
    - novelty_bonus_as_truth
    - curiosity_as_authority
    - endless_exploration
    - exploration_without_scope_boundary
    - numeric_KL_required_for_v0

  deferred:
    - production_learnable_frontier_detector
    - learning_progress_metric_registry
    - irreducible_noise_classifier
    - curiosity_budget_policy
    - exploration_memory_cell_registry
    - frontier_exhaustion_dashboard
```

---

### 50.8 Round 16 accepted kernel

```yaml
learnable_kl_frontier_curiosity_kernel:
  core_sentence: >
    shadowMAS should treat curiosity as governed exploration of the learnable frontier:
    prioritize residual zones that are high enough, reducible, scope-relevant, fresh,
    and safe; deprioritize familiar zones and stop when remaining residuals are
    irreducible, stale, poisoned, unsafe, or not worth current exploration budget.

  principles:
    - curiosity_targets_learning_progress_not_raw_surprise
    - residual_delta_matters_more_than_residual_level
    - novelty_is_seed_signal_not_truth_signal
    - frontier_memory_prevents_detachment
    - return_then_explore_before_new_probe
    - irreducible_noise_requires_stop_or_quarantine
    - exploration_requires_scope_authority_and_budget_boundary
    - semantic_KL_proxy_is_enough_for_v0
```

---

### 50.9 Candidate shadowMAS primitives from Round 16

#### 50.9.1 Learnable frontier record

```yaml
learnable_frontier_record:
  frontier_id:
  zone:
  residual_kind: validation_gap | truth_conflict | missing_dependency | cross_domain_bridge_gap | unknown_runtime_behavior | other
  residual_level: low | medium | high | blocker
  residual_delta_after_last_probe: reduced | unchanged | increased | unknown
  learnability_estimate: low | medium | high | unknown
  reducibility_evidence:
  scope_relevance: low | medium | high
  authority_allowed: true | false | review_required | human_only
  safety_risk: low | medium | high
  freshness: fresh | aging | stale
  decision: explore | return_then_explore | monitor | stop | quarantine | escalate
```

#### 50.9.2 Learning progress probe

```yaml
learning_progress_probe:
  probe_id:
  frontier_id:
  baseline_residual:
  probe_action:
  expected_information_gain:
  actual_information_gain:
  validation_gain:
  confidence_gain:
  residual_after_probe:
  learning_progress: negative | zero | low | medium | high
  next_action: continue | change_probe | stop | escalate
```

#### 50.9.3 Irreducible noise classifier

```yaml
irreducible_noise_classifier:
  zone:
  repeated_probe_count:
  residual_delta_history:
  evidence_gain_history:
  suspected_noise_source:
    - random_environment
    - unavailable_dependency
    - adversarial_or_poisoned_signal
    - underspecified_goal
    - outside_scope
    - measurement_error
  classification: not_noise | likely_irreducible | poisoned | blocked_by_missing_authority | underspecified
  mitigation: stop | quarantine | request_scope_decision | require_new_evidence | human_review
```

#### 50.9.4 Curiosity budget policy

```yaml
curiosity_budget_policy:
  task_id:
  exploration_budget:
    max_probes:
    max_tokens:
    max_tool_calls:
    max_runtime:
  budget_priority:
    - high_reducibility
    - high_scope_relevance
    - high_validation_gain
    - low_security_risk
  hard_stops:
    - authority_boundary_hit
    - no_learning_progress_after_n_probes
    - stale_or_poisoned_field
    - out_of_scope_repo_or_file
    - acceptance_criteria_already_satisfied
```

#### 50.9.5 Frontier exhaustion report

```yaml
frontier_exhaustion_report:
  task_id:
  explored_frontiers:
  exhausted_frontiers:
  stopped_reasons:
    - familiar_already_compressed
    - irreducible_noise
    - outside_scope
    - budget_exhausted
    - authority_boundary
    - unsafe_to_continue
  remaining_residuals:
  decision_needed:
  truth_status: exploration_runtime_evidence_only
```

---

### 50.10 Impact on existing shadowMAS

Candidate changes touch:

```yaml
impacted_surfaces:
  current_truth:
    reason: may refine no-blind-traversal and exploration/inspection discipline if promoted

  governance_matrix:
    reason: curiosity signals must remain R/T4/T5 runtime evidence, not T2 truth or T0 authority

  prompt_layering_contract:
    reason: runtime adapters may need explicit exploration scope and curiosity budget boundaries

  packet_future:
    reason: learnable_frontier_record and frontier_exhaustion_report may influence task_packet/review_packet fields

  runtime_future:
    reason: exploration budgets, probe loops, and stop conditions belong to R-layer execution policy

  memory_plane:
    reason: frontier memory looks like reusable memory but should remain runtime/working memory unless promoted

  security_policy_future:
    reason: curiosity must not authorize blind repo traversal, sensitive data exploration, or field poisoning amplification

  zh_tw_human_docs:
    reason: high-value explanation if promoted; humans must understand curiosity means governed learnability, not unrestricted exploration
```

Change-impact warning:

```text
Do not update canonical truth yet.
This round creates an active candidate kernel for learnable-frontier exploration.
Promotion would require review of no-blind-traversal rules, runtime exploration budgets,
packet/review fields, memory-plane status, security boundaries, and human-facing explanation.
```

---

### 50.11 R16 compact decision packet

```yaml
round_16_decision_packet:
  round: R16
  v4_node: M-V_Curiosity_as_Learnable_KL_Frontier
  accepted_kernel: Learnable_KL_Frontier_Curiosity
  kernel_status: candidate_kernel

  accepted_primitives:
    - learnable_frontier_record
    - learning_progress_probe
    - irreducible_noise_classifier
    - curiosity_budget_policy
    - frontier_exhaustion_report

  hard_boundaries:
    - curiosity_is_not_surprise_maximization
    - novelty_is_not_learning_value
    - intrinsic_reward_is_not_truth_or_authority
    - exploration_requires_scope_and_budget
    - blind_repo_traversal_remains_forbidden
    - irreducible_noise_requires_stop_or_quarantine
    - semantic_KL_proxy_not_numeric_KL_requirement

  next_round:
    round: document_optimization_or_v4_closeout
    topic: consolidate_remaining_v4_and_document_optimization
    purpose: after completing M-V, prepare final v4 convergence map and document optimization pass
```



---

## 51. Current document status after R16 M-V content update

```yaml
document_status:
  version: v1.8
  canonical: false
  active_design_relevance: high
  safe_to_modify_next_round: true
  latest_added_content_round: R16_M-V_Curiosity_as_Learnable_KL_Frontier
  latest_document_review: pass_7_closeout_horizon_and_single_entry_hardening
  latest_document_only_change: none_this_round
  latest_content_change: learnable_kl_frontier_curiosity_round_added
  current_best_reading_path:
    - 0.1 Must-see active decision ledger
    - 0.2 Must-see document control plane v1.8
    - 0.3 Current kernel index
    - 0.4 Decision-state map
    - 50. Round 16 — M-V Curiosity = Learnable KL Frontier
    - 51. Current document status after R16 M-V content update
  current_main_document_debt:
    - candidate_primitives_need_consolidated_index
    - paper_evidence_may_need_appendix_restructure_later
    - historical_document_self_optimization_passes_should_eventually_move_to_appendix_or_split_file
    - accepted_rejected_deferred_lists_may_need_grouped_table_when_larger
    - future_content_rounds_must_update_top_indices_immediately
    - curiosity_kernel_requires_frontier_boundary
    - learnable_frontier_record_may_overlap_with_residual_action_value_and_signal_field_zone
    - exploration_memory_must_not_be_mistaken_for_approved_shared_memory
    - frontier_exhaustion_stop_condition_needs_runtime_budget_policy
    - curiosity_policy_must_reinforce_no_blind_traversal_in_human_docs_if_promoted
  estimated_document_only_rounds_to_stable_single_file: 3
  estimated_document_only_rounds_to_stable_if_split_allowed: 2
  intended_next_document_optimization:
    version: v1.9_or_next_document_only_pass
    target: consolidated_primitive_candidate_index_plus_final_v4_convergence_map
  intended_next_content_update: none_remaining_from_original_recommended_v4_sequence_unless_user_requests_extra_comparison_round
```

## 52. Document self-optimization — eighth pass ToT×MoE×CoT×LATS可審查版

> status: document design review pass 8  
> object under review: post-R16 single active design log  
> goal: consolidate all planned v4 imports into a usable decision surface.  
> note: CoT remains internal; this section records inspectable reasoning outputs, candidate branches, votes, and decisions.

---

### 52.1 Problem diagnosis

After R16, the planned v4 content path is complete for the current cycle.
The document now has enough research evidence and enough candidate kernels.
The main bottleneck is no longer discovery.
The bottleneck is **promotion readiness**.

Reader risks at v1.8:

```yaml
reader_risks:
  primitive_scattering:
    symptom: primitives are distributed across many round logs
    consequence: future schema work must rediscover them manually

  convergence_invisibility:
    symptom: each kernel is clear locally, but global v4 convergence pattern is implicit
    consequence: readers may not know which families should be promoted first

  promotion_ambiguity:
    symptom: accepted design kernels appear close to canonical language
    consequence: future agents may patch truth files without formal change-impact review
```

Therefore v1.9 applies a navigation and promotion-readiness optimization:

```text
round logs remain intact;
top control plane now provides primitive families, convergence map, and promotion queue.
```

---

### 52.2 ToT branches

```yaml
document_tot_branches:
  A_append_another_status_only:
    decision: rejected
    reason: would not solve primitive scattering or promotion ambiguity

  B_full_rewrite_into_short_summary:
    decision: rejected
    reason: would destroy evidence trace and paper-to-design auditability

  C_extract_every_primitive_into_one_giant_table:
    decision: rejected
    reason: technically complete but recreates a giant surface at the top of the file

  D_consolidate_by_primitive_family:
    decision: accepted
    reason: groups primitives by future owner surface while preserving round evidence

  E_create_final_v4_convergence_map:
    decision: accepted
    reason: shows what the entire v4 cycle contributed after all planned content rounds

  F_create_promotion_change_impact_queue:
    decision: accepted
    reason: prevents active kernels from being mistaken for immediate canonical patches

  G_split_the_file_now:
    decision: deferred
    reason: still following single active design log requirement; split remains recommended if the file becomes operationally painful
```

---

### 52.3 MoE votes

```yaml
document_moe_votes:
  CEO:
    vote: accept D + E + F
    reason: the research program has enough content; the leadership surface now needs decision readiness
    risk: if every primitive is promoted, shadowMAS becomes overbuilt

  CTO:
    vote: accept D strongly
    reason: primitive families map to future schema/runtime/review work packages better than raw round order
    risk: field-level schemas are still not ready for implementation

  Security:
    vote: accept F strongly
    reason: promotion queue must preserve truth layers, human authority, and runtime-not-truth boundaries
    risk: signal field, score, or CoT traces could become hidden authority if not gated

  CSO:
    vote: accept E
    reason: final v4 convergence map turns research synthesis into product/design narrative
    risk: too much abstraction could hide actionable next steps

  CFO:
    vote: accept D + F
    reason: family grouping and promotion queue reduce maintenance cost and prevent premature infrastructure spending
    risk: promoting runtime-heavy primitives before packet/review basics would increase complexity rent
```

---

### 52.4 LATS result

```yaml
document_lats_result:
  best_node:
    name: Primitive Family Index + Final Convergence Map + Promotion Queue
    score: 0.96
    status: accepted_and_applied
    why:
      - solves primitive scattering without giant-table overload
      - shows all planned v4 content has converged into a small number of design pressures
      - separates non-canonical active kernels from canonical patch candidates
      - gives future change-impact review a ready queue
      - preserves single-file traceability

  applied_now:
    - upgraded document control plane to v1.9
    - added 0.7 Consolidated primitive family index
    - added 0.8 Final v4 convergence map
    - added 0.9 Promotion and change-impact queue
    - updated closeout horizon: one remaining document-only closeout round if no new research is added
    - added this eighth document self-optimization pass

  rejected:
    - giant primitive table
    - full rewrite
    - automatic canonical promotion
    - deleting historical round evidence

  deferred:
    - splitting into separate files
    - field-level schemas for every primitive
    - direct canonical patching
```

---

### 52.5 Accepted document-level rule after v1.9

```text
All future work should treat this file in four tiers:
1. Top control plane and decision indexes = current navigation surface.
2. Promotion queue = candidate canonical review surface.
3. Round logs = evidence and rationale surface.
4. Historical self-optimization logs = trace, not reading path.
```

---

### 52.6 Remaining closeout work

```yaml
remaining_document_closeout:
  target_version: v2.0
  goal: freeze_reading_path
  tasks:
    - mark older document self-optimization sections as appendix-grade trace
    - add a stable reading order for human, agent, and canonical-review modes
    - prepare P1 canonical proposal as a separate patch plan if requested
    - decide whether to split primitive register out of this file
  estimated_rounds_if_no_new_v4_content: 1
```

---

## 53. Current document status after v1.9 document optimization

```yaml
current_document_status:
  version: v1.9
  latest_update_type: document_optimization
  latest_content_round: R16_M-V_Curiosity_as_Learnable_KL_Frontier
  v4_content_import_status: complete_for_current_plan
  latest_document_review: pass_8_v4_convergence_index_and_promotion_queue

  current_top_surfaces:
    - 0.1 active decision ledger
    - 0.2 document control plane v1.9
    - 0.3 current kernel index
    - 0.4 decision-state map
    - 0.7 consolidated primitive family index
    - 0.8 final v4 convergence map
    - 0.9 promotion and change-impact queue

  document_only_rounds_remaining_if_no_new_content: 1

  next_recommended_action:
    name: v2.0 closeout / freeze reading path
    purpose: demote historical optimization logs, stabilize reader modes, and optionally prepare P1 canonical proposal

  canonical_change_status:
    changed_canonical_truth_files: false
    promoted_primitives: none
    promoted_kernels: none
    requires_change_impact_review_before_any_canonical_patch: true
```

v1.9 decision:

```text
The v4 active design import is complete enough to stop content accumulation under the current plan.
The next meaningful step is not another research round; it is either:
1. v2.0 document closeout, or
2. P1 canonical proposal drafting for residual-first review, layer composition, variety audit, and reviewer drift monitoring.
```

---

## 54. Document self-optimization — ninth pass ToT×MoE×CoT×LATS可審查版

> status: document closeout review  
> object under review: v1.9 post-v4 active design log  
> goal: freeze the single-file reading path, demote historical process logs, and prepare the first canonical proposal batch without changing canonical truth.

### 54.1 Problem diagnosis after v1.9

v1.9 solved the largest recall problem by adding:

```yaml
v1_9_solved:
  - primitive family index
  - final v4 convergence map
  - promotion/change-impact queue
```

The remaining problem was not missing content. It was **closeout ambiguity**:

```yaml
remaining_risks_before_v2_0:
  - readers may still read the file linearly
  - historical self-optimization logs may compete with current navigation
  - P1 promotion queue is visible but not yet shaped as a patch plan
  - file-splitting decision is implicit
  - polished active log may look canonical even though it is non-canonical
```

### 54.2 ToT branches

```yaml
document_tot_branches:
  A_add_more_summaries:
    decision: rejected
    reason: summary count was no longer the bottleneck; additional summaries would enlarge the control plane

  B_delete_historical_self_optimization_logs:
    decision: rejected
    reason: would reduce traceability and erase why current structure exists

  C_mark_historical_logs_as_appendix_grade_trace:
    decision: accepted
    reason: preserves history while preventing process notes from becoming the reading path

  D_freeze_role_based_reading_paths:
    decision: accepted
    reason: human, agent, and canonical-review readers need different first-pass routes

  E_prepare_P1_patch_plan_without_applying_it:
    decision: accepted
    reason: turns promotion queue into actionable review material while preserving non-canonical status

  F_split_file_immediately:
    decision: rejected_for_now
    reason: split would create sync overhead before any formal patch package exists

  G_record_split_conditions:
    decision: accepted
    reason: gives future maintainers a clear trigger instead of vague discomfort
```

### 54.3 MoE votes

```yaml
moe_votes:
  CEO:
    vote: accept D + E + G
    reason: the file must become decision-usable, not merely complete
    warning: do not let v2.0 look like canonical approval

  CTO:
    vote: accept D + E
    reason: role-based reading paths and P1 patch shape are directly usable for future implementation planning
    warning: do not create required schemas until packet contracts are reviewed

  Security:
    vote: accept C + E strongly
    reason: historical notes and active candidates must not masquerade as authority
    warning: reviewer drift, signal fields, and scores must remain evidence until promoted

  CSO:
    vote: accept D + G
    reason: frozen reading paths preserve the strategic story and prevent giant-surface regression
    warning: excessive indexing can become its own giant surface

  CFO:
    vote: accept C + G
    reason: avoid immediate split until there is clear ROI; maintain one-file continuity for now
    warning: if formal patching begins, split to reduce maintenance cost
```

### 54.4 LATS result

```yaml
lats_result:
  best_node:
    name: Frozen Reading Path with Prepared P1 Patch Plan
    score: 0.95
    status: accepted_and_applied
    why:
      - closes the last planned document-only optimization round
      - preserves one-file continuity
      - prevents historical process logs from competing with current status
      - makes P1 canonical proposal actionable without applying it
      - records split conditions without forcing premature file fragmentation

  applied_now:
    - upgraded document control plane to v2.0
    - changed document_only_rounds_remaining_to_stable to 0
    - added 0.10 Frozen reading paths
    - added 0.11 Historical self-optimization log status
    - added 0.12 P1 canonical proposal patch plan
    - added 0.13 Split decision record
    - added this ninth document self-optimization pass

  rejected:
    - additional giant summary surface
    - deleting historical optimization logs
    - immediate file split
    - automatic canonical promotion

  deferred:
    - formal P1 canonical patch drafting
    - primitive register split
    - field-level schema extraction
```

### 54.5 Accepted document-level rule after v2.0

```text
This file is now stable as a non-canonical active design log under the current v4 plan.
Future work should either:
1. draft a bounded canonical patch proposal from P1,
2. split the file when implementation-level schemas are needed, or
3. start a new research cycle with its own maintenance cadence.

Do not keep adding document-only optimization passes unless new content changes the primitive families or promotion queue.
```

---

## 55. Final document status v2.2

> purpose: single authoritative status block at the end of the file.
> supersedes the historical v2.0 closeout status (former § 55) and the
> v2.1 pass-10 self-review (former § 56). Both removed in v2.2 because
> 0.14 + 0.15 already carry the operative decisions; keeping duplicate
> status sections at the end created authority confusion at file tail.

```yaml
final_document_status:
  version: v2.2
  status: stable_single_file_active_design_log_with_P1_handoff_ready_and_review_fixes_applied
  latest_content_round: R16_M-V_Curiosity_as_Learnable_KL_Frontier
  latest_document_review: external_reviewer_feedback_v2_2

  v4_content_import_status: complete_for_current_plan
  document_only_rounds_remaining_if_no_new_content: 0
  canonical_truth_changed: false
  promoted_kernels: none
  promoted_primitives: none

  changes_in_v2_2:
    - added top-of-file TL;DR block
    - unified kernel status naming: accepted_kernel | candidate_kernel
    - replaced ~95-item active_accepted_candidates flat list with reference to 0.7
    - candidate_1 target_surface now points to real files
      (02_packets/review_packet.v0.yaml, 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md)
    - 0.14 recommended_P1_order item 1 synced with same real-file targets
    - added 0.14 p1_exit_criteria
    - added 0.15.1 filled example (P1-001) as drafter starting point
    - folded D8/D14/D15/D16/D17 fixed_in_* debts under historical_fixed_debts
    - removed former § 55 (v2.0 closeout status) and § 56 (pass-10 self-review)

  next_best_step:
    action: draft canonical proposal packet P1-001
    first_candidate: residual_first_report_minimum_shape
    primary_target_file: 02_packets/review_packet.v0.yaml
    secondary_target_file: 02_packets/PACKET-FIELD-DICTIONARY.v0.en.md
    starting_point: § 0.15.1 filled example
    do_not:
      - reopen v4 research
      - batch-promote all candidates
      - split this file before P1-001 patch shape is known
      - treat this active log as canonical truth
```

v2.2 decision:

```text
The active design log is fixed for review feedback. Reading paths are stable.
The correct next move is to draft canonical proposal packet P1-001 for
residual_first_report_minimum_shape, using § 0.15.1 as starting point.
Proposal must pass change-impact review and human approval gate before
any change is applied to 02_packets/review_packet.v0.yaml.
```
