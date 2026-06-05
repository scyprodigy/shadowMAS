#!/usr/bin/env python3
"""Advisory pre-merge checker: changes under 01_truth/ should carry a review_packet.

Read-only. ADVISORY. This is NOT runtime enforcement and not a merge blocker by itself;
it surfaces a finding so the human git-review gate (see .github/CODEOWNERS) can act.

A change to a canonical-truth file should be accompanied by a review_packet whose
source_refs reference the changed path and which carries a promotion_snapshot
(per 02_packets/review_packet.v0.yaml + GOVERNANCE-MATRIX promotion rules).

Usage:
  # explicit (testable, no git needed):
  python3 tools/check_truth_change.py --changed 01_truth/X.v0.en.md --reviews-dir <dir>
  # git mode:
  python3 tools/check_truth_change.py --base origin/main   # diff base...HEAD
  python3 tools/check_truth_change.py                       # default: staged (--cached)

Exit: 0 = no finding (no 01_truth change, or all changes covered); 1 = finding (advisory).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
TRUTH_PREFIX = "01_truth/"
DEFAULT_REVIEW_ROOTS = ["07_working", "examples/packets"]


def changed_via_git(base: str | None) -> list[str]:
    if base:
        cmd = ["git", "-C", str(REPO), "diff", "--name-only", f"{base}...HEAD"]
    else:
        cmd = ["git", "-C", str(REPO), "diff", "--name-only", "--cached"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"ERROR: git diff failed: {proc.stderr.strip()}", file=sys.stderr)
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def load_review_packets(review_roots: list[Path]) -> list[dict]:
    packets: list[dict] = []
    for root in review_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.yaml"):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(data, dict) and data.get("packet_type") == "review_packet":
                packets.append(data)
    return packets


def review_covers(path: str, packets: list[dict]) -> bool:
    for packet in packets:
        refs = packet.get("source_refs")
        if not isinstance(refs, list):
            continue
        referenced = any(
            isinstance(ref, dict)
            and (ref.get("source_path") == path
                 or (ref.get("source_id") and str(ref.get("source_id")) in path))
            for ref in refs
        )
        if referenced and packet.get("promotion_snapshot"):
            return True
    return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Advisory: changes under 01_truth/ should carry a referencing review_packet."
    )
    parser.add_argument("--changed", nargs="*", help="explicit changed paths (skips git)")
    parser.add_argument("--base", help="git base ref; diff base...HEAD")
    parser.add_argument("--reviews-dir", action="append",
                        help="review_packet search root (repeatable)")
    args = parser.parse_args(argv)

    changed = args.changed if args.changed is not None else changed_via_git(args.base)
    truth_changed = [c for c in changed if c.startswith(TRUTH_PREFIX)]
    if not truth_changed:
        print("OK no 01_truth/ changes to gate")
        return 0

    roots = [Path(r) if Path(r).is_absolute() else REPO / r
             for r in (args.reviews_dir or DEFAULT_REVIEW_ROOTS)]
    packets = load_review_packets(roots)

    findings = [p for p in truth_changed if not review_covers(p, packets)]
    for path in truth_changed:
        print(f"  {path}: {'MISSING review_packet' if path in findings else 'covered'}")

    if findings:
        print(f"FINDING {len(findings)} canonical-truth change(s) lack a referencing "
              f"review_packet with promotion_snapshot (advisory; human git review required).")
        return 1
    print("OK all 01_truth/ changes carry a referencing review_packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
