# DECISION-no-mass-filename-rename.v0.en | decision record: mixed legacy naming in working drafts stays; no mass rename
# related: [policy_filename_memo, DECISION-no-covert-random-audit-v0, REJECTION-KNOWLEDGE-DIRECTION, rationale_index]
# phase: draft_non_canonical

> status: DRAFT / working-only / non-canonical / authority: none
> this file records a decision NOT to perform an action; it is not a rename proposal
> policy owner: `policy_filename_memo.md` (this record extracts, does not supersede)

# Decision

Do not mass-rename existing files to a single naming convention.

The mixed naming under `07_working/drafts/**` (lowercase snake_case alongside
UPPERCASE-WITH-HYPHENS legacy and dotted working markers) is sanctioned by the
path-sensitive filename policy, not an accident. The zone is classified
`flexible_research_with_legacy_structured_semantic` in
`policy_filename_memo.md`, and that memo's "Out of scope" section states the
decision directly: "No mass rename of existing grandfathered files. The hook
is PreToolUse only; existing files coexist with the new rules."

# Rejection scope

- applies to existing tracked files across all layers, strongest in
  `07_working/drafts/**`
- new files still follow the path policy table at write time (PreToolUse hook)
- does not forbid renaming one file for a concrete reason (collision,
  pollution, broken reference), with references updated per AGENTS.md

# Rejection reasons

- references are load-bearing: renames force reference updates across docs,
  tools, tests, and compiled surfaces; mass rename maximizes that blast radius
  for zero semantic gain
- machine surfaces already depend on existing prefixes, including the
  `DECISION-*` glob in `tools/build_rework_guard.py` and `test_*` discovery
- git history continuity: mass rename degrades `git log --follow` ergonomics
  across the whole working area at once
- the apparent inconsistency is path-scoped by design: strict zones
  (`tools/`, `02_packets/`, `tests/`) are already uniform; the flexible zone
  is intentionally permissive

# Reopen conditions

Revisit only if one of the following occurs:

- the filename policy memo is promoted and revised to drop the
  grandfathering clause
- a release / public-hygiene milestone explicitly budgets for a one-time
  normalization pass including all reference updates
- tooling emerges that performs rename plus full reference rewrite plus
  compiled-surface regeneration atomically, reviewed and approved

# Anti-resurrection note

This record exists because a repo-wide audit (2026-06-11) flagged the mixed
naming as drift before reading the policy memo. The flag was retracted; the
mixing is policy. Future audits should hit this record first.
