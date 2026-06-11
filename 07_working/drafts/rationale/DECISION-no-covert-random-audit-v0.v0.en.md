# DECISION-no-covert-random-audit-v0 | draft rationale for not building covert random audit in v0
# related: [SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-CHANGE-IMPACT-MAP, first_user_smoke, SESSION-LOG-INTEGRITY]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> owner review required before any promotion or downstream change
> this file records a decision NOT to build a feature; it is not a feature proposal

# Decision
v0 does not build or claim covert/random post-delivery audit.

That capability is deferred to v-future and is meaningful only at multi-party scale
(see "v-future Reopen Conditions"). At solo / beachhead scale the audited party,
operator, verifier, and log owner are effectively the same person and machine, so
covertness and randomness add no real value over deterministic, visible checks.

# Verified v0 Scope
v0 keeps and documents the existing shadowMAS-owned validation surfaces, with a
default of zero new code. The honest scope is deterministic post-delivery validation
of shadowMAS artifacts, not a quality-measurement system.

Limits:
- "post-delivery" means after delivery of a shadowMAS artifact, not after an arbitrary
  product feature delivery.
- v0 builds no new gate engine, adds no new runtime state, and makes no quality claim.
- not claimed: deterrence, independence, quality-rate, covertness, tamper-proof assurance.

# Ownership Boundary
shadow gates shadow; product gates product.

Product-required build/test/deploy paths must not depend on shadowMAS.

A product owner may optionally reference shadowMAS in their own evaluation flow, but
shadowMAS must not run or own product tests/lint/build, and the product's required
path must remain able to build, test, deploy, and operate with shadowMAS absent
(see SHADOWMAS-CURRENT-TRUTH Hard Separation Rule / Boundary invariant).

# Existing shadow-owned validation surfaces
`tools/first_user_smoke.py` is already the thin wrapper for this surface; it self-labels
as not a runtime engine and makes no authority/production-safety claim. v0 default is to
document it, not to rebuild it.

ADVISORY checks must not be described as gates.

Taxonomy (verified against the actual scripts):

blocking (non-zero exit on a real problem; already chained in first_user_smoke):
- unit tests (`python3 -m unittest discover tests`)
- packet validator (`05_scripts/validate/shadowmas_validate.py`) for task/review/memory packets
- L1 authority fixtures (`tools/shadowmas_minimal_validator.py`, positive and negative)
- L2 inspector (`tools/inspect_l2_fixture.py`)
- candidate registry checker (`tools/check_candidate_registry.py`)

blocking but NOT in first_user_smoke (repo hygiene / meta; better kept as separate CI steps):
- pollution scanner (`tools/check_no_pollution.py`, exit 1 on a match)
- validator drift (`tools/check_validator_drift.py`)

advisory (never blocks; produces a finding for the human git-review gate, not a gate result):
- translation drift (`tools/check_translation_drift.py`); exits 0 even when the embedding
  backend is unavailable
- truth-change checker (`tools/check_truth_change.py`); self-labeled ADVISORY, contextual
  (only meaningful when `01_truth/` changes); exit 1 is a finding, not a block

Folding the pollution scanner or validator-drift check into first_user_smoke is a separate,
explicitly named decision, not a vague "minor tweak"; default is to leave smoke as-is and
keep those as standalone CI steps.

# Rejected Claims Ledger
covert/random post-delivery audit was rejected for v0 because, at the current solo /
beachhead scale:
- solo scale: audited party, operator, verifier, and log owner are the same person/machine
- self-audit, not independent audit: there is no separation between auditor and audited
- CI dominance: for regression detection, deterministic visible CI/pre-commit checks are
  strictly better than hidden random sampling of the same checks
- no statistical power: low delivery volume x low sampling rate cannot yield a meaningful
  quality-rate estimate; hash chaining gives tamper evidence, not statistical power
- no structural covertness: the agent shares the machine and repo, so the audit usually
  degrades to policy-hidden / self-audit rather than structurally covert
- deterrence is a category error on stateless per-call agents: inspection-game deterrence
  needs a persistent, self-interested, memoryful player; for a stateless per-call LLM the
  deterrence statement collapses into one more prompt instruction. It transfers only to
  memoryful / self-improving agents, which is not the v0 default.

# Optional Chronology
A personal chronology log is optional and OFF by default. If wanted, reuse the existing
hash-chained run log (`shadowmas_run.py` / SESSION-LOG-INTEGRITY) as a personal
reproducibility aid only. It must not be described as independent audit, deterrence,
quality measurement, or tamper-proof assurance.

# v-future Reopen Conditions
Revisit covert/random audit only when ALL of the following hold:
- the audited agent/operator is distinct from the auditor
- trigger, seed, decision, log, and checks live outside the working agent's read scope
- checks are pre-registered by an owner/orchestrator/spec, or agent-independent by
  construction (e.g., build/lint/property checks)
- isolated delivery snapshots (throwaway checkout / worktree / temp copy) exist
- delivery volume is large enough for statistics
- escalation is owned by an independent reviewer / CI / operator

Until all hold, any "random audit" surface is enterprise-scoped and out of scope for v0.

# Non-Promotion Note
This file is not canonical truth. It lives in `07_working/` and is non-canonical by
location and intent. It records a decision NOT to build a feature, so that the idea is
not resurrected at the wrong scale by a future reader who sees only the words
"random audit". Any move toward canonical truth (e.g., `01_truth/`, `02_packets/`) or a
real runtime requires explicit owner review and change-impact per SHADOWMAS-CURRENT-TRUTH.
