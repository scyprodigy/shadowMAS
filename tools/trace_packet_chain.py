#!/usr/bin/env python3
"""Reconstruct a packet's evidence chain: who references it, what it cites, both directions.

Read-only. ADVISORY. This is the personal-scale incident-reconstruction
primitive (see deferred_state_inventory): given a packet_uid, answer from
packet artifacts alone — what did this packet cite, which packets reference
it, and which files are in its evidence surface. It reconstructs; it does not
judge, approve, or claim completeness beyond the scanned roots.

Edges walked:
- outbound: source_refs (source_id -> packet, source_path -> file),
  related_packets
- inbound: any scanned packet whose source_refs / related_packets name the uid

Usage:
  python3 tools/trace_packet_chain.py <packet_uid>
  python3 tools/trace_packet_chain.py <packet_uid> --root <dir> --depth 3

Exit: 0 = chain printed; 1 = uid not found in scanned roots; 2 = setup error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]


def load_packets(roots: list[Path]) -> dict[str, tuple[Path, dict]]:
    packets: dict[str, tuple[Path, dict]] = {}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(data, dict) and "packet_uid" in data and "packet_type" in data:
                packets[str(data["packet_uid"])] = (path, data)
    return packets


def outbound_edges(data: dict) -> tuple[list[str], list[str]]:
    packet_ids: list[str] = []
    file_paths: list[str] = []
    for ref in data.get("source_refs") or []:
        if not isinstance(ref, dict):
            continue
        if ref.get("source_id"):
            packet_ids.append(str(ref["source_id"]))
        if ref.get("source_path"):
            file_paths.append(str(ref["source_path"]))
    for rid in data.get("related_packets") or []:
        packet_ids.append(str(rid))
    return packet_ids, file_paths


def inbound_uids(uid: str, packets: dict[str, tuple[Path, dict]]) -> list[str]:
    hits = []
    for other_uid, (_, data) in packets.items():
        if other_uid == uid:
            continue
        pkt_ids, _ = outbound_edges(data)
        if uid in pkt_ids:
            hits.append(other_uid)
    return sorted(hits)


def describe(uid: str, packets: dict[str, tuple[Path, dict]], repo: Path) -> str:
    if uid not in packets:
        return f"{uid} (not found in scanned roots)"
    path, data = packets[uid]
    return (f"{uid} [{data.get('packet_type', '?')}, status={data.get('status', '?')}, "
            f"risk={data.get('risk', '?')}] @ {path.relative_to(repo)}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Reconstruct a packet's evidence chain.")
    parser.add_argument("packet_uid")
    parser.add_argument("--root", action="append", help="search root (repeatable)")
    parser.add_argument("--repo", help="repo root (default: this repo)")
    parser.add_argument("--depth", type=int, default=2, help="outbound walk depth (default 2)")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else REPO
    if not repo.is_dir():
        print(f"ERROR: repo root not a directory: {repo}", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]
    packets = load_packets(roots)

    if args.packet_uid not in packets:
        print(f"NOT FOUND: {args.packet_uid} in {len(packets)} scanned packet(s)")
        return 1

    print(f"chain for {describe(args.packet_uid, packets, repo)}\n")

    print("INBOUND (packets that reference this one):")
    inbound = inbound_uids(args.packet_uid, packets)
    for uid in inbound:
        print(f"  <- {describe(uid, packets, repo)}")
    if not inbound:
        print("  (none in scanned roots)")

    print("\nOUTBOUND (what this packet cites), walked to depth "
          f"{args.depth}:")
    seen: set[str] = set()
    frontier = [(args.packet_uid, 0)]
    cited_files: dict[str, bool] = {}
    while frontier:
        uid, depth = frontier.pop(0)
        if uid in seen or depth > args.depth:
            continue
        seen.add(uid)
        if uid not in packets:
            print(f"  {'  ' * depth}-> {uid} (not found in scanned roots)")
            continue
        if depth > 0:
            print(f"  {'  ' * depth}-> {describe(uid, packets, repo)}")
        pkt_ids, file_paths = outbound_edges(packets[uid][1])
        for fp in file_paths:
            cited_files.setdefault(fp, (repo / fp).exists())
        for pid in pkt_ids:
            frontier.append((pid, depth + 1))

    print("\nEVIDENCE FILES (cited across the walked chain):")
    for fp, exists in sorted(cited_files.items()):
        marker = "ok" if exists else "MISSING"
        print(f"  [{marker}] {fp}")
    if not cited_files:
        print("  (none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
