> status: working-area intake rule
> authority: 07_working/drafts intake handling only
> scope: 07_working/drafts/
> not canonical truth
> not packet schema
> not runtime contract
> not product specification
> not a promotion rule by itself
> do not treat as canonical top truth

# DRAFT-ENTRY-RULE.v0

## Purpose
Define what may enter `07_working/drafts/`, what should stay external or archive-only, and what should skip drafts because it is ready for a formal patch.

This rule prevents `07_working/drafts/` from becoming a junk drawer, scratchpad pile, or literature warehouse.

## Scope
This rule governs intake into `07_working/drafts/` only.

It applies to:
- working drafts
- bounded research memos
- bounded rationale candidates
- draft support bundles with clear source basis
- source-evidence files likely to be reused by later sessions
- future formalization candidates that are not ready for direct patching

## Non-Scope
This rule does not:
- redefine `01_truth/` canonical content
- create or change packet schemas
- define runtime contracts
- define product specifications
- change registry status or authority semantics
- create an ADR system
- create validators or CI
- decide promotion into T3 or T2 truth
- act as a promotion rule by itself

## Entry Criteria
An artifact may enter `07_working/drafts/` when most of the following are true:
When criteria are mixed, prefer not entering drafts unless a human/head decision marks the artifact as reusable draft support.

- The topic is single and well-bounded.
- The artifact has become a reusable memo, not scattered notes.
- The artifact explicitly marks itself as non-canonical unless separately promoted.
- The artifact has source support, companion references, or clear provenance when external claims matter.
- The artifact is likely to be cited or reused by later sessions.
- The artifact preserves high-value reasoning that would otherwise be lost.

## Do Not Enter Drafts
Do not place these in `07_working/drafts/` by default:
- One-off links or scattered session residue.
- Lesson queue items that still need routing.
- Unfiltered research dumps.
- Giant literature warehouses.
- Artifacts that are already ready for a narrow formal patch.
- Temporary notes without problem restatement or reusable conclusion.
- Duplicate copies of canonical truth files.
- Product-repo domain material unless clearly marked as external evidence or draft support.

## Ready for Formal Patch
If an artifact is already small, stable, bounded, and directly patchable into an owner file, do not park it in drafts by default.

Prefer a narrow formal patch over creating another draft when the owner file and change boundary are clear.

## Minimum Useful Draft Package
A draft package should include:
- a human-readable memo
- companion references when external sources matter
- an explicit boundary or status note
- an unresolved / not-yet-canonical section where needed

## Draft Header Requirements
Every draft should state:
- status
- authority or lack of authority
- source lane or source basis when relevant
- promotion requirements or do-not-promote reason when relevant

## Source Support Requirements
Drafts should preserve enough support for later sessions to inspect why the draft exists.

Acceptable support includes:
- source file paths
- source archive names
- citations or URLs
- claim/support notes
- provenance notes
- explicit source-evidence headers

External research should be distilled into claims, principles, or bounded findings before it enters drafts. Raw source piles should stay external, temporary, or archive-only until shaped.

## Retention and Cleanup
Retain drafts while they are likely to support future review, comparison, or formalization.

Clean up or archive drafts when:
- their owner file has absorbed the useful rule
- they are superseded by a later draft or formal patch
- they are no longer reusable
- they lack source support and cannot be repaired

Do not delete source evidence that is still needed for provenance.

## Promotion Boundary
Draft presence does not equal approval.

Draft usefulness does not equal truth.

Drafts may be design discussion input, rationale support, or future formalization candidates.

Drafts are not approved truth.

Drafts may support later T3/T2 review but do not bypass promotion gates.

External research may inform shadowMAS but must be distilled before promotion.

## Open Decisions
- final archive policy for old drafts
- whether draft intake needs a machine-readable index
- whether references files need a stricter schema
- how to mark a draft as fully absorbed without deleting provenance

## Change Impact
This rule governs `07_working/drafts/` intake only.

It does not redefine `01_truth` canonical content.

If future changes alter file-status or truth-status semantics, review the registry and Change Impact Map.
