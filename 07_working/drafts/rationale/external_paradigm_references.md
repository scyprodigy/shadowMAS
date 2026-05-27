# external_paradigm_references | working rationale capturing external frameworks, papers, and prior art that shadowMAS's existing distillation may have missed
# related: [calibration_framework_note, deferred_state_inventory, negative_audit_cycle_routine, rationale_index]
# phase: working_draft

> Status: working draft / external-reference capture
> Authority: none (rationale only; does not promote anything into canonical truth)
> Do not promote without authority-boundary review

# External Paradigm References

## Purpose
shadowMAS has been distilled across many sessions and multiple domains
in computer science, multi-agent governance, and packet protocol
design. This file captures external frameworks, papers, and prior art
that the distillation appears to have **missed** but could
meaningfully inform future shadowMAS design decisions.

It is rationale only. It does not modify canonical truth, packet
schemas, registries, or runtime. Adoption of any item here requires
its own atomic round with proper authority-boundary review.

## Synthesis Discipline (show your work)

shadowMAS is by design a synthesis layer. It deliberately ingests
ideas from many fields (multi-agent communication, legal theory,
formal verification, cognitive science, safety engineering,
governance, information-flow security, etc.) and re-combines them
at the authority-boundary layer. **Borrowing is the design intent,
not a problem.**

The failure mode this section guards against is not similarity to
prior art — it is **silent miss**: building something whose prior
art you did not know existed, or knew but did not document the
diff against.

### The line between synthesis and reinvention

| Situation | Verdict |
|---|---|
| Your mechanism resembles prior art + you know it + you wrote attribution + you can state the diff | synthesis ✓ |
| Your mechanism resembles prior art + you did not know prior art existed | reinvention ✗ |
| Your mechanism resembles prior art + you knew but did not document attribution or diff | silent miss ✗ (grey reinvention) |
| Your mechanism does not overlap any prior art that a serious search surfaces | genuinely novel ✓ (earned by search) |

### Three operational tests

**Test 1 — One-sentence diff.** For any shadowMAS mechanism that
plausibly overlaps a known external concept, the doc must contain
one sentence of the form "this differs from X by Y." If you cannot
write that sentence, you may not have known X existed.

**Test 2 — Attribution graph.** Each shadowMAS component should
have a traceable input graph showing which external concepts
contributed. A component sitting in isolation in that graph is a
flag — either genuinely novel (then earned by search) or silent
miss.

**Test 3 — Vocabulary economy.** When introducing a new term,
check whether a standardized term already covers the concept. Use
the standard term unless the diff is meaningful enough to justify
new vocabulary.

### Going forward

- Before proposing a new packet field, packet family, validator
  enum value, governance vocabulary, or runtime mechanism, **grep
  this file** (and search adjacent literature) for prior art.
- If prior art exists, the choice is "adopt with attribution",
  "adapt with attribution + one-sentence diff", or "refuse with
  explicit reason." Refusal is fine; silent miss is not.
- A "shadowMAS is genuinely original here" claim must survive at
  least one serious search round before being asserted.
- shadowMAS originality is not suppressed. A3 (geology unconformity)
  began as a "plausibly genuinely novel" claim, but a later
  recursive application of this discipline surfaced prior art in DB
  theory (tombstones, SQL NULL semantics) and the claim was
  downgraded to "novel application of an established pattern." See
  the A3 entry below for the one-sentence diff. The point is that
  "genuinely novel" must be **earned** by a prior-art check, not
  assumed by absence of prior reference.

### Concrete handles for the check

- grep this file for the topic keyword
- web search "field + concept + year"
- ask whether the same problem appears in: distributed systems,
  multi-agent communication, legal theory, formal verification,
  cognitive science, safety engineering, organizational theory,
  or information-flow security
- if nothing surfaces after a serious pass, record the claim of
  novelty with the search trail

## Categorization
- **A** Paradigm-level new lenses — would reframe TARGET-TRUTH axes
- **B** Axis fillers — concrete mechanism for shadowMAS's weakest axes
- **C** Mechanism prior art — shadowMAS appears to propose something
  already standardized elsewhere; reference for adopt-vs-reinvent decision
- **D** Defensive validations — academic support for shadowMAS's current
  design choices, especially counterfactual ones
- **E** Implementation menus — concrete options to consult when the
  corresponding trigger arrives

## Triage State

10 entries across 5 categories. Their applicability to active
shadowMAS work varies. Quick filter for "what to read first if
time is limited":

