# DECISION-review-brief-primary-direction.v0.en | decision record: primary direction is a task-scoped pre-sign-off review brief; rejection-knowledge surfacing is the first input wedge
# related: [SHADOWMAS-TARGET-TRUTH, SHADOWMAS-POSITIONING-STATEMENT, RATIONALE-attention-budget-review, REJECTION-KNOWLEDGE-DIRECTION, external_paradigm_references, deferred_state_inventory, rationale_index]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> this record fixes a product-direction decision for tool-layer work; it does not modify canonical truth
> canonical-truth or packet-schema changes derived from this direction require their own review packets

# Decision

The primary product direction for shadowMAS tool-layer work is a
**task-scoped pre-sign-off review brief**: a local-first, read-only,
one-screen compilation that a human consults before signing off on
AI-assisted work. It surfaces, for the task at hand only:

- prior rejections and their reopen conditions
- prior lessons and outcomes of similar past decisions
- staleness or breakage of cited evidence (ghost dependencies)
- risk, reversibility, and rollback path
- a bounded, typed check list
- coverage limits of the compilation itself

The first shipped input feed (wedge) is **rejection-knowledge
surfacing**: stop agents and humans from re-proposing what was already
rejected, by matching the task scope against recorded rejection,
decision, deferral, and lesson records.

A sign-off receipt (one terminal `review_packet` using the existing v0
schema, statuses, and fields) is a by-product of the flow, never the
pitch. No fourth packet family is introduced.

# Positioning basis

As agent output volume grows, the scarce resource in AI-assisted work
is human review attention, not generation capacity. Existing tooling
concentrates on the moments after work happens (capture, attribution,
attestation, compliance logs) or on write-time enforcement. The moment
before the accountable human decides is unoccupied among the verified
neighbors listed below (a bounded claim, not a market survey). shadowMAS already
owns the vocabulary and primitives for that moment: risk-ordered review
agendas, reading-cost estimates, rejection records with reopen
conditions, ghost-dependency validity checks, and promotion gates.

The goal is not faster review; undifferentiated acceleration worsens
rubber-stamping. The goal is routing scarce attention to what only a
human can judge, and absorbing the rest through structure and
reversibility.

# Prior-art map (synthesis discipline: one-sentence diffs)

