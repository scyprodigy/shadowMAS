# PERSONALIZATION-MEMORY-ADAPTATION-CANDIDATE-LIFECYCLE-NOTE.v0.en.md | draft clarification note for memory and adaptation candidate lifecycle wording
# related: [PERSONALIZATION-ADAPTATION-READINESS-CONTRACT, MEMORY-PLANE-HARNESS, SHADOWMAS-CANDIDATE-REGISTRY, SHADOWMAS-LESSONS-QUEUE, PACKET-FIELD-DICTIONARY]
# phase: personalization_candidate_lifecycle_clarification_draft

# Personalization Memory / Adaptation Candidate Lifecycle Note v0 Draft

## Status

NON-CANONICAL DRAFT.

This is a clarification note only.
It is not implementation.
It is not a memory backend.
It is not learned personalization.
It is not approval authority.
It is not canonical truth.
It does not modify the existing personalization readiness contract.
It does not modify `01_truth/`, `02_packets/`, `03_memory/`, validators,
runtime behavior, tests, packet fixtures, or product repositories.

This draft requires owner review before any promotion or downstream update.

## Purpose

This note clarifies lifecycle wording around memory and adaptation candidates.

It exists because phrases such as "approved memory packet candidates" can be
misread as mixed lifecycle states. The word `approved` must not blur with the
word `candidate`. Future personalization, memory, packet, registry, and review
surfaces should use explicit lifecycle state names instead of ambiguous mixed
phrases.

## Core Clarification

Approved and candidate must remain separate lifecycle states.

A candidate is reviewable material, not approval.

An approved item is no longer merely a candidate for that exact lifecycle step.
It may still be a candidate for a later, stronger step, but that later target
must be stated explicitly.

A memory packet candidate can be accepted for review intake without being
approved as reusable memory.

A candidate can be accepted as evidence without being promoted to truth, memory,
authority, or runtime behavior.

Any approval wording must state approved_for_what.

## Suggested Lifecycle Vocabulary

| State | What it means | What it does not mean | Who or what may assign it | Human review required |
|---|---|---|---|---|
| `observed_signal` | A runtime, review, human correction, handoff, or task event was noticed as possible evidence. | Not evidence validation, not a candidate, not memory, not truth, not authority. | Runtime feed, agent report, human note, or audit surface may record it as observation. | Not always for recording; required before reuse or promotion. |
| `evidence_record` | The signal has been bounded, source-linked, and preserved as evidence for review. | Not approval, not reusable memory, not truth, not runtime behavior. | Human reviewer, scoped agent, validator, or registry process may prepare it if allowed by task scope. | Required before it can influence future behavior. |
| `candidate_for_review` | A bounded item is ready to be reviewed by a human or owner. | Not accepted, not approved, not promoted, not reusable guidance. | Candidate registry, review packet, or human-authorized draft process may assign it. | Yes, to move beyond candidate status. |
| `accepted_for_review` | A reviewer accepts the item into the review queue or review surface. | Not promoted to memory, not approved for reuse, not canonical truth. | Human reviewer or owner-approved intake gate. | Yes. |
| `approved_for_limited_use` | A human approves bounded use in a stated scope, such as one project, one task lane, or one review lane. | Not canonical truth, not broad shared memory, not runtime authority, not cross-project rule. | Human reviewer or owner within the declared scope. | Yes. |
| `promoted_to_memory` | A reviewed item becomes approved shared memory under the memory-plane rules. | Not canonical truth, not runtime authority, not product-repo write-back. | Human-approved memory promotion path. | Yes. |
| `promoted_to_canonical_truth` | A reviewed item becomes approved truth through the canonical truth promotion path. | Not automatic, not inferred from memory, not inferred from review status. | Human / owner canonical promotion path. | Yes, stronger review required. |
| `rejected` | The item must not be reused or reintroduced without new evidence. | Not deferred, not stale, not accepted for review. | Human reviewer, owner, or an approved fail-closed gate if one later exists. | Yes, unless a future approved gate explicitly rejects malformed input. |
| `stale` | The item may still be interpretable, but its source basis or scope changed and it requires re-review. | Not rejected, not active reusable memory, not current truth. | Invalidation process, human review, or future approved checker. | Yes before active reuse. |
| `invalidated` | The item must stop being treated as active because its source basis, scope, or safety condition no longer holds. | Not reusable memory, not live candidate, not approval. | Human reviewer, owner, or future approved invalidation process. | Yes for reactivation or replacement. |

## Memory / Adaptation Candidate Rules

- Repeated signal is evidence, not authority.
- Candidate registry is not approval.
- Lessons queue is not learned personalization.
- Memory plane harness is not memory backend.
- `accepted_for_review` is not `promoted_to_memory`.
- `approved_for_limited_use` is not canonical truth.
- `promoted_to_memory` is not runtime authority.
- `promoted_to_canonical_truth` requires a separate canonical promotion path.
- `evidence_record` may support review, but does not become memory by itself.
- `candidate_for_review` may be useful, but does not authorize reuse by itself.

## Forbidden Mixed Phrases

Avoid or rewrite:

- approved candidate
- approved memory candidate
- approved adaptation candidate
- candidate-approved memory
- reviewed truth candidate
- promoted candidate unless target is explicit

Safer replacements:

- `candidate_for_review`
- `accepted_for_review`
- `approved_for_limited_use`
- `promoted_to_memory`
- `promoted_to_canonical_truth`
- `rejected_candidate`
- `invalidated_candidate`

If using `promoted candidate` in prose, include the explicit target, for example
`candidate promoted_to_memory` or `candidate promoted_to_canonical_truth`.

## Claim Ceiling Rules

- Candidate-level wording cannot imply approval.
- Evidence-level wording cannot imply memory.
- Memory-level wording cannot imply canonical truth.
- Runtime wording cannot be inferred from memory or review status.
- Approval must always state approved_for_what.
- A review status is not a truth status unless a separate authority boundary
  says so.
- A memory status is not runtime permission.
- A candidate status is not a write-back permission.

## Examples

Valid examples:

- "This lesson is a candidate_for_review."
- "This pattern is accepted_for_review but not promoted_to_memory."
- "This memory packet is approved_for_limited_use in this project scope only."
- "This candidate is rejected because project truth changed."

Invalid examples:

- "This is an approved candidate."
- "This memory candidate is approved."
- "This review candidate is now truth."
- "This repeated signal should automatically become memory."

## Interaction With Personalization Readiness Contract

This note does not replace the personalization adaptation readiness contract.

Future schema work should use explicit lifecycle state names.

Future implementation must not infer lifecycle transitions from ambiguous
wording.

Owner / human review remains required for promotion.

If a future personalization or adaptation surface needs lifecycle fields, it
should preserve candidate, review acceptance, limited approval, memory
promotion, and canonical truth promotion as separate states.

## Non-Goals

This draft does not create or authorize:

- schema change
- memory store
- runtime behavior
- automatic promotion
- automatic personalization
- candidate registry implementation change
- lessons queue behavior change
- canonical truth update
- validator code
- personalization engine
- product-repo write-back

## Do Not Promote Yet

This remains draft because final lifecycle vocabulary, schema placement,
authority validation, memory backend behavior, and personalization implementation
boundaries are unresolved.