### Actively shaping (3) — high near-term yield
- **C1 Speech Act + FIPA ACL** — directly catches recommendation
  enum extensions and packet vocabulary debates; useful on the next
  packet-vocabulary change
- **A3 Geology unconformity (+ DB tombstones + SQL NULL semantics)**
  — concrete addition for session_log when it activates; design now
  rather than retrofit
- **D1 GSAR coherence trap** — academic insurance against drifting
  into agent self-correction without typed grounding

### Wait-on-trigger (3) — load when conditions arise
- **A2 SAFEFLOW IFC** — load when R-layer substrate is selected
- **B1 ALMA meta-learned memory** — load when axis 3 (dynamic
  adaptation) gets a concrete implementation effort
- **A1 Active Inference** — load when a "non-blocking governance"
  use case appears

### Library only (4) — kept for completeness, no current pull
- **C2 Common Law + CBR** — precedent registry mechanism; large
  effort, low near-term signal
- **E1 Jidoka + CRM** — multi-agent same-task safety; no such scope
  yet
- **E2 Sandbox substrates** — implementation menu for R-layer
- **E3 Watertight blast radius** — packet field mechanism; no
  evidence of wide-blast packet problem yet

Promotion between buckets is allowed without further review; just
update this section. Demotion to "remove" requires a one-line
reason recorded here.

---

## A. Paradigm-level new lenses

### A1. Active Inference / Free Energy Principle as governance dimension
- **Sources**: Friston et al., 2007–present; specifically
  arxiv 2412.10425 "Active Inference for Self-Organizing Multi-LLM Systems"
- **shadowMAS gap**: axis 2 (authority boundary) is currently 100%
  external constraint — T-layer rules + gates + validators + hooks.
  Nothing about shaping internal priors.
- **What it adds**: Active inference frames governance as "shift from
  external constraints toward internal modulation of prior preferences."
  Multi-LLM active inference systems already exist.
- **Potential impact on TARGET-TRUTH**: axis 2 could split into
  2a "external boundary" + 2b "prior shaping." Target invariant might
  need to add "shadowMAS may shape but not lock the prior."
- **Risk**: prior shaping has a wide gray area; can drift into
  "telling agents how to think" and erode user final authority.
  Framing must remain advisory.
- **Trigger to consider**: when a real use case demands non-blocking
  governance (where external rejection is too coarse).

### A2. SAFEFLOW / FIDES — Information Flow Control as axis 2 enforcement substrate
- **Sources**: arxiv 2506.07564 "SAFEFLOW: A Principled Protocol for
  Trustworthy and Transactional Autonomous Agent Systems";
  arxiv 2510.11108 "A Vision for Access Control in LLM-based Agent
  Systems"; FIDES, Progent (Apr 2025), SEAgent (Jan 2026),
  MiniScope (Dec 2025); historical: Myers and Liskov, Decentralized
  Label Model (DLM), late 1990s
- **shadowMAS gap**: T-layers, data_class (R3), source_refs, and
  artifact_refs are governance vocabulary, not a runtime flow
  enforcement mechanism. shadowMAS's authority boundary is currently
  declared, not propagated through computation.
- **What it adds**: per-data-item confidentiality + integrity labels
  that track provenance across agents, tools, users, and
  environments. Augmented with type information for safe
  declassification (FIDES innovation).
- **Potential impact on TARGET-TRUTH**: axis 2 graduates from
  "vocabulary + external boundary" to also include "runtime flow
  enforcement." promotion gates (T4 → T3 → T2) can be framed as
  DLM-style declassification with a human gate.
- **Risk**: full DLM is heavy machinery; shadowMAS does not need it
  in v0. Borrow patterns, do not adopt wholesale.
- **Trigger to consider**: when R-layer substrate is selected,
  IFC labels should be the substrate vocabulary.

### A3. Geology unconformity → explicit memory gap markers
- **Sources**:
  - stratigraphic geology (Hutton, Smith, 18th–19th century) — the
    visual metaphor of explicit-gap-as-evidence
  - **DB tombstone records** (Cassandra, DynamoDB; distributed
    database literature) — marks "deleted, not absent" so reads can
    distinguish a removed record from a never-existed record
  - **SQL NULL semantics** (Codd, 1970s) — distinguishes "unknown",
    "not applicable", and "missing" rather than collapsing them into
    one absence
- **shadowMAS gap**: memory plane currently records "what happened."
  It does not distinguish between
  (a) positive absence: agent ran, recorded nothing of interest, and
      explicitly confirmed the period was quiet, and
  (b) unknown absence: no record because the agent crashed, the log
      system failed, or someone deleted records.
  These look identical at the data level but mean opposite things for
  audit.
