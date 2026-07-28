# SHADOWMAS-POSITIONING-STATEMENT.v0.draft.en | draft positioning statement for controlled-alpha shadowMAS
# related: [SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, README, DECISION-review-brief-primary-direction]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before README, website, or canonical-truth use
> this draft balances current v0 capability with target direction; it is not a release claim

# Positioning

shadowMAS is a local-first layer that gives you a packet form for AI-assisted work: something you can validate, inspect, and hand to a human. It is not the agent runtime; its target is the authority-bounded layer around runtime work. By design it does not run your agents, own your tools, or sit in their execution path.

You bring your own agents, models, memory, and project. By design shadowMAS does not prescribe a workflow; in v0 it also has no cloud service of its own. It sits alongside the tools you already use. Packets are authored, not auto-captured. Personal adaptation is a target direction, not a v0 capability.

Two insistences:

- Non-invasive: your product repo must build, test, deploy, and operate without shadowMAS. shadowMAS validates its own artifacts; it does not gate, run, or own product checks.
- Authority-integrity: schema validity does not make a label like "approved" or "truth" true. shadowMAS makes the packet's fields, evidence, and boundary visible for human review; v0 does not enforce authority at runtime.

The long-term direction is to be usable by many people with their own tools. The first concrete form is one developer running several coding agents on a local machine, who wants AI-assisted work expressed as inspectable packets without adopting a heavyweight platform.

The first concrete tool expression of that form is the task-scoped pre-sign-off review brief (`tools/scope_rework_guard.py`, `tools/compose_review_brief.py`; direction record: `DECISION-review-brief-primary-direction.v0.en.md`). Premise: as agent output grows, the scarce resource is human review attention. The brief compiles, for one bounded task, what the accountable human should know before signing off — prior rejections with reopen conditions, stale or broken cited evidence, risk and rollback, a bounded typed check list — and reveals the compiler recommendation only after the human records a judgment. The design goal is routing scarce attention, not faster review. Format decisions follow published cognitive-load and review-quality evidence as design rationale; this is not a claim that shadowMAS implements neuroscience or measurably improves oversight. The sign-off receipt (an ordinary v0 review_packet) is a by-product of the flow, not the pitch.

Interoperability direction: the packet's common shell is kept self-contained so that a packet can travel as a data payload inside larger transport protocols (for example, as a data part of an agent-to-agent message). This is a design constraint on the shell, not a shipped integration; v0 ships no protocol binding.

It is not an agent framework, workflow/runtime engine, memory database, replacement for your project's truth, or production-safety guarantee. Today it is controlled-alpha: packet schemas, validators, fixtures, workspace helpers, and inspection surfaces — material to inspect, not a verdict to apply.

# Claim Discipline

- current-tense claims must map to v0 surfaces
- target claims must be labeled as direction
- validators check representation, not authority semantics
- shadowMAS validates shadowMAS artifacts; products gate products
- no claim of production safety, runtime enforcement, automatic review generation, personalization, or cloud privacy guarantee

# Promotion Note

This file lives in `07_working/`. Any use in `README.md`, `01_truth/`, or external-facing material requires owner review and change-impact.
