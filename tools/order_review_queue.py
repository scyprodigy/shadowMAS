#!/usr/bin/env python3
"""Deterministic review agenda: order pending review packets by risk, estimate reading cost.

Read-only. ADVISORY. This tool implements the attention-budget direction's v0
primitive (see RATIONALE-attention-budget-review): instead of reviewing in
arrival order, the human gets a deterministic agenda — highest risk first
while attention is fresh, low-risk items batched at the end. It makes NO
empirical claim about review quality or attention; it only removes ordering
randomness and makes reading cost visible before the human commits time.

Cost estimate = packet word count + word counts of its minimal_checks
must_read files. Estimates are sizes, not minutes; calibration to time is
explicitly out of scope for v0.

Usage:
  python3 tools/order_review_queue.py                # scan default root 07_working
  python3 tools/order_review_queue.py --root <dir>   # explicit roots (repeatable)
  python3 tools/order_review_queue.py --all-statuses # include non-pending packets

Exit: 0 = agenda printed (even if empty); 2 = setup error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working"]
PENDING_STATUSES = {"ready_for_human", "under_review"}
RISK_ORDER = ["r4_human_only", "r3_sensitive", "r2_guarded", "r1_routine", "r0_trivial"]
BATCH_RISKS = {"r0_trivial", "r1_routine"}


def word_count(text: str) -> int:
    return len(text.split())


def load_review_packets(roots: list[Path]) -> list[tuple[Path, dict]]:
    packets = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(data, dict) and data.get("packet_type") == "review_packet":
                packets.append((path, data))
    return packets


def reading_cost(packet_path: Path, data: dict, repo: Path) -> tuple[int, list[str]]:
    cost = word_count(packet_path.read_text(encoding="utf-8"))
    missing = []
    checks = data.get("minimal_checks")
    if isinstance(checks, dict):
        for ref in checks.get("must_read") or []:
            target = repo / str(ref)
            if target.exists():
                cost += word_count(target.read_text(encoding="utf-8"))
            else:
                missing.append(str(ref))
    return cost, missing


def risk_rank(risk: str) -> int:
    return RISK_ORDER.index(risk) if risk in RISK_ORDER else len(RISK_ORDER)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Order pending review packets into a review agenda.")
    parser.add_argument("--root", action="append", help="search root (repeatable)")
    parser.add_argument("--repo", help="repo root (default: this repo)")
    parser.add_argument("--all-statuses", action="store_true",
                        help="include review packets in any status")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else REPO
    if not repo.is_dir():
        print(f"ERROR: repo root not a directory: {repo}", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]

    rows = []
    for path, data in load_review_packets(roots):
        status = data.get("status", "?")
        if not args.all_statuses and status not in PENDING_STATUSES:
            continue
        cost, missing = reading_cost(path, data, repo)
        rows.append({
            "uid": data.get("packet_uid", path.name),
            "risk": data.get("risk", "?"),
            "status": status,
            "cost_words": cost,
            "decision": str(data.get("decision_needed", "")).strip(),
            "missing": missing,
        })

    # deterministic: risk severity first, then larger items inside a tier,
    # then uid as a stable tiebreak; low-risk tail is presented as one batch
    rows.sort(key=lambda r: (risk_rank(r["risk"]), -r["cost_words"], r["uid"]))
    head = [r for r in rows if r["risk"] not in BATCH_RISKS]
    tail = [r for r in rows if r["risk"] in BATCH_RISKS]

    total = sum(r["cost_words"] for r in rows)
    print(f"review agenda: {len(rows)} pending packet(s), ~{total} words total reading")
    for label, group in (("REVIEW FIRST (high risk, attention fresh)", head),
                         ("BATCH TOGETHER (low risk)", tail)):
        if not group:
            continue
        print(f"\n{label}:")
        for i, r in enumerate(group, 1):
            print(f"  {i}. [{r['risk']}] {r['uid']} (~{r['cost_words']} words, {r['status']})")
            if r["decision"]:
                print(f"     decision: {r['decision']}")
            for m in r["missing"]:
                print(f"     WARNING must_read missing: {m}")
    if not rows:
        print("nothing pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
