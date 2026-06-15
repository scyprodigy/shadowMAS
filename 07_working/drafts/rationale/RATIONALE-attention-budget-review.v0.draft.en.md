# RATIONALE-attention-budget-review.v0.draft.en | direction draft: human attention as a budgeted, schedulable review resource
# related: [RATIONALE-calibrated-trust-gates, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, deferred_state_inventory]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before any schema, runtime, or claim use
> direction capture only; v0 ships no attention accounting

# Attention-Budgeted Review

## The gap
Review queues everywhere are first-in-first-out plus an instruction to
"review carefully." `RATIONALE-calibrated-trust-gates` already records
why that fails: attention degrades structurally with repetition, and
no instruction fixes it. The unexplored next step is to treat human
attention as a budgeted resource with explicit accounting, instead of
an assumed constant.

## Direction (not yet schema, not yet runtime)
- a review packet may later carry a predicted review cost (reading
  size, decision complexity, risk tier already exists)
- a review queue may later be scheduled against an attention budget
  rather than arrival order:
  - high-risk decisions surface when budget is fresh
  - low-risk items batch instead of interleaving
  - when budget is spent, the queue degrades visibly (defer, batch,
    escalate) instead of degrading silently into rubber-stamping
- supervision mode (`human_live_pair` / `human_available_delegate` /
  `human_away_autonomous`) is the existing control surface this would
  extend; it already encodes human availability, just not attention

## Evidence plan, not evidence
The review-card experiment (review-cost compression vs risk coverage,
`feat/dynamic-anchor-v2`) is the natural data source. Until it
produces numbers, this direction makes no empirical claim. Cognitive
load and vigilance-decrement literature motivate the design; they are
motivation, not proof that this implementation works.

## Why incumbents will not build this
Platform vendors optimize for engagement time, not for governing the
user's attention as a scarce resource the user owns. The misalignment
is structural, which is what makes a local-first, user-owned layer the
plausible home for attention accounting.

## What this draft does not claim
- no v0 capability claim; nothing in the current repo measures or
  schedules attention
- no claim of empirical human-oversight improvement (forbidden per
  AGENTS.md until evidence exists in-repo)
- no medical or neuroscientific authority claim

## v0 primitive (2026-06-12)
`tools/order_review_queue.py` implements the deterministic part of this
direction: pending review packets ordered by risk tier (high risk while
attention is fresh, low risk batched), with visible word-count reading
cost per item. It removes arrival-order randomness and makes cost
visible; it makes no attention or quality claim and does not schedule
against a measured budget.

## Promotion path
The empirical half stays blocked on data: the review-card experiment
must produce at least one measured compression/coverage result before
any budget-calibration field proposal. Then: candidate field sketch
under `07_working/`, governance review per change-impact rules before
anything touches `02_packets/`.