- **What it adds**: explicit "unconformity marker" records that say
  "between T_a and T_b, no recorded events; gap_reason
  = scheduled_idle | agent_crash | unobserved | deliberate_redaction;
  recorded_by = ..."
- **One-sentence diff vs prior art**: DB tombstones mark deleted
  records inside a row-oriented store, and SQL NULL distinguishes
  missing-value semantics inside a relation; A3 applies the same
  gap-marker pattern to **agent-level observation periods** in a
  temporal memory plane, where the gap itself carries audit-relevant
  meaning rather than being purely an internal-storage concern.
- **Potential impact on MEMORY-PLANE-HARNESS**: a new record type or
  packet field. SESSION-LOG-INTEGRITY spec could incorporate
  unconformity markers as part of hash chain integrity.
- **Risk**: tempting to over-mark; gap markers should be reserved for
  intentional or detected gaps, not auto-generated for every idle
  millisecond.
- **Trigger to consider**: when session_log plane gets a real
  implementation, design unconformity marker semantics from day one.
- **Novelty status**: **novel application** of established DB
  gap-marker patterns (tombstones + NULL semantics) to AI agent
  memory architecture. Not pure novelty. The category (gap markers
  as first-class data) is borrowed with attribution; the application
  layer (agent observation periods) is what shadowMAS adds.
- **Self-correction note**: this entry was originally written as
  "plausibly genuinely novel." Recursive application of the
  Synthesis Discipline section above surfaced DB-theory prior art
  during a later review round. The entry is now reframed accordingly.
  See the Notes section at the bottom of this file for the meta
  observation.

---

## B. Axis 3+4 fillers (weakest axes)

### B1. ALMA — Meta-learned Agentic Memory Designs
- **Source**: arxiv 2602.07755 "Learning to Continually Learn via
  Meta-learning Agentic Memory Designs" (Feb 2026); related:
  MAPLE (arxiv 2602.13258), MAGMA (Jan 2026), Modular Memory
  (arxiv 2603.01761)
- **shadowMAS gap**: MEMORY-PLANE-HARNESS hand-designs three planes
  (session_log / working_memory / shared_memory) with hand-crafted
  invalidation rules. axis 3 (dynamic adaptation) is TARGET-TRUTH's
  weakest axis with no implementation direction.
- **What it adds**: meta-learned memory designs that outperform
  hand-crafted across four sequential decision-making domains.
  Provides a concrete mechanism for axis 3 + axis 4 to co-evolve.
- **Risk**: meta-learning the memory topology means shadowMAS
  modifies its own structure. This intersects the target invariant
  "automation may not expand its envelope by itself." Must clarify
  that meta-learning operates inside the envelope and the envelope
  itself is human-defined.
- **Trigger to consider**: when shadowMAS gets any real personalization
  or project-specific adaptation requirement, ALMA-style meta-learning
  is the leading candidate mechanism.

---

## C. Mechanism prior art (shadowMAS proposed; literature already has)

These two imports were identified through adversarial cross-domain
review of shadowMAS's vocabulary. Subsequent literature search shows
that AI / multi-agent communities have published prior art that
shadowMAS's distillation appears to have skipped. shadowMAS should
adopt or refuse with explicit reason, not reinvent.

### C1. Speech Act Theory → FIPA ACL illocutionary-force vocabulary for packets
- **Sources**: Austin "How to Do Things with Words" 1962; Searle
  "Speech Acts" 1969; **FIPA ACL** (Foundation for Intelligent
  Physical Agents Agent Communication Language), IEEE-standardized
  1995–2002
- **shadowMAS gap**: packets are typed by FAMILY (task / memory /
  review) but not by ILLOCUTIONARY FORCE. The review_packet
  `recommendation` enum mixes Searle's act categories:
  - `approve` = declarative (saying it makes it so)
  - `reject` = declarative
  - `escalate` = directive (asking another to act)
  - `defer` = commissive (committing self to future action)
  - `revise` = directive
  - `unpromote` = declarative
  The R4 round that added `unpromote` felt the strain of this
  category mismatch but resolved it within the existing flat enum.
- **Prior art**: FIPA ACL requires a `performative` field on every
  message: request, inform, propose, confirm, query, not understood,
  agree, refuse, ... Semantics tied to BDI (beliefs / desires /
  intentions) mental states. Used in agent communication for 25+
  years.
- **What shadowMAS could adopt**: an `act_force` field on
  packet_common_shell with the five Searle categories (assertive /
  directive / commissive / expressive / declarative) OR with the
  FIPA performative vocabulary. Probably the five Searle categories
  are right for shadowMAS — finer than packet_family, coarser than
  FIPA's 20+ performatives.
