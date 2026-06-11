# SHADOWMAS-POSITIONING-STATEMENT.v0.draft.en | draft positioning statement for controlled-alpha shadowMAS
# related: [SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, README]
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
