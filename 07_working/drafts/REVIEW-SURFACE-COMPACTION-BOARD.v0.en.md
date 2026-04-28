> status: working draft / design board
> authority: none
> not canonical truth
> not packet schema law
> not runtime implementation
> not UI specification
> not renderer implementation
> not approval authority
> source basis: SHADOWMAS-REVIEW-SURFACE-COMPACTION-SUMMARY.v0.en.md and Shadowmas-fast-review-form-research-mergeback-notes

# REVIEW-SURFACE-COMPACTION-BOARD.v0

## Purpose
Preserve review-surface and fast-review compaction decisions as future patch candidates without expanding packet schemas or replacing human review authority.

This board records design direction only. It does not define packet law, implement a renderer, create a UI specification, or approve any review outcome.

## Review Surface Boundary
- Review surface compaction is a rendering / presentation discipline, not a new truth layer.
- Machine-side review evidence remains authoritative.
- Renderer output must not become source of truth.
- Human final authority remains separate from review packets, renderers, runtime adapters, and compaction tiers.
- This board does not implement renderer behavior.

## Source-Supported Direction / Not Yet Schema Law
- Review should be decision-first, not story-first.
- Review should be recognition-first, not recall-heavy.
- Chunking is essential.
- Progressive disclosure is useful but must not hide must-see information.
- Comparison support matters when decisions depend on state or alternative comparison.
- Narrative `change_summary` should not dominate the primary decision surface.
- `do_not_need_to_read` is a useful cognitive-load reducer.
- `acceptance_check_result` should usually stay near the review surface, but not necessarily in the first visible block.

## Balanced Fast-Review Candidate Baseline
This section records the current candidate structure. It is not `review_packet` schema law.

Four macro-chunks:
1. Review decision
2. What changed
3. Why it matters now
4. What blocks / conditions decision

Candidate primary fields:
- `decision_needed`
- `recommended_action`
- `change_units`
- `impact_surface`
- `why_you_are_seeing_this`
- `evidence_at_a_glance`
- `risk_summary`
- `unresolved_questions`
- `safe_to_approve_if`

Candidate secondary fields:
- `minimal_checks.must_read`
- `must_compare`
- `do_not_need_to_read`
- `acceptance_check_result`
- `source_basis_summary`

Expandable / deep materials:
- full rationale
- full source refs
- full artifact refs
- packet lineage
- rejected alternatives
- long history
- raw logs / raw notes / full patches

## Rendering Compaction Model

### Tier 0 - Decision line
- what is being reviewed
- recommended action
- headline risk
- scope touched

### Tier 1 - Compact evidence
- changed `truth_touchpoints`
- satisfied or violated `acceptance_criteria`
- `stop_condition` hits
- unresolved items
- promotion candidates if any

### Tier 2 - Raw evidence reference
- pointers only
- raw evidence opened only for spot-check, doubt, or audit

Rule:
Compaction may select and format machine evidence. It may not paraphrase facts into unverifiable prose.

## Anti-Bloat And Safety Rules
- Primary surface should remain four macro-chunks, not a flat long list.
- `change_units` should stay small and named.
- `unresolved_questions` should stay concrete and decision-relevant.
- `must_compare` should become structured comparison support, not a vague reminder.
- `do_not_need_to_read` should be preserved but not overload the primary view.
- Full rationale and raw logs belong below the primary path.
- `compaction_dropped` or equivalent transparency marker may be needed if information is intentionally omitted from first view.
- Renderer must not create approval outcome.

## Candidate Future Patch Queue

| Order | Queue item | Candidate target file(s) | Why it matters | Blocked by what decision | Safe to patch independently? |
|---|---|---|---|---|---|
| 1 | packet field dictionary review-field refinement audit | `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md`, `02_packets/review_packet.v0.yaml` | checks whether candidate fields duplicate or refine existing review vocabulary | whether review concepts need dictionary wording before schema changes | Yes, as audit only. |
| 2 | review_packet rendering-tier metadata decision | `02_packets/review_packet.v0.yaml`, future review-surface contract | decides whether Tier 0 / Tier 1 / Tier 2 needs machine-side metadata | whether rendering tier is schema metadata or renderer contract only | No, likely affects packet surface. |
| 3 | structured `must_compare` / `comparison_block` decision | `02_packets/review_packet.v0.yaml`, packet dictionary | turns comparison from reminder into recognition-first support | whether comparison support is field shape, renderer behavior, or both | Yes, after audit. |
| 4 | review surface compaction contract decision | future governance or runtime-adapter contract | prevents renderer drift without making render output truth | standalone contract vs embedded governance/runtime guidance | No, may affect runtime-adapter lane. |
| 5 | cognitive-burden principle promotion decision | current truth, governance matrix, human-facing rationale if needed | decides whether recognition-first guidance becomes cross-system principle | wording stability and promotion level | No, requires governance review. |
| 6 | human-facing review guide / rationale note decision | future human-facing rationale or guide | preserves research reasoning without bloating canonical files | whether rationale belongs in `06_human_docs/` or remains working draft | Yes, if non-canonical. |

## What Not To Do Yet
- Do not modify `review_packet` schema now.
- Do not add render-tier metadata now.
- Do not create renderer implementation.
- Do not create UI or GUI spec.
- Do not promote cognitive-burden principle into current truth now.
- Do not expand minimum required fields for `review_packet` now.
- Do not copy long research notes into canonical docs.

## External File Deletion Condition
After this board is committed and reviewed, the owner may delete:
- `SHADOWMAS-REVIEW-SURFACE-COMPACTION-SUMMARY.v0.en.md`
- `Shadowmas-fast-review-form-research-mergeback-notes.docx` or its text export

## Do Not Promote Yet
This board is working evidence only. It preserves source-supported review-surface decisions so later work can choose narrow patches, rationale notes, or no action.

No canonical truth, packet schema, review packet schema, registry, runtime file, UI, renderer, validator, CI, or implementation is changed by this board.
