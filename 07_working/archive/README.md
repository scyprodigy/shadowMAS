# 07_working_archive/README | placeholder explaining the archive folder convention
# related: [SHADOWMAS-FILE-STATUS-REGISTRY, active_log_archive_plan, active_log_move_plan]
# phase: archive_convention

# 07_working/archive/ — archive folder convention

## Purpose
This directory holds files that have been intentionally moved out of
active working draft folders but retained for provenance.

Per `03_memory/registry/SHADOWMAS-FILE-STATUS-REGISTRY.v0.yaml`
`folder_defaults`, anything placed here inherits:

- `status: archived`
- `authority: historical_only`

Files here are not canonical truth and not current working material.
They are retained so that future audit cycles, candidate registry
provenance pointers, and external reviewers can still inspect the
historical evidence.

## How files arrive here
A file should move here only through an explicit plan-then-execute
flow, mirroring the pattern established by
`07_working/drafts/rationale/active_log_archive_plan.yaml`:

1. Write a plan that describes options (keep / archive / delete) and
   lists every path reference that would need to update.
2. Get human approval of the disposition.
3. Execute the move in a single atomic commit that:
   - performs `git mv` of the file into `07_working/archive/`,
   - updates every path reference identified in the plan, and
   - leaves all canonical-truth surfaces and packet schemas untouched.
4. Verify with the standard verification floor (pollution scanner,
   candidate registry checker, validator-schema drift checker, unit
   tests) before commit.

## What this directory does not do
- It does not promote anything to canonical truth.
- It does not authorize deletion of archived files. Deletion is a
  separate decision that requires its own approval flow.
- It does not host new working drafts. Use
  `07_working/drafts/` for active drafts.

## Current contents
Files currently archived here are tracked individually by git.
Each archived file should have at least one provenance pointer
from somewhere else in the repo (typically the rationale folder or
candidate registry) so that the archive is reachable through
content, not only through filesystem path discovery.
