> status: draft / source-evidence
> authority: none
> do not promote without governance review
> source lane: runtime-adapter missing contract drafts

# LEGACY-INTAKE-NORMALIZATION.v0

## Purpose
Define how non-packet history, chat, docs, screenshots, Claude/Cursor/Codex outputs, or pre-shadow work enters shadowMAS as evidence or candidate material.

This is a working draft, not canonical truth. It does not modify `01_truth/`, `02_packets/`, `03_memory/`, or `04_runtime/`.

Runtime adapters adapt execution and do not redefine truth.

## Scope
- legacy source capture
- evidence preservation
- packet-candidate conversion
- loss and uncertainty accounting
- authority-claim handling

## Non-Scope
- no automatic approval of legacy material
- no rewrite of legacy sources as if packet-native
- no OCR, screenshot parser, validator, CI, or hook implementation
- no canonical packet schema changes
- no product repo write-back

## Legacy Source Kinds
- chat transcripts
- ad hoc docs or notes
- screenshots
- Claude, Cursor, Codex, Ollama, or other agent outputs
- pre-shadow task history
- exported archives
- product repo artifacts used as evidence

## Minimum Legacy Intake Record
A draft record SHOULD include:
- `legacy_source_id`
- `source_kind`
- `source_path_or_location`
- `source_hash`
- `capture_time`
- `captured_by`
- `preservation_status`
- `extraction_method`
- `candidate_packet_family`
- `confidence`
- `loss_notes`
- `unresolved_authority_claims`
- `source_refs`
- `human_confirmation_required`

## Source Preservation
Original source preservation is required.

Rules:
- keep raw source available or document why it cannot be preserved
- do not delete source archives before governed confirmation
- preserve enough provenance to inspect conversion quality
- converted summaries do not replace original evidence

## Extraction / Conversion Rules
- non-packet material may enter shadowMAS as evidence or candidate, not approved truth
- converted packet candidates must carry confidence, loss notes, and unresolved authority claims
- do not rewrite legacy material as if it was packet-native from the beginning
- extraction SHOULD distinguish direct claims, inferred claims, and missing claims
- adapter wrapping SHOULD precede packet-candidate conversion when source context is weak

## Loss Accounting
Each conversion SHOULD state:
- what was omitted
- what was uncertain
- what was normalized
- what could not be verified
- whether original ordering, speaker identity, or artifact context was lost

## Authority Claims
Legacy source authority must be explicit.

Rules:
- a source saying "approved" is not enough unless the approval authority is traceable
- host-native output, cache, retrieval, and agent memory are not truth sources
- project-domain claims must be checked against project-local truth
- shadowMAS governance claims must be checked against shadowMAS truth layers

## Packet Candidate Conversion
Candidate output SHOULD identify:
- target packet family
- mapping from source fields to packet fields
- fields added during normalization
- fields left unknown
- confidence and loss notes
- required human confirmation

## Human Confirmation Requirements
Human confirmation is required when:
- source authority is ambiguous
- the conversion would influence promotion
- project business truth is inferred
- legacy material conflicts with canonical truth
- loss notes affect acceptance criteria or routing

## Rules
- MUST preserve original sources or record preservation failure.
- MUST NOT promote non-packet material directly into approved truth.
- SHOULD keep converted packet candidates inspectable.
- MAY use adapter-specific extraction aids only as draft support.

## Open Decisions
- final legacy intake record schema
- acceptable hash and archive policy
- screenshot and binary evidence handling
- confidence scale semantics
- where legacy intake records and converted candidates should live

## Promotion Requirements
Before promotion, this draft needs:
- human governance review
- examples from at least chat, doc, screenshot, and agent-output sources
- alignment with packet compatibility levels
- source preservation policy
- decision on storage location and lifecycle

## Do Not Promote Yet
This remains draft because conversion loss policy, confidence semantics, and legacy intake storage are unresolved.