- Mneme (https://mnemehq.com/, https://github.com/MnemeHQ/mneme):
  compiles ADRs into constraints and blocks violating agent edits at
  write time. Diff: the review brief is read-only and pre-decision; it
  informs the accountable human instead of blocking the agent, covers
  rejections/lessons/staleness beyond code edits, and never enforces.
  Closest live neighbor; strongest three-year threat.
- Handprint (https://handprint.sh/): extracts and cryptographically
  signs human decisions from agent-session transcripts. Diff: Handprint
  records decisions after they happen; the brief prepares the decision
  before it happens and treats the receipt as a by-product.
- AIR Blackbox (https://airblackbox.ai/) and Runfile
  (https://runfile.ai/): tamper-evident capture and compliance
  attestation layers. Diff: capture layers record what the agent did;
  the brief compiles what the human needs to know to decide.
- Cursor Agent-Trace (https://github.com/cursor/agent-trace): open
  attribution format for AI-generated code at file/line granularity.
  Diff: attribution answers "who wrote this"; the brief answers "what
  must I check before approving this." Complementary, not competing.
- ContextOS (https://contextosai.com/): enterprise decision runtime
  with sealed DecisionRecords. Diff: enterprise runtime tier; the brief
  is personal-scale, vendor-neutral, and runs with no platform.
- HARP (https://harp-protocol.github.io/): draft out-of-band human
  authorization protocol. Diff: HARP transports an approval; the brief
  prepares its content. Potential future interop, not competition.
- mcp-adr-analysis-server
  (https://github.com/tosin2013/mcp-adr-analysis-server) and
  MCP-as-a-Judge (https://github.com/OtherVibes/mcp-as-a-judge):
  ADR analysis and LLM evaluation gates inside agent sessions. Diff:
  both add model judgment into the loop; the brief adds curated,
  deterministic evidence for the human's judgment and keeps model
  recommendations advisory and last.

Demand evidence: an empirical study of AI-authored pull requests found
61.38% received no recorded review activity and human involvement
shifting from evaluation to agent-steering
(https://arxiv.org/html/2605.02273v1). Review-quality limits
(~400 LOC, 60-90 minute sessions) are long-established
(https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/).
Regulatory timing note: the Digital Omnibus on AI deferring EU AI Act
high-risk obligations (Annex III to 2027-12-02, Annex I embedded
systems to 2028-08-02) is in force as Regulation (EU) 2026/1744,
published in the Official Journal on 2026-07-24 and in force from
2026-07-27 (http://data.europa.eu/eli/reg/2026/1744/oj); it was
adopted by European Parliament vote on 2026-06-16
(https://www.europarl.europa.eu/news/en/press-room/20260611IPR45207/ai-act-ep-approves-simplification-measures-and-nudifier-app-ban)
and by Council final approval on 2026-06-29
(https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/).
This direction does not depend on compliance framing and must not be
marketed as a compliance, signing, or audit product.

# Defensible core

Three existing shadowMAS assets differentiate the brief from all
verified neighbors; if they do not measurably matter, the brief
collapses into reformatted constraint output and the direction should
be killed (see kill condition):

1. source validity: ghost-dependency and staleness checking
   (`tools/check_memory_validity.py`)
2. conditional rejection semantics: reopen conditions and
   anti-resurrection notes, not dead blocklists
   (`rejection_*.v0.yaml`, `tools/build_rework_guard.py`)
3. attention budgeting: risk-first ordering with visible reading cost
   (`tools/order_review_queue.py`)

# Design principles annex (rationale, not functional claims)

The brief's format decisions cite the following evidence-backed
principles. They justify design shape; they are not claims that
shadowMAS implements neuroscience or empirically improves oversight.

1. plan-structure: code comprehension engages domain-general executive
   networks rather than the language network, so the brief presents
   intent, invariants, and a delocalized-pieces map instead of prose
   narrative (https://anna-ivanova.net/publication/ivanova-2020-comprehension/;
   Soloway's delocalized-plans documentation work).
2. review-budget: defect detection collapses beyond roughly 400
   changed lines or 60-90 minutes; over-budget work is chunked and
   scheduled, never rendered as one large diff
   (https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/).
3. counter-evidence-first: explanations can increase overreliance, and
   evaluators favor confirming evidence; the brief renders evidence and
   disconfirmers first, asks for the human judgment, and reveals the
   compiler recommendation last (https://arxiv.org/abs/2102.09692;
   https://arxiv.org/abs/2507.19486).
4. honest-coverage: information foraging follows scent; a false "all
   clear" is the worst output, so a no-hit result must read "no hit
   within bounded coverage" with an explicit coverage manifest
   (Pirolli & Card, information foraging theory).
5. load-triage: cognitive load theory separates intrinsic, extraneous,
   and germane load; formatting overhead goes to zero, intrinsic load
   is chunked, judgment itself is preserved (Sweller).
6. reversibility-lever: recovery cost drives required review depth;
   rollback path is a mandatory brief field and irreversible actions
   escalate the risk tier (existing risk-dimension vocabulary).
7. relevance-selection: a line enters the brief only when its expected
   decision impact justifies its processing cost, and unevidenced
   statements do not enter at all (Grice's maxims; Sperber & Wilson,
   relevance theory).
8. feedback-restoration: expert intuition is reliable only with valid
   cues and fast feedback, both absent when reviewing AI output; the
   brief surfaces outcomes of similar past decisions where recorded
   (Klein and Kahneman, conditions for intuitive expertise).
9. checklist-limits: the checks section holds at most seven items,
   each typed DO-CONFIRM or READ-DO; longer checklists degrade
   compliance (Degani & Wiener 1993; Gawande).
10. review-mode-accounting: records distinguish direct human
    evaluation, agent steering, and automated checks, because these are
    empirically distinct behaviors and conflating them fabricates
    oversight (https://arxiv.org/html/2605.02273v1).

# Boundaries

- read-only tools; no product-repo writes; no daemons or watchers
- no blind full-repo traversal: bounded, task-scoped intake only
- no new packet family; receipt uses the existing `review_packet`
- recommendation stays advisory, separate from status, rendered last
- approval is never inferred from tests passing, agent text, command
  success, or session termination
- review-mode accounting lives in the brief artifact and in existing
  optional receipt fields (`tags` and `source_refs` relations), never as
  machine subgrammar inside human-facing free-text fields; the common
  shell's `signed_by` field stays unused until real cryptographic
  signing exists — no declaration-only signature metadata
- a review mode (`direct_human_evaluation`, `agent_steering`,
  `automated_check`) is recorded only when evidence supports it; an
  interactive terminal is an interaction channel, not authentication,
  and never justifies a human-evaluation claim by itself
- this direction does not unlock the deferred session-log plane or the
  personal-scale incident-reconstruction surface; the brief is
  pre-decision advisory material, not forensics
- no canonical-truth edits flow from this record without their own
  review packets

# Kill condition

Evaluate after roughly six months of dogfooding and at least 30
eligible sign-offs (risk r2_guarded and above). Kill the brief
direction if any two hold:

- under 40% of eligible sign-offs voluntarily consult the brief first
- under 10% of consulted briefs lead to an observable added check,
  revision, rejection, or reopening
- median compose-plus-triage overhead exceeds two minutes

Fallback if killed: ship rejection-knowledge surfacing alone as a
narrow task-scoped checker; abandon the broader brief-and-receipt
thesis.

# Reopen conditions

- the kill condition fires (fallback path above)
- a verified neighbor ships an equivalent pre-decision brief with
  validity tracking and conditional rejection semantics, removing the
  defensible core
- packet schema v1 work begins and supersedes the receipt mapping

# Anti-resurrection note

This record exists so future direction debates start from the recorded
elimination (enterprise governance, orchestration, memory
infrastructure, attribution formats, and capture layers were evaluated
and declined as occupied territory) instead of re-running the market
scan from scratch.
