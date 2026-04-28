> status: working draft / gap board
> authority: none
> not canonical truth
> not packet schema law
> not memory registry law
> not runtime implementation
> not a validator or CI task
> source basis: MAS_PACKET_SCHEMA_V0.yaml and shadowMAS_old_branch_disposition.md

# LEGACY-PACKET-MEMORY-GAP-BOARD.v0

## Purpose
Preserve still-useful packet, memory, and lifecycle details from the old shadowMAS schema branch as future patch candidates.

This board does not treat `MAS_PACKET_SCHEMA_V0.yaml` as current truth. It records what has already been absorbed, what may still deserve later small patches, and which old vocabulary should not be carried forward.

## Already Absorbed / Safe To Stop Tracking As Raw Legacy
- T/L/R separation appears to be represented in current shadowMAS vocabulary through the current truth and governance matrix.
- Minimum packet families appear to be represented: `task_packet`, `memory_packet`, and `review_packet`.
- YAML, `snake_case`, `source_refs`, `artifact_refs`, and basic `handoff` direction appear to be represented in the packet dictionary and packet YAMLs.
- Memory is not truth, cache is not authority, retrieval does not arbitrate truth, and promotion gates appear to be represented in current truth, governance, and memory harness text.
- No blind traversal and no giant prompt appear to be represented as current core principles.

## Candidate Future Patch: Risk Dimensions
Old detail:
- `truth_impact`
- `blast_radius`
- `dependency_risk`
- `recovery_cost`

Current status:
- The concepts exist in current truth direction as risk dimensions.
- The current shared packet shell has `risk` as a tier field, but the four dimensions are not yet packet-level machine fields.

Candidate future shape:
- `risk_tier`
- `risk_profile.truth_impact`
- `risk_profile.blast_radius`
- `risk_profile.dependency_risk`
- `risk_profile.recovery_cost`

Risks of adopting too early:
- scoring may become false precision
- packet authors may fill numbers mechanically without review discipline
- validators may enforce immature semantics
- risk tier and risk profile may drift if their relationship is not governed

Likely target files for later patch:
- `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md`
- `02_packets/packet_common_shell.v0.yaml`
- `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` only if the baseline meaning changes

Do not implement now.

## Candidate Future Patch: task_packet Execution Controls
Old details and current classification:

| Old detail | Classification | Notes |
|---|---|---|
| `why_now` | likely useful | A related optional task-context shape appears to exist; future work may refine review expectations. |
| `required_context` | likely useful | A related `inputs` shape appears to exist; preserve as blocking-context concept. |
| `optional_context` | likely useful | A related `inputs` shape appears to exist; preserve as non-blocking useful context. |
| `preferred_worker` | maybe defer | A related `worker_plan` shape appears to exist; avoid hard-coding old worker roles. |
| `fallback_worker` | maybe defer | A related `worker_plan` shape appears to exist; useful only if worker naming is governed. |
| `allow_fanout` | likely useful | A related shape appears to exist; future semantics should define when fanout is allowed. |
| `fanout_limit` | likely useful | A related shape appears to exist; future semantics should prevent uncontrolled parallelism. |
| `retry_limit` | likely useful | A related shape appears to exist; future semantics should align with R-layer retry policy. |
| `blocked_policy` / `on_blocked.action` | likely useful | A related `on_blocked.action` shape appears to exist; naming should not be changed casually. |
| `next_allowed_work` | likely useful | A related `on_blocked` shape appears to exist; preserve constrained-progress meaning. |
| `deliverables` | likely useful | A related shape appears to exist; overlaps with `expected_outputs` and may need future boundary clarification. |

Do not add fields now. The future patch, if any, should refine semantics and duplication boundaries rather than copy the old schema wholesale.

## Candidate Future Patch: Memory Validity / Invalidation Detail
Old details:
- `validity_scope`
- `applies_to.modules`
- `applies_to.task_types`
- `review_after`
- `source_hashes`
- `approved_shared`, `stale`, `broken_reference`, `superseded`, and `archived` style states

Appears covered:
- `memory_packet.v0.yaml` appears to have `validity.applies_to`, `validity.review_after`, `invalidation.current_state`, and `invalidation.source_hashes` as optional shapes.
- `memory_packet.v0.yaml` appears to distinguish `approved_shared`, `stale`, `broken_reference`, `superseded`, and `archived`.
- `MEMORY-PLANE-HARNESS.v0.en.md` appears to explain memory is not truth, invalidation triggers, reuse-safety metadata, and status/invalidation boundaries.
- The file-status registry appears to define related status semantics for reusable artifacts.

Useful future refinement:
- decide whether `validity_scope` should be a named field or remain expressed by `validity.applies_to`
- define when source hashes are expected versus optional
- clarify how memory packet status, registry status, and invalidation snapshot should align in reports

