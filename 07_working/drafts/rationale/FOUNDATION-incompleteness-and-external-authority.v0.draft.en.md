# FOUNDATION-incompleteness-and-external-authority.v0.draft.en | draft rationale: why shadowMAS keeps final authority outside the formal packet system
# related: [SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-TARGET-TRUTH, SHADOWMAS-POSITIONING-STATEMENT]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before README, website, or canonical-truth use
> these results are cited as structural analogy and intellectual discipline, not as theorems that shadowMAS implements or that prove its design

# Why this note
shadowMAS already insists "schema-valid is not authority-valid" and keeps final authority with a human (T0) outside the packet system. This note records the foundational analogy that motivates that choice, and, more importantly, fences off how it may and may not be cited.

# The structural analogy (legitimate use)
- Tarski (undefinability of truth): a sufficiently expressive formal language cannot contain a truth predicate that decides truth for all of its own sentences; defining that truth requires a richer metalanguage outside the object language.
- Goedel (second incompleteness): a consistent, sufficiently strong, effectively axiomatized formal system cannot prove its own consistency from within.
- Loeb (the Loebian obstacle, as used in AI-alignment research): a formal system cannot in general license trust in its own proofs or self-reference without external grounding.
- Common shape: a self-referential formal system cannot be its own final arbiter of truth, consistency, or self-trust. Final judgment of those properties has to sit at a level outside the system.
- shadowMAS echoes this shape by design: validators operate at the object level (representation); final authority (is this authority-valid? may it be promoted?) is placed at a level outside the packet system, the human owner T0. This is why "validators check representation, not authority semantics" is an architecture choice consistent with a known limit on self-reference, not a v0 shortcut.

# Claim discipline (how this may and may not be cited)
- DO cite these as motivation, structural analogy, and intellectual discipline for keeping final authority outside the formal system.
- DO NOT claim the theorems apply literally to shadowMAS: the packet schema is a data-validation language and is not asserted to meet the theorems' hypotheses (arithmetic-level expressive power, formal provability, consistency, effective axiomatization).
- DO NOT equate "authority-valid" with arithmetic "truth": authority is a normative/social predicate. The legitimate analogy is between the object/meta hierarchy and shadowMAS's validation/authority split, not between authority and Tarskian truth.
- DO NOT claim the theorems prove a human is necessary: they imply that some level outside the object system is required. That the external level is a human (T0) is shadowMAS's design choice, not a corollary. A stronger formal system could be the metalevel, yielding an infinite tower of metalevels, not a human.
- TREAT Loeb as the weakest, most motivational link: LLM agents are not formal provability systems; the Loebian obstacle is an alignment-research analogy, not an applied result about LLMs.
- USE as "why", never as "what": shadowMAS does not implement, encode, or rest on these theorems as a feature. Citing them as a feature would be exactly the overclaim the positioning discipline forbids.

# What it gives shadowMAS
A rigorous, well-known reason that "expecting a system to certify its own truth or authority from within is the wrong default." It turns shadowMAS's human-outside-the-loop choice from a bare preference into a choice aligned with a famous structural limit on self-reference. It is backbone for the manifesto's "why", not a new capability.

# Open questions
- Whether to cite at all in owner-facing material, or keep this purely internal. Risk: Goedel is the most abused theorem in popular writing; any citation invites "the Goedel move".
- Exact wording in any manifesto or README use must pass the Claim Discipline above and owner review.
- Whether the buildable cousins (proof-carrying authorization / access-control logic / deontic logic) deserve a separate note, since those are "what" candidates while this note is strictly "why".

# Promotion note
This file lives in `07_working/`. Any use in the manifesto, `README.md`, `01_truth/`, or external-facing material requires owner review and change-impact. Non-canonical.
