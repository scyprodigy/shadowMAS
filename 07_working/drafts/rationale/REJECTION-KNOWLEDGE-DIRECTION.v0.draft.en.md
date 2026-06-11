# REJECTION-KNOWLEDGE-DIRECTION.v0.draft.en | direction draft: rejected decisions as first-class, retrievable records
# related: [DECISION-no-covert-random-audit-v0, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, deferred_state_inventory, MEMORY-PLANE-HARNESS]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before any packet-family proposal or schema work
> direction capture only; v0 ships no rejection packet family

# Rejection Knowledge as a First-Class Record

## The gap
Memory systems record what was learned. Almost none record what was
rejected and why. The cost appears later: a rejected idea resurfaces
through retrieval, a new session, or a new agent, and is re-litigated
or re-built at the wrong scale because the rejection left no
structured trace.

shadowMAS already pays this cost down by hand. The repo contains
several rejection-shaped records, each in a different ad-hoc shape:

- `DECISION-no-covert-random-audit-v0.v0.en.md` — rejected claims
  ledger plus explicit reopen conditions
- `SHADOWMAS-CURRENT-TRUTH.v0.en.md` Technology Bias — "do not adopt
  early" list (DSPy, LangGraph, Letta, CrewAI, heavy orchestration)
- `SHADOWMAS-CURRENT-TRUTH.v0.en.md` WFGY Position — reference-only,
  explicitly not approved truth
- `SHADOWMAS-TARGET-TRUTH.v0.en.md` Non-Goals — identity-level
  rejections
- `history_pollution_residual_risk.md` — deferred-with-conditions
  decision record

## Candidate common shape
Extracted from the existing records, a unified rejection record needs
roughly these fields (names provisional, not a schema):

- `rejected_claim` — the idea, feature, or adoption being rejected
- `rejection_scope` — the scale or context in which the rejection
  holds (for example: solo scale, v0, this repo only)
- `rejection_reasons` — structured list; each reason should survive
  being read without the original conversation
- `reopen_conditions` — concrete conditions under which the rejection
  must be revisited; "never" must be stated explicitly, not implied
- `source_refs` — where the rejection was decided and recorded
- `anti_resurrection_note` — one line telling a future reader why
  this record exists at all

The strongest existing instance (`DECISION-no-covert-random-audit`)
already carries all six informally. That file is the reference
implementation of the shape.

## Why this fits shadowMAS
- It is authority-boundary work: a rejection is a decision artifact
  with scope and reopen conditions, exactly what packets express.
- It complements invalidation: invalidation says "this memory is no
  longer safe to reuse"; rejection says "this idea was evaluated and
  declined under these conditions." Different lifecycle, same
  discipline.
- It is cheap: the records already exist; only the shape is missing.
- Inhibitory knowledge is harder to retain than positive knowledge
  for humans and retrieval systems alike; a structured record is the
  countermeasure that does not depend on anyone's memory.

## What this draft does not claim
- no new packet family in v0
- no claim that existing memory products lack internal equivalents;
  the claim is only that no structured rejection surface exists in
  shadowMAS today and the raw material does
- no neuroscience or cognitive-science authority claim; the
  inhibitory-learning analogy is motivation, not evidence

## Paper simulation (2026-06-11)
Status: two strongly-shaped instances exist
(`DECISION-no-covert-random-audit-v0`, `DECISION-no-mass-filename-rename`).
The CURRENT-TRUTH "do not adopt early" list and WFGY position are
rejection-shaped but weakly shaped: they carry claim, scope, and reopen
direction, but not per-item reasons. "Strongly shaped" therefore means:
all six fields recoverable from the record without the original
conversation.

Rendering the newest instance through the candidate shape, as a paper
test only (not a schema, not a packet):

```yaml
rejected_claim: mass-rename existing files to a single naming convention
rejection_scope: all tracked layers; strongest in 07_working/drafts/**;
  single-file renames with concrete cause remain allowed
rejection_reasons:
  - references are load-bearing; mass rename maximizes blast radius for
    zero semantic gain
  - machine surfaces depend on existing prefixes (DECISION-* glob,
    test_* discovery)
  - git log --follow ergonomics degrade across the whole working area
  - apparent inconsistency is path-scoped policy, not accident
reopen_conditions:
  - filename policy memo promoted and grandfathering clause dropped
  - release milestone budgets a one-time normalization pass
  - atomic rename+reference-rewrite+regeneration tooling approved
source_refs:
  - 07_working/drafts/rationale/DECISION-no-mass-filename-rename.v0.en.md
  - 07_working/drafts/rationale/policy_filename_memo.md
anti_resurrection_note: a repo audit re-flagged sanctioned mixed naming
  as drift before reading the policy owner; this record absorbs that
  class of rework
```

Observations from the simulation: the shape holds; `rejection_scope`
wants to express both path scope and allowed exceptions, which suggests
scope may need two subfields (`applies_to`, `exceptions`) when a real
schema is drafted. No other field strained.

## Promotion path
1. Keep authoring new rejections in the current decision-record style.
2. When a third strongly-shaped instance exists, draft
   `rejection_record` as a candidate packet-family proposal under
   `07_working/` (not `02_packets/`).
3. Packet-family promotion requires governance review per
   `SHADOWMAS-CURRENT-TRUTH.v0.en.md` change-impact rules.
