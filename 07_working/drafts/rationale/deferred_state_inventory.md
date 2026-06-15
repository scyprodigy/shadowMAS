# deferred_state_inventory | working rationale listing intentionally-deferred shadowMAS surfaces with their unlock triggers
# related: [MEMORY-PLANE-HARNESS, SHADOWMAS-LESSONS-QUEUE, SHADOWMAS-TARGET-TRUTH, rationale_index]
# phase: working_draft

> Status: working draft / honest-deferral record
> Authority: none (records what is deferred and when to revisit; does not authorize implementation)
> Do not promote without authority-boundary review

# Deferred State Inventory

## Purpose
shadowMAS deliberately leaves several surfaces unimplemented in v0.
Without explicit unlock triggers, deferred items risk becoming
silently abandoned. This file lists each deferred surface, why it
is deferred, and what concrete event should cause the deferral to
be revisited.

This is honesty bookkeeping. It does not implement anything and does
not by itself authorize implementation.

## Memory plane placeholders
Three planes are declared by
`03_memory/MEMORY-PLANE-HARNESS.v0.en.md` and represented by
placeholder README files. Each is intentionally unimplemented in v0.

### `03_memory/session_log/`
- declared purpose: append-only session trace recording
- v0 state: placeholder README + `SESSION-LOG-INTEGRITY.v0.en.md`
  spec (Phase E of the 2026-05 audit cycle)
- unlock trigger: first concrete need to record a session trace
  across a session boundary, OR first request to audit a past
  session, OR first explicit feature requiring tamper-evidence
- implementation gate: the spec at SESSION-LOG-INTEGRITY must be
  reviewed and promoted before backend selection

### `03_memory/working_memory/`
- declared purpose: current task-critical active state
- v0 state: placeholder README only
- unlock trigger: first concrete agent workflow that needs
  cross-call state that does not fit in a packet or a session log
- implementation gate: must not become a backdoor to silently
  promote ephemeral state into shared memory

### `03_memory/shared_memory/`
- declared purpose: approved reusable memory below canonical truth
- v0 state: placeholder README only
- unlock trigger: first concrete reusable memory candidate that
  survives promotion review and needs a placement, OR first cross
  -agent reuse case
- implementation gate: promotion gate semantics must be specified
  before any artifact is placed here

## Runtime adapter drafts under lock
Five drafts under `07_working/drafts/runtime_adapter/` are locked by
`07_working/drafts/SHADOWMAS-LESSONS-QUEUE.v0.yaml` with the rationale
"runtime-adapter must not preempt version-governance lane". Each is
listed below with its declared unlock trigger.

### `AGENT-JOIN-CONTRACT.v0.en.md`
- declared purpose: contract for an agent dynamically joining
  shadowMAS
- lock reason: requires stable packet contract + delegated-envelope
  schema, neither of which is finalized
- unlock trigger: packet contract reaches `.v1` candidacy and a
  delegated-envelope schema is drafted

### `PROJECT-INTAKE-CONTRACT.v0.en.md`
- declared purpose: contract for an arbitrary project attaching to
  shadowMAS
- lock reason: requires the write-back automation contract, which is
  itself "Still Not Final" per CURRENT-TRUTH
- unlock trigger: write-back automation contract drafted

### `LEGACY-INTAKE-NORMALIZATION.v0.en.md`
- declared purpose: normalization of non-packet legacy inputs
- lock reason: depends on the packet compatibility layer which is
  still in proposal state
- unlock trigger: `PACKET-COMPATIBILITY-LAYER.v0.en.md` reaches
  approved status

### `RUNTIME-ADAPTER-CONTRACT.v0.en.md`
- declared purpose: general runtime adapter contract for Claude
  Code, Cursor, Codex, Ollama, hooks, skills
- lock reason: tool-specific adapter prompts have not stabilized;
  CURRENT-TRUTH lists runtime adapter contract as "Still Not Final"
- unlock trigger: at least one runtime adapter (e.g. Claude Code)
  has been operated under shadowMAS for one full release window with
  recorded lessons

### `PACKET-COMPATIBILITY-LAYER.v0.en.md`
- declared purpose: compatibility levels between native packets and
  non-native inputs
- lock reason: relates to legacy intake normalization which is also
  locked