- **What shadowMAS should NOT adopt**: FIPA's full BDI semantics —
  too heavy for shadowMAS's lightweight packet IR philosophy.
- **Risk**: adopting force taxonomy changes axis 1 vocabulary at the
  root. All existing packet fixtures, validators, and tests must be
  reviewed if act_force becomes required.
- **Trigger to consider**: next time the `recommendation` enum is
  extended (R4-style situation), pause and decide whether the
  extension is really a new category that needs separate force
  typing. If yes, this is the moment to do the import properly.

### C2. Common Law precedent → Case-Based Reasoning (CBR) for judgment accumulation
- **Sources**: stare decisis (English common law tradition);
  Schank's dynamic memory model 1982; Kolodner's CYRUS 1983;
  Lebowitz's IPP 1983; Ashley 1988 (legal CBR);
  arxiv 2311.10934 "Case Repositories: Towards Case-Based Reasoning
  for AI Alignment" (2023);
  arxiv 2504.06943 "Review of CBR for LLM Agents" (2025)
- **shadowMAS gap**: governance is 100% civil-law-style (code
  declared upfront in 01_truth/). Every review_packet is a fresh
  re-derivation from first principles. There is no precedent
  registry, no case retrieval, no judgment accumulation. Same
  situations get re-judged from scratch.
- **Prior art**: CBR has process primitives — case retrieval,
  adaptation, retention. Five paradigmatic CBR variants exist:
  statistically-oriented, model-based, planning-oriented,
  exemplar-based, adversarial/precedent-based. The 2023 alignment
  paper applies CBR directly to AI governance.
- **What shadowMAS could adopt**: a `04_runtime/precedent_registry/`
  or `03_memory/precedent_plane/` surface. Each approved review_packet
  is automatically indexed by a `situation_fingerprint` (packet
  shape + scope + risk + recommendation + outcome). New
  review_packets get a precedent retrieval pass that surfaces the N
  most-similar past cases as advisory context for human review.
- **What shadowMAS should NOT adopt**: binding precedent. shadowMAS
  precedent should remain **advisory** (informs but does not bind),
  preserving the existing target invariant that human authority is
  never auto-replaced.
- **Risk**: precedent retrieval becomes a back-door promotion path
  if not advisory-only. Must explicitly say "retrieval hit is not
  approval" (mirroring shadowMAS's existing memory rule).
- **Trigger to consider**: when review_packet volume becomes high
  enough that re-judging from scratch becomes expensive. Currently
  near-zero volume; not urgent.
- **This is a non-ML route to axis 3**: precedent accumulation IS
  learning from past, without meta-learning, RL, or model updates.

---

## D. Defensive validations

### D1. GSAR typed grounding + coherence trap — validates shadowMAS's "no agent self-correction" choice
- **Sources**: Reflexion (arxiv 2303.11366, 2023); 2026 preprint on
  self-evaluation information-theoretic limits (the coherence trap
  result); GSAR framework (2026)
- **The result**: a 2026 preprint proves that when generator and
  evaluator share correlated error modes, self-evaluation provides
  weak evidence of correctness. Iterative self-critique amplifies
  confidence without adding information — a "coherence trap" where
  the agent convinces itself with increasingly polished but still
  wrong reasoning.
- **GSAR's solution**: typed grounding — each agent claim is tagged
  with evidence type (retrieved document, tool output, model
  inference). Cross-agent critique is allowed only on claims in
  categories where the critiquing agent has verification access.
- **Why this matters for shadowMAS**: shadowMAS's current design has
  no agent self-correction. All disagreement routes to review_packet
  for human review. This was an implicit choice; the coherence-trap
  result makes the choice **explicitly defensible**: doing agent
  self-correction without typed grounding is unsafe by an
  information-theoretic argument.
- **What shadowMAS should NOT change**: keep the "no agent
  self-correction" default. Surface review_packet for any
  disagreement.
- **What shadowMAS should add later if self-correction is ever
  introduced**: typed grounding on every claim (this aligns with
  Speech Act act_force from C1 and with IFC labels from A2).
- **Captures a real shadowMAS strength**: the existing rule
  "review_packet MUST always carry a text projection" supports
  typed grounding because typed grounding requires readable evidence.

---

## E. Operational / implementation menus

### E1. Jidoka Andon Cord + CRM upward challenge ritual
- **Sources**: Toyota Production System (jidoka / autonomation,
  1950s; Andon cord); aviation Crew Resource Management (post-1977
  Tenerife disaster)
