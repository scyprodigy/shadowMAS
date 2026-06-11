# RATIONALE-calibrated-trust-gates.v0.draft.en | why deterministic checks exist: trust calibration, not sustained human attention
# related: [DECISION-no-covert-random-audit-v0, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-POSITIONING-STATEMENT, calibration_framework_note]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before any promotion or downstream change

# Calibrated Trust and Deterministic Gates

## Why this draft exists
shadowMAS keeps human review gates and deterministic validation checks side by
side. The reason is recorded nowhere as a single rationale; this draft captures
it so the design intent survives future sessions.

## Three trust failure modes
Human trust in delegated agent work fails in two opposite directions:

- **Under-trust**: the human re-verifies everything by hand. Delegation buys
  nothing; capacity is wasted and the operator burns out.
- **Over-trust**: the human approves without reading. The review gate still
  exists on paper but has become rubber-stamping; defects pass through a gate
  that everyone believes is working.
- **Calibrated trust**: the human knows which boundary the agent operates
  inside, verifies the boundary instead of every artifact, and spends attention
  only where machines cannot decide.

## Attention fatigue is structural, not a discipline problem
Repeated review of similar artifacts degrades human attention. Approval rates
that climb over time reflect declining scrutiny at least as much as rising
quality. No instruction to "review carefully" fixes this, because the failure
is produced by repetition itself.

Design consequence: any gate whose effectiveness depends on sustained human
attention will degrade with use. A gate design is only credible if it still
works at session 100, not just on day one.

## What shadowMAS does about it
- **Deterministic, visible checks carry the repetitive load.** Representation
  invariants (schema validity, fixture conformance, registry consistency,
  pollution patterns) are checked by machines that do not fatigue. These checks
  are deterministic and visible by design; v0 explicitly rejected covert or
  random sampling at solo scale (see
  `DECISION-no-covert-random-audit-v0.v0.en.md`).
- **Human attention is reserved for what machines cannot check.** Authority,
  promotion, truth elevation, and scope decisions stay human. The review
  surface is compressed (review_packet) so the human reads less, not more,
  per decision.
- **Schema validity never substitutes for authority validity.** Validators
  check representation, not authority semantics (see v0 Claim Boundary in
  `SHADOWMAS-CURRENT-TRUTH.v0.en.md`). A passing check earns reuse of machine
  effort, not human trust.

## Relationship to calibration_framework_note
`calibration_framework_note.md` is about a different calibration: the shape of
a model's confidence over its own outputs (distributional metadata on
memory_packet). This draft is about the human side: how the operator's trust
in delegated work should be allocated. Both are advisory surfaces; neither
arbitrates authority.

## What this draft does not claim
- no production-safety guarantee
- no runtime enforcement claim
- no quality-rate measurement claim
- no claim that current v0 checks cover all representation invariants

## Promotion path
Working-only rationale. Any use in `01_truth/`, `README.md`, or external-facing
material requires owner review and change-impact per
`SHADOWMAS-CURRENT-TRUTH.v0.en.md`.
