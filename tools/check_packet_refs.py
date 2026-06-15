#!/usr/bin/env python3
"""Repo-wide packet reference-integrity gate: no packet edge may dangle.

Read-only. ADVISORY. The evidence-chain surfaces (chain tracing, forensics,
genealogy) are only trustworthy if packet references resolve. This gate walks
every packet's reference edges and reports any that do not resolve, for the
human review gate to act on. It mutates nothing.

Edges checked, across all packet types under the scanned roots:
- source_refs[].source_id      -> must resolve to a known packet_uid
- source_refs[].source_path    -> must resolve to a file
- related_packets[]            -> must resolve to a known packet_uid
- minimal_checks.must_read[]   -> must resolve to a file
- promotion_snapshot.source_hashes[].source_path -> must resolve to a file

source_id values that do not look like local packet uids are skipped (an edge
may legitimately name an external artifact); a value matching the local uid
naming shape but absent from the scanned set is a finding.

Usage:
  python3 tools/check_packet_refs.py
  python3 tools/check_packet_refs.py --root <dir> --repo <root>

Exit: 0 = no dangling edges; 1 = findings (advisory); 2 = setup error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets"]


def load_packets(roots: list[Path]) -> list[tuple[Path, dict]]:
    packets = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(data, dict) and "packet_uid" in data and "packet_type" in data:
                packets.append((path, data))
    return packets


def looks_like_packet_uid(value: str) -> bool:
    # local uids in this repo are hyphenated tokens ending -vN-NNN or similar;
    # heuristic: contains a hyphen and no path separator or whitespace
    return "-" in value and "/" not in value and " " not in value


def check_packet(path: Path, data: dict, known_uids: set[str], repo: Path) -> list[str]:
    findings = []
    uid = data.get("packet_uid", path.name)

    def file_missing(p: str) -> bool:
        return not (repo / str(p)).exists()

    for ref in data.get("source_refs") or []:
        if not isinstance(ref, dict):
            continue
        sid = ref.get("source_id")
        if sid and looks_like_packet_uid(str(sid)) and str(sid) not in known_uids:
            findings.append(f"{uid}: dangling source_id (no such packet): {sid}")
        spath = ref.get("source_path")
        if spath and file_missing(spath):
            findings.append(f"{uid}: dangling source_path (no such file): {spath}")

    for rid in data.get("related_packets") or []:
        if looks_like_packet_uid(str(rid)) and str(rid) not in known_uids:
            findings.append(f"{uid}: dangling related_packet (no such packet): {rid}")

    checks = data.get("minimal_checks")
    if isinstance(checks, dict):
        for ref in checks.get("must_read") or []:
            if file_missing(ref):
                findings.append(f"{uid}: dangling must_read (no such file): {ref}")

    snapshot = data.get("promotion_snapshot")
    if isinstance(snapshot, dict):
        for entry in snapshot.get("source_hashes") or []:
            if isinstance(entry, dict) and entry.get("source_path") and file_missing(entry["source_path"]):
                findings.append(
                    f"{uid}: dangling promotion_snapshot source_path: {entry['source_path']}"
                )

    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check packet reference integrity across the repo.")
    parser.add_argument("--root", action="append", help="search root (repeatable)")
    parser.add_argument("--repo", help="repo root for resolving paths (default: this repo)")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else REPO
    if not repo.is_dir():
        print(f"ERROR: repo root not a directory: {repo}", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]

    packets = load_packets(roots)
    known_uids = {str(data["packet_uid"]) for _, data in packets}

    findings = []
    for path, data in packets:
        findings.extend(check_packet(path, data, known_uids, repo))

    for line in findings:
        print(f"FINDING {line}")
    print(f"checked {len(packets)} packet(s), {len(known_uids)} known uid(s)")
    if findings:
        print(f"{len(findings)} dangling reference(s) (advisory; human review decides).")
        return 1
    print("OK no dangling packet references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
