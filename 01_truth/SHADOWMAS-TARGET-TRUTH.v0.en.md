# shadowmas_target_truth | north-star identity and long-term trajectory for shadowMAS
# related: [SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-PROMPT-LAYERING-CONTRACT, SHADOWMAS-CHANGE-IMPACT-MAP]
# phase: target_truth

# SHADOWMAS-TARGET-TRUTH.v0.en.md

## Purpose
This file describes what shadowMAS exists to grow toward.

It is the target / north-star truth. It is not a description of current
capability.

For what v0 can honestly do today, see
`01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`.

This file exists so that current v0 limitations are not mistaken for
shadowMAS's final identity, and so that future contributors, agents, and
reviewers can see the direction the project is being built toward.

## Target Identity
shadowMAS is designed to become an adaptive authority-bounded
cognitive-operation substrate for AI-assisted work.

It turns human intent, agent actions, reviews, memory candidates,
promotions, rollbacks, and handoffs into minimal inspectable packet IR.

## Core Target Sentence
shadowMAS v0 enforces representation invariants, not authority semantics;
but shadowMAS exists to grow an adaptive packet-IR shadow layer that
makes AI-assisted work reviewable, memory-aware, authority-bounded,
dynamically adaptive, and eventually delegably autonomous without
allowing automation to expand its own authority.

## Five Core Axes
shadowMAS's target identity has five core axes. None of them alone
captures the project; all five together describe it.

1. **packet IR** — AI-assisted work expressed as inspectable packets:
   task packets, review packets, memory candidates, promotions,
   rollbacks, handoffs, delegated envelopes. Packet is the
   intermediate representation, not a file format.

2. **authority boundary** — each packet makes explicit what it may
   touch, what counts as evidence versus durable consequence, who
   may approve, and what may not be silently promoted.

3. **dynamic adaptation** — shadow gradually grows a personalized
   and project-specific shadow state: which kinds of mistakes recur,
   which memories are reusable, which decisions require review,
   which review surfaces can be compressed for this user, team, or
   project. This is not a fixed workflow engine and not a DAG
   template.

4. **memory topology** — memory is layered semantically, not stored
   as chat history. Layers include preference, lesson, warning,
   project convention, canonical candidate, obsolete fact, and
   temporary workaround. The goal is to lower review cost and
   reduce repeated mistakes.

5. **delegated bounded autonomy** — automation may eventually
   decompose, execute, validate, rollback, summarize, and prepare
   promotion briefs inside an explicit delegated authority envelope.
   The envelope is human-granted and never self-expanded.

## Target Invariant
automation may operate inside a delegated authority envelope;
automation may not expand that envelope by itself.

## Adaptation Rule
Learned adaptation must remain layer-labeled:
preference, lesson, warning, project convention, canonical candidate,
obsolete fact, or temporary workaround.

Adaptation MUST NOT silently promote preference into truth.

This rule prevents the most common failure mode of self-adapting
systems: that learned patterns get promoted to laws.

## v0 vs Target Gap
v0 enforces representation invariants: packet shape, enum values,
required fields, status sets, version literal, recommendation enum,
and filename-major alignment.

v0 does not enforce authority semantics.

By axis:
- **axis 1 packet IR**: vocabulary and validators present; coverage
  matches v0 packet families (task, memory, review)
- **axis 2 authority boundary**: vocabulary present; enforcement
  primarily social and process-based (maintainer review, branch
  protection, path-scoped commits)
- **axis 3 dynamic adaptation**: **least developed**; LESSONS-QUEUE
  mechanism present but entries empty; CANDIDATE-REGISTRY is
  hand-registered, not learned; no personalization surface exists
- **axis 4 memory topology**: harness specified; three plane
  placeholders intentionally unimplemented in v0; SESSION-LOG-INTEGRITY
  spec drafted; no backend selected
- **axis 5 delegated bounded autonomy**: runtime directories
  scaffolded (`04_runtime/{inbox,packetized,...}/` all empty);
  handoff packet block exists; no runtime engine; runtime adapter
  drafts locked under `do_not_promote`

axis 3 dynamic adaptation is the weakest. It is also shadowMAS's
distinguishing niche. A reader who sees only axes 1, 2, and 4 may
mistake shadowMAS for a packetized governance protocol. The
intended identity is more.

## Trajectory Ladder
The target capability grows in this order. Each step assumes the
prior step exists.

1. shape representation
2. review compression
3. evidence-carrying packets
4. memory and promotion discipline
5. delegated execution envelopes
6. semantic authority checks
7. fail-closed policy gates
8. bounded autonomous orchestration

v0 is solid at steps 1–3, has vocabulary for step 4, has placeholders
for steps 5–8, and has no implementation of steps 6–8.

## Claim Boundary
A schema-valid packet is not necessarily authority-valid.

Validators enforce representation invariants, not authority semantics.

Advisory fields are evidence-carrying fields, not enforcement
mechanisms.

These three statements apply to current v0 capability and remain
true throughout the trajectory: even when fail-closed policy gates
are added, the gates check what they check, not everything.

## Non-Goals
shadowMAS is not, and is not designed to become:
- a vocabulary or naming convention only
- a packet format only
- a validator-only tool
- a memory database
- a LangGraph, CrewAI, AutoGen, or Dapr replacement
- a GitHub branch-protection wrapper
- a safety runtime in the sense of guaranteeing production safety
- an unbounded autonomous controller
- a system that may expand its own authority

The trajectory includes bounded autonomous orchestration (step 8 of
the ladder). That is bounded by the target invariant: automation
operates inside a delegated envelope and never expands it by itself.

## Relationship to CURRENT-TRUTH
`SHADOWMAS-CURRENT-TRUTH.v0.en.md` describes what v0 can honestly
do today.

This file (`SHADOWMAS-TARGET-TRUTH.v0.en.md`) describes what
shadowMAS exists to grow toward.

Both are required for honest description:
- mistaking CURRENT-TRUTH for the full identity under-claims shadowMAS
- mistaking TARGET-TRUTH for current capability over-claims shadowMAS

When current and target appear to conflict, both stay; the conflict
is the gap shadowMAS is working to close.

## Still Open
The following are intentionally open and refined as the trajectory
progresses:
- exact form of personalization (axis 3)
- exact memory-placement rules (axis 4)
- exact policy-gate language (ladder steps 6–7)
- exact delegated-envelope schema (ladder step 8)
- exact human-review compression surface
