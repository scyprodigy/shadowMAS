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

Exit: 0 = agenda printed (even if empty); 2 = setup or scan error. Malformed
YAML fails closed, and must_read paths outside --repo are never opened.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _shadowmas_readonly import load_yaml_documents, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working"]
PENDING_STATUSES = {"ready_for_human", "under_review"}
RISK_ORDER = ["r4_human_only", "r3_sensitive", "r2_guarded", "r1_routine", "r0_trivial"]
BATCH_RISKS = {"r0_trivial", "r1_routine"}


def word_count(text: str) -> int:
    return len(text.split())


def load_review_packets(
    roots: list[Path],
) -> tuple[list[tuple[Path, dict]], list[str]]:
    documents, errors = load_yaml_documents(roots)
    packets = [
        (path, data)
        for path, data in documents
        if isinstance(data, dict) and data.get("packet_type") == "review_packet"
    ]
    return packets, errors


def reading_cost(packet_path: Path, data: dict, repo: Path) -> tuple[int, list[str]]:
    cost = word_count(packet_path.read_text(encoding="utf-8"))
    warnings = []
    checks = data.get("minimal_checks")
    if checks is not None and not isinstance(checks, dict):
        warnings.append("minimal_checks has invalid shape (expected object)")
    elif isinstance(checks, dict):
        must_read = checks.get("must_read")
        if must_read is not None and not isinstance(must_read, list):
            warnings.append("must_read has invalid shape (expected list)")
        elif isinstance(must_read, list):
            for ref in must_read:
                target, error = resolve_repo_reference(repo, ref)
                if error:
                    warnings.append(f"must_read invalid: {ref!r} ({error})")
                elif target is not None and target.is_file():
                    cost += word_count(target.read_text(encoding="utf-8"))
                else:
                    warnings.append(f"must_read missing: {ref}")
    return cost, warnings


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

    packets, load_errors = load_review_packets(roots)
    if load_errors:
        for error in load_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    uid_paths: dict[str, Path] = {}
    for path, data in packets:
        uid = data.get("packet_uid")
        if not isinstance(uid, str) or not uid.strip():
            print(
                f"ERROR: invalid review packet_uid in {path}: expected non-empty string",
                file=sys.stderr,
            )
            return 2
        if uid in uid_paths:
            print(
                f"ERROR: duplicate review packet_uid {uid}: {uid_paths[uid]}, {path}",
                file=sys.stderr,
            )
            return 2
        uid_paths[uid] = path

    rows = []
    for path, data in packets:
        status = data.get("status", "?")
        if not args.all_statuses and (
            not isinstance(status, str) or status not in PENDING_STATUSES
        ):
            continue
        try:
            cost, warnings = reading_cost(path, data, repo)
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: unable to read review evidence for {path}: {exc}", file=sys.stderr)
            return 2
        rows.append({
            "uid": str(data.get("packet_uid", path.name)),
            "risk": str(data.get("risk", "?")),
            "status": str(status),
            "cost_words": cost,
            "decision": str(data.get("decision_needed", "")).strip(),
            "warnings": warnings,
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
            for warning in r["warnings"]:
                print(f"     WARNING {warning}")
    if not rows:
        print("nothing pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
