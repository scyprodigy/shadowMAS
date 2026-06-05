# EXTERNAL-INTAKE-CANONICAL-CANDIDATE-REVIEW-NOTE.v0.draft | draft review note for external intake canonical-candidate readiness
# related: [MDL-MISSION-ISSUE-TEMPLATE, EXTERNAL-MDL-MISSION-PACKET-SCHEMA, MDL-MISSION-GATE-WORKFLOW, EXTERNAL-MDL-MISSION-VALIDATOR-SPEC]
# phase: external_intake_canonical_candidate_review_note_draft

# External Intake Canonical-Candidate Review Note v0 Draft

## Status

DRAFT REVIEW NOTE ONLY.

This note is non-canonical. It is not promotion, not implementation, not a
validator, not an issue template, not a workflow, and not public intake. It does
not enable external intake.

This note does not move any draft into `01_truth/`, does not make any schema
canonical, does not create or install a GitHub issue template, does not create
or install a GitHub workflow, and does not implement validator behavior.

## Purpose

This note records that the external intake draft chain is ready for owner/human
canonical-candidate review as an inactive draft chain.

It does not decide promotion. It summarizes readiness, invariants, blocked
activation decisions, and owner decision points for human review.

## Artifact List

- `MDL-MISSION-ISSUE-TEMPLATE.v0.draft.yml`
- `EXTERNAL-MDL-MISSION-PACKET-SCHEMA.v0.draft.md`
- `MDL-MISSION-GATE-WORKFLOW.v0.draft.yml`
- `EXTERNAL-MDL-MISSION-VALIDATOR-SPEC.v0.draft.md`

## Classification Table

| Artifact | canonical_candidate_ready | inactive_only | implementation_blocked | human_decision_required | Notes |
|---|---:|---:|---:|---:|---|
| `MDL-MISSION-ISSUE-TEMPLATE.v0.draft.yml` | yes, as inactive form draft | yes | yes, for active public use | yes | Ready for review as a draft form shape; must not be copied to `.github/ISSUE_TEMPLATE/` without explicit approval. |
| `EXTERNAL-MDL-MISSION-PACKET-SCHEMA.v0.draft.md` | yes, as inactive schema document | yes | no implementation in this artifact | yes | Ready for review as a bounded packet schema draft; not canonical truth. |
| `MDL-MISSION-GATE-WORKFLOW.v0.draft.yml` | yes, as inactive gate spec | yes | yes, for workflow implementation or activation | yes | Ready for review as gate behavior design; not a runnable GitHub Actions workflow. |
| `EXTERNAL-MDL-MISSION-VALIDATOR-SPEC.v0.draft.md` | yes, as inactive validator spec | yes | yes, for executable validator implementation or activation | yes | Ready for review as future enforcement contract; not validator code. |

## Shared Invariants

- Form collects.
- Gate/validator decides.
- Nothing becomes a shadow candidate without `pass` plus human-gated review.
- `claim_ceiling <= candidate`.
- `gate_result` is gate-assigned only.
- Reporter-submitted `gate_result` hard-rejects the packet.
- No packet can self-declare `pass`, `flag_for_human_review`, or `reject`.
- ROUTE and EVID cannot raise authority.
- CORE is bounded human residual.
- CTRL caps authority and stores quarantine and acknowledgements.
- Acknowledgements are necessary but not sufficient.
- Best-effort detection is not the authority guarantee.

## Denied Actions And Non-Absorption

External intake must not directly become or request:

- canonical truth
- schema change
- glossary promotion
- memory ingestion
- n8n workflow import
- runtime behavior change
- product-repo write-back
- external repo scan
- authority approval
- task verification

External intake must also reject or deny absorption of:

- raw logs
- secrets
- workflow graphs
- diffs / patches / schema edits

## Simulation Evidence

- Issue-template simulation passed for inactive draft use.
- Full packet schema simulation passed.
- Validator-rule simulation passed.
- `gate_result` hard-reject wording was patched and audited.
- Remaining implementation work is parser, detector, label/comment behavior, and
  workflow behavior, not concept rules.

## Still Blocked Before Public Intake

Public or active intake remains blocked on:

- human approval
- active issue-template decision
- active gate workflow decision
- executable validator implementation design
- private-intake / public-secret risk decision
- bot comment / label behavior implementation review

## Explicit Non-Goals

This note:

- does not promote drafts into `01_truth/`
- does not make the schema canonical
- does not activate public intake
- does not create an issue template under `.github/ISSUE_TEMPLATE/`
- does not create a workflow under `.github/workflows/`
- does not implement a validator
- does not allow external repo scanning

## Owner Decision Points

- Should external intake drafts be promoted to canonical candidate?
- Should the issue-template remain inactive until gate implementation exists?
- Should public intake be delayed until private/pre-submit secret handling
  exists?
- Should validator implementation be designed before active workflow?

## Recommended Next Step

Human review first.

No automatic promotion. No active workflow. No public intake.