- **shadowMAS gap**:
  - jidoka: shadowMAS stop_conditions are agent-self-defined.
    No peer broadcast stop. A second agent observing an invariant
    violation cannot pull a cord.
  - CRM: shadowMAS authority is delegation-downward only. There is
    no explicit upward-challenge ritual ("Captain, I have concerns
    about X" with mandatory acknowledgement). Lower-authority agents
    seeing problems can only escalate asynchronously via review_packet.
- **Potential additions**:
  - new `stop_signal_packet` family (or runtime broadcast surface):
    any agent emits a stop signal, all agents in the same task scope
    receive it and must acknowledge before continuing
  - new `challenge_packet` (or extend handoff): lower-authority
    agent challenges a specific higher-authority decision;
    higher-authority must explicitly acknowledge or override with reason
- **Trigger to consider**: when shadowMAS has more than one active
  agent in a single task scope (currently rare).

### E2. Sandbox substrates for R-layer
- **Sources**: Firecracker microVMs (AWS, 2018+); gVisor (Google);
  Kata Containers; various 2026 agent sandbox guides
- **shadowMAS gap**: R-layer substrate is listed under "Still Not
  Final" in CURRENT-TRUTH and has no concrete candidate.
- **Direct adoption menu** when R-layer is selected: Firecracker
  microVMs (hardware boundary), gVisor (user-space kernel), Kata
  (VM + container hybrid). "Sandbox-first / twin environment" pattern:
  prove a change in a twin environment before touching production.
- **Trigger to consider**: when R-layer is actually selected (not in
  v0 scope per ledger).

### E3. Watertight blast radius (naval architecture)
- **Sources**: ship compartmentalization; Plimsoll line (1876)
- **shadowMAS gap**: hard separation exists across repos, but
  within a single packet there is no declared blast radius limit.
  A packet labeled `risk: r0_trivial` could still touch many files
  if scope is broad.
- **Potential addition**: packet_common_shell optional
  `blast_radius_limit: {max_files, max_lines, max_truth_surfaces}`.
  Runtime hook enforces.
- **Trigger to consider**: when there is evidence of a packet that
  declared low risk but landed wide blast. Currently no data.

---

## How to use this doc

- Before opening a new audit cycle, scan section A for paradigm-level
  lenses that may now apply.
- When TARGET-TRUTH axis 3 or 4 is being implemented, consult B1
  (ALMA) as the leading candidate.
- When the `recommendation` enum is extended again or any packet
  vocabulary is debated, pause and check C1 (Speech Act / FIPA ACL)
  before adding more enum values.
- When designing precedent / case retrieval / decision-history
  features, consult C2 (CBR) for established process primitives.
- Keep D1 (coherence trap) referenced in any future discussion of
  agent self-correction.
- Treat section E as menus, not commitments.

## How NOT to use this doc

- Do not adopt any item here without an explicit atomic round with
  authority-boundary review.
- Do not treat the absence of an item from this doc as evidence that
  shadowMAS has already covered the topic.
- Do not let "we cited a paper" become "we implement the paper."

## Promotion conditions
An item moves from rationale to canonical truth only after:
- a concrete shadowMAS use case demands it, and
- a packet schema or truth file proposal is drafted, and
- governance review (per CHANGE-IMPACT-MAP) is performed, and
- the proposal passes the verification floor
  (see negative_audit_cycle_routine.md).

## Out of scope
This file does not:
- modify canonical truth, packet schemas, registries, or runtime
- adopt any external framework
- bind future shadowMAS design choices
- enumerate every paper in adjacent fields
- replace the candidate registry as the authoritative record of
  in-flight design candidates

## Notes
- Three items in section A are intentionally listed with explicit
  trigger conditions to avoid premature adoption.
- C1 and C2 are placed in their own section because they highlight
  cases where shadowMAS appears to be reinventing wheels that other
  communities standardized decades ago. Awareness of this prior art
  is worth more than the import itself.
- A3 (geology unconformity) was first written as "plausibly
  genuinely novel" because initial search did not surface AI memory
  literature using this metaphor. A later recursive review applied
  the Synthesis Discipline section to this file itself and surfaced
  DB-theory prior art (tombstones, SQL NULL semantics) that the
  initial search missed. A3 is now reframed as a **novel
  application** of established DB gap-marker patterns to AI agent
  memory architecture, not pure novelty. This self-correction is a
  worked example of the discipline and is preserved here as
  evidence that the discipline applies to the discipline doc itself.
