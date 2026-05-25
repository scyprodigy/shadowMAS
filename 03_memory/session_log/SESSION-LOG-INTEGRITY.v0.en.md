# session_log_integrity | hash-chain integrity spec for session_log memory plane
# related: [MEMORY-PLANE-HARNESS, SHADOWMAS-CURRENT-TRUTH, SHADOWMAS-FILE-STATUS-REGISTRY]
# phase: v0-spec

# SESSION-LOG-INTEGRITY.v0

## Purpose
This file specifies the integrity model for the `session_log` memory plane.

It is a spec, not an implementation. `session_log/` remains intentionally
unimplemented in v0 per `03_memory/MEMORY-PLANE-HARNESS.v0.en.md`.

## Goal
Prevent silent tampering with recorded session traces while keeping the
storage backend simple, inspectable, and reversible.

## Core Rule
Session log entries are append-only and content-addressed via a hash chain.

Each new entry binds to the previous entry's hash so any retroactive
modification breaks the chain in a detectable way.

## Minimum Entry Shape
Each entry should carry at least:
- `entry_id`: stable identifier
- `prev_hash`: content hash of the immediately preceding entry, or the
  reserved value `genesis` for the first entry
- `entry_hash`: content hash of this entry, computed excluding the
  `entry_hash` field itself
- `created_at`: RFC3339 UTC timestamp
- `payload`: recorded session content

## Hash Function Direction
- prefer SHA-256 for v0
- hash input excludes the `entry_hash` field
- hash input includes `prev_hash` so chain linkage is part of the digest
- hash function may evolve through a normal CHANGE-IMPACT-MAP review

## Append-Only Rule
- entries MUST NOT be edited in place
- corrections enter as new entries that reference the prior entry via
  `related_entries` and explicitly mark the prior entry as superseded
- physical deletion is allowed only through governed retention policy and
  must record the deletion event itself as an entry

## Verification
A verifier walks the chain from the most recent entry backwards:
- recomputes each `entry_hash` from current content
- compares against the value stored on the next entry's `prev_hash`
- any mismatch is a tamper-evidence finding

Verification is read-only and produces advisory output.

## Authority Boundary
- the hash chain is integrity evidence, not authority
- a valid chain does not approve the contents of its entries
- a broken chain triggers review; it does not automatically invalidate
  prior decisions

## Backend
This spec does not select a backend.
File-per-entry, single append-only file, embedded SQLite, or other
storage may all conform as long as the entry shape and append-only rule
are honored.

## Still Not Final
- exact entry serialization format (YAML, JSON, NDJSON, ...)
- exact retention policy
- exact verification tool surface
- exact integration with `task_packet`, `memory_packet`, and
  `review_packet` cross-references
