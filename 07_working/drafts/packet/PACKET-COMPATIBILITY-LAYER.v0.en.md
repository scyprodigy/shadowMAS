> status: working draft
> authority: none
> not canonical truth
> not runtime implementation
> not packet schema law unless later promoted through governance
> source basis: SHADOWMAS-RUNTIME-ADAPTER-MERGEBACK.v0.md

# PACKET-COMPATIBILITY-LAYER.v0

## Purpose
Define compatibility levels between native shadowMAS packets and non-native inputs.

This is a working draft, not canonical truth. It does not modify `01_truth/`, canonical `02_packets/`, `03_memory/`, or `04_runtime/`.

Runtime adapters adapt execution and do not redefine truth.

## Scope
- compatibility levels for intake and routing
- promotion permission by compatibility level
- loss and uncertainty handling
- relationship to canonical packet contract

## Non-Scope
- no replacement of canonical `02_packets` packet files
- no validator, CI, or YAML diff implementation
- no new canonical packet family
- no final packet storage location
- no full SemVer or version-governance edge-case resolution

## Compatibility Levels
Packet compatibility is not binary. It must preserve uncertainty and loss.
PC-levels are packet-compatibility maturity levels, not shadowMAS L-layer role/operation levels.

- `PC0 raw_intake_evidence`: raw chat/doc/output/source; no direct routing; no promotion.
- `PC1 adapter_wrapped_artifact`: raw source plus metadata; limited routing; no direct promotion.
- `PC2 packet_candidate`: normalized packet-shaped object; may route after review; no direct canonical promotion.
- `PC3 approved_packet`: reviewed packet; may route; promotion only through governed gate.

## Routing Permission by Level
- `PC0`: may be inspected by a human or adapter, but should not be routed as a task packet
- `PC1`: may be routed for normalization or review only
- `PC2`: may route after review confirms required fields and uncertainty notes
- `PC3`: may route as an approved packet within its declared scope

## Promotion Permission by Level
- `PC0`: no promotion
- `PC1`: no direct promotion; may become PC2 after normalization
- `PC2`: no direct canonical promotion; may be reviewed for approval
- `PC3`: promotion beyond packet handling still requires the governed truth gate

## Minimum Contract Elements
Each level record SHOULD include:
- `compatibility_level`
- `source_refs`
- `packet_family_target`
- `normalization_status`
- `confidence`
- `loss_notes`
- `unresolved_authority_claims`
- `routing_permission`
- `promotion_permission`
- `review_owner`

## Loss / Uncertainty Handling
- uncertainty must travel with the artifact
- loss notes must not be stripped during normalization
- missing required fields should block routing above PC1 unless reviewed
- inferred values should be marked as inferred
- adapter metadata must not override packet semantics

## Relationship to Canonical Packet Contract
Packet contract remains logical; YAML is the v0 default codec.

This draft does not replace canonical `02_packets` packet files.

Rules:
- canonical packet fields remain governed by `02_packets/`
- `packet_common_shell.PROPOSAL.v0.yaml` is proposal evidence only
- adapter-wrapped artifacts may point toward packet shape, but they are not approved packets
- compatibility levels describe intake maturity, not truth authority

## Rules
- MUST distinguish raw evidence from approved packets.
- SHOULD route the lowest sufficient level for review or normalization.
- MUST NOT promote PC0, PC1, or PC2 directly into canonical truth.
- MAY use PC2 candidates to prepare review packets when uncertainty is explicit.

## Open Decisions
- final packet compatibility schema
- exact storage path for PC1 and PC2 artifacts
- YAML compatibility diff implementation
- enum-addition and unknown-value handling
- relationship to future packet validators

## Promotion Requirements
Before promotion, this draft needs:
- human governance review
- reconciliation with canonical packet dictionary and schemas
- examples for all four levels
- decision on storage and lifecycle
- validator design review without implementing validators in this task

## Do Not Promote Yet
This remains draft because compatibility storage, validator behavior, and YAML diff rules are unresolved.
