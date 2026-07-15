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

Exit: 0 = no finding (no 01_truth change, or all changes covered);
      1 = finding (advisory); 2 = setup or input scan error.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from _shadowmas_readonly import load_yaml_documents

REPO = Path(__file__).resolve().parents[1]
TRUTH_PREFIX = "01_truth/"
DEFAULT_REVIEW_ROOTS = ["07_working", "examples/packets"]


def changed_via_git(base: str | None) -> tuple[list[str], str | None]:
    if base:
        cmd = ["git", "-C", str(REPO), "diff", "--name-only", f"{base}...HEAD"]
    else:
        cmd = ["git", "-C", str(REPO), "diff", "--name-only", "--cached"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        detail = proc.stderr.strip() or f"git exited {proc.returncode}"
        return [], f"git diff failed: {detail}"
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()], None


def load_review_packets(review_roots: list[Path]) -> tuple[list[dict], list[str]]:
    documents, errors = load_yaml_documents(review_roots)
    packets = [
        data
        for _, data in documents
        if isinstance(data, dict) and data.get("packet_type") == "review_packet"
    ]
    return packets, errors


def promotion_snapshot_covers(path: str, snapshot: object) -> bool:
    if not isinstance(snapshot, dict):
        return False
    snapshot_at = snapshot.get("snapshot_at")
    source_hashes = snapshot.get("source_hashes")
    if not isinstance(snapshot_at, str):
        return False
    try:
        parsed_snapshot_at = datetime.strptime(snapshot_at, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    if parsed_snapshot_at.strftime("%Y-%m-%dT%H:%M:%SZ") != snapshot_at:
        return False
    if not isinstance(source_hashes, list):
        return False
    return any(
        isinstance(entry, dict)
        and (entry.get("source_path") == path or entry.get("path") == path)
        and any(
            isinstance(entry.get(key), str) and bool(entry[key].strip())
            for key in ("hash", "sha256", "source_hash")
        )
        for entry in source_hashes
    )


def review_covers(path: str, packets: list[dict]) -> bool:
    for packet in packets:
        packet_uid = packet.get("packet_uid")
        if not isinstance(packet_uid, str) or not packet_uid.strip():
            continue
        refs = packet.get("source_refs")
        if not isinstance(refs, list):
            continue
        referenced = any(
            isinstance(ref, dict) and ref.get("source_path") == path
            for ref in refs
        )
        if referenced and promotion_snapshot_covers(path, packet.get("promotion_snapshot")):
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

    if args.changed is not None:
        changed = args.changed
    else:
        changed, git_error = changed_via_git(args.base)
        if git_error:
            print(f"ERROR: {git_error}", file=sys.stderr)
            return 2
    truth_changed = [c for c in changed if c.startswith(TRUTH_PREFIX)]
    if not truth_changed:
        print("OK no 01_truth/ changes to gate")
        return 0

    roots = [Path(r) if Path(r).is_absolute() else REPO / r
             for r in (args.reviews_dir or DEFAULT_REVIEW_ROOTS)]
    packets, load_errors = load_review_packets(roots)
    if load_errors:
        for error in load_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

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
