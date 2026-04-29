# shadowMAS Packet Validator

## Purpose
This validator is read-only.

It validates one YAML packet file against the current shadowMAS v0 packet contract.

## Current command
Direct command:

```bash
python3 05_scripts/validate/shadowmas_validate.py <packet-file>
```

Logical future command shape:

```bash
shadowmas validate <packet-file>
```

## What it validates
It currently validates:

- `packet_type`
- required fields
- `schema_version: v0`
- filename `.vN` major mismatch
- family-specific status
- `source_refs`
- `artifact_refs`
- `handoff`
- deprecated handoff fields

## What it does not do
It does not:

- run agents
- attach to product repos
- write back changes
- auto-fix packets
- run hooks
- run CI
- validate JSON
- validate multiple files
- support stdin
- enforce full SemVer

## Exit codes
- `0`: valid packet
- `1`: validation errors
- `2`: usage / input / parse failure

## Development notes
- Use `python3`.
- Use `PYTHONDONTWRITEBYTECODE=1` when compiling/checking to avoid `__pycache__`.
