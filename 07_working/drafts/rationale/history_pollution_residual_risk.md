# history_pollution_residual_risk | record of deferred history rewrite with explicit residual-risk acceptance
# related: [SHADOWMAS-LESSONS-QUEUE, calibration_framework_note, rationale_index]
# phase: working_draft

> Status: working draft / governance decision record
> Authority: none (records a decision; does not itself promote anything)
> Do not promote without authority-boundary review

# History Pollution Residual Risk

## Purpose
This file records that history rewrite of the shadowMAS repository was
considered, evaluated, and intentionally deferred. It exists so that the
deferral is repo-visible rather than living only in agent memory, and so
that any future agent or human running a pollution scan does not have to
re-derive the decision from scratch.

## HEAD state
As of commit `b3a8d7e` (and forward), the current tree contains no
known pollution patterns:

- no personal local username or home path
- no commercial-project name leakage
- no third-party email
- no API keys, cryptographic keys, or cloud credential patterns

Current-tree cleanup was completed via R8 (portable git-toplevel fallback
in `.claude/hooks/check_header.sh`) and earlier sanitization passes.

## History pollution — known classes
The full git history (144 commits as of decision time) still contains
the following classes of pollution. Exact strings are intentionally not
reproduced here to avoid re-introducing them.

| Class | Severity | Notes |
|---|---|---|
| Local developer username / home path | LOW-MED | introduced once, removed at HEAD; symmetric pattern in history |
| Commercial-project name and module / route vocabulary | MEDIUM | introduced once, sanitized at HEAD; some draft files still show the vocabulary in older commits |
| Real personal email in commit author metadata | MED-HIGH | mixed with the privacy-preserving noreply form across history |
| Third-party email in file content (outreach / proposal trail) | HIGH | involves third-party PII, not only the maintainer's |

Detailed counts and source commits are recorded in the R8b scan output
of the audit session and intentionally not duplicated here.

## Decision
History rewrite was deferred. Rationale:

- Rewrite blocks daily development; release / public-hygiene phase is a
  more natural window than mid-development.
- No tokens, API keys, or cryptographic credentials are involved, so
  there is no acute compromise to rotate against.
- The HEAD tree is already clean, so new commits do not extend the
  contaminated surface.
- Once rewrite is scheduled, the approved runbook (runbook v3 with
  immutable + working mirror, single filter-repo invocation, strict
  verify, remote refs/pull/* check, branch-protection toggle pair) is
  ready for execution.

## Residual risk (explicitly accepted)
By deferring rewrite, the following risks remain in force until the
release / public-hygiene phase:

- Third-party email and outreach trail remains visible in older
  commits, including any forks, clones, or GitHub server-side caches.
- Personal author email is reachable to anyone reading the commit
  metadata of older commits.
- Local developer username and home path are reachable in older
  commits, contributing minor OS-user identity exposure.
- Commercial-project name and module vocabulary are reachable in
  older commits, exposing prior product-domain context.
- Any external clone, fork, or mirror that already exists cannot be
  reached by a later rewrite and may retain the pollution indefinitely.

These risks are accepted for the deferral window. Acceptance is not
silent: it is recorded here and surfaced in the lessons queue.

## Reconsideration triggers
Move the decision back to "rewrite now" if any of the following occur:

- A release event or public-hygiene milestone is scheduled.
- An external contributor or fork count crosses a threshold that
  materially raises third-party PII exposure.
- A new pollution class with higher severity (for example tokens,
  credentials, customer data) is found in HEAD or history.
- Legal, compliance, or partnership pressure requires demonstrable
  history cleanup.

## References
- `.claude/hooks/check_header.sh` (R8 cleanup commit `b3a8d7e`)
- `07_working/drafts/SHADOWMAS-LESSONS-QUEUE.v0.yaml` (first real lesson
  entry derived from this decision)
- audit-session R8b scan output (in session transcript, not in repo)
- runbook v3 (history rewrite procedure, in session transcript, not in
  repo)

## Update 2026-05-28
The "Commercial-project name and module / route vocabulary" class listed
in the table above has been rewritten on `main` via `git-filter-repo`
(two passes during the May 2026 emergency cycle). Specific remediation:

- The previously-committed cleanup-disposition draft whose filename
  embedded the product token was removed from all reachable history via
  `--invert-paths` and force-pushed.
- All product-context substrings in historical file blobs were replaced
  with neutral placeholders via `--replace-text` rules held in `/tmp`
  (rules file never tracked, deleted post-run).
- The single affected commit message was rewritten via
  `--replace-message`.
- One in-source scanner pattern that itself contained the personal
  email handle was switched to a runtime base64 decode so the literal
  token no longer appears in any tracked source.
- The local backup tag `backup/pre-public-main-split-*` that still
  reached the pre-rewrite history was deleted; reflog expired and gc
  pruned the dangling commits.
- A backup mirror was retained locally at
  `~/workspace/shadow-mas.backup-20260528-133424` for a rollback window.

The remaining classes (personal author email, third-party PII) continue
under the original deferral plan above and are unchanged. The local
`private/schmidt-package` branch was left untouched per a separate
scope decision and is not pushed to `origin`.

The corresponding structural lesson is recorded as `lesson_0002` in
`07_working/drafts/SHADOWMAS-LESSONS-QUEUE.v0.yaml`.

## Update 2026-06-11
A targeted rewrite removed
`07_working/drafts/rationale/SHADOWMAS-MANIFESTO-DRAFT.v0.md` from all
reachable history via `git-filter-repo --invert-paths` and force-push,
following the same procedure as the May 2026 cycle. Reason: the file
mixed Chinese prose into an agent-facing draft and carried positioning
claims (flagship identity comparison, unsourced statistics, a gate
description contradicting `DECISION-no-covert-random-audit-v0`) that
the owner rejected. Salvageable concepts were generalized first into
`RATIONALE-calibrated-trust-gates.v0.draft.en.md` and the
interoperability paragraph of
`SHADOWMAS-POSITIONING-STATEMENT.v0.draft.en.md`.

Known residual: GitHub server-side caches and any pre-existing clone,
fork, or mirror may retain the pre-rewrite commits; this residual is
accepted, consistent with the original deferral record above. The
remaining deferred pollution classes (personal author email,
third-party PII) are unchanged by this update.

Rollback-window closure: the local backup mirror
`~/workspace/shadow-mas.backup-20260611` (which retained the
pre-rewrite history including the removed file) was deleted on
2026-06-11 after the rewritten remote was confirmed healthy across
several subsequent pushes. The May 2026 mirror was already gone. No
local copy of the pre-rewrite history remains on this machine.

## Out of scope
This file does not:

- reproduce the polluted strings (to avoid re-introducing them)
- modify any canonical truth
- promote itself into approved truth
- specify when rewrite will actually happen for the remaining deferred classes
- act as a substitute for the future rewrite execution
