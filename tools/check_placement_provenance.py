#!/usr/bin/env python3
"""Enforce that every shared_memory artifact has an approved promotion review packet.

This is real enforcement, not advisory: it is wired into CI and FAILS the build
when an artifact appears in 03_memory/shared_memory/ without provenance. It
closes the gap named in NEGATIVE-AUDIT-SESSION-2026-06-15 F7: the promotion gate
was a convention that nothing prevented bypassing. With this check, dropping a
file into shared_memory directly (no eligibility check, no review packet) breaks
CI instead of silently passing.

Provenance requirement, per file in 03_memory/shared_memory/ (excluding README):
- it parses as a memory_packet, AND
- some review_packet under 07_working/ with status `approved` references it,
  either by the artifact's packet_uid (in the review's source_refs source_id or
  related_packets) or by the artifact's `promoted.via_review` naming that
  review's packet_uid.

A withdrawn promotion sets the review status to `closed`; such a review no
longer counts as provenance, so a withdrawn artifact must also be removed from
shared_memory (which is the point — withdrawal means it leaves).

Usage:
  python3 tools/check_placement_provenance.py

Exit: 0 = every shared_memory artifact has approved provenance (or folder empty);
      1 = at least one artifact lacks it; 2 = setup error.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SHARED = REPO / "03_memory" / "shared_memory"
REVIEW_ROOTS = [REPO / "07_working"]


def load_approved_reviews() -> list[dict]:
    reviews = []
    for root in REVIEW_ROOTS:
        if not root.exists():
            continue
        for path in list(root.rglob("*.yaml")) + list(root.rglob("*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if (isinstance(data, dict)
                    and data.get("packet_type") == "review_packet"
                    and data.get("status") == "approved"):
                reviews.append(data)
    return reviews


def review_covers(uid: str, via_review: str | None, reviews: list[dict]) -> bool:
    for review in reviews:
        if via_review and str(review.get("packet_uid")) == str(via_review):
            return True
        ids = set()
        for ref in review.get("source_refs") or []:
            if isinstance(ref, dict) and ref.get("source_id"):
                ids.add(str(ref["source_id"]))
        for rid in review.get("related_packets") or []:
            ids.add(str(rid))
        if uid in ids:
            return True
    return False


def main() -> int:
    if not SHARED.is_dir():
        print(f"ERROR: missing {SHARED}", file=sys.stderr)
        return 2

    artifacts = [p for p in sorted(SHARED.iterdir())
                 if p.is_file() and p.suffix in {".yaml", ".yml"}]
    reviews = load_approved_reviews()

    findings = []
    for path in artifacts:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            findings.append(f"{path.name}: not parseable yaml: {exc}")
            continue
        if not isinstance(data, dict) or data.get("packet_type") != "memory_packet":
            findings.append(f"{path.name}: not a memory_packet (only promoted memory belongs here)")
            continue
        uid = str(data.get("packet_uid", ""))
        promoted = data.get("promoted")
        via = promoted.get("via_review") if isinstance(promoted, dict) else None
        if not review_covers(uid, via, reviews):
            findings.append(
                f"{path.name}: no approved promotion review_packet references {uid or '(no uid)'} "
                f"— shared_memory placement without provenance is forbidden"
            )

    for line in findings:
        print(f"FINDING {line}")
    print(f"checked {len(artifacts)} shared_memory artifact(s) against "
          f"{len(reviews)} approved review packet(s)")
    if findings:
        print(f"{len(findings)} provenance violation(s) — shared_memory artifacts must be "
              f"promoted through an approved review packet, not placed directly.")
        return 1
    print("OK every shared_memory artifact has approved promotion provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