- unlock trigger: a real legacy intake case appears and forces
  shape decisions

## Shared Core standalone source file
- declared purpose: one-page cross-project reusable behavior floor
  (Layer 1 of the prompt layering contract)
- v0 state: concept formalized; represented indirectly through
  CURRENT-TRUTH and QUICKREF; no dedicated file
- why deferred: content is stable but low-urgency; writing it is a
  new truth surface requiring governance review
- unlock trigger: first second-project adoption of shadowMAS rules,
  OR first runtime adapter that needs to compose Layer 1 separately

## Candidate registry split
- declared purpose: keep `SHADOWMAS-CANDIDATE-REGISTRY.v0.yaml`
  reviewable as it grows (currently ~105 KB, ~26 candidates in one
  hand-maintained YAML)
- v0 state: single file; `tools/check_candidate_registry.py` validates it
- why deferred: split or per-candidate files plus a compiled index is
  premature at current volume
- unlock trigger: registry exceeds 50 candidates OR 200 KB, OR a
  merge conflict occurs inside the registry file

## Shadow genealogy (cross-owner lesson import)
- declared purpose: let one person's lessons / memory packets be
  imported by another owner as downgraded candidates with forced
  re-validation, instead of inherited trust
- v0 state: import primitive exists (`tools/import_memory_candidate.py`:
  forced status downgrade, confidence cap, provenance, re-validation
  trigger); full exchange format and placement semantics remain deferred
- why deferred: solo scale has no second owner; designing import
  semantics without a real importer invites speculation
- unlock trigger: first real second human (collaborator or team
  member) wants to reuse this repo's lessons, OR a fork asks for a
  lesson-exchange format

## Personal-scale incident reconstruction (forensics surface)
- declared purpose: answer, from packet chains alone, "what did the
  agent see, under which truth version, and who approved it" after an
  agent-caused incident
- v0 state: reconstruction primitive exists
  (`tools/trace_packet_chain.py`: inbound referencers, outbound
  citations, cited-file existence from a packet_uid); the incident
  workflow and session-log assembly remain deferred
- why deferred: no incident has required it; building forensics
  before the first real reconstruction request risks designing for
  imagined incidents
- unlock trigger: first real incident where the owner needs to
  reconstruct an agent decision chain, OR external liability /
  accountability pressure reaches personal-scale agent work

## Other deferred surfaces tracked elsewhere
For completeness, these deferrals are tracked in their own files;
they are listed here only as cross-references.

| Surface | Tracked in |
|---|---|
| User/project adaptation profile implementation | `07_working/drafts/personalization/USER-PROJECT-ADAPTATION-PROFILE-SCHEMA.v0.en.md` ("Future Unlocks" + "Do Not Promote Yet") |
| History rewrite of personal email + third-party PII | `07_working/drafts/rationale/history_pollution_residual_risk.md` |
| Distributional calibration metadata | `07_working/drafts/rationale/calibration_framework_note.md` |
| Active design log P5 cluster extraction | `07_working/drafts/rationale/active_design_ledger.yaml` |
| Validator multi-version dispatch | `01_truth/SHADOWMAS-SCHEMA-VERSION-MIGRATION.v0.en.md` |
| R-layer runtime substrate | `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` "Still Not Final" |

## Discipline
A deferred surface must:

- exist in this inventory OR have its own deferral record
- name at least one concrete unlock trigger
- be reviewed at least once per significant audit cycle to confirm
  the deferral is still appropriate

If a deferred surface accumulates more than two cycles without any
review, the audit cycle owner should explicitly choose: promote it
to active work, or restate the deferral with updated trigger.

Silent deferral is forbidden. This file is the explicit record.

## Reconsideration triggers (global)
Even outside per-surface triggers, the entire inventory should be
revisited if:

- a release / public-hygiene milestone is scheduled
- shadowMAS adopts a `.v1` packet line (per
  `01_truth/SHADOWMAS-SCHEMA-VERSION-MIGRATION.v0.en.md`)
- a contributor or fork count crosses a threshold that materially
  raises the cost of deferred items
- legal, compliance, or partnership pressure forces a check

## Out of scope
This file does not:

- implement any deferred surface
- modify any canonical truth
- override the lock status declared in LESSONS-QUEUE entries
- specify timelines (only unlock triggers, not dates)
