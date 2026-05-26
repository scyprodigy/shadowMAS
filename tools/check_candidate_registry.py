#!/usr/bin/env python3
"""Validate CANDIDATE-REGISTRY entries against declared required_fields.

Reads 03_memory/registry/SHADOWMAS-CANDIDATE-REGISTRY.v0.yaml and asserts
that every entry under `candidates[*]` carries every field listed in
`candidate_entry_schema.required_fields`.

This closes the self-governance gap: the registry that records candidates
was not itself validated. With this checker in CI, a malformed candidate
entry breaks the build instead of silently drifting.

Exit codes:
  0  all entries valid
  1  one or more entries missing required fields (or registry shape broken)
  2  usage / file / yaml parse error

Usage:
  python3 tools/check_candidate_registry.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent
    / "03_memory"
    / "registry"
    / "SHADOWMAS-CANDIDATE-REGISTRY.v0.yaml"
)


def main() -> int:
    if not REGISTRY_PATH.is_file():
        print(f"ERROR: registry not found at {REGISTRY_PATH}", file=sys.stderr)
        return 2

    try:
        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"ERROR: yaml parse failed: {exc}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("ERROR: registry root must be a mapping", file=sys.stderr)
        return 2

    schema = data.get("candidate_entry_schema")
    if not isinstance(schema, dict):
        print(
            "ERROR: candidate_entry_schema missing or not a mapping",
            file=sys.stderr,
        )
        return 2

    required_fields = schema.get("required_fields")
    if not isinstance(required_fields, list) or not required_fields:
        print(
            "ERROR: candidate_entry_schema.required_fields must be a non-empty list",
            file=sys.stderr,
        )
        return 2

    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        print("ERROR: candidates must be a list", file=sys.stderr)
        return 2

    findings = []
    for idx, entry in enumerate(candidates):
        if not isinstance(entry, dict):
            findings.append((idx, "<not-a-mapping>", ["entry is not a mapping"]))
            continue
        missing = [f for f in required_fields if f not in entry]
        cid = entry.get("candidate_id", "<no candidate_id>")
        if missing:
            findings.append((idx, cid, missing))

    if findings:
        print(
            f"REGISTRY DIRTY: {len(findings)} of {len(candidates)} "
            f"candidate(s) have missing required fields"
        )
        for idx, cid, missing in findings:
            print(f"  [#{idx}] candidate_id={cid}: missing {missing}")
        return 1

    print(
        f"OK all {len(candidates)} candidates carry the "
        f"{len(required_fields)} required fields"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