Do not copy blindly:
- old rigid `memory_kind` and `memory_scope` enums
- old lifecycle labels without reconciling registry semantics
- hash fields as proof of truth or approval

## Candidate Future Patch: Review Next-Step Routing
Old details:
- `next_if_approved`
- `next_if_rejected`
- structured `changed_files`
- structured `commits`
- structured `behavior_change`
- `risk_summary.key_risks`

Current status:
- `review_packet.v0.yaml` currently keeps review compact and human-readable.
- `change_summary` and `risk_summary` are strings, not structured blocks.
- `recommendation` remains advisory and does not replace human authority.

Why useful:
- helps mergeback and human review pipelines continue after a decision
- makes next steps inspectable instead of buried in prose
- can reduce repeated handoff ambiguity

Boundary:
- not full `review_packet` schema law yet
- should be reconciled with current fast-review work before implementation
- do not add fields now

## Candidate Future Patch: Ghost Dependency Rule
Old concept:
- deleted or superseded files must not remain active through old memory, stale index entries, old summaries, or broken references

Why it matters:
- prevents cached or summarized material from pretending removed or superseded sources remain valid
- keeps memory and retrieval below truth authority
- protects later agents from silently trusting stale continuity artifacts

Current status:
- The memory harness appears to contain a direct Ghost Dependency Rule.
- The registry appears to have review rules for source changed, deleted, moved, renamed, superseded, stale, broken_reference, superseded, and archived behavior.

Likely target files if later refinement is still needed:
- `03_memory/MEMORY-PLANE-HARNESS.v0.en.md`
- `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
- future invalidation policy if created

Do not implement now. Treat this as likely represented, with future patches limited to clarifying reports or automation boundaries.

## Candidate Future Patch: T2 Lifecycle Semantics
Old lifecycle ideas:
- `draft`
- `approved`
- `effective`
- `superseded`
- `deprecated`
- `rejected`

Current registry comparison:
- `working_draft` covers draft-like non-authoritative work.
- `truth_candidate` covers pending review.
- `approved_truth` covers approved canonical truth.
- `superseded` and `archived` exist.
- `stale` and `broken_reference` cover source-condition problems.
- `deprecated` and `effective` are not currently first-class registry statuses.

Preserve as lifecycle-semantics candidate:
- decide whether `effective` is needed beyond `approved_truth`
- decide whether `deprecated` is a status, metadata flag, or transition note
- decide how rejection differs between packet status, memory status, and file-status registry entries

Do not rename current registry statuses now.

## Deprecated Old Vocabulary / Do Not Carry Forward
- `O-stack` is old naming; current vocabulary is `L-layer`.
- `decisioner`, `coder`, `reviewer`, `mergeback`, `runtime`, `indexer`, and `retriever` old role enum should not become a canonical enum.
- Old read order should not override the current intake pack or runtime loading map.
- Rigid `memory_kind` and `memory_scope` enums should remain reference vocabulary only unless later validated.

## Future Patch Queue

| Order | Queue item | Candidate target file(s) | Why it matters | Blocked by what decision | Safe to patch independently? |
|---|---|---|---|---|---|
| 1 | risk dimensions decision | `02_packets/PACKET-FIELD-DICTIONARY.v0.en.md`, `02_packets/packet_common_shell.v0.yaml` | separates risk tier from risk profile | scoring semantics and tier/profile relationship | Yes, if packet versioning review is included. |
| 2 | task_packet execution controls decision | `02_packets/task_packet.v0.yaml`, packet dictionary | current fields exist but may need clearer semantics | worker naming, fanout, retry, and deliverable boundaries | Yes, mostly semantic refinement. |
| 3 | memory validity / source hash decision | `02_packets/memory_packet.v0.yaml`, `03_memory/MEMORY-PLANE-HARNESS.v0.en.md` | improves reuse safety and drift detection | hash expectation policy and status/invalidation alignment | Yes, if memory and packet surfaces are reviewed together. |
| 4 | review next-step routing decision | `02_packets/review_packet.v0.yaml`, fast-review drafts if still active | supports mergeback and human review continuation | fast-review reconciliation and desired structured shape | Yes, after fast-review alignment. |
| 5 | ghost dependency rule | `03_memory/MEMORY-PLANE-HARNESS.v0.en.md`, registry, future invalidation policy | prevents stale memory/index/summary authority leakage | whether more formal invalidation policy is needed | Yes, but a related rule appears to be represented. |
| 6 | T2 lifecycle semantics | registry, governance matrix, change impact map if meaning changes | clarifies truth lifecycle transitions | whether `effective` and `deprecated` are statuses, flags, or notes | No, likely touches status semantics and needs broader review. |

## Do Not Promote Yet
This board is working evidence only. It exists to retire raw legacy files safely by preserving unresolved details as inspectable future patch candidates.

No canonical truth, packet schema, memory registry, validator, CI, or runtime behavior is changed by this board.
