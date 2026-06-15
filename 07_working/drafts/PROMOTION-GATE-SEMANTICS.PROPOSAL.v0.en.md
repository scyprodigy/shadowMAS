# PROMOTION-GATE-SEMANTICS.PROPOSAL.v0.en | proposal: minimum T4->T3 promotion gate semantics for memory candidates
# related: [GOVERNANCE-MATRIX, MEMORY-PLANE-HARNESS, deferred_state_inventory, memory_compiled_surface_discipline, check_memory_validity, check_packet_refs]
# phase: proposal_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before this becomes truth and before any artifact is placed in 03_memory/shared_memory/
> this specifies a gate; it does not itself promote anything

# Minimum T4->T3 Promotion Gate Semantics

## Why this exists
`deferred_state_inventory.md` blocks placing any artifact in
`03_memory/shared_memory/` until "promotion gate semantics must be specified".
CURRENT-TRUTH lists "final promotion gate semantics" under Still Not Final.
A real candidate now exists (`memory_compiled_surface_discipline.v0.yaml`,
status `candidate`, `promotion_candidate: yes`) and cannot move without this
spec. This proposal supplies the minimum gate so the first promotion is a
mechanical, reviewable act rather than an ad-hoc decision.

## Scope
- In scope: `T4 -> T3` only — an execution-feed memory candidate becoming
  approved shared memory (`status: approved_shared`).
- Out of scope: `T3 -> T2` (shared memory to canonical truth) keeps its
  existing stronger, human-only gate per GOVERNANCE-MATRIX; automatic or
  agent-initiated promotion; any promotion that bypasses human/delegated
  authority.

## Eligibility preconditions (mechanical)
A `memory_packet` is promotion-eligible only if ALL hold. These are
machine-checkable and intended to back a future `check_promotion_eligibility`
tool:

1. `packet_type: memory_packet` and `schema_version: v0`; passes
   `05_scripts/validate/shadowmas_validate.py`.
2. `promotion_candidate: "yes"`.
3. `status` is `candidate` (not `captured`, `draft`, `stale`,
   `broken_reference`, `rejected`, `superseded`, or `archived`).
4. `source_refs` is non-empty and every cited path resolves
   (`tools/check_packet_refs.py` clean for this packet).
5. `invalidation_triggers` is non-empty.
6. No `broken_reference` or `stale` finding from
   `tools/check_memory_validity.py`.
7. `confidence` is present; a low value does not block but must be visible to
   the reviewer (confidence is evidence, not authority).

Passing all seven makes a candidate *eligible for review*. Eligibility is not
approval.

## The promotion act
1. A `review_packet` references the candidate (`source_refs` with
   `relation: reviews`) and carries a `promotion_snapshot` over the candidate's
   `source_refs` paths, so source drift between review and placement is
   detectable.
2. A human, or delegated decision authority within an explicit owner grant,
   records the decision. Self-promotion by an automated worker without that
   grant is forbidden.
3. On approval: the candidate's `status` becomes `approved_shared`, and the
   artifact is placed at `03_memory/shared_memory/<name>.v0.yaml`. The review
   packet is retained as the promotion evidence.
4. Before placement, the `promotion_snapshot` is re-compared to current source
   state; a mismatch forces re-review (the same TOCTOU discipline already used
   for truth changes).

## After placement
- The placed artifact remains subject to `tools/check_memory_validity.py`; the
  ghost-dependency rule (MEMORY-PLANE-HARNESS) applies unchanged. Source
  invalidation marks it `stale`/`broken_reference` and pauses reuse.
- `approved_shared` is still below canonical truth. It may inform planning and
  review but must not be cited as `T2` truth.
- A registry entry (in the existing candidate/file-status registries) records
  the promotion outcome.

## Explicitly still deferred
- automatic or scheduled promotion (human/delegated act only for v0)
- `T3 -> T2` promotion semantics
- a `check_promotion_eligibility` tool implementing the seven preconditions
  (the natural next mechanical step once this spec is reviewed)
- shared-memory retention, naming, and indexing policy beyond single-file
  placement

## Promotion path of this proposal
This is a non-canonical working proposal. It unblocks nothing by itself.
Sequence: owner review of this spec -> (optionally) implement
`check_promotion_eligibility` -> author the first promotion review packet for
`memory_compiled_surface_discipline` -> first `03_memory/shared_memory/`
placement. Each step is separate and human-gated.
