#!/usr/bin/env python3
"""Import an external memory packet as a downgraded candidate requiring re-validation.

This is the shadow-genealogy primitive (see deferred_state_inventory): lessons
and memories can cross owners, but trust cannot. An imported memory packet is
forcibly downgraded on entry — whatever its status and confidence were in the
source shadow, here it becomes a candidate awaiting this owner's review.

Forced on import:
- status -> candidate (whatever it was)
- promotion_candidate -> "yes" only if it was "yes"; otherwise stays "no"
- confidence -> capped at the import ceiling (default 0.5)
- provenance block added: original owner/status/confidence, import time
- invalidation_triggers gains a mandatory re-validation entry

The tool writes the downgraded copy to stdout or --out (inside 07_working/ by
convention). It never writes outside the destination it is given, never
mutates the source file, and import is not approval: the normal human
review / promotion gate still applies to the imported candidate.

Usage:
  python3 tools/import_memory_candidate.py <external_packet.yaml> [--out <path>]
                                           [--ceiling 0.5] [--importer <name>]

Exit: 0 = imported copy emitted; 1 = input not a memory packet; 2 = setup error.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

IMPORT_TRIGGER = ("imported from an external shadow; must be re-validated against "
                  "this repo's sources before any reuse")


def downgrade(data: dict, ceiling: float, importer: str) -> dict:
    original = {
        "original_owner": data.get("owner"),
        "original_status": data.get("status"),
        "original_confidence": data.get("confidence"),
        "imported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "imported_by": importer,
    }
    out = dict(data)
    out["status"] = "candidate"
    out["owner"] = importer
    try:
        confidence = float(data.get("confidence", ceiling))
    except (TypeError, ValueError):
        confidence = ceiling
    out["confidence"] = min(confidence, ceiling)
    if out.get("promotion_candidate") != "yes":
        out["promotion_candidate"] = "no"
    triggers = list(data.get("invalidation_triggers") or [])
    if IMPORT_TRIGGER not in triggers:
        triggers.append(IMPORT_TRIGGER)
    out["invalidation_triggers"] = triggers
    out["import_provenance"] = original
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Import an external memory packet as a downgraded candidate."
    )
    parser.add_argument("source", help="external memory packet yaml")
    parser.add_argument("--out", help="destination path (default: stdout)")
    parser.add_argument("--ceiling", type=float, default=0.5,
                        help="confidence cap applied on import (default 0.5)")
    parser.add_argument("--importer", default="local_owner",
                        help="owner name recorded for the imported candidate")
    args = parser.parse_args(argv)

    source = Path(args.source)
    if not source.is_file():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        return 2
    try:
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"ERROR: source not parseable yaml: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict) or data.get("packet_type") != "memory_packet":
        print("REFUSED: input is not a memory_packet; genealogy import only "
              "carries memory-shaped records")
        return 1

    imported = downgrade(data, args.ceiling, args.importer)
    text = yaml.safe_dump(imported, sort_keys=False, allow_unicode=True)
    if args.out:
        out_path = Path(args.out)
        out_path.write_text(text, encoding="utf-8")
        print(f"imported -> {out_path} (status=candidate, "
              f"confidence<={args.ceiling}; review gate still applies)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
