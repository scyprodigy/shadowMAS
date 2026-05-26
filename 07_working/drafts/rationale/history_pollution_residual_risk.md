# history_pollution_residual_risk | public-history privacy controls and limits
# related: [SHADOWMAS-LESSONS-QUEUE, negative_audit_cycle_routine, rationale_index]
# phase: working_draft

# Public History Privacy

This working record describes privacy controls and their limits. It grants no
authority and does not assert that a person accepted an exposure risk.

## Scope

Inspect file contents, filenames, commit messages, and author and committer
metadata. A clean checkout does not imply clean history. Scan detection rules,
tests, cleanup reports, and reversible encodings as potential exposure surfaces.
Keep identifying match values and recovery material outside public source.

## Remediation

Remove identifying data from reachable history, use a public no-reply commit
identity, and verify the rewritten result before publishing it. Preserve useful
methods through generalized descriptions rather than private case details.
Deleting a branch or adding a deletion commit does not erase an earlier version.

Use `tools/check_public_privacy.py --history` for generic public-history checks.
Operator-specific checks must additionally inspect known private identifiers
without embedding them, even encoded, in tracked source. A passing pattern scan
does not prove that every private fact or semantic variant has been removed.

## Remaining limits

Rewriting reachable history does not erase existing clones, mirrors, or hosted
views accessible through old object identifiers. Verify the published branch
separately; consult the hosting provider for remaining sensitive cached views.
Record exact affected identifiers and operational details only in private
remediation evidence. Do not turn that evidence into a new public disclosure.

Reference: [GitHub sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
