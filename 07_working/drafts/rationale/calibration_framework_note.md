# calibration_framework_note | working rationale draft for treating calibration as a distribution, not a single number
# related: [rationale_evaluation_drift, active_design_log, MEMORY-PLANE-HARNESS, SHADOWMAS-CURRENT-TRUTH]
# phase: working_draft

> Status: working draft / source-evidence
> Authority: none
> Do not promote without governance review

# Calibration Framework Note

## Why this draft exists
shadowMAS currently handles uncertainty through two surfaces:

- `confidence` on `memory_packet` (a single 0.0–1.0 number)
- `invalidation_triggers` and `invalidation.current_state` for liveness

This is sufficient for routine reuse decisions but does not cover the
shape of model uncertainty that inference systems actually produce. The
gap was noted indirectly by `rationale_evaluation_drift.md`
(second-order evaluation drift) and by active design log §36.

## The gap, in one sentence
A single confidence number cannot distinguish:

- a model that is moderately sure across every plausible answer, and
- a model that is sharply sure of one wrong answer.

These two states often look identical at the field level but should
trigger different review treatment.

## Direction (not yet schema)
This note records intended direction, not a schema commitment.

- treat calibration as distributional metadata, not a scalar
- preferred carriers when present (future packet extension):
  - top-k candidates with their respective likelihoods
  - entropy or a low-cost distributional summary
  - reliability diagram bin or expected calibration error reference,
    when measurable
- distributional metadata MUST remain advisory and MUST NOT arbitrate
  authority or promotion

## Why advisory only
shadowMAS already enforces:

- retrieval hit is not approval
- relevance is not authority
- confidence is not promotion

Calibration metadata is the same shape of evidence. It improves the
quality of review but does not replace the human or governed promotion
gate.

## Relationship to existing surfaces
- complements `confidence` on `memory_packet`; does not replace it
- mirrors the existing `invalidation.source_hashes` pattern (evidence,
  not authority)
- maps cleanly onto inference systems whose native outputs are
  distributional (for example energy-based or latent-prediction
  systems), without committing shadowMAS to that class of system

## Scope this note does not cover
- exact packet field naming
- exact distributional summary format
- how to compute calibration at runtime
- which agents are responsible for emitting it

## Promotion path
This draft becomes a formal candidate only when:

- a concrete use case demands distributional review, and
- a packet schema proposal is drafted (likely as
  `02_packets/calibration_metadata.PROPOSAL.v0.yaml`), and
- governance review approves the proposal

Until then this file is rationale only.

## References
- `07_working/drafts/rationale/rationale_evaluation_drift.md`
- `07_working/archive/shadowmas_cross_domain_active_design_log_v_0_1_doc_optimized_v2_2.md` §36
- `03_memory/MEMORY-PLANE-HARNESS.v0.en.md` (retrieval and authority boundary)
- `04_runtime/LOCAL-MODEL-BASELINE.v0.en.md` (mxbai-embed-large baseline)
