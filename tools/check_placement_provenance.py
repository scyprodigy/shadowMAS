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
- some review_packet under 07_working/ with status `approved` covers it, where
  "covers" means EITHER
    (a) the review references the artifact's own packet_uid (in source_refs
        source_id or related_packets), OR
    (b) the artifact's `promoted.via_review` names that review AND the same
        review references the artifact's `promoted.from_packet` (the candidate
        it was promoted from).
  Path (b) requires the named review to have actually reviewed the source
  candidate; merely pointing `via_review` at any approved review is not enough,
  which closes the forgeable-via_review hole noted in
  NEGATIVE-AUDIT-SESSION-2026-06-15 (Step 4 review).

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


def review_referenced_ids(review: dict) -> set[str]:
    ids = set()
    for ref in review.get("source_refs") or []:
        if isinstance(ref, dict) and ref.get("source_id"):
            ids.add(str(ref["source_id"]))
    for rid in review.get("related_packets") or []:
        ids.add(str(rid))
    return ids


def review_covers(uid: str, via_review: str | None, from_packet: str | None,
                  reviews: list[dict]) -> bool:
    for review in reviews:
        refs = review_referenced_ids(review)
        # (a) an approved review references this artifact's own uid
        if uid and uid in refs:
            return True
        # (b) the artifact names the review that promoted it, AND that review
        # actually reviewed the candidate this artifact was promoted from.
        # via_review alone is not sufficient: the named review must reference
        # from_packet, so pointing via_review at an unrelated approved review
        # (forgery) does not pass.
        if (via_review and from_packet
                and str(review.get("packet_uid")) == str(via_review)
                and from_packet in refs):
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
        promoted = data.get("promoted") if isinstance(data.get("promoted"), dict) else {}
        via = promoted.get("via_review")
        from_packet = str(promoted.get("from_packet")) if promoted.get("from_packet") else None
        if not review_covers(uid, via, from_packet, reviews):
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
