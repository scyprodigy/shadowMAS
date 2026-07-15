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

Exit: 0 = chain printed; 1 = uid not found in scanned roots; 2 = setup error,
including malformed YAML or an ambiguous duplicate packet_uid.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _shadowmas_readonly import load_yaml_documents, resolve_repo_reference

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = ["07_working", "examples/packets", "03_memory/shared_memory"]
PACKET_TYPES = {"task_packet", "memory_packet", "review_packet"}


def load_packets(
    roots: list[Path],
) -> tuple[dict[str, tuple[Path, dict]], list[str]]:
    documents, errors = load_yaml_documents(roots)
    packets: dict[str, tuple[Path, dict]] = {}
    for path, data in documents:
        if not isinstance(data, dict):
            continue
        raw_packet_type = data.get("packet_type")
        is_known_packet_type = (
            isinstance(raw_packet_type, str) and raw_packet_type in PACKET_TYPES
        )
        if "packet_uid" not in data and not is_known_packet_type:
            continue
        packet_type = raw_packet_type
        if not isinstance(packet_type, str) or packet_type not in PACKET_TYPES:
            errors.append(f"invalid packet_type in {path}: {packet_type!r}")
            continue
        raw_uid = data.get("packet_uid")
        if not isinstance(raw_uid, str) or not raw_uid.strip():
            errors.append(f"invalid packet_uid in {path}: expected non-empty string")
            continue
        if raw_uid in packets:
            errors.append(
                f"duplicate packet_uid {raw_uid}: {packets[raw_uid][0]}, {path}"
            )
            continue
        source_refs = data.get("source_refs")
        if source_refs is not None:
            if not isinstance(source_refs, list):
                errors.append(f"invalid source_refs in {path}: expected list")
                continue
            if any(not isinstance(item, dict) for item in source_refs):
                errors.append(f"invalid source_refs item in {path}: expected object")
                continue
        related_packets = data.get("related_packets")
        if related_packets is not None and not isinstance(related_packets, list):
            errors.append(f"invalid related_packets in {path}: expected list")
            continue
        packets[raw_uid] = (path, data)
    return packets, errors


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
    try:
        display_path = path.resolve().relative_to(repo.resolve())
    except (OSError, RuntimeError, ValueError):
        display_path = path
    return (f"{uid} [{data.get('packet_type', '?')}, status={data.get('status', '?')}, "
            f"risk={data.get('risk', '?')}] @ {display_path}")


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
    if args.depth < 0:
        print("ERROR: depth must be greater than or equal to zero", file=sys.stderr)
        return 2
    roots = [Path(r) if Path(r).is_absolute() else repo / r
             for r in (args.root or DEFAULT_ROOTS)]
    packets, load_errors = load_packets(roots)
    if load_errors:
        for error in load_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

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
    cited_files: dict[str, str] = {}
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
            target, error = resolve_repo_reference(repo, fp)
            if error:
                cited_files.setdefault(fp, "OUTSIDE_REPO")
            elif target is not None:
                cited_files.setdefault(fp, "ok" if target.is_file() else "MISSING")
        for pid in pkt_ids:
            frontier.append((pid, depth + 1))

    print("\nEVIDENCE FILES (cited across the walked chain):")
    for fp, marker in sorted(cited_files.items()):
        print(f"  [{marker}] {fp}")
    if not cited_files:
        print("  (none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
